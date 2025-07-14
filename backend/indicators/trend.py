import backtrader as bt

class TALibIndicators(bt.Indicator):
    lines = ()  

    def __init__(self):
        self.adx = bt.talib.ADX(self.data.high, self.data.low, self.data.close, timeperiod=14)
        self.adxr = bt.talib.ADXR(self.data.high, self.data.low, self.data.close, timeperiod=14)

        self.aroon = bt.talib.AROON(self.data.high, self.data.low, timeperiod=14)
        self.aroonosc = bt.talib.AROONOSC(self.data.high, self.data.low, timeperiod=14)

        self.bop = bt.talib.BOP(self.data.open, self.data.high, self.data.low, self.data.close)
        self.cci = bt.talib.CCI(self.data.high, self.data.low, self.data.close, timeperiod=14)
        self.cmo = bt.talib.CMO(self.data.close, timeperiod=14)
        self.dx = bt.talib.DX(self.data.high, self.data.low, self.data.close, timeperiod=14)

        self.macd = bt.talib.MACD(self.data.close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.macdext = bt.talib.MACDEXT(self.data.close, fastperiod=12, fastmatype=0,
                                        slowperiod=26, slowmatype=0,
                                        signalperiod=9, signalmatype=0)
        self.macdfix = bt.talib.MACDFIX(self.data.close, signalperiod=9)

        self.mfi = bt.talib.MFI(self.data.high, self.data.low, self.data.close, self.data.volume, timeperiod=14)
        self.mom = bt.talib.MOM(self.data.close, timeperiod=10)
        self.rsi = bt.talib.RSI(self.data.close, timeperiod=14)
        self.trix = bt.talib.TRIX(self.data.close, timeperiod=30)
        self.willr = bt.talib.WILLR(self.data.high, self.data.low, self.data.close, timeperiod=14)

        self.minus_di = bt.talib.MINUS_DI(self.data.high, self.data.low, self.data.close, timeperiod=14)
        self.minus_dm = bt.talib.MINUS_DM(self.data.high, self.data.low, timeperiod=14)
        self.plus_di = bt.talib.PLUS_DI(self.data.high, self.data.low, self.data.close, timeperiod=14)
        self.plus_dm = bt.talib.PLUS_DM(self.data.high, self.data.low, timeperiod=14)

        self.ppo = bt.talib.PPO(self.data.close, fastperiod=12, slowperiod=26, matype=0)
        self.roc = bt.talib.ROC(self.data.close, timeperiod=10)
        self.rocp = bt.talib.ROCP(self.data.close, timeperiod=10)
        self.rocr = bt.talib.ROCR(self.data.close, timeperiod=10)
        self.rocr100 = bt.talib.ROCR100(self.data.close, timeperiod=10)

        self.stoch = bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
                                    fastk_period=5, slowk_period=3, slowk_matype=0,
                                    slowd_period=3, slowd_matype=0)

        self.stochf = bt.talib.STOCHF(self.data.high, self.data.low, self.data.close,
                                      fastk_period=5, fastd_period=3, fastd_matype=0)

        self.stochrsi = bt.talib.STOCHRSI(self.data.close,
                                          timeperiod=14, fastk_period=5,
                                          fastd_period=3, fastd_matype=0)

        self.ultosc = bt.talib.ULTOSC(self.data.high, self.data.low, self.data.close,
                                      timeperiod1=7, timeperiod2=14, timeperiod3=28)
