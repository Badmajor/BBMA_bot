import time

import MetaTrader5 as mt5
import pandas as pd

from data.config import SERVER, LOGIN, PASSWORD


class BandsT:
    def __init__(self, tf, symbol, t):
        self._status_ = mt5.initialize(login=LOGIN, server=SERVER, password=PASSWORD)
        self.tf = tf
        self.symbol = symbol
        self.rates20 = mt5.copy_rates_from(symbol, tf, t, 20)
        self.rates10 = mt5.copy_rates_from(symbol, tf, t, 10)
        self.rates5 = mt5.copy_rates_from(symbol, tf, t, 5)
        self.rates_now = mt5.copy_rates_from(symbol, tf, t, 1)
        mt5.shutdown()
        self.quote = pd.DataFrame(self.rates_now).mean()
        self.sma = pd.DataFrame(self.rates20).mean().close
        self.wma_low_10 = pd.DataFrame(self.rates10).mean().low
        self.wma_low_5 = pd.DataFrame(self.rates5).mean().low
        self.wma_high_10 = pd.DataFrame(self.rates10).mean().high
        self.wma_high_5 = pd.DataFrame(self.rates5).mean().high

    def upper(self):
        df = pd.DataFrame(self.rates20)
        df['close'] = (df['close'] - self.sma) ** 2
        return self.sma + (2 * (df.mean().close ** 0.5))

    def lower(self):
        df = pd.DataFrame(self.rates20)
        df['close'] = (df['close'] - self.sma) ** 2
        return self.sma - (2 * (df.mean().close ** 0.5))

    def check_csm_csak(self):
        U, L = self.upper(), self.lower()
        h, l = self.quote.high, self.quote.low
        if U > h and l > L:
            return False
        else:
            return L -l


class Symbols:
    def __init__(self):
        self._status_ = mt5.initialize(login=68066228, server="RoboForex-Pro", password="Android19")
        self.all = pd.DataFrame(mt5.symbols_get())
        self.count = len(mt5.symbols_get())
