import pandas as pd, talib

def generate_signal(df: pd.DataFrame, timeperiod: int = 14, fastk_period: int = 5, fastd_period: int = 3) -> pd.Series:
    fastk, fastd = talib.STOCHRSI(df['Close'],
                                  timeperiod=timeperiod,
                                  fastk_period=fastk_period,
                                  fastd_period=fastd_period,
                                  fastd_matype=0)
    return (fastk > fastd) & (fastk < 20)

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 14, "min": 1, "max": 100},
        "fastk_period": {"type": "int", "default": 5, "min": 1, "max": 50},
        "fastd_period": {"type": "int", "default": 3, "min": 1, "max": 50}
    }
