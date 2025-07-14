import pandas as pd, talib

def generate_signal(df: pd.DataFrame,
                    fastperiod: int = 12,
                    slowperiod: int = 26,
                    signalperiod: int = 9) -> pd.Series:
    macd, signal, _ = talib.MACD(df["Close"], fastperiod, slowperiod, signalperiod)
    return macd > signal  # 黃金交叉

def param_schema():
    return {
        "fastperiod": {"type": "int", "default": 12, "min": 1, "max": 100},
        "slowperiod": {"type": "int", "default": 26, "min": 1, "max": 100},
        "signalperiod": {"type": "int", "default": 9, "min": 1, "max": 100}
    }
