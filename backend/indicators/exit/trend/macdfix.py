import pandas as pd, talib

def generate_signal(df: pd.DataFrame, signalperiod: int = 9) -> pd.Series:
    macd, signal, _ = talib.MACDFIX(df["Close"], signalperiod=signalperiod)
    return macd > signal  # 黃金交叉

def param_schema():
    return {
        "signalperiod": {"type": "int", "default": 9, "min": 1, "max": 100}
    }
