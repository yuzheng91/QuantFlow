import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    minus_di = talib.MINUS_DI(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return minus_di < 20  # 可依策略調整

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
