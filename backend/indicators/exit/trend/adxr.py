import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    adxr = talib.ADXR(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return adxr > 25

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
