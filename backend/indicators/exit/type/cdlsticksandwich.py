import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    return talib.CDLSTICKSANDWICH(df["Open"], df["High"], df["Low"], df["Close"]) != 0

def param_schema():
    return {}
