import backtrader as bt
import pandas as pd
import numpy as np
import talib as ta

def run_backtest(strategy_class):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class)

    df = pd.read_csv('data/AAPL_daily_2012_2024.csv', index_col='Date', parse_dates=True)
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    start_value = 10000

    cerebro.broker.setcash(start_value)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=80)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    strat = results[0]
    final_value = cerebro.broker.getvalue()
    print(f"Final Portfolio Value: {final_value:.2f}")

    start_date = df.index[0]
    end_date = df.index[-1]
    years = (end_date - start_date).days / 365.25
    cagr = (final_value / start_value) ** (1 / years) - 1

    sharpe = strat.analyzers.sharpe.get_analysis()
    drawdown = strat.analyzers.drawdown.get_analysis()

    return {
        "start_value": round(start_value, 2),
        "final_value": round(final_value, 2),
        "cagr": round(cagr * 100, 2),
        "sharpe": round(sharpe.get("sharperatio", 0), 2),
        "max_drawdown": round(drawdown.max.drawdown, 2),
        "drawdown_duration": drawdown.max.len
    }


if __name__ == '__main__':
    run_backtest()
    