import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    mfi = talib.MFI(df["High"], df["Low"], df["Close"], df["Volume"], timeperiod=timeperiod)
    return mfi > 50  # 可自訂閾值

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
