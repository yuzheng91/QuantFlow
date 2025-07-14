import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    adx = talib.ADX(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return adx > 25  # 可自定閾值（這裡是示範）

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
