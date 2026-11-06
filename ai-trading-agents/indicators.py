"""
Indicators: extra columns calculated from the price.

A moving average is the average closing price of the last N days.
It smooths out daily zigzags so the trend is easier to see.
- SMA_20 (fast): reacts quickly to new prices
- SMA_50 (slow): reacts slowly
When the fast line crosses ABOVE the slow line, the trend may be turning up
("golden cross"). When it crosses BELOW, the trend may be turning down.
"""
import pandas as pd


def add_moving_averages(data):
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    return data


def load_prices(path):
    """Read a price CSV with dates as the row labels."""
    return pd.read_csv(path, index_col="Date", parse_dates=True)
