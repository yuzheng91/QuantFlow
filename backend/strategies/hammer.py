import backtrader as bt
import talib
import numpy as np

class HammerStrategy(bt.Strategy):
    params = dict(rr=3)

    def __init__(self):
        self.hammer = bt.talib.CDLHAMMER(
            self.data.open,
            self.data.high,
            self.data.low,
            self.data.close
        )

        self.order = None
        self.entry_price = None
        self.sl = None
        self.tp = None
        self.bar_executed = None

    def next(self):
        if len(self.data) < 7:
            return

        if not self.position:
            if (
                self.hammer[-1] == 100 and
                self.data.close[-3] < self.data.close[-4] and
                self.data.close[-4] < self.data.close[-5] and
                self.data.close[-5] < self.data.close[-6]
            ):
                self.entry_price = self.data.open[0] 
                self.sl = self.data.low[-1]  
                self.tp = self.entry_price + self.params.rr * (self.entry_price - self.sl)
                self.order = self.buy()
                self.bar_executed = len(self)

        elif self.position:
            price = self.data.close[0]
            if price <= self.sl:
                self.close()
            elif price >= self.tp:
                self.close()


