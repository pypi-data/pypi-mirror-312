import pandas as pd
import datetime as dt
from extended_algo_vector.market import MarketSource
from extended_algo_vector.market.utils.common import get_market_data_source_dir
from extended_algo_vector.market.utils.use_cached_market_data import use_cached_market_data
import logging
import re
import pathlib
import os
from ib_async.contract import Contract
from extended_algo_vector.market.qualify_contracts import qualify_contracts

class Ticks:

    def __init__(self, contract: Contract|str, start: dt.datetime, end: dt.datetime, agg_consecutive_last_px=True,
                 use_cache=True,
                 **kwargs):
        '''
        :param agg_consecutive_last_px: sequential prices where last_px is the same will be rolled into one record with last_sz and tick_count summed to drastically shrink tick dataset for iteration
        :param use_cache: leveraging ticks is an expensive operation so best to leverage cache to reduce load time
        '''

        source = kwargs.pop('source', MarketSource.IQFEED_TICK)
        assert end - start >= dt.timedelta(milliseconds=0), 'end date must be greater than start date'
        assert end - start <= dt.timedelta(days=32), 'reading tick data is expensive, limit to <31 days'

        self.contract = qualify_contracts(contract)
        self.start = start
        self.end = end

        self.kwargs = kwargs
        self.agg_consecutive_last_px = agg_consecutive_last_px
        self._source_dir = get_market_data_source_dir(source=source)
        self.use_cache = use_cache
        self.freq = None

        self.data = self._load_historical_data()


    @use_cached_market_data
    def _load_historical_data(self):

        path_symbol_dir = self._source_dir / self.contract
        print(path_symbol_dir)


        re_pattern = re.compile(r"(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2}).zip")
        files_to_load = [(pathlib.Path(f'{path_symbol_dir}/{x}'), *re_pattern.search(x).groups()) for x in os.listdir(
            path_symbol_dir)]
        files_to_load = pd.DataFrame(files_to_load, columns=['filename', 'year', 'month','day'])
        files_to_load[['year', 'month','day']] = files_to_load[['year', 'month','day']].apply(pd.to_numeric)
        files_to_load['datetime'] = files_to_load.apply(lambda x: dt.datetime(x.year, x.month, x.day), axis=1)

        files_to_load['start'] = self.start
        files_to_load['end'] = self.end

        files_to_load = files_to_load[files_to_load.datetime.between(files_to_load.start, files_to_load.end, inclusive='both')]

        df = []
        for x in files_to_load.itertuples():
            try:
                _data = pd.read_pickle(x.filename, compression='zip')
                df.append(_data)
            except FileNotFoundError:
                logging.error(f'File not found: {self.contract} {x.filename}')

        df = pd.concat(df, ignore_index=True)
        df = df.sort_values('datetime', ascending=True)
        df = df.query(f'datetime >= @self.start and datetime <= @self.end')
        df['tick_count'] = 1

        if self.agg_consecutive_last_px:
            df['group'] = (df['last'] != df['last'].shift()).cumsum()
            df = df.groupby(['group', 'last']).agg({'datetime': 'last', 'last_sz': 'sum', 'tick_count': 'sum'})
            df = df.reset_index().drop('group', axis=1)

        return df
