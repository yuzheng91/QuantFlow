import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    midpoint = talib.MIDPOINT(df['Close'], timeperiod=timeperiod)
    return df['Close'] > midpoint

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
