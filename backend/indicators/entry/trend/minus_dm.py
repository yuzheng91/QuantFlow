import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    minus_dm = talib.MINUS_DM(df["High"], df["Low"], timeperiod=timeperiod)
    return minus_dm < 10  # 可依策略調整

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
