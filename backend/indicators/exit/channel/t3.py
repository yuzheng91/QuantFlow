import pandas as pd, talib

def generate_signal(df: pd.DataFrame,
                    timeperiod: int = 5,
                    vfactor: float = 0.7) -> pd.Series:
    t3 = talib.T3(df["Close"], timeperiod=timeperiod, vfactor=vfactor)
    return df["Close"] > t3

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 5, "min": 1, "max": 400},
        "vfactor": {"type": "float", "default": 0.7, "min": 0.0, "max": 1.0}
    }
