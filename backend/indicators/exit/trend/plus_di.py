import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    plus_di = talib.PLUS_DI(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return plus_di > 25  # 自訂閾值

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
