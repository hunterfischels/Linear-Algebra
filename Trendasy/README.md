# Trendasy — Stock Theme & Subsector Trend Tracker

A research project tracking how **news and government contracts** correlate to **relative stock-market
gains** across the cycle's hottest subsectors (semiconductors, memory/HBM, photonics, drones, space,
quantum, nuclear, defense, rare earths, and more). Coverage 2024 → June 2026.

> This project lives in its own `Trendasy/` directory, separate from the repository's linear-algebra
> code at the repo root. Figures are approximate — **not investment advice.**

## Contents

| Path | What it is |
|---|---|
| [`STOCK_THEME_TRENDS_TRACKER.md`](./STOCK_THEME_TRENDS_TRACKER.md) | Master cross-sector catalyst timeline + 9 subsector deep-dives (narrative, key-ticker performance, dated event timelines, sources). |
| [`WATCHLISTS_AND_FUNDAMENTALS.md`](./WATCHLISTS_AND_FUNDAMENTALS.md) | Per-ETF watchlists with EPS growth, P/E, forward P/E, margins, and backlog; 5-year ETF return tables. |
| [`streamlit_app/`](./streamlit_app) | **Interactive dashboard** (Streamlit): adjustable start date, clickable news nodes, 87 ETFs grouped by subsector, fundamentals tabs, live Yahoo refresh. |
| [`assets/interactive_etf_chart.html`](./assets/interactive_etf_chart.html) | Standalone interactive chart (no install — open in a browser). |
| [`assets/*.png`](./assets) | Static 5-year relative-performance charts. |
| [`index.html`](./index.html) | Landing page (also the GitHub Pages site root). |

## Run the app

```bash
cd Trendasy/streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

See [`streamlit_app/README.md`](./streamlit_app/README.md) for details and free deployment on
Streamlit Community Cloud (main file: `Trendasy/streamlit_app/app.py`).

## Data sources

Prices: Yahoo Finance (daily adjusted-close). Fundamentals: stockanalysis.com + company IR / SEC
filings (~June 2026). Catalysts: curated from Reuters, CNBC, Defense News, White House / DOE / DARPA /
NASA, and company releases (cited in the markdown docs).
