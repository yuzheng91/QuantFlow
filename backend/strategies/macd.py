import backtrader as bt
import pandas as pd

class MACDStrategy(bt.Strategy):
        
    params = (
        ('fast', 12),
        ('slow', 26),
        ('signal', 9),
    )

    def __init__(self):
        macd_ind = bt.indicators.MACD(self.data.close,
                                       period_me1=self.params.fast,
                                       period_me2=self.params.slow,
                                       period_signal=self.params.signal)
        self.macd = macd_ind.macd
        self.signal = macd_ind.signal

    def next(self):
        if not self.position:
            if self.macd[0] > self.signal[0] and self.macd[-1] <= self.signal[-1]:
                self.buy()
        else:
            if self.macd[0] < self.signal[0] and self.macd[-1] >= self.signal[-1]:
                self.close()
                

