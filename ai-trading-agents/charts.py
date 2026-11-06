# Week 2: draw each stock's price with its two moving averages and save the charts.
# Run download_data.py first, so the data/ folder has the CSV files.

import os
import pandas as pd
import matplotlib.pyplot as plt
from indicators import add_moving_averages

os.makedirs("charts", exist_ok=True)    # make the charts/ folder if it is not there yet

# file name in data/  ->  name to show in the chart title
stocks = {"VALE": "VALE", "BHP": "BHP", "RIO": "RIO", "FMG_AX": "FMG.AX"}

# One chart per stock: the full 10 years
for file_name, title in stocks.items():
    data = pd.read_csv("data/" + file_name + ".csv", index_col=0, parse_dates=True)
    data = add_moving_averages(data)

    data[["Close", "SMA_20", "SMA_50"]].plot(figsize=(12, 6), title=title + " with moving averages")
    plt.ylabel("Price")
    plt.savefig("charts/" + file_name.lower() + "_sma.png")
    plt.close()                         # close it, so the next chart starts fresh
    print("Saved charts/" + file_name.lower() + "_sma.png")
