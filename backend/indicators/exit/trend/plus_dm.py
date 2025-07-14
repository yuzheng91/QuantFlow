import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    plus_dm = talib.PLUS_DM(df["High"], df["Low"], timeperiod=timeperiod)
    return plus_dm > 10

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
