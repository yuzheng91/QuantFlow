import numpy as np
import pandas as pd
import talib
import backtrader as bt

class VolumeReversalStrategy(bt.Strategy):
    params = dict(
        lookback_std=100,
        price_gap_days=5,
        vol_window=5,
        hold_period=5,
        direction="long"
    )

    def __init__(self):
        self.order = None
        self.entry_bar = None
        self.entry_price = None
        self.sl = None
        self.tp = None

        self.pr_chg = self.data.close(-self.p.price_gap_days - 1) - self.data.close(-1)
        self.avg_vol = bt.indicators.SimpleMovingAverage(self.data.volume(-1), period=self.p.vol_window)
        self.past_avg_vol = bt.indicators.SimpleMovingAverage(self.data.volume(-self.p.vol_window - 1), period=self.p.vol_window)

    def next(self):
        if len(self.data) < self.p.lookback_std + self.p.vol_window:
            return

        pr_chg = self.data.close[-1] - self.data.close[-(self.p.price_gap_days + 1)]
        std_ = np.std([
            self.data.close[-(i + 1)] - self.data.close[-(i + self.p.price_gap_days + 1)]
            for i in range(self.p.lookback_std)
        ])

        avg_vol = np.mean([self.data.volume[-i] for i in range(1, self.p.vol_window + 1)])
        past_avg_vol = np.mean([self.data.volume[-i] for i in range(self.p.vol_window + 1, 2 * self.p.vol_window + 1)])

        large_move = abs(pr_chg) > std_
        shrinking_vol = avg_vol < past_avg_vol

        long_signal = large_move and shrinking_vol and pr_chg < 0
        short_signal = large_move and shrinking_vol and pr_chg > 0

        entry_signal = None
        if self.p.direction.lower() == "long":
            entry_signal = long_signal
        elif self.p.direction.lower() == "short":
            entry_signal = short_signal

        if not self.position:
            if entry_signal:
                self.entry_price = self.data.open[0]
                self.sl = self.entry_price * 0.98
                self.tp = self.entry_price * 1.04
                self.entry_bar = len(self)
                self.order = self.buy() if self.p.direction == "long" else self.sell()
                self.log(f"VOLUME REVERSAL ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        elif self.position:
            if self.data.close[0] <= self.sl and self.position.size > 0:
                self.log(f"VOLUME REVERSAL STOP LOSS - Price: {self.data.close[0]:.2f}")
                self.close()
            elif self.data.close[0] >= self.tp and self.position.size > 0:
                self.log(f"VOLUME REVERSAL TAKE PROFIT - Price: {self.data.close[0]:.2f}")
                self.close()
            elif len(self) - self.entry_bar >= self.p.hold_period:
                self.log(f"VOLUME REVERSAL TIME EXIT - Price: {self.data.close[0]:.2f}")
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