# AI Trading Agents — Iron Ore Market Simulator

This project replays about ten years of real stock market history, one day at a time, and lets three
"robot traders" (agents) decide when to buy and sell with fake money. The stocks are big mining
companies (Vale, BHP, Rio Tinto, Fortescue) whose prices move with iron ore — the commodity my mother
trades professionally. The goal is to find out, honestly, which simple strategy works best in a crash,
a boom and a slump, and to explain why.

> No real money is ever used. Everything is a simulation on past data.

---

## Where things are

```
ai-trading-agents/
├── README.md              ← this page
├── requirements.txt       ← the Python libraries the project needs
├── LEARNING_LOG.md        ← date, what broke, how I fixed it
│
├── week1_practice.py      ← Week 1: first script, draws a chart from sample.csv
├── sample.csv             ← a tiny made-up price table, only for Week 1 practice
│
├── download_data.py       ← Week 2: downloads real prices into data/
├── indicators.py          ← Week 2: adds the 20-day and 50-day moving averages
├── charts.py              ← Week 2: draws price + moving average charts into charts/
│
├── agents.py              ← the trading robots: Buy and Hold (Week 3), Momentum (Week 4)
├── backtest.py            ← Weeks 3–4: the backtester, the scoring, and the agents' race
│
├── data/                  ← real price CSVs (filled when you run download_data.py)
├── charts/                ← saved chart images
└── notes/                 ← written work: Domain Brief, Mom's comments, "no peeking" rule, Week 4 verdict
```

## How to run it (on your own computer)

1. Open the **`ai-trading-agents`** folder in VS Code (File → Open Folder). The scripts look for
   `data/` and `charts/` next to them, so open this folder itself, not the folder above it.
2. Open the terminal in VS Code (View → Terminal) and install the libraries once:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scripts in this order:
   ```bash
   python week1_practice.py
   ```
   ```bash
   python download_data.py
   ```
   ```bash
   python charts.py
   ```
   ```bash
   python backtest.py
   ```
   ```bash
   python backtest.py BHP
   ```

`download_data.py` needs the internet. It only has to run once; after that the prices are saved in `data/`.

---

## Weeks 1–4 checklist

**Week 1 — Understand the market, set up tools**
- [x] Interview Mom (about 90 min, record with permission)
- [ ] Write it up → `notes/week1_domain_brief.md`
- [ ] Install Python 3.11+, VS Code (+ Python extension), make a GitHub account
- [x] Project README (this page)
- [x] `week1_practice.py` — run it and see a chart appear

**Week 2 — Real data and signal charts**
- [x] `download_data.py`, `indicators.py`, `charts.py`
- [x] Run `download_data.py` → 4 CSVs appear in `data/`
- [x] Run `charts.py` → 4 charts appear in `charts/`
- [ ] Show the charts to Mom → write `notes/week2_mom_chart_notes.md`

**Week 3 — The backtester**
- [x] `backtest.py` with the backtester and the scoring code; the Buy and Hold agent in `agents.py`
- [x] Run it → Buy and Hold chart and the printed statistics
- [ ] Write the "no peeking" rule in your own words → `notes/week3_no_peeking_rule.md`

**Week 4 — The Momentum agent**
- [x] `agents.py` with the Momentum agent
- [ ] Run `python backtest.py` and `python backtest.py BHP` → `charts/race_VALE.png`, `charts/race_BHP.png` and the scores side by side
- [ ] Find 3 Momentum trades on the Week 2 chart; write the five-sentence verdict → `notes/week4_verdict.md`
- [ ] Ask Mom about trend-following → add her answer to `notes/week4_verdict.md`

The project rule: AI tools can help write code, but I must be able to explain every line I keep.
