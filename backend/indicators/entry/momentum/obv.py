import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    obv = talib.OBV(df["Close"], df["Volume"])
    return obv > obv.mean()

def param_schema():
    return {}
