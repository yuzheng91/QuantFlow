import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (('period', 14), ('bottom', 30), ('top', 70))

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi[0] < self.params.bottom:
                self.buy()
        else:
            if self.rsi[0] > self.params.top:
                self.close()