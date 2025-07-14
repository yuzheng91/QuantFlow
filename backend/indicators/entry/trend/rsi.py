import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    rsi = talib.RSI(df["Close"], timeperiod=timeperiod)
    return rsi < 30  # 超賣可進場（範例策略）

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
