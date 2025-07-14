import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    ad = talib.AD(df["High"], df["Low"], df["Close"], df["Volume"])
    return ad > ad.mean()

def param_schema():
    return {}
