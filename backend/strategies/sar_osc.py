import backtrader as bt

class SAROscStrategy(bt.Strategy):
    params = dict(
        acceleration=0.02,
        maximum=0.2,
        fastk_period=5,
        slowk_period=3,
        slowd_period=3,
        fastd_period=3,
    )

    def __init__(self):
        self.order = None

        self.sar = bt.talib.SAR(self.data.high, self.data.low,
                                acceleration=self.p.acceleration,
                                maximum=self.p.maximum)

        stochf = bt.talib.STOCHF(self.data.high, self.data.low, self.data.close,
                                fastk_period=self.p.fastk_period,
                                fastd_period=self.p.fastd_period)

        self.fastk = stochf.lines.fastk
        self.fastd = stochf.lines.fastd

        stoch = bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
                            fastk_period=self.p.fastk_period,
                            slowk_period=self.p.slowk_period,
                            slowd_period=self.p.slowd_period)

        self.slowk = stoch.lines.slowk
        self.slowd = stoch.lines.slowd

    def next(self):
        if len(self.data) < 10:
            return

        current_close = self.data.close[0]
        sar_value = self.sar[0]
        fastk_value = self.fastk[0]
        fastd_value = self.fastd[0]
        slowk_value = self.slowk[0]
        slowd_value = self.slowd[0]

        long_signal = (sar_value < current_close and
                       fastk_value > slowk_value and
                       fastd_value > slowd_value)

        short_signal = (sar_value > current_close and
                        fastk_value < slowk_value and
                        fastd_value < slowd_value)

        if not self.position:
            if long_signal:
                self.buy()
                self.log(f"LONG ENTRY - Price: {current_close:.2f}")
        else:
            if short_signal:
                self.close()
                self.log(f"EXIT - Price: {current_close:.2f}")

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

