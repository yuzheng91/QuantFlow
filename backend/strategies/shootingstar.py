import backtrader as bt

class ShootingStarStrategy(bt.Strategy):
    params = dict(rr=2)

    def __init__(self):
        self.order = None
        self.entry_price = None
        self.sl = None
        self.tp = None

        self.pattern = bt.talib.CDLSHOOTINGSTAR(
            self.data.open, self.data.high, self.data.low, self.data.close
        )

    def next(self):
        if len(self.data) < 6:
            return

        signal_today = self.pattern[-2] 
        falling_trend = (
            self.data.close[-2] > self.data.close[-3] > self.data.close[-4] > self.data.close[-5]
        )

        if not self.position:
            if signal_today == -100 and falling_trend:
                self.entry_price = self.data.open[0]
                self.sl = self.data.high[-1]
                self.tp = self.entry_price - self.p.rr * (self.sl - self.entry_price)
                self.order = self.sell()
                self.log(f"SHORT ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")
        elif self.position.size < 0: 
            price = self.data.close[0]
            if price >= self.sl:
                self.log(f"STOP LOSS - Price: {price:.2f}")
                self.close()
            elif price <= self.tp:
                self.log(f"TAKE PROFIT - Price: {price:.2f}")
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

