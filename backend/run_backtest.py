# 1. backend/run_backtest.py
import importlib
import pandas as pd
import backtrader as bt
import numpy as np

class CustomStrategy(bt.Strategy):
    def __init__(self, entry_signal, exit_signal):
        self.entry_signal = entry_signal
        self.exit_signal = exit_signal
        self.signal_index = 0  # 為每根K棒取對應位置
        self.daily_value = [] # 儲存每日資產
        self.daily_dates = []
        self.signal_log = [] # 紀錄買賣點(time, signal)
        self.trades = []

    def next(self):
        if self.signal_index >= len(self.entry_signal):
            return

        current_date = self.data.datetime.date(0)
        
        if not self.position and self.entry_signal.iloc[self.signal_index]:
            self.buy()
            self.signal_log.append({"time": current_date.strftime("%Y-%m-%d"), "signal": "buy"})
        elif self.position and self.exit_signal.iloc[self.signal_index]:
            self.sell()
            self.signal_log.append({"time": current_date.strftime("%Y-%m-%d"), "signal": "sell"})
        self.signal_index += 1
        # 每一根 K 棒結束時記錄帳戶總值
        self.daily_value.append(self.broker.getvalue())
        self.daily_dates.append(current_date)
    
    def notify_trade(self, trade):
        if trade.isclosed:
            pnl = trade.pnl
            self.trades.append(pnl)

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
    df = pd.read_csv("data/MSFT.csv", index_col="Date", parse_dates=True)
    kline_data = [
        {
            "time": date.strftime("%Y-%m-%d"),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"]
        }
        for date, row in df.iterrows()
    ]

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
    
    strategy = results[0]
    
    final_value = cerebro.broker.getvalue()
    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days / 365.25
    cagr = (final_value / start_value) ** (1 / years) - 1
    sharpe = strategy.analyzers.sharpe.get_analysis()
    drawdown = strategy.analyzers.drawdown.get_analysis()
    signals = strategy.signal_log
    returns = strategy.trades
    wins = sum([1 for r in returns if r > 0])
    win_rate = wins / len(returns)
    num_trades = len(returns)
    avg_pl = np.mean(returns)
    profits = [r for r in returns if r > 0]
    losses = [r for r in returns if r < 0]
    profit_factor = sum(profits) / abs(sum(losses)) if losses else np.inf
    max_profit = max(returns)
    max_loss = min(returns)
    calmar_ratio = cagr / abs(drawdown.max.drawdown) if drawdown.max.drawdown != 0 else np.inf
    return {
        "start_value": round(start_value, 2),
        "final_value": round(final_value, 2),
        "cagr": round(cagr * 100, 2),
        "sharpe": round(sharpe.get("sharperatio", 0), 2),
        "max_drawdown": round(drawdown.max.drawdown, 2),
        "drawdown_duration": drawdown.max.len,
        "win_rate": round(win_rate, 4),
        "num_trades": num_trades,
        "avg_pl": round(avg_pl, 2),
        "profit_factor": round(profit_factor, 2),
        "max_profit": round(max_profit, 2),
        "max_loss": round(max_loss, 2),
        "calmar_ratio": round(calmar_ratio, 2),
        "signals": signals,
        "kline": kline_data,
    }
