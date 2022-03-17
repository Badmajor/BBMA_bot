import asyncio
import time

import MetaTrader5 as mt5
import pandas as pd

from data.const import tf_dict
from util.GetData import Bands
from util.GetData_test import BandsT


async def fuk(tf, symbol):
    bands = Bands(tf, symbol)
    while not bands.check_csm_csak():
        print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
        print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
        print('Open:', bands.candle.open, 'Close:', bands.candle.close)
        print('SMA:', bands.sma)
        print('без паники')
        print(time.asctime())
        print(symbol, tf_dict.get(tf) / 60)
        print()
        time.sleep(tf_dict.get(tf))
        bands = Bands(tf, symbol)

    print('↓' if 0 > bands.check_csm_csak() else '↑')
    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
    print('SMA:', bands.sma)
    print('без паники')
    print(time.asctime())
    print(symbol, tf_dict.get(tf) / 60)
    print()

symbol_tuple = ('GBPUSD', 'EURUSD', 'AUDUSD')
tf_tuple = (5, 10, 30)


async def main():
    for s in symbol_tuple:
        for t in tf_tuple:
            await fuk(t, s)


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()
