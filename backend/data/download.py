import yfinance as yf
import pandas as pd
import time
import os

tickers = [
    "AAPL", "MSFT", "JPM", "V", "PG", "JNJ", "UNH", "HD", "INTC", "KO",
    "MRK", "PFE", "DIS", "CVX", "VZ", "IBM", "WMT", "MCD", "NKE", "BA",
    "TRV", "AXP", "CAT", "GS", "MMM", "CSCO", "DOW", "WBA", "AMGN", "HON"
]

start_date = "2012-01-03"
end_date = "2024-12-27"

output_dir = "dow30_data"
os.makedirs(output_dir, exist_ok=True)

for ticker in tickers:
    print(f"Downloading {ticker}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            data.to_csv(f"{output_dir}/{ticker}.csv")
        else:
            print(f"⚠️ No data for {ticker}")
    except Exception as e:
        print(f"❌ Error downloading {ticker}: {e}")

    time.sleep(2)  # ✅ 等 2 秒防止 API 封鎖