import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    ht = talib.HT_TRENDLINE(df["Close"])
    return df["Close"] > ht

def param_schema():
    return {}  # 沒有參數可設定
