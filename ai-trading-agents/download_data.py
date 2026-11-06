"""
Week 2: download about 10 years of real daily prices for four mining
companies whose share prices move with iron ore.

Run once:  python download_data.py
Creates:   data/VALE.csv, data/BHP.csv, data/RIO.csv, data/FMG_AX.csv
"""
import os
import yfinance as yf

tickers = ["VALE", "BHP", "RIO", "FMG.AX"]  # FMG.AX = Fortescue, listed in Australia

os.makedirs("data", exist_ok=True)  # make the data folder if it isn't there yet

for t in tickers:
    print("Downloading", t)
    data = yf.download(
        t,
        start="2015-01-01",
        end="2025-12-31",
        auto_adjust=True,          # adjusts old prices for dividends and stock splits
        multi_level_index=False,   # keeps simple column names: Open, High, Low, Close, Volume
        progress=False,
    )

    if data.empty:
        print("  Nothing came back for", t, "- check your internet and try again")
        continue

    filename = "data/" + t.replace(".", "_") + ".csv"  # "FMG.AX" -> "FMG_AX"
    data.to_csv(filename)
    print("  Saved", len(data), "days of data to", filename)
