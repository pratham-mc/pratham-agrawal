"""
Weeks 3 and 4: the backtester, and a head-to-head race between agents.

Replays history one day at a time, lets each agent decide what to do,
and keeps track of the fake money.

Run:   python backtest.py            (Buy and Hold vs Momentum on VALE)
       python backtest.py BHP        (another stock: BHP, RIO, FMG_AX)
       python backtest.py sample.csv (practice data)
"""
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from indicators import add_moving_averages, load_prices
from agents import buy_and_hold, momentum_agent

STARTING_CASH = 100000
FEE = 0.001  # 0.1% charged on every buy and every sell, like a real broker


def run_backtest(data, decide_function, starting_cash=STARTING_CASH):
    """
    Replays history one day at a time.
    - data: the price table with indicators already added
    - decide_function: an agent; it looks at history so far and returns
      "buy", "sell" or "hold"
    Returns: a list of daily portfolio values, and a list of all trades made.
    """
    cash = starting_cash
    shares = 0
    daily_values = []
    trades = []

    for i in range(60, len(data)):  # start at day 60 so the 50-day average exists
        history = data.iloc[: i + 1]  # only data up to "today" - no peeking!
        today = data.index[i]
        price = float(data["Close"].iloc[i])

        decision = decide_function(history)

        if decision == "buy" and cash > 0:
            shares = cash * (1 - FEE) / price  # spend all cash, minus the fee
            cash = 0
            trades.append((today.date(), "BUY", round(price, 2)))
        elif decision == "sell" and shares > 0:
            cash = shares * price * (1 - FEE)  # sell everything, minus the fee
            shares = 0
            trades.append((today.date(), "SELL", round(price, 2)))

        daily_values.append(cash + shares * price)  # what everything is worth today

    return daily_values, trades


def worst_drawdown(values):
    """
    The scariest fall from a high point, in percent.
    If the money went from 100,000 down to 70,000 at some point,
    that's a -30% drawdown, even if it recovered later.
    """
    peak = values[0]
    worst = 0
    for v in values:
        if v > peak:
            peak = v  # new high point
        drop = (v - peak) / peak * 100
        if drop < worst:
            worst = drop
    return worst


def score(values, trades):
    final = values[-1]
    return {
        "Final value": round(final),
        "Total return %": round((final / STARTING_CASH - 1) * 100, 1),
        "Worst drawdown %": round(worst_drawdown(values), 1),
        "Number of trades": len(trades),
    }


if __name__ == "__main__":
    # Work out which price file to use
    choice = sys.argv[1] if len(sys.argv) > 1 else "VALE"
    path = choice if choice.endswith(".csv") else "data/" + choice + ".csv"
    name = "practice data" if choice.endswith(".csv") else choice

    if not os.path.exists(path):
        print("No file", path, "- run python download_data.py first")
        sys.exit()

    data = load_prices(path)
    if len(data) <= 60:
        print("Only", len(data), "days in", path, "- the backtest needs more than 60 days")
        sys.exit()
    data = add_moving_averages(data)
    dates = data.index[60:]  # the days the backtest covered

    # The agents taking part in the race: name to show -> agent function
    agents = {"Buy and Hold": buy_and_hold, "Momentum": momentum_agent}

    all_values = {}   # each agent's daily portfolio values
    all_trades = {}   # each agent's list of trades
    all_scores = {}   # each agent's score card
    for agent_name, agent in agents.items():
        values, trades = run_backtest(data, agent)
        all_values[agent_name] = values
        all_trades[agent_name] = trades
        all_scores[agent_name] = score(values, trades)

    # 1) The scores side by side: one row per agent
    print("Head-to-head on", name)
    print("From", dates[0].date(), "to", dates[-1].date(), "-", len(dates), "trading days")
    print()
    print(pd.DataFrame.from_dict(all_scores, orient="index"))  # orient="index": one row per agent
    print()

    # 2) The Momentum agent's trades, numbered, so you can find them on the Week 2 chart
    print("Momentum trades:")
    for number, (day, action, price) in enumerate(all_trades["Momentum"], start=1):
        print(f"  {number}. {action} on {day} at {price}")

    # 3) One chart with one line per agent
    os.makedirs("charts", exist_ok=True)
    plt.figure(figsize=(12, 6))
    for agent_name, values in all_values.items():
        plt.plot(dates, values, label=agent_name)
    plt.axhline(STARTING_CASH, color="grey", linestyle="--", label="Starting cash")
    plt.title("Buy and Hold vs Momentum on " + name + ": value of 100,000 of fake money")
    plt.ylabel("Portfolio value")
    plt.gca().yaxis.set_major_formatter("{x:,.0f}")  # show 400,000 instead of 0.4 x 1e6
    plt.grid(alpha=0.3)
    plt.legend()
    filename = "charts/race_" + name.replace(" ", "_") + ".png"
    plt.savefig(filename, dpi=120, bbox_inches="tight")
    print("Saved", filename)
    plt.show()
