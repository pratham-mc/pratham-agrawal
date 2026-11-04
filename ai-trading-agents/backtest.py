# Week 3: a simple backtester.
# A backtester replays history one day at a time and tracks how much fake money a strategy would have.
# Only four ideas:
#   1. walk through the days in order
#   2. show the agent only the past (no peeking at tomorrow!)
#   3. buy or sell with a small fee
#   4. write down the portfolio value every day

import pandas as pd


def run_backtest(data, decide_function, starting_cash=100000):
    """
    Replays history one day at a time.
    - data: the price table with indicators already added
    - decide_function: a function that looks at history so far and returns
      "buy", "sell", or "hold"
    Returns: a list of daily portfolio values, and a list of all trades made.
    """
    cash = starting_cash
    shares = 0
    daily_values = []
    trades = []

    for i in range(60, len(data)):              # start at day 60 so the averages exist
        history = data.iloc[:i + 1]             # only data up to "today" - no peeking!
        today = data.index[i]
        price = float(data["Close"].iloc[i])

        decision = decide_function(history)

        if decision == "buy" and cash > 0:
            shares = cash * 0.999 / price       # 0.1% fee, like a real broker charges
            cash = 0
            trades.append((today, "BUY", round(price, 2)))
        elif decision == "sell" and shares > 0:
            cash = shares * price * 0.999       # fee on the way out too
            shares = 0
            trades.append((today, "SELL", round(price, 2)))

        daily_values.append(cash + shares * price)

    return daily_values, trades


# ---------- Agent 1: Buy and Hold ----------
# An agent is just a function that looks at the history and returns "buy", "sell" or "hold".
def buy_and_hold(history):
    return "buy"    # tries to buy every day; after day one there is no cash left,
                    # so it simply holds forever. The perfect lazy baseline.


# ---------- Scoring ----------
def worst_drawdown_pct(values):
    """The scariest fall from a high point, in %.
    If the money went from 100,000 down to 70,000 at some point, that is a -30% drawdown,
    even if it recovered later."""
    peak = values[0]
    worst = 0
    for v in values:
        peak = max(peak, v)                     # highest value seen so far
        drop = (v - peak) / peak * 100          # how far below that high we are today
        worst = min(worst, drop)                # keep the biggest drop
    return worst


def score(values, trades, starting_cash=100000):
    final = values[-1]
    return {
        "Final value": round(final),
        "Total return %": round((final / starting_cash - 1) * 100, 1),
        "Worst drawdown %": round(worst_drawdown_pct(values), 1),
        "Number of trades": len(trades),
    }


# The code below only runs when you run this file directly (python backtest.py).
# Next week, agents.py can import run_backtest from here without re-running all of this.
if __name__ == "__main__":
    import os
    import matplotlib.pyplot as plt
    from indicators import add_moving_averages

    os.makedirs("charts", exist_ok=True)

    data = pd.read_csv("data/VALE.csv", index_col=0, parse_dates=True)
    data = add_moving_averages(data)

    values, trades = run_backtest(data, buy_and_hold)
    stats = score(values, trades)

    print("Buy and Hold on VALE")
    print(f"Final value: {stats['Final value']:,.0f}")
    print(f"Total return: {stats['Total return %']:.1f}%")
    print(f"Worst drop from a peak (drawdown): {stats['Worst drawdown %']:.1f}%")
    print(f"Number of trades: {stats['Number of trades']}")
    print("Trades:", trades)

    # values[0] is day 60, so the matching dates are data.index[60:]
    plt.figure(figsize=(12, 6))
    plt.plot(data.index[60:], values)
    plt.title("Buy and Hold on VALE - 100,000 of fake money")
    plt.ylabel("Portfolio value")
    plt.savefig("charts/buy_and_hold.png")
    print("Saved charts/buy_and_hold.png")
    plt.show()
