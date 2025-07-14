import backtrader as bt
import numpy as np
import pandas as pd
import talib

import backtrader as bt
import talib
import numpy as np


class BollingerBandsStrategy(bt.Strategy):
    params = dict(
        n=60,
        rr=2  # risk-reward ratio for TP
    )

    def __init__(self):
        self.order = None
        self.entry_price = None
        self.sl = None
        self.tp = None

        self.bb = bt.talib.BBANDS(self.data.close, timeperiod=self.p.n, matype=talib.MA_Type.T3)
        self.bb_upper = self.bb.lines.upperband
        self.bb_middle = self.bb.lines.middleband
        self.bb_lower = self.bb.lines.lowerband

        self.returns = bt.indicators.PercentChange(self.data.close)
        self.ret_std = bt.indicators.StandardDeviation(self.returns, period=self.p.n)

    def next(self):
        if len(self.data) < self.p.n + 5:
            return

        close = self.data.close
        upper = self.bb_upper
        ret = self.returns
        r_std = self.ret_std

        if not self.position:
            if (
                upper[-3] > close[-3] and
                upper[-2] < close[-2] and
                r_std[-2] < ret[-2]
            ):
                self.entry_price = self.data.open[0]
                self.sl = self.data.low[-1]
                self.tp = self.entry_price + self.p.rr * (self.entry_price - self.sl)
                self.order = self.buy()
                self.log(f"LONG ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        elif self.position:
            price = self.data.close[0]
            if price <= self.sl:
                self.log(f"STOP LOSS HIT - Price: {price:.2f}")
                self.close()
            elif price >= self.tp:
                self.log(f"TAKE PROFIT HIT - Price: {price:.2f}")
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
