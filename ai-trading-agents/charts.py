"""
Week 2: draw each stock with its two moving averages and save the pictures.

Run:       python charts.py
Creates:   charts/VALE_sma.png, charts/BHP_sma.png, charts/RIO_sma.png, charts/FMG_AX_sma.png

For practice data instead:  python charts.py sample.csv
"""
import os
import sys
import matplotlib.pyplot as plt
from indicators import add_moving_averages, load_prices

os.makedirs("charts", exist_ok=True)


def draw_chart(path, name, start=None):
    data = load_prices(path)
    data = add_moving_averages(data)
    if start:
        data = data[data.index >= start]  # keep only rows from this date onward

    data[["Close", "SMA_20", "SMA_50"]].plot(
        figsize=(12, 6), title=name + " with 20-day and 50-day moving averages"
    )
    plt.ylabel("Price")
    plt.grid(alpha=0.3)

    filename = "charts/" + name.replace(" ", "_") + "_sma.png"
    plt.savefig(filename, dpi=120, bbox_inches="tight")
    plt.close()  # close it so the next chart starts fresh
    print("Saved", filename)


if len(sys.argv) > 1:
    # A file was given on the command line, e.g. python charts.py sample.csv
    draw_chart(sys.argv[1], "practice data")
else:
    for name in ["VALE", "BHP", "RIO", "FMG_AX"]:
        path = "data/" + name + ".csv"
        if os.path.exists(path):
            draw_chart(path, name)
        else:
            print("No file", path, "- run python download_data.py first")

