import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    atr = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=timeperiod)
    return atr > atr.mean()

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
