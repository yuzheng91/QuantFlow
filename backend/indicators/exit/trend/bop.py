import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    bop = talib.BOP(df["Open"], df["High"], df["Low"], df["Close"])
    return bop > 0  # 可依策略調整閾值

def param_schema():
    return {}  # BOP 無參數
