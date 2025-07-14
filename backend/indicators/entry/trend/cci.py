import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    cci = talib.CCI(df["High"], df["Low"], df["Close"], timeperiod=timeperiod)
    return cci > 100  # 可調整為 >0 或其他閾值

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
