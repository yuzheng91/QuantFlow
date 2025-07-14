import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    dx = talib.DX(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return dx > 20

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
