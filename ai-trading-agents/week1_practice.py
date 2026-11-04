# Week 1: my first script.
# It reads a small table of prices, prints the first rows, and draws a chart.
# If you see "No module named pandas", run this in the terminal:  pip install pandas matplotlib

import pandas as pd                 # pandas = tables of data (called DataFrames)
import matplotlib.pyplot as plt     # matplotlib = drawing charts

# sample.csv is a tiny made-up price table, just for practice.
data = pd.read_csv("sample.csv")

print(data.head())                  # shows the first 5 rows of the table

data["Close"].plot(title="My first market chart")   # draw the "Close" column as a line
plt.show()                                           # open the chart window
