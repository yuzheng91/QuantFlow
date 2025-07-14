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
        if not self.position and self.entry_signal[self.signal_index]:
            self.buy()
        elif self.position and self.exit_signal[self.signal_index]:
            self.sell()
        self.signal_index += 1
        # 每一根 K 棒結束時記錄帳戶總值
        self.daily_value.append(self.broker.getvalue())
        self.daily_dates.append(self.data.datetime.date(0))

def backtest(entry_category: str, entry_indicator: str, exit_category: str, exit_indicator: str, entry_params: dict,
             exit_params: dict):
    df = pd.read_csv("data/AAPL_daily_2012_2024.csv", index_col="Date", parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)
    entry_module = importlib.import_module(f"indicators.entry.{entry_category}.{entry_indicator}")
    exit_module = importlib.import_module(f"indicators.exit.{exit_category}.{exit_indicator}")

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(CustomStrategy,
                        entry_signal=entry_module.generate_signal(df, **entry_params),
                        exit_signal=exit_module.generate_signal(df, **exit_params))
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
