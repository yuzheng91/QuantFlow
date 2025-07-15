import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import quantstats as qs

matplotlib.use("Agg")

def compute_drawdown(series):
    cummax = series.cummax()
    drawdown = (series - cummax) / cummax
    return drawdown

def build_drawdown_chart_b64(portfolio_values, dates):
    """回傳策略與 benchmark 的 drawdown 比較圖（base64編碼）"""
    series = pd.Series(portfolio_values, index=pd.to_datetime(dates))
    strategy_dd = compute_drawdown(series)

    try:
        df_bench = pd.read_csv("data/SPX_2012_2024.csv", index_col="Date", parse_dates=True)
        df_bench = df_bench.loc[series.index]  # 日期對齊
        benchmark_close = df_bench["Close"]
        benchmark_dd = compute_drawdown(benchmark_close)
    except Exception as e:
        print(f"[WARNING] Benchmark 加載失敗: {e}")
        benchmark_dd = pd.Series(index=strategy_dd.index, data=0)

    # 繪圖
    import matplotlib.pyplot as plt
    import io, base64

    plt.figure(figsize=(12, 4))
    plt.plot(strategy_dd, label="Strategy Drawdown", lw=2)
    plt.plot(benchmark_dd, label="Benchmark Drawdown", lw=1.2, ls="--")
    plt.fill_between(strategy_dd.index, strategy_dd, alpha=0.3)
    plt.fill_between(benchmark_dd.index, benchmark_dd, alpha=0.2)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title("Drawdown Comparison")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

def build_chart_b64(portfolio_values, dates):
    """使用 QuantStats 畫出策略 vs Benchmark，輸出 base64 圖片字串"""

    # 將策略資產值轉成報酬率（透過每日資產變化）
    series = pd.Series(portfolio_values, index=pd.to_datetime(dates))
    returns = series.pct_change().fillna(0)

    # 嘗試讀入 benchmark (S&P 500)
    try:
        df_bench = pd.read_csv("data/SPX_2012_2024.csv", index_col="Date", parse_dates=True)
        df_bench = df_bench.loc[returns.index]  # 日期對齊
        benchmark_returns = df_bench["Close"].pct_change().fillna(0)
        common_index = returns.index.intersection(benchmark_returns.index)
        returns = returns.loc[common_index]
        returns.name = "Strategy"
        benchmark_returns = benchmark_returns.loc[common_index]
    except Exception as e:
        print(f"[WARNING] Benchmark 加載失敗: {e}")
        benchmark_returns = None

    # ➤ 用 QuantStats 畫圖到緩衝區
    buf = io.BytesIO()
    qs.plots.returns(
        returns,
        benchmark=benchmark_returns,
        savefig=buf
    )
    plt.close()

    # ➤ 編碼成 base64
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


