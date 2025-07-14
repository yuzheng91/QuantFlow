import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    osc = talib.AROONOSC(df["High"], df["Low"], timeperiod=timeperiod)
    return osc > 0

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
