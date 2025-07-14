import numpy as np
import pandas as pd
import talib
import backtrader as bt

class BearishFractal(bt.Indicator):
    lines = ('signal',)

    def __init__(self):
        self.addminperiod(5)

    def next(self):
        if len(self.data) < 5:
            self.lines.signal[0] = 0
            return

        # Bearish fractal (high swing low)
        is_fractal = (
            self.data.low[-2] > self.data.low[-1] and
            self.data.low[-2] > self.data.low[-3] and
            self.data.low[-2] > self.data.low[0] and
            self.data.low[-2] > self.data.low[-4]
        )
        self.lines.signal[0] = -100 if is_fractal else 0


class BearishWilliamsFractalsStrategy(bt.Strategy):
    params = dict(sl_pct=0.02, tp_pct=0.04, max_hold_days=30)

    def __init__(self):
        self.fractal = BearishFractal(self.data)
        self.order = None
        self.entry_bar = None
        self.entry_price = None
        self.sl = None
        self.tp = None

    def next(self):
        if not self.position:
            if self.fractal[-2] == -100:  # 前一根出現 bearish fractal
                self.entry_price = self.data.open[0]
                self.sl = self.entry_price * (1 + self.p.sl_pct)
                self.tp = self.entry_price * (1 - self.p.tp_pct)
                self.entry_bar = len(self)
                self.order = self.sell()
                self.log(f"ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        elif self.position.size < 0:
            price = self.data.close[0]
            if price >= self.sl:
                self.log(f"STOP LOSS HIT - Price: {price:.2f}")
                self.close()
            elif price <= self.tp:
                self.log(f"TAKE PROFIT HIT - Price: {price:.2f}")
                self.close()
            elif len(self) - self.entry_bar >= self.p.max_hold_days:
                self.log(f"MAX HOLD DAYS EXIT - Price: {price:.2f}")
                self.close()

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED - Price: {order.executed.price:.2f}")
            elif order.issell():
                self.log(f"SELL EXECUTED - Price: {order.executed.price:.2f}")

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(f"TRADE CLOSED - PnL: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}")

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")
