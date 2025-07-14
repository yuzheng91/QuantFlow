import pandas as pd, talib

def generate_signal(df: pd.DataFrame,
                    startvalue: float = 0.02,
                    offsetonreverse: float = 0.02,
                    accelerationinitlong: float = 0.02,
                    accelerationlong: float = 0.02,
                    accelerationmaxlong: float = 0.2,
                    accelerationinitshort: float = 0.02,
                    accelerationshort: float = 0.02,
                    accelerationmaxshort: float = 0.2) -> pd.Series:
    sarext = talib.SAREXT(df['High'], df['Low'],
                          startvalue=startvalue,
                          offsetonreverse=offsetonreverse,
                          accelerationinitlong=accelerationinitlong,
                          accelerationlong=accelerationlong,
                          accelerationmaxlong=accelerationmaxlong,
                          accelerationinitshort=accelerationinitshort,
                          accelerationshort=accelerationshort,
                          accelerationmaxshort=accelerationmaxshort)
    return df['Close'] > sarext

def param_schema():
    return {
        "startvalue": {"type": "float", "default": 0.02, "min": 0.0, "max": 1.0},
        "offsetonreverse": {"type": "float", "default": 0.02, "min": 0.0, "max": 1.0},
        "accelerationinitlong": {"type": "float", "default": 0.02},
        "accelerationlong": {"type": "float", "default": 0.02},
        "accelerationmaxlong": {"type": "float", "default": 0.2},
        "accelerationinitshort": {"type": "float", "default": 0.02},
        "accelerationshort": {"type": "float", "default": 0.02},
        "accelerationmaxshort": {"type": "float", "default": 0.2}
    }
