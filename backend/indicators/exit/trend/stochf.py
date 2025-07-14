import pandas as pd, talib

def generate_signal(df: pd.DataFrame, fastk_period: int = 5, fastd_period: int = 3) -> pd.Series:
    fastk, fastd = talib.STOCHF(df['High'], df['Low'], df['Close'],
                                fastk_period=fastk_period,
                                fastd_period=fastd_period,
                                fastd_matype=0)
    return (fastk > fastd) & (fastk < 20)

def param_schema():
    return {
        "fastk_period": {"type": "int", "default": 5, "min": 1, "max": 50},
        "fastd_period": {"type": "int", "default": 3, "min": 1, "max": 50}
    }
