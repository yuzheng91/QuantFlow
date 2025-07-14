import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 15) -> pd.Series:
    trix = talib.TRIX(df["Close"], timeperiod=timeperiod)
    return trix > 0

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 15, "min": 1, "max": 100}
    }
