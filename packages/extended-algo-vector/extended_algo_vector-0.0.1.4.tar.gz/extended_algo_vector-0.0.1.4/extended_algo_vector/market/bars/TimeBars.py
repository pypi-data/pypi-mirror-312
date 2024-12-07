import os
import pathlib
import pandas as pd
import datetime as dt
from extended_algo_vector.market.utils.common import get_market_data_source_dir
from extended_algo_vector.market import MarketSource, resample_market_data
from extended_algo_vector.market.utils.use_cached_market_data import use_cached_market_data
from extended_algo_vector.market.utils.common import MarketSource
import logging
import re
from extended_algo_vector.market.qualify_contracts import qualify_contracts
from ib_async import Contract


class TimeBars:

    def __init__(self, source: MarketSource, contract: Contract, start: dt.datetime, end: dt.datetime, freq=None,
                 use_cache=False, **kwargs):
        '''
        :param freq: Returning historical data will be Seconds or Minutes based on source. Resample data into a different time-freq (5Min, 1H, 1W ...)
        '''

        assert end - start >= dt.timedelta(milliseconds=0), 'end date must be greater than start date'

        self.contract = contract
        self.start = start
        self.end = end
        self.freq = freq
        if not self.freq:
            self.freq = '1S' if source in [MarketSource.IQFEED_SECOND] else "1Min"

        self.use_cache = use_cache
        self.kwargs = kwargs

        self.source_type = source
        self.source_dir = get_market_data_source_dir(source)

        self.data = self._load_historical_data()

    @use_cached_market_data
    def _load_historical_data(self):

        path_symbol_dir = self.source_dir / qualify_contracts(self.contract)

        re_pattern = re.compile(r"(?P<year>\d{4})_(?P<month>\d{2}).zip")
        files_to_load = [(pathlib.Path(f'{path_symbol_dir}/{x}'), *re_pattern.search(x).groups()) for x in os.listdir(
            path_symbol_dir)]

        files_to_load = pd.DataFrame(files_to_load, columns=['filename', 'year', 'month'])
        files_to_load[['year', 'month']] = files_to_load[['year', 'month']].apply(pd.to_numeric)
        files_to_load['day'] = 1
        files_to_load['datetime'] = files_to_load.apply(lambda x: dt.datetime(x.year, x.month, x.day), axis=1)

        files_to_load['end'] = self.end + pd.offsets.MonthEnd(0)
        if self.start.day == 1:
            files_to_load['start'] = self.start - pd.offsets.MonthBegin(0)
        else:
            files_to_load['start'] = self.start - pd.offsets.MonthBegin(1)

        files_to_load['start'] = files_to_load['start'].dt.date
        files_to_load['end'] = files_to_load['end'].dt.date

        files_to_load = files_to_load[files_to_load.datetime.between(files_to_load.start, files_to_load.end, inclusive='both')]

        df = []
        for x in files_to_load.itertuples():
            try:
                _data = pd.read_pickle(x.filename, compression='zip')
                df.append(_data)
            except FileNotFoundError:
                logging.error(f'File not found: {self.contract} {x.filename}')

        df = pd.concat(df, ignore_index=True)
        df = df.query(f'datetime >= @self.start and datetime <= @self.end')

        df = resample_market_data(df, freq=self.freq)

        return df
