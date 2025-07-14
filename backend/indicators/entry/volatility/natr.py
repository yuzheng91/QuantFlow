import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    natr = talib.NATR(df['High'], df['Low'], df['Close'], timeperiod=timeperiod)
    return natr > natr.mean()

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
