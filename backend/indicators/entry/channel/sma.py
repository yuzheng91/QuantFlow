import pandas as pd
import talib

def generate_signal(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    若收盤價 > SMA，則產生進場訊號。
    回傳一個布林序列（True 代表發出進場訊號）
    """
    sma = talib.SMA(df['Close'], timeperiod=period)
    return df['Close'] > sma
def param_schema():
    return {
        "period": {"type": "int", "default": 20, "min": 1, "max": 400},
    }
