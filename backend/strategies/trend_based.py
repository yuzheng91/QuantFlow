import backtrader as bt

class TrendBasedStrategy(bt.Strategy):
    params = dict(
        rr=2,
        n_EMA=10,
        acc_SAR=0.04,
        max_step_SAR=0.2,
        fastk_period=14,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0,
    )

    def __init__(self):
        self.order = None
        self.entry_price = None
        self.sl = None
        self.tp = None

        # 改寫為 bt.talib 包裝器
        self.ema = bt.talib.EMA(self.data.close, timeperiod=self.p.n_EMA)
        self.psar = bt.talib.SAR(self.data.high, self.data.low, 
                                 acceleration=self.p.acc_SAR, maximum=self.p.max_step_SAR)

        stoch = bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
                       fastk_period=self.p.fastk_period,
                       slowk_period=self.p.slowk_period,
                       slowk_matype=self.p.slowk_matype,
                       slowd_period=self.p.slowd_period,
                       slowd_matype=self.p.slowd_matype)

        self.stoch_k = stoch.slowk
        self.stoch_d = stoch.slowd

    def next(self):
        if len(self.data) < 20:
            return

        price = self.data.close[0]

        cond_long = (
            self.ema[-1] < price and
            self.psar[-1] < price and
            self.stoch_k[-1] > self.stoch_d[-1] and
            self.stoch_k[-1] < 80
        )

        cond_short = (
            self.ema[-1] > price and
            self.psar[-1] > price and
            self.stoch_k[-1] < self.stoch_d[-1] and
            self.stoch_k[-1] > 20
        )

        if not self.position:
            if cond_long:
                self.entry_price = self.data.open[0]
                self.sl = self.data.low[-1]
                self.tp = self.entry_price + self.p.rr * (self.entry_price - self.sl)
                self.order = self.buy()
                self.log(f"LONG ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

            elif cond_short:
                self.entry_price = self.data.open[0]
                self.sl = self.data.high[-1]
                self.tp = self.entry_price - self.p.rr * (self.sl - self.entry_price)
                self.order = self.sell()
                self.log(f"SHORT ENTRY - Price: {self.entry_price:.2f}, SL: {self.sl:.2f}, TP: {self.tp:.2f}")

        elif self.position:
            if self.position.size > 0:
                if price <= self.sl:
                    self.log(f"LONG STOP - Price: {price:.2f}")
                    self.close()
                elif price >= self.tp:
                    self.log(f"LONG TAKE PROFIT - Price: {price:.2f}")
                    self.close()
            elif self.position.size < 0:
                if price >= self.sl:
                    self.log(f"SHORT STOP - Price: {price:.2f}")
                    self.close()
                elif price <= self.tp:
                    self.log(f"SHORT TAKE PROFIT - Price: {price:.2f}")
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