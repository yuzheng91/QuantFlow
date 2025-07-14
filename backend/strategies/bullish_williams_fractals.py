import numpy as np
import pandas as pd
import talib
import backtrader as bt

class BullishFractalIndicator(bt.Indicator):
    lines = ('signal',)
    plotinfo = dict(subplot=True, plotlinelabels=True)

    def __init__(self):
        self.addminperiod(5)

    def next(self):
        if len(self.data) < 5:
            self.lines.signal[0] = 0
            return

        is_fractal = (
            self.data.close[-2] < self.data.close[-1] and
            self.data.close[-2] < self.data.close[-3] and
            self.data.close[-1] < self.data.close[0] and
            self.data.close[-3] < self.data.close[-4]
        )
        self.lines.signal[0] = 100 if is_fractal else 0

class BullishWilliamsFractalsStrategy(bt.Strategy):
    params = dict(sl_pct=0.02, tp_pct=0.04, max_hold_days=30)

    def __init__(self):
        self.fractal = BullishFractalIndicator(self.data)

        self.order = None
        self.entry_bar = None
        self.entry_price = None
        self.sl = None
        self.tp = None

    def next(self):
        if not self.position:
            if self.fractal[-1] == 100:
                self.entry_price = self.data.open[0]
                self.sl = self.entry_price * (1 - self.p.sl_pct)
                self.tp = self.entry_price * (1 + self.p.tp_pct)
                self.entry_bar = len(self)
                self.order = self.buy()
                self.log(f"ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        elif self.position:
            price = self.data.close[0]
            if price <= self.sl:
                self.log(f"STOP LOSS HIT - Price: {price:.2f}")
                self.close()
            elif price >= self.tp:
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
