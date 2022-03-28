import asyncio
import threading
import time

from data.config import ADMIN
from data.const import tf_dict, symbol_tuple, tf_tuple
from loader import bot
from util.GetData import Bands


async def catch_signal(ts: tuple):
    sym, tf = ts
    tf_human = get_tf(tf)
    print(sym, tf_human)
    bands = Bands(tf, sym)
    while True:
        trend = bands.check_csm_csak()
        if not trend:
            await asyncio.sleep(tf_dict.get(tf))
            bands = Bands(tf, sym)
        else:
            print('↓' if 0 > trend else '↑', sym, tf_human)
            print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
            print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
            print('Open:', bands.candle.open, 'Close:', bands.candle.close)
            print('SMA:', bands.sma)
            print('цена:', bands.bid)
            print('поймал, тренд')
            print(time.asctime())
            print()
            flag = 0
            if trend > 0:
                while bands.bid > max(bands.wma_low_10, bands.wma_low_5):
                    await asyncio.sleep(1)
                    flag += 1
                    if flag == tf_dict.get(tf) * 8:
                        print(sym, tf)
                        print('Flag:', flag)
                        break
                    bands = Bands(tf, sym)
                else:
                    print(sym, tf_human)
                    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
                    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
                    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
                    print('цена:', bands.bid)
                    print('wma_low_max:', max(bands.wma_low_10, bands.wma_low_5))
                    print('поймал, re-entry')
                    print(time.asctime())
                    await send_alert(text=f'поймал re-entry ↑ {sym, tf_human}')
                    print()
                    await asyncio.sleep(tf_dict.get(tf))
                    bands = Bands(tf, sym)
            else:
                while bands.bid < min(bands.wma_high_5, bands.wma_high_10):
                    await asyncio.sleep(1)
                    flag += 1
                    if flag == tf_dict.get(tf) * 8:
                        break
                    bands = Bands(tf, sym)
                else:
                    print(sym, tf_human)
                    print('Upper:', bands.upper(), 'quote high:', bands.candle.high)
                    print('Lower:', bands.lower(), 'quote low:', bands.candle.low)
                    print('Open:', bands.candle.open, 'Close:', bands.candle.close)
                    print('цена:', bands.bid)
                    print('wma_high_min:', min(bands.wma_high_5, bands.wma_high_10))
                    print('поймал, re-entry')
                    print(time.asctime())
                    await send_alert(text=f'поймал re-entry ↓ {sym, tf_human}')
                    print()
                    await asyncio.sleep(tf_dict.get(tf))
                    bands = Bands(tf, sym)


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
    for t in tf_tuple:
        for s in symbol_tuple:
            arg_list.append((s, t))
    return arg_list


async def send_alert(text):
    for ad in ADMIN.split(', '):
        try:
            await bot.send_message(chat_id=ad, text=text)
        except:
            continue
