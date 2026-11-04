# Week 2: download about 10 years of real daily prices for four mining companies.
# Run it once (it needs the internet). The prices are saved as CSV files in the data/ folder.
#   VALE   = Vale (Brazil)
#   BHP    = BHP (Australia)
#   RIO    = Rio Tinto (Australia / UK)
#   FMG.AX = Fortescue (Australia, listed in Sydney, prices in Australian dollars)

import os
import yfinance as yf

tickers = ["VALE", "BHP", "RIO", "FMG.AX"]

os.makedirs("data", exist_ok=True)      # make the data/ folder if it is not there yet

for t in tickers:
    print("Downloading", t)

    # auto_adjust=True: prices are adjusted for dividends and stock splits,
    # so a buy-and-hold result is fair and not distorted by those events.
    data = yf.download(t, start="2015-01-01", end="2025-12-31", auto_adjust=True, progress=False)

    if len(data) == 0:
        print("  Nothing came back for", t, "- check the internet connection and try again.")
        continue

    # Newer versions of yfinance give each column two names: ("Close", "VALE").
    # We download one ticker at a time, so we keep only the first name: "Close".
    # Without this line the CSV gets two header rows and is hard to read back in.
    data.columns = data.columns.get_level_values(0)

    # "FMG.AX" becomes "FMG_AX.csv" (a dot in a file name can be confusing)
    data.to_csv("data/" + t.replace(".", "_") + ".csv")

    print("  Saved", len(data), "days of data")
