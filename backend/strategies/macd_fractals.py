import numpy as np
import pandas as pd
import talib
import backtrader as bt

class MACDFractalsStrategy(bt.Strategy):
    params = dict(sl_pct=0.02, tp_pct=0.04, max_hold_days=30)
    params = (
        ('sl_pct', 0.02),
        ('tp_pct', 0.04),
        ('max_hold_days', 30),
        ('fast', 12),
        ('slow', 26),
        ('signal', 9),
    )

    def __init__(self):
        self.order = None
        self.entry_bar = None
        self.entry_price = None
        self.sl = None
        self.tp = None
        macd_ind = bt.indicators.MACD(self.data.close,
                                       period_me1=self.params.fast,
                                       period_me2=self.params.slow,
                                       period_signal=self.params.signal)
        self.macd = macd_ind.macd
        self.signal = macd_ind.signal

    def next(self):
        if len(self.data) < 6:
            return

        is_bullish_fractal = (
            self.data.low[-3] < self.data.low[-2] and
            self.data.low[-3] < self.data.low[-4] and
            self.data.low[-3] < self.data.low[-5] and
            self.data.low[-3] < self.data.low[-1]
        )

        macd_cross = self.macd[-2] < self.signal[-2] and self.macd[-1] > self.signal[-1]

        if not self.position:
            if is_bullish_fractal and macd_cross:
                self.entry_price = self.data.open[-1]
                self.sl = self.entry_price * (1 - self.p.sl_pct)
                self.tp = self.entry_price * (1 + self.p.tp_pct)
                self.entry_bar = len(self)
                self.order = self.buy()
                self.log(f"MACD FRACTAL BUY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        elif self.position:
            if self.data.close[0] <= self.sl:
                self.log(f"MACD FRACTAL STOP LOSS - Price: {self.data.close[0]:.2f}")
                self.close()
            elif self.data.close[0] >= self.tp:
                self.log(f"MACD FRACTAL TAKE PROFIT - Price: {self.data.close[0]:.2f}")
                self.close()
            elif len(self) - self.entry_bar >= self.p.max_hold_days:
                self.log(f"MACD FRACTAL MAX HOLD EXIT - Price: {self.data.close[0]:.2f}")
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