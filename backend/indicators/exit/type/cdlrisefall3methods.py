import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    return talib.CDLRISEFALL3METHODS(df["Open"], df["High"], df["Low"], df["Close"]) != 0

def param_schema():
    return {}