import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    return talib.CDLABANDONEDBABY(df["Open"], df["High"], df["Low"], df["Close"], penetration=0.3) > 0

def param_schema():
    return {
        "penetration": {"type": "float", "default": 0.3, "min": 0, "max": 1}
    }
