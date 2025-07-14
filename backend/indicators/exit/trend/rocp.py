import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 10) -> pd.Series:
    rocp = talib.ROCP(df["Close"], timeperiod=timeperiod)
    return rocp > 0

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 10, "min": 1, "max": 100}
    }
