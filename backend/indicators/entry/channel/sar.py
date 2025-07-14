import pandas as pd, talib

def generate_signal(df: pd.DataFrame,
                    acceleration: float = 0.02,
                    maximum: float = 0.2) -> pd.Series:
    sar = talib.SAR(df["High"], df["Low"],
                    acceleration=acceleration,
                    maximum=maximum)
    return df["Close"] > sar

def param_schema():
    return {
        "acceleration": {"type": "float", "default": 0.02, "min": 0.001, "max": 1.0},
        "maximum": {"type": "float", "default": 0.2, "min": 0.01, "max": 1.0}
    }
