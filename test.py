import time

from data.const import symbol_tuple, tf_tuple, tf_dict
from util.GetData import Bands

from multiprocessing import Pool


def get_pare_s_tf():
    my_list = []
    for i in symbol_tuple:
        for j in tf_tuple:
            my_list.append((i, j))
    print(my_list)
    my_tuple = tuple(my_list)
    print(my_tuple)
    return my_list


def get_alert(data: tuple):
    sym, tf = data
    bands = Bands(tf, sym)
    while True:
        while not bands.check_csm_csak():
            no_alert(sym, tf)
            time.sleep(tf_dict.get(bands.tf))
            bands = Bands(tf, sym)
        alert(bands, sym, tf)
        time.sleep(tf_dict.get(bands.tf))
        bands = Bands(tf, sym)


def no_alert(sym, tf):
    print('\n', sym, tf)
    print('без паники')
    print(time.asctime())
    print()


def alert(bands, sym, tf):
    print('\n', sym, tf)
    print('↓' if 0 > bands.check_csm_csak() else '↑')
    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
    print('SMA:', bands.sma)
    print('поймал, ёбана!!!!')
    print(time.asctime())
    print()


if __name__ == '__main__':
    with Pool(len(get_pare_s_tf())) as p:
        ar = get_pare_s_tf()
        p.map(get_alert, ar)
