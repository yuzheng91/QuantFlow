# 1. backend/run_backtest.py
import importlib
import pandas as pd
import backtrader as bt
from chart import build_chart_b64, build_drawdown_chart_b64

class CustomStrategy(bt.Strategy):
    def __init__(self, entry_signal, exit_signal):
        self.entry_signal = entry_signal
        self.exit_signal = exit_signal
        self.signal_index = 0  # 為每根K棒取對應位置
        self.daily_value = [] # 儲存每日資產
        self.daily_dates = []

    def next(self):
        if self.signal_index >= len(self.entry_signal):
            return
        if not self.position and self.entry_signal.iloc[self.signal_index]:
            self.buy()
        elif self.position and self.exit_signal[self.signal_index]:
            self.sell()
        self.signal_index += 1
        # 每一根 K 棒結束時記錄帳戶總值
        self.daily_value.append(self.broker.getvalue())
        self.daily_dates.append(self.data.datetime.date(0))

def combine_signals(signals, mode='and'):
    if not signals:
        return pd.Series([False] * (signals[0]));
    
    combined = signals[0].copy()
    for sig in signals[1:]:
        if mode == 'and':
            combined &= sig
        elif mode =='or':
            combined |= sig
    return combined
        

def backtest(entry_indicators,exit_indicators, entry_mode='and', exit_mode='or'):
    df = pd.read_csv("data/AAPL_daily_2012_2024.csv", index_col="Date", parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)
    
    # --- Load entry signals ---
    entry_signals = []
    for ind in entry_indicators:
        cat = ind["category"]
        name = ind["name"]
        params = ind.get("params", {})
        mod = importlib.import_module(f"indicators.entry.{cat}.{name}")
        func = getattr(mod, "generate_signal")
        entry_signals.append(func(df.copy(), **params))

    combined_entry = combine_signals(entry_signals, mode=entry_mode)

    # --- Load exit signals ---
    exit_signals = []
    for ind in exit_indicators:
        cat = ind["category"]
        name = ind["name"]
        params = ind.get("params", {})
        mod = importlib.import_module(f"indicators.exit.{cat}.{name}")
        func = getattr(mod, "generate_signal")
        exit_signals.append(func(df.copy(), **params))

    combined_exit = combine_signals(exit_signals, mode=exit_mode)

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(CustomStrategy,
                        entry_signal=combined_entry,
                        exit_signal=combined_exit)
    start_value = 10000
    cerebro.broker.setcash(start_value)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=80)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    results = cerebro.run()
    
    start = results[0]
    portfolio_val = start.daily_value
    portfolio_dates = pd.to_datetime(start.daily_dates)
    
    final_value = cerebro.broker.getvalue()
    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days / 365.25
    cagr = (final_value / start_value) ** (1 / years) - 1
    sharpe = start.analyzers.sharpe.get_analysis()
    drawdown = start.analyzers.drawdown.get_analysis()
    chart_b64 = build_chart_b64(
        portfolio_values = portfolio_val,
        dates            = portfolio_dates
    )
    drawdown_chart_b64 = build_drawdown_chart_b64(
        portfolio_values = portfolio_val,
        dates            = portfolio_dates
    )
    return {
        "start_value": round(start_value, 2),
        "final_value": round(final_value, 2),
        "cagr": round(cagr * 100, 2),
        "sharpe": round(sharpe.get("sharperatio", 0), 2),
        "max_drawdown": round(drawdown.max.drawdown, 2),
        "drawdown_duration": drawdown.max.len,
        "chart"           : chart_b64  ,
        "drawdown_chart": drawdown_chart_b64,
    }
