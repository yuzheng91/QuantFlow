import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 30) -> pd.Series:
    kama = talib.KAMA(df["Close"], timeperiod=timeperiod)
    return df["Close"] > kama

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 30, "min": 1, "max": 400}
    }
