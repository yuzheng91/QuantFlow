import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14) -> pd.Series:
    aroon_down, aroon_up = talib.AROON(df["High"], df["Low"], timeperiod=timeperiod)
    return aroon_up > aroon_down

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100}
    }
