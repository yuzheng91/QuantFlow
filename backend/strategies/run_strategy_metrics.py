from backtrader import Cerebro
from main import run_backtest
from strategies.rsi import RSIStrategy
from strategies.macd import MACDStrategy
from strategies.bollinger_bands import BollingerBandsStrategy
from strategies.bullish_marubozu import BullishMarubozuStrategy
from strategies.bullish_williams_fractals import BullishWilliamsFractalsStrategy
from strategies.hammer import HammerStrategy
from strategies.macd_fractals import MACDFractalsStrategy
from strategies.sar_osc import SAROscStrategy
from strategies.bearish_williams_fractals import BearishWilliamsFractalsStrategy
from strategies.hangingman import HangingmanStarStrategy
from strategies.rsi import RSIStrategy
from strategies.shootingstar import ShootingStarStrategy
from strategies.trend_based import TrendBasedStrategy
from strategies.volume_reversal import VolumeReversalStrategy
from datetime import date

def run_strategy_metrics():
    strategies = [
        {"name": "MACD", "class": MACDStrategy},
        {"name": "RSI", "class": RSIStrategy},
        {"name": "BollingerBands", "class": BollingerBandsStrategy},
        {"name": "BullishMarubozu", "class": BullishMarubozuStrategy},
        {"name": "BullishWilliamsFractal", "class": BullishWilliamsFractalsStrategy},
        {"name": "MACDFractal", "class": MACDFractalsStrategy},
        {"name": "SAROSC", "class": SAROscStrategy},
        {"name": "Hammer", "class": HammerStrategy},
        {"name": "BearishWilliamsFractal", "class": BearishWilliamsFractalsStrategy},
        {"name": "Hangingman", "class": HangingmanStarStrategy},
        {"name": "Shootingstar", "class": ShootingStarStrategy},
        {"name": "TrendBased", "class": TrendBasedStrategy},
        {"name": "VolumeReversal", "class": VolumeReversalStrategy},
    ]

    results = []

    for strategy in strategies:
        metrics = run_backtest(strategy["class"])
        results.append({
            "name": strategy["name"],
            "cagr": round(metrics.get("cagr", 0), 2),
            "max_drawdown": round(metrics.get("max_drawdown", 0), 2),
            "sharpe": round(metrics.get("sharpe", 0), 2),
            "start_value": round(metrics.get("start_value", 0), 2),
            "final_value": round(metrics.get("final_value", 0), 2)
        })

    return results
