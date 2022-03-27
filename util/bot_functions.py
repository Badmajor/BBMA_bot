import threading
import time

from data.const import tf_dict, symbol_tuple, tf_tuple
from util.GetData import Bands

locker = threading.Lock()


def catch_signal(ts: tuple):
    sym, tf = ts
    locker.acquire()
    tf_human = get_tf(tf)
    print(sym, tf_human)
    locker.release()
    bands = Bands(tf, sym)
    while True:
        trend = bands.check_csm_csak()
        if not trend:
            time.sleep(tf_dict.get(tf))
            bands = Bands(tf, sym)
        else:
            locker.acquire()
            print('↓' if 0 > trend else '↑', sym, tf_human)
            print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
            print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
            print('Open:', bands.candle.open, 'Close:', bands.candle.close)
            print('SMA:', bands.sma)
            print('цена:', bands.bid)
            print('поймал, тренд')
            print(time.asctime())
            print()
            locker.release()
            flag = 0
            if trend > 0:
                while bands.bid > max(bands.wma_low_10, bands.wma_low_5):
                    time.sleep(1)
                    flag += 1
                    if flag == tf_dict.get(tf) * 8:
                        print(sym, tf)
                        print('Flag:', flag)
                        break
                    bands = Bands(tf, sym)
                else:
                    locker.acquire()
                    print(sym, tf_human)
                    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
                    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
                    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
                    print('цена:', bands.bid)
                    print('wma_low_max:', max(bands.wma_low_10, bands.wma_low_5))
                    print('поймал, re-entry')
                    print(time.asctime())
                    print()
                    time.sleep(tf_dict.get(tf))
                    bands = Bands(tf, sym)
                    locker.release()
            else:
                while bands.bid < min(bands.wma_high_5, bands.wma_high_10):
                    time.sleep(1)
                    flag += 1
                    if flag == tf_dict.get(tf) * 8:
                        break
                    bands = Bands(tf, sym)
                else:
                    locker.acquire()
                    print(sym, tf_human)
                    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
                    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
                    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
                    print('цена:', bands.bid)
                    print('wma_high_min:', min(bands.wma_high_5, bands.wma_high_10))
                    print('поймал, re-entry')
                    print(time.asctime())
                    print()
                    time.sleep(tf_dict.get(tf))
                    bands = Bands(tf, sym)
                    locker.release()


def get_tf(tf):
    minutes = tf_dict.get(tf) / 60
    if minutes >= 40320:
        return f'{int(minutes // 40320)} Мес'
    elif minutes >= 10080:
        return f'{int(minutes // 10080)} Н'
    elif minutes >= 1440:
        return f'{int(minutes) // 1440} Д'
    elif minutes >= 60:
        return f'{int(minutes) // 60} Ч'
    else:
        return f'{int(minutes)} Мин'


def get_arg_list() -> list[tuple]:
    arg_list = []
    for s in symbol_tuple:
        for t in tf_tuple:
            arg_list.append((s, t))
    return arg_list


def watch_mt5():
    threads = []
    for i in get_arg_list():
        t = threading.Thread(name=f'{i[0]} {str(get_tf(i[1]))}', target=catch_signal, args=(i, ))
        threads.append(t)
        t.start()
    print(threads)
