import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    willr = talib.WILLR(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return willr < -80  # 超賣區

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
