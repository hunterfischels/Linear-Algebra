# Thematic ETF & Subsector Trend Tracker — Streamlit app

Interactive dashboard for the stock-theme tracker: relative-performance chart with an adjustable
start date, clickable news nodes, a deep ETF universe grouped by subsector, and per-subsector
watchlists with fundamentals.

## Run locally

```bash
cd Trendasy/streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## Features

- **Adjustable start date** — pick a preset window (1M/3M/6M/1Y/2Y/3Y/YTD/Max) or switch to
  **Custom** for a day-level start slider. Every selected line rebases to 100 at the start so you can
  read short-term *relative* trends.
- **Clickable key-news nodes** — ◆ diamonds sit on the lines at curated catalysts; click one to read
  the event. The "Catalysts in view" table and the **Event timeline** tab stay in sync.
- **Deep ETF universe** — 87 ETFs + SPY benchmark, grouped by subsector; legend shows
  `TICKER · subsector`. Add a whole subsector at once, or All / None / Core.
- **Watchlists & fundamentals** — per-subsector tables with EPS growth, P/E, forward P/E, gross /
  operating / net margins, and backlog.
- **Live refresh** — "Refresh selected from Yahoo" re-pulls prices (needs internet); otherwise the
  bundled snapshot in `data/` is used.

## Data

- `data/etf_prices.json` — daily 5y adjusted-close (Yahoo Finance), per ticker + subsector label.
- `data/events.json` — curated catalysts mapped to a representative ETF.
- `data/fundamentals.json` — per-subsector fundamentals (stockanalysis.com + company IR/SEC, ~Jun 2026).

Figures are **approximate** — verify before use. **Not investment advice.**

## Deploy (free)

Push the repo and deploy on [Streamlit Community Cloud](https://share.streamlit.io): point it at
`Trendasy/streamlit_app/app.py`. (Main file path: `Trendasy/streamlit_app/app.py`.)
