import pandas as pd, talib

def generate_signal(df: pd.DataFrame) -> pd.Series:
    tr = talib.TRANGE(df['High'], df['Low'], df['Close'])
    return tr > tr.mean()

def param_schema():
    return {}
