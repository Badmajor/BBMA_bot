import time

import MetaTrader5 as mt5

from data.const import tf_dict
from util.GetData import Bands


def re_entry(tf, symbol, trend):
    bands = Bands(tf, symbol)
    flag = 0
    if trend > 0:
        while bands.bid < min(bands.wma_high_5, bands.wma_high_10):
            print('Не дергаемся, ловим хай')
            print(time.asctime())
            time.sleep(1)
            flag += 1
            if flag == tf_dict.get(tf):
                return
    else:
        while bands.bid > max(bands.wma_high_5, bands.wma_high_10):
            print('Не дергаемся, ловим лоу')
            print(time.asctime())
            time.sleep(1)
            flag += 1
            if flag == tf_dict.get(tf):
                return
        print('↓' if 0 > bands.check_csm_csak() else '↑')
        print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
        print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
        print('Open:', bands.candle.open, 'Close:', bands.candle.close)
        print('цена:', bands.bid)
        print('поймал, ёбана!!!!')
        print(time.asctime())
        print()


symbol = 'EURUSD'
tf = mt5.TIMEFRAME_M2
bands = Bands(tf, symbol)

while True:
    while not bands.check_csm_csak():
        print('без паники')
        print(time.asctime())
        print()
        time.sleep(tf_dict.get(tf))
        bands = Bands(tf, symbol)

    print('↓' if 0 > bands.check_csm_csak() else '↑')
    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
    print('SMA:', bands.sma)
    print('CSAK или CSM')
    print(time.asctime())
    print()
    re_entry(tf, symbol, bands.check_csm_csak())
    time.sleep(tf_dict.get(bands.tf))
    bands = Bands(tf, symbol)




catch_signal('AUDCAD', 10)
