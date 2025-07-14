import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 10) -> pd.Series:
    rocr100 = talib.ROCR100(df["Close"], timeperiod=timeperiod)
    return rocr100 > 100

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 10, "min": 1, "max": 100}
    }
