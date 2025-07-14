import pandas as pd, talib

def generate_signal(df: pd.DataFrame,
                    timeperiod: int = 5,
                    nbdevup: float = 2,
                    nbdevdn: float = 2,
                    matype: int = 0) -> pd.Series:
    upper, middle, lower = talib.BBANDS(df["Close"],
                                        timeperiod=timeperiod,
                                        nbdevup=nbdevup,
                                        nbdevdn=nbdevdn,
                                        matype=matype)
    return df["Close"] > upper

def param_schema():
    return {
        "timeperiod": {"type": "int", "default": 5, "min": 1, "max": 400},
        "nbdevup": {"type": "float", "default": 2, "min": 0, "max": 10},
        "nbdevdn": {"type": "float", "default": 2, "min": 0, "max": 10},
        "matype": {"type": "int", "default": 0, "min": 0, "max": 8}
    }
