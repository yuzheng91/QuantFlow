import backtrader as bt


class BullishMarubozuStrategy(bt.Strategy):
    params = dict(lookback=3)

    def __init__(self):
        self.marubozu = bt.talib.CDLMARUBOZU(
            self.data.open, self.data.high, self.data.low, self.data.close
        )
        self.order = None
        self.sl = None
        self.tp = None
        self.entry_price = None

    def next(self):
        if len(self) < self.p.lookback + 2:
            return

        if not self.position:
            if self.marubozu[-2] == 100:
                lows = [self.data.low[-i] for i in range(2, self.p.lookback + 2)]
                sl = min(lows)
                self.entry_price = self.data.open[0]
                self.sl = sl
                self.tp = self.entry_price + (self.entry_price - sl)
                self.order = self.buy()
                self.log(f"BUY at {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        else:
            if self.data.close[0] <= self.sl:
                self.log(f"STOP LOSS at {self.data.close[0]:.2f}")
                self.close()

            elif self.data.close[0] >= self.tp:
                self.log(f"TAKE PROFIT at {self.data.close[0]:.2f}")
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
