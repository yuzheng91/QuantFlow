import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod1: int = 7, timeperiod2: int = 14, timeperiod3: int = 28) -> pd.Series:
    ultosc = talib.ULTOSC(df["High"], df["Low"], df["Close"],
                          timeperiod1=timeperiod1,
                          timeperiod2=timeperiod2,
                          timeperiod3=timeperiod3)
    return ultosc > 50

def param_schema():
    return {
        "timeperiod1": {"type": "int", "default": 7, "min": 1, "max": 50},
        "timeperiod2": {"type": "int", "default": 14, "min": 1, "max": 100},
        "timeperiod3": {"type": "int", "default": 28, "min": 1, "max": 200}
    }
