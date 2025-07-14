import pandas as pd, talib

def generate_signal(df: pd.DataFrame, fastk_period: int = 5, slowk_period: int = 3, slowd_period: int = 3) -> pd.Series:
    slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Close'],
                               fastk_period=fastk_period,
                               slowk_period=slowk_period,
                               slowk_matype=0,
                               slowd_period=slowd_period,
                               slowd_matype=0)
    return (slowk > slowd) & (slowk < 20)  # 黃金交叉且超賣

def param_schema():
    return {
        "fastk_period": {"type": "int", "default": 5, "min": 1, "max": 50},
        "slowk_period": {"type": "int", "default": 3, "min": 1, "max": 50},
        "slowd_period": {"type": "int", "default": 3, "min": 1, "max": 50},
    }
