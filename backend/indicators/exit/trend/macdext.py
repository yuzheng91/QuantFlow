import pandas as pd, talib

def generate_signal(df: pd.DataFrame,
                    fastperiod: int = 12,
                    fastmatype: int = 0,
                    slowperiod: int = 26,
                    slowmatype: int = 0,
                    signalperiod: int = 9,
                    signalmatype: int = 0) -> pd.Series:
    macd, signal, _ = talib.MACDEXT(df["Close"],
                                    fastperiod, fastmatype,
                                    slowperiod, slowmatype,
                                    signalperiod, signalmatype)
    return macd > signal

def param_schema():
    return {
        "fastperiod": {"type": "int", "default": 12, "min": 1, "max": 100},
        "fastmatype": {"type": "int", "default": 0, "min": 0, "max": 8},
        "slowperiod": {"type": "int", "default": 26, "min": 1, "max": 100},
        "slowmatype": {"type": "int", "default": 0, "min": 0, "max": 8},
        "signalperiod": {"type": "int", "default": 9, "min": 1, "max": 100},
        "signalmatype": {"type": "int", "default": 0, "min": 0, "max": 8}
    }
