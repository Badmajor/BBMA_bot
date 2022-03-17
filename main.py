import time

import MetaTrader5 as mt5

from data.const import tf_dict
from util.GetData import Bands

symbol = 'EURUSD'
tf = mt5.TIMEFRAME_M10
bands = Bands(tf, symbol)

while True:
    while not bands.check_csm_csak():
        print('без паники')
        print(time.asctime())
        print()
        time.sleep(tf_dict.get(bands.tf))
        bands = Bands(tf, symbol)

    print('↓' if 0 > bands.check_csm_csak() else '↑')
    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
    print('SMA:', bands.sma)
    print('поймал, ёбана!!!!')
    print(time.asctime())
    print()
    time.sleep(tf_dict.get(bands.tf))
    bands = Bands(tf, symbol)