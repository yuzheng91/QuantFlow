import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    midprice = talib.MIDPRICE(df['High'], df['Low'], timeperiod=timeperiod)
    return df['Close'] > midprice

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
