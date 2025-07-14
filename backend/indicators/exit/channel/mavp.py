import pandas as pd, talib
import numpy as np

def generate_signal(df: pd.DataFrame,
                    minperiod: int = 2,
                    maxperiod: int = 30,
                    matype: int = 0) -> pd.Series:
    periods = np.random.randint(minperiod, maxperiod+1, size=len(df))
    mavp = talib.MAVP(df['Close'], periods, minperiod, maxperiod, matype=matype)
    return df['Close'] > mavp

def param_schema():
    return {
        "minperiod": {"type": "int", "default": 2, "min": 1, "max": 30},
        "maxperiod": {"type": "int", "default": 30, "min": 2, "max": 100},
        "matype": {"type": "int", "default": 0, "min": 0, "max": 8}
    }
