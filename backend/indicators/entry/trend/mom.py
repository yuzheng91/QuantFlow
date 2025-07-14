import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 10) -> pd.Series:
    mom = talib.MOM(df["Close"], timeperiod=timeperiod)
    return mom > 0

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 10, "min": 1, "max": 100}
    }
