import pandas as pd, talib

def generate_signal(df: pd.DataFrame, penetration: float = 0.3) -> pd.Series:
    return talib.CDLEVENINGSTAR(df["Open"], df["High"], df["Low"], df["Close"], penetration=penetration) < 0

def param_schema():
    return {
        "penetration": {"type": "float", "default": 0.3, "min": 0, "max": 1}
    }
