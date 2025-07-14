import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 30, matype: int = 0) -> pd.Series:
    ma = talib.MA(df['Close'], timeperiod=timeperiod, matype=matype)
    return df['Close'] > ma

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 30, "min": 1, "max": 100},
        "matype": {"type": "int", "default": 0, "min": 0, "max": 8}
    }
