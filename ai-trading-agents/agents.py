"""
The trading robots ("agents").

An agent is just a function. It looks at the price history up to today
and answers with one word: "buy", "sell" or "hold".
All agents live in this one file. More arrive in Weeks 4 and 6.
"""


def buy_and_hold(history):
    # Says "buy" every day. On day one it spends all the cash, so after that
    # there is no money left to buy with, and it simply holds forever.
    # This is the lazy baseline every smarter agent has to beat.
    return "buy"
