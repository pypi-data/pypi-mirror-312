from abc import ABC, abstractmethod
import logging
import datetime as dt
import pandas as pd
import numpy as np
from pathlib import Path
from extended_algo_vector.market import MarketData
from extended_algo_vector.engine.create_audit_file import create_audit_file
from extended_algo_vector.engine.create_consolidated_stats import create_consolidated_stats
from extended_algo_vector.engine.create_stop_entries import create_stop_entries
from extended_algo_vector.engine.create_limit_entries import create_limit_entries
import inspect
from tqdm import tqdm
from extended_algo_vector import OrderType
from pandas.tseries import offsets
import dataclasses
from uuid import uuid1
from ib_async import Contract
from extended_algo_vector.market.qualify_contracts import qualify_contracts, contract_details
from extended_algo_vector import OrderType, Action
from ast import literal_eval


class VectorStrategy(ABC):

    def __init__(self, contract: Contract, profit_target=100., stop_loss=100.,
                 breakeven_trigger: float = None, breakeven_stop_loss=0.,
                 closeout_ttl: (offsets.DateOffset | dt.time) = pd.offsets.Hour(1),
                 signal_ttl: offsets.DateOffset = pd.offsets.Hour(1),

                 restrict_feature_cols=[],
                 feature_lookback_period=pd.offsets.Second(0),
                 feature_lookforward_period=pd.offsets.Second(0),

                 save_dir_root: Path = None, override_strategy_name: str = None, chunk_stats: int = None, **kwargs):
        '''

        :param contract: References the ib_async contract
        :param profit_target: Force profit target exit
        :param stop_loss: Force stop loss exit
        :param breakeven_tigger(o): Adjust stop loss when price moves in favor and exceeds breakeven price
        :param breakeven_stop_loss: Requires price to exceed breakeven trigger for stop loss to be adjusted to breakeven price
        :param closeout_ttl: pd.offsets(..) generates closeout offsetting signal time; However time forces a hard closeout at time
        :param quantity: default quanity if signal_data does not contain quantity column

        :param restrict_feature_cols: Restrict the columns that are tracked in the pnl data
        :param feature_lookback_period: Provides leading features data for entry analysis
        :param feature_lookforward_period: Provides trailing features data for exit analysis
        :param save_dir_root: Override default location where strategy metadata are saved
        :param override_strategy_name: Override the strategy name
        :param chunk_stats: Generate stats in fixed chunks for decay analysis
        '''

        self.strategy_name = self.__class__.__name__ if not override_strategy_name else override_strategy_name

        self.contract = contract
        self.symbol = qualify_contracts(contract)

        self.sym_detail = contract_details(self.contract)

        if not save_dir_root:
            self.save_dir = Path(inspect.getfile(self.__class__)).parent / self.strategy_name / self.symbol
        else:
            save_dir_root = save_dir_root if isinstance(save_dir_root, Path) else Path(save_dir_root)
            self.save_dir = save_dir_root / self.strategy_name / self.symbol

        self.save_dir.mkdir(exist_ok=True, parents=True)

        self.stats_chunk = chunk_stats

        self.profit_target = profit_target
        self.breakeven_trigger = breakeven_trigger
        self.breakeven_stop_loss = breakeven_stop_loss
        self.stop_loss = stop_loss
        self.closeout_ttl = closeout_ttl
        self.signal_timeout = signal_ttl

        self.restrict_feature_cols = set(restrict_feature_cols)
        self.feature_lookback_period = feature_lookback_period
        self.feature_lookforward_period = feature_lookforward_period
        self.kwargs = kwargs

        self.market_data = pd.DataFrame()

        logging.info(f'Running {self.strategy_name} | {self.symbol}')

    # TODO: As other MarketData (economic calendar or abstract alerts) becomes available, polymorph the datatype
    def register_market_data(self, feeds: [MarketData]):
        # TODO: Creating the method for registering market data and allowing for several feeds to be injected into the strategy

        market_data = []
        for x in feeds:
            mkt = x.data
            mkt = mkt.set_index('datetime')
            mkt.columns = pd.MultiIndex.from_product([[x.contract], mkt.columns])
            market_data.append(mkt)

        # TODO: I this the symbol that is being traded is the most imporatnt to include
        df = pd.concat(market_data, axis=1)
        df = df[~df[(self.symbol, 'close_p')].isnull()]
        df = df.ffill()
        df = df.sort_index()

        logging.info(f'Consolidating and registering market data\n{df}')

        self.market_data = df
        self.features_data = pd.DataFrame()
        self.signal_data = self.market_data.copy()

        return df

    @abstractmethod
    def signal(self) -> pd.DataFrame(columns=['signal']):
        # TODO: This helper statement needs to be updated to reflect MKT, STP, LMT as well ad dynamic PT SL and BT offsets
        raise NotImplementedError('''
            Must return dataframe with datetime index and signal column

            Provide logic for generating trading signal by leveraging df = self.signal_data
            The signal dataframe must contain the following as a minimum
            signal (-1 = NEW SHORT TRADE | 1 = NEW LONG TRADE | 0 = NO ACTION ) as the inception of the trade
            quantity is always defaulted to 1/lot sizes based on commission.
            to implement a scalp and swing strategy, implement separately and consolidate using ConstructPortfolioOfStrategies

            Please note that only one symbol can be traded per strategy. If you want two instruments to be traded
            Clone the strategy for the other symbol and construct the consolidated portfolio separately

            ''')

    def _explode_oco_entries(self):
        def _column_rename_eval(x):
            try:
                value = literal_eval(x)
                if value[1] == '':
                    return value[0]
                return value
            except:
                return x


        df = self.signal_data

        # This is a hack to explode multi-columns dataframe by converting the columns to a single str(tuple) and then back
        df.columns = [str(tuple(col)) for col in df.columns]
        df['entries'] = df[str(('entries', ''))].apply(lambda x: x.orders)
        df = df.explode('entries')
        df = df.drop(str(('entries','')), axis=1, errors='ignore')
        df.columns = [_column_rename_eval(x) for x in df.columns]

        df['is_live'] = df[self.symbol, 'is_live']
        for req_cols in ['signal', 'entries']:
            if req_cols not in df.columns:
                df[req_cols] = np.nan

        try:
            df.set_index('datetime', inplace=True)
        except:
            ...

        df = df[df.is_live == 1]
        df = df[(df.signal.abs() == 1) | (~df.entries.isnull())]


        df['oco_id'] = df['entries'].apply(lambda x: x.get('oco_id'))
        df['entries'] = df['entries'].apply(lambda x: x.get('entries'))
        logging.info(df)

        df = pd.concat([df, df.entries.apply(dataclasses.asdict).apply(pd.Series)], axis=1)

        df['signal'] = df['action'].apply(lambda x: {'BUY': 1, 'SELL': -1}.get(x.value))

        df['pt_offset'] = df.profit_target_px
        df['sl_offset'] = df.stoploss_px
        df['bt_offset'] = df.breakeven_trigger_px

        df['entry_type'] = df.order_type
        df['entry_price'] = df.signal_px
        df['signal_timeout'] = df.signal_ttl

        df['empty_oco_id'] = df.oco_id.apply(lambda x: uuid1())
        df['oco_id'] = np.where(df.oco_id.isnull(), df.empty_oco_id, df.oco_id)
        df = df.drop(['empty_oco_id'], axis=1)

        # except:
        #     df['oco_id'] = df.index.to_series().apply(lambda x: f'{uuid1()}-{int(x.timestamp()) * 1000}')
        #     df['signal_time'] = df.index

        assert 'signal' in df.columns, '"signal" or "entries" column not defined in signal()!'
        logging.info(f'Signals generated from Strategy\n{df[df.signal.abs() >= 1]}')

        return df

    def _calculate_sl_pt_bt_bsl(self):
        df = self.signal_data
        # TODO: This part of the code is getting really messy, and I think I need to extract it out once done
        if 'pt_offset' not in df.columns:
            df['pt_offset'] = self.profit_target
        df['pt_offset'] = df['pt_offset'].fillna(self.profit_target)
        df['pt_offset'] = df['pt_offset'].apply(lambda x: ((x // self.sym_detail.tick_size) * self.sym_detail.tick_size))
        df['pt_offset'] = np.where(df.pt_offset <= 0, 0, df.pt_offset)

        df['pt'] = np.where((df.signal == -1), df.entry_price - df.pt_offset, np.nan)
        df['pt'] = np.where((df.signal == 1), df.entry_price + df.pt_offset, df.pt)

        if 'sl_offset' not in df.columns:
            df['sl_offset'] = self.stop_loss
        df['sl_offset'] = df['sl_offset'].fillna(self.stop_loss)
        df['sl_offset'] = df['sl_offset'].apply(lambda x: ((x // self.sym_detail.tick_size) * self.sym_detail.tick_size))
        df['sl_offset'] = np.where(df.sl_offset <= 0, 0, df.sl_offset)

        df['sl'] = np.where((df.signal == -1), df.entry_price + df.sl_offset, np.nan)
        df['sl'] = np.where((df.signal == 1), df.entry_price - df.sl_offset, df.sl)

        for x in ['bt_offset', 'bsl_offset', 'bt', 'bsl']:
            if x not in df.columns:
                df[x] = np.nan

        if self.breakeven_trigger:
            # If breakeven stoploss price is greater than breakeven trigger, set it to breakeven trigger price
            #  As this case is not a valid condition. I was debating between setting bt_offset to 0

            df['bt_offset'] = np.where(df['bt_offset'].isin([True, False]), self.breakeven_trigger, df['bt_offset'])
            df['bsl_offset'] = df['bsl_offset'].fillna(self.breakeven_stop_loss)

            df['bt_offset'] = np.where(df.bt_offset <= 0, 0, df.bt_offset)
            df['bsl_offset'] = np.where(df.bsl_offset <= 0, 0, df.bsl_offset)
            df['bsl_offset'] = np.where(df.bsl_offset >= df.bt_offset, df.bt_offset, df.bsl_offset)

            df['bt'] = np.where(df.signal == -1, df.entry_price - df.bt_offset, np.nan)
            df['bt'] = np.where(df.signal == 1, df.entry_price + df.bt_offset, df.bt)

            df['bsl'] = np.where(df.signal == -1, df.entry_price - df.bsl_offset, np.nan)
            df['bsl'] = np.where(df.signal == 1, df.entry_price + df.bsl_offset, df.bsl)

        if isinstance(self.closeout_ttl, (offsets.DateOffset | dt.timedelta)):
            df['forced_closeout'] = df.entry_time + self.closeout_ttl
        elif isinstance(self.closeout_ttl, dt.time):
            df['forced_closeout'] = df.entry_time.apply(lambda x: dt.datetime.combine(x, self.closeout_ttl))

        tqdm.pandas(desc='Calculating exit condition')
        df['exit'] = df.progress_apply(self._generate_mfe_mae_stats, axis=1)

        df[['exit_price', 'exit_time', 'exit_type', 'bt_trigger_time']] = pd.DataFrame(df.exit.tolist(), index=df.index)
        df = df.drop('exit', axis=1, errors='ignore')
        # try:
        # except:
        #     df['exit_price'] = np.nan
        #     df['exit_time'] = pd.NaT
        #     df['exit_type'] = ""
        #     df['bt_trigger_time'] = pd.NaT

        return df

    def _generate_mfe_mae_stats(self, x):
        # TODO: Need a way of dynamically exiting the position in profit or in loss based on a threshold m['4_threshold']

        # try:
        # Assumption is that tradeable symbol is within market data
        m = self.market_data[self.symbol]
        m = m[x.entry_time:][['high_p', 'low_p', 'close_p']]

        m = m.loc[m.index <= x.forced_closeout]
        m = m.iloc[1:]

        m['1_sl_exit'] = np.where(((x.signal == -1) & (m.high_p >= x.sl)) |
                                  ((x.signal == 1) & (m.low_p <= x.sl)), x.sl, np.nan)
        m['2_pt_exit'] = np.where(((x.signal == -1) & (m.low_p <= x.pt)) |
                                  ((x.signal == 1) & (m.high_p >= x.pt)), x.pt, np.nan)
        m['3_cl_exit'] = np.nan
        m.loc[m.index[-1], '3_cl_exit'] = m.iloc[-1]['close_p']

        if self.breakeven_trigger:
            m['4_bsl_exit'] = np.where(((x.signal == -1) & (m.high_p >= x.bsl)) | ((x.signal == 1) & (m.low_p <= x.bsl)),
                                       x.bsl, np.nan);
            m['5_bt_exit'] = np.where(((x.signal == -1) & (m.low_p <= x.bt)) | ((x.signal == 1) & (m.high_p >= x.bt)), x.bt,
                                      np.nan);
            m['5_bt_exit'] = m['5_bt_exit'].fillna(method='ffill');
            m['4_bsl_exit'] = np.where(m['5_bt_exit'].isnull(), np.nan, m['4_bsl_exit'])

            try:
                bt_tigger_time = m[m['5_bt_exit'].notna()].index[0]
            except (KeyError, IndexError):
                bt_tigger_time = pd.NaT
        else:
            bt_tigger_time = pd.NaT

        exit_cols = ['1_sl_exit', '2_pt_exit', '3_cl_exit']
        if self.breakeven_trigger:
            exit_cols.append('4_bsl_exit')

        m.drop_duplicates(exit_cols, inplace=True)
        m = m.drop('5_bt_exit', axis=1, errors='ignore')
        m.dropna(thresh=4, inplace=True)

        exit = m.iloc[0][exit_cols].sort_index().dropna().reset_index()
        exit['index'] = exit['index'].map(
            {'1_sl_exit': 'stop_loss', '3_cl_exit': 'close_out', '2_pt_exit': 'profit_target', '4_bsl_exit': 'breakeven'})

        exit_type = exit.iloc[0][0]
        exit_price = exit.iloc[0][1]
        exit_time = exit.columns[1]

        if exit_time < bt_tigger_time:
            bt_tigger_time = pd.NaT

        return [exit_price, exit_time, exit_type, bt_tigger_time]

        # except (IndexError, ValueError):
        #     logging.info(f'   - Could not compute exit stats for the following timestamp {x.name}')
        #     return [np.nan, np.nan, np.nan]

    def _apply_stoploss_and_profit_targets(self):
        # TODO: Clean up all the if-else statement once that I used to rush the implementation of MTK, LMT, STP orders
        # TODO: I need to understand the difference between MKT, LMT, STP and what this if_else statement is capturing
        df = self.signal_data
        assert 'signal' in df.columns, 'signal column missing, please set [-1=SHORT, 1=LONG] for abstract method signal() '

        try:
            df.set_index('datetime', inplace=True)
        except:
            pass

        if 'quantity' not in df.columns:
            df['quantity'] = self.kwargs.get('quantity', 1)
        df['quantity'].fillna(0)

        df = df[df[(self.symbol, 'is_live')] == 1]

        df = df[df['signal'] != 0]
        df = df[~df['signal'].isnull()]
        df = df[df['quantity'] > 0]


        if 'signal_timeout' not in df.columns:
            df['signal_timeout'] = self.signal_timeout
        df['signal_timeout'] = df['signal_timeout'].fillna(self.signal_timeout)
        df['signal_timeout'] = df.signal_time + df.signal_timeout

        if 'entry_type' in df.columns:
            df_stop_entries = df[df.entry_type == OrderType.STP].copy()
            df_limit_entries = df[df.entry_type == OrderType.LMT].copy()

            df = df[~df.index.isin(df_stop_entries.index)]
            df = df[~df.index.isin(df_limit_entries.index)]

            df['entry_price'] = df[(self.symbol, 'close_p')]

            df_stop_entries = create_stop_entries(self, df_stop_entries)
            df_limit_entries = create_limit_entries(self, df_limit_entries)

            df = pd.concat([df, df_stop_entries, df_limit_entries])
            if 'entry_time' not in df.columns:
                df['entry_time'] = pd.NaT
            df['entry_time'] = np.where(df.entry_time.isnull(), df.index, df.entry_time)
            df['entry_type'] = df.entry_type.apply(lambda x: x.value)

        else:
            df['entry_price'] = df[self.symbol].close_p
            df['entry_time'] = df.index
            df['entry_type'] = 'MKT'
            df['signal_timeout'] = pd.NaT

        return df

    def _calc_trades(self):
        df = self.signal_data

        df['symbol'] = self.contract
        df['tick_multiplier'] = self.sym_detail.multiplier
        df['commission'] = round(df.quantity * self.sym_detail.commission, 2)
        df['direction'] = df.signal.map({-1: 'SHORT', 1: 'LONG'})
        df['commission'] = round(df.quantity * self.sym_detail.commission * 2, 2)
        df['pnl_tick'] = round(df.exit_price - df.entry_price, 2)
        df['pnl_tick'] = np.where(df.direction == 'SHORT', df.pnl_tick * -1, df.pnl_tick)
        df['time_to_live'] = df.exit_time - df.entry_time
        df['pnl_amount'] = round((df.exit_price - df.entry_price) * self.sym_detail.multiplier * df.quantity, 2)
        df['pnl_amount'] = np.where(df.direction == 'SHORT', df.pnl_amount * -1, df.pnl_amount)
        df['pnl_with_commission'] = round(df.pnl_amount - df.commission, 2)

        # Drop duplicated OCO orders, keep the first entry,
        # if there are two entries on the same price, penalize by taking the worst trade
        df = df.sort_values(['entry_time', 'pnl_tick'], ascending=[True, True])

        # TODO: This is causing an failure. I am wondering why this is in place.
        #  I wounder what the OCO_ID is being used for

        try:
            df = df.drop_duplicates('oco_id', keep='first')
        except KeyError:
            ...

        df = df[
            ['symbol', 'entry_type', 'signal_time', 'signal_timeout', 'entry_time', 'exit_time', 'direction', 'entry_price',
             'exit_price', 'quantity', 'commission', 'pnl_tick', 'time_to_live', 'pnl_amount', 'pnl_with_commission',
             'exit_type', 'pt', 'sl', 'bt', 'bsl', 'forced_closeout', 'bt_trigger_time']]
        df = df.reset_index(drop=True)

        return df

    def run(self):
        s = dt.datetime.now()
        assert not self.market_data.empty, NotImplementedError(
            'Provide register_market_data([...])\n Market data has not been registered....abort!')
        self.signal_data = self.signal()

        self.features_data = self.signal_data.reset_index().copy()
        self.market_data.to_pickle(self.save_dir / 'market_data.p')
        self.features_data.to_pickle(self.save_dir / 'features_data.p')

        self.signal_data = self._explode_oco_entries()
        self.signal_data = self._apply_stoploss_and_profit_targets()
        self.signal_data = self._calculate_sl_pt_bt_bsl()

        self.pnl_data = self._calc_trades()
        self.stats_data = create_consolidated_stats(self)  # Note stats will update self.pnl_data

        self.signal_data.to_pickle(self.save_dir / 'signal_data.p')
        self.pnl_data.to_pickle(self.save_dir / 'pnl_data.p')
        self.stats_data.to_pickle(self.save_dir / 'stats_data.p')

        create_audit_file(self)

        e = dt.datetime.now()
        logging.info(f'Saving {self.__class__.__name__} strategy details...\n{self.save_dir}')
        logging.info(f'Elapsed time: {e - s}')
