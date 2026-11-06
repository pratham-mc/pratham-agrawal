"""
The trading robots ("agents").

An agent is just a function. It looks at the price history up to today
and answers with one word: "buy", "sell" or "hold".
All agents live in this one file. More arrive in Weeks 4 and 6.
"""
import pandas as pd


def buy_and_hold(history):
    # Says "buy" every day. On day one it spends all the cash, so after that
    # there is no money left to buy with, and it simply holds forever.
    # This is the lazy baseline every smarter agent has to beat.
    return "buy"


def momentum_agent(history):
    # Week 4. Philosophy: "the trend is your friend".
    # Prices that started rising often keep rising for a while.
    today = history.iloc[-1]     # the most recent day the agent can see
    fast = today["SMA_20"]       # 20-day average: reacts quickly
    slow = today["SMA_50"]       # 50-day average: reacts slowly

    if pd.isna(fast) or pd.isna(slow):
        return "hold"            # not enough days yet to work out the averages

    if fast > slow:
        return "buy"             # uptrend: be in the market
    else:
        return "sell"            # downtrend: get out and wait in cash
