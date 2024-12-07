from enum import Enum, auto
from pathlib import Path
import os


class MarketSource(Enum):
    IQFEED_TICK = auto()
    IQFEED_SECOND = auto()
    IQFEED_MINUTE = auto()


class MarketDataType(Enum):
    TICK = auto()
    TIME = auto()
    TICK_VOLUME = auto()
    TICK_COUNT = auto()
    TICK_DOLLAR = auto()
    SECONDS_VOLUME = auto()  # IB provides a minimum of 5 seconds bars
    SECONDS_DOLLAR = auto()  # IB provides a minimum of 5 seconds bars

    # TODO: I think it should be mimic IB_VOLUME or IB_DOLLAR
    # TODO: I would like to mimic seconds volume and dollar bar and 125 ms IB tick data aswell


def get_market_data_source_dir(source: MarketSource):
    path_root_market_data_dir = Path(os.getenv('MARKET_DATA_LOCAL_DIR'))
    source_dir = None

    match source:
        case MarketSource.IQFEED_TICK:
            source_dir = path_root_market_data_dir / 'tick_data'
        case MarketSource.IQFEED_SECOND:
            source_dir = path_root_market_data_dir / 'iq_seconds_data'
        case MarketSource.IQFEED_MINUTE:
            source_dir = path_root_market_data_dir / 'minute_data'

    return source_dir
