from ib_async import Contract
import datetime as dt
from dataclasses import dataclass


@dataclass(slots=True)
class ContractDetails:
    contract: Contract
    multiplier: float
    tick_size: float
    commission: float
    rth_start: dt.time
    rth_end: dt.time
    bin: int


def contract_details(contract: Contract):
    if contract.secType == 'STK':
        return ContractDetails(contract=contract, multiplier=1, tick_size=0.01, commission=1.38, bin=1000, rth_start=dt.time(9, 30), rth_end=dt.time(16, 0))

    elif contract.secType in ('CASH', 'FUT'):
        detail = {
            'MES': ContractDetails(contract=contract, multiplier=12.5, tick_size=0.25, commission=1.61, bin=1, rth_start=dt.time(9, 30), rth_end=dt.time(16, 0)),
            'ES': ContractDetails(contract=contract, multiplier=50, tick_size=0.25, commission=1.61, bin=1, rth_start=dt.time(9, 30), rth_end=dt.time(16, 0)),

            'MCL': ContractDetails(contract=contract, multiplier=100, tick_size=0.01, commission=1.61, bin=1, rth_start=dt.time(9, 0), rth_end=dt.time(15, 0)),
            'CL': ContractDetails(contract=contract, multiplier=1000, tick_size=0.01, commission=1.61, bin=1, rth_start=dt.time(9, 0), rth_end=dt.time(15, 0)),

        }.get(contract.symbol)

        if detail is None:
            KeyError(f'contract details not configured for {contract=}!')
        else:
            return detail


def qualify_contracts(contract: Contract | str):
    if isinstance(contract, str):
        return contract

    if contract.secType in ['FUT']:
        value = {
            '6A': '@AD#',
            '6B': '@BP#',
            '6C': '@CD#',
            '6E': '@EU#',
            '6J': '@JY#',
            '6N': '@NE#',
            '6S': '@SF#',
            '6M': '@PX#',
            'ZN': '@TY#',
            'ES': '@ES#',
            'CL': 'QCL#',
            'GC': 'QGC#',
            'MES': '@ES#',
            'MCL': 'QCL#',
        }.get(contract.symbol)
        return value

    elif contract.secType in ['CASH']:
        return {
            'AUD.USD': '@AD#',
            'GBP.USD': '@BP#',
            'CAD.USD': '@CD#',
            'EUR.USD': '@EU#',
            'JPY.USD': '@JY#',
            'NZD.USD': '@NE#',
            'MXN.USD': '@PX#',
            'CHF.USD': '@SF#',
        }.get(contract.symbol)

    elif contract.secType in ['STK']:
        return contract.symbol

    raise NotImplemented(f'Following contract not mapped: {contract.secType} {contract.symbol}')
