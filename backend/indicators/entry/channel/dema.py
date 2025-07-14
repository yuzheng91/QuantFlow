import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 30) -> pd.Series:
    dema = talib.DEMA(df['Close'], timeperiod=timeperiod)
    return df['Close'] > dema

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 30, "min": 1, "max": 100}
    }
