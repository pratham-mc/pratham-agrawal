# Week 2: moving averages - my first trading signal.
#
# A moving average smooths out the daily zigzags.
#   SMA_20 = average of the last 20 closing prices (reacts fast)
#   SMA_50 = average of the last 50 closing prices (reacts slowly)
# When SMA_20 crosses ABOVE SMA_50 the trend may be turning up   ("golden cross", a buy signal).
# When SMA_20 crosses BELOW SMA_50 the trend may be turning down ("death cross", a sell signal).
# The first 19 / 49 rows have no average yet (not enough days), so they are empty (NaN).

import pandas as pd


def add_moving_averages(data):
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    return data
