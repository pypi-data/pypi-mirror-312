from extended_algo_vector.market.utils.resample_market_data import (agg_resample_ticks, round_tick_bar_count,
                                                                    rename_iqfeed_tick_cols)
from extended_algo_vector.market.utils.use_cached_market_data import use_cached_market_data
import datetime as dt
import numpy as np
from extended_algo_vector.market.bars.TimeBars import TimeBars
from extended_algo_vector.market import MarketSource
from ib_async import Contract
from extended_algo_vector.market.qualify_contracts import qualify_contracts

# Note: This is my interpretation of generating dollar bars similar to IB Market data
#  IB Realtime Bars are sampled at 5 seconds

class SecondsVolumeBars:

    def __init__(self, contract:Contract, start: dt.datetime, end: dt.datetime, freq: int,
                 use_cache=True, **kwargs):
        '''
        :param freq: create bar when dollar amount exceeds a freq, calculated using last_px time last_sz
        '''
        self.contract = qualify_contracts(contract)
        self.start = start
        self.end = end
        self.kwargs = kwargs
        self._ticks = self._get_seconds_resample_data()
        self.use_cache = use_cache

        self.freq = freq
        assert self.freq >= 1

        self._ticks['last'] = self._ticks['close_p']
        self._ticks['last_sz'] = self._ticks['prd_vlm']

        self._ticks['dollar_traded'] = self._ticks["last"] * self._ticks["prd_vlm"]
        self.data = self._convert_to_bars(groupby_field="dollar_traded", groupby_count=self.freq)

    def _get_seconds_resample_data(self):
        ticks = TimeBars(contract=self.contract, start=self.start, end=self.end, source=MarketSource.IQFEED_SECOND, freq='5s',
                         kwargs=self.kwargs, )
        return ticks.data

    @use_cached_market_data
    def _convert_to_bars(self, groupby_field, groupby_count):
        df = self._ticks
        filtered_agg = {key: agg_resample_ticks[key] for key in df.columns if key in agg_resample_ticks}
        df = df.groupby(round_tick_bar_count(np.cumsum(df[groupby_field]), groupby_count)).agg(filtered_agg)

        df = df.droplevel(0, axis=1)

        df = df.rename(columns=rename_iqfeed_tick_cols)
        return df["datetime open_p high_p low_p close_p prd_vlm".split()]
