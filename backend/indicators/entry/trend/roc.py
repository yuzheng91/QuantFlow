import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 10) -> pd.Series:
    roc = talib.ROC(df["Close"], timeperiod=timeperiod)
    return roc > 0

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 10, "min": 1, "max": 100}
    }
