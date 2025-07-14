import pandas as pd, talib

def generate_signal(df: pd.DataFrame, fastperiod: int = 12, slowperiod: int = 26, matype: int = 0) -> pd.Series:
    ppo = talib.PPO(df["Close"], fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)
    return ppo > 0

def param_schema():
    return {
        "fastperiod": {"type": "int", "default": 12, "min": 1, "max": 50},
        "slowperiod": {"type": "int", "default": 26, "min": 1, "max": 100},
        "matype": {"type": "int", "default": 0, "min": 0, "max": 8}
    }
