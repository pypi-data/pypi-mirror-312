import datetime as dt

import pandas as pd

from extended_algo_vector.utils.db_connector.MySQLDBConnection import MySQLDBConnection
from collections import defaultdict
from extended_algo_vector.market.utils.use_cached_market_data import use_cached_market_data

# TODO: I would like to implement a datetime, event dataset that can be included in the vector strategy
# TODO: I need to verify the proper behaviour for resample > 1Min. For example resampling on 1Day with label right shifts
#  The events by one day which is not the desired result

class EconomicCalendar:

    def _impact_and_event(self, impact, event_name):
        result = defaultdict(list)
        for key, value in zip(impact, event_name):
            result[key].append(value)

        return result

    def __init__(self, start: dt.datetime, end: dt.datetime, countries: list = [], impacts: list = [], freq='1Min', use_cache=True):
        ''':param impacts [HIGH, MEDIUM, LOW]
        :param countries [USD, CAD, JPY, ...]
        :param freq resamples the datetime and groups the events for resample period
        '''
        self.contract = 'economic_cal'
        self.start = start
        self.end = end
        self.freq = freq
        self.countries = [f"'{x.upper().strip()}'" for x in countries]
        self.impacts = [f"'{x.upper().strip()}'" for x in impacts]

        self.use_cache = use_cache
        self.data = self._get_data()

    @use_cached_market_data
    def _get_data(self):
        cols = ['datetime', 'country', 'impact', 'name']
        query = f'''select {", ".join(cols)} from investing_economic where `datetime` >= "{self.start:%Y/%m/%d %H:%M:%S}" and 
        `datetime` <= "{self.end:%Y/%m/%d %H:%M:%S}"'''

        if self.countries:
            query = query + f' and country in ({", ".join(self.countries)})'

        if self.impacts:
            query = query + f' and impact in ({", ".join(self.impacts)})'

        query = query + ' order by datetime desc'

        try:
            dbcon = MySQLDBConnection()
            dbcon.connect()
            df = dbcon.get_dataframe(query=query)
            df['datetime'] = df['datetime'].apply(pd.to_datetime, format='%Y/%m/%d %H:%M:%S')

            df = df.groupby([pd.Grouper(freq=self.freq, key='datetime', label='right'), 'country']).agg(list)

            df['event'] = df.apply(lambda x: self._impact_and_event(x['impact'], x['name']), axis=1)
            df = df.unstack('country')
            df = df.drop(['impact', 'name'], axis=1).droplevel(0, axis=1)
            df = df.reset_index()
        except:
            df = pd.DataFrame()
        finally:
            dbcon.disconnect()

        return df


if __name__ == '__main__':
    import logging

    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    data = EconomicCalendar(start=dt.datetime(2024, 1, 1), end=dt.datetime(2024, 1, 10), impacts=['HIGH', 'MEDIUM'],
                            countries=['USD'], freq='1Min')
