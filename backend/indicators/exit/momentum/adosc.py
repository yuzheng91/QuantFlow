import pandas as pd, talib

def generate_signal(df: pd.DataFrame, fastperiod: int = 3, slowperiod: int = 10) -> pd.Series:
    adosc = talib.ADOSC(df["High"], df["Low"], df["Close"], df["Volume"],
                        fastperiod=fastperiod, slowperiod=slowperiod)
    return adosc > 0

def param_schema():
    return {
        "fastperiod": {"type": "int", "default": 3, "min": 1, "max": 50},
        "slowperiod": {"type": "int", "default": 10, "min": 2, "max": 100}
    }
