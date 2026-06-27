"""
Thematic ETF & Subsector Trend Tracker — Streamlit app.

Features
- Relative-performance chart with an adjustable start date (presets + day-level slider)
  that rebases every selected ETF to 100 to isolate short-term relative trends.
- Clickable key-news nodes on the lines (select a diamond to read the catalyst).
- Deep ETF universe (87 ETFs + SPY) grouped by subsector; legend shows "TICKER · subsector".
- Watchlists & fundamentals per subsector (EPS growth, P/E, fwd P/E, margins, backlog).
- Optional live refresh of prices from Yahoo Finance.

Run:  streamlit run streamlit_app/app.py
Data: bundled JSON in ./data (offline by default); "Refresh from Yahoo" pulls live prices.
"""
from __future__ import annotations
import json, datetime as dt, urllib.request
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parent / "data"
st.set_page_config(page_title="Thematic ETF Trend Tracker", page_icon="📈", layout="wide")

PALETTE = ["#4da3ff","#3cb44b","#f58231","#e6194B","#911eb4","#42d4f4","#f032e6","#bfef45",
           "#fabed4","#469990","#9A6324","#e6beff","#aaffc3","#ffd8b1","#a9a9a9","#ffe119",
           "#00d8b4","#dcbeff","#fffac8","#808000"]


# ----------------------------- data loading -----------------------------
@st.cache_data
def load(name: str):
    return json.loads((DATA / name).read_text())


def fetch_yahoo(ticker: str, rng="5y", interval="1d") -> dict | None:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?range={rng}&interval={interval}&includeAdjustedClose=true")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            res = json.load(r)["chart"]["result"][0]
        ts = res["timestamp"]; q = res["indicators"]
        adj = q.get("adjclose", [{}])[0].get("adjclose") if q.get("adjclose") else None
        ser = adj or q["quote"][0]["close"]
        return {dt.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d"): round(float(v), 2)
                for t, v in zip(ts, ser) if v is not None}
    except Exception:
        return None


prices = load("etf_prices.json")
events = load("events.json")
funds = load("fundamentals.json")

# session copy so live refresh can override bundled data
if "prices" not in st.session_state:
    st.session_state.prices = prices
P = st.session_state.prices
dates: list[str] = P["dates"]
TK: dict = P["tickers"]
all_tickers = sorted(TK.keys(), key=lambda t: (TK[t]["sub"], t))
color_of = {t: PALETTE[i % len(PALETTE)] for i, t in enumerate(all_tickers)}
label_of = {t: f"{t} · {TK[t]['sub']}" for t in all_tickers}


def nearest_idx(d: str) -> int:
    lo, hi = 0, len(dates) - 1
    if d <= dates[0]:
        return 0
    if d >= dates[-1]:
        return hi
    while lo < hi:                       # first index with dates[i] >= d
        mid = (lo + hi) // 2
        if dates[mid] < d:
            lo = mid + 1
        else:
            hi = mid
    return lo


def rebase(ticker: str, start: int):
    s = TK[ticker]["series"]
    base = next((v for v in s[start:] if v is not None), None)
    if base is None:
        return None
    return [None if (i < start or v is None) else round(100 * v / base, 2) for i, v in enumerate(s)]


# ----------------------------- sidebar -----------------------------
st.sidebar.title("📈 Trend Tracker")
st.sidebar.caption(f"Bundled prices as of **{P.get('generated','?')}** · Yahoo Finance adj-close")

subs = sorted({TK[t]["sub"] for t in all_tickers})
pick_sub = st.sidebar.multiselect("Quick-add a whole subsector", subs, default=[])

if "sel" not in st.session_state:
    st.session_state.sel = list(P["defaults"])

c1, c2, c3 = st.sidebar.columns(3)
if c1.button("Core"):
    st.session_state.sel = list(P["defaults"])
if c2.button("All"):
    st.session_state.sel = list(all_tickers)
if c3.button("None"):
    st.session_state.sel = []
for t in all_tickers:                    # apply subsector quick-add
    if TK[t]["sub"] in pick_sub and t not in st.session_state.sel:
        st.session_state.sel.append(t)

selected = st.sidebar.multiselect(
    "Tickers (ticker · subsector)", options=all_tickers,
    default=st.session_state.sel, format_func=lambda t: label_of[t], key="sel")

st.sidebar.divider()
if st.sidebar.button("🔄 Refresh selected from Yahoo (live)"):
    prog = st.sidebar.progress(0.0, "Fetching…")
    new = dict(st.session_state.prices["tickers"])
    todo = selected or all_tickers
    union = set(dates)
    fetched = {}
    for i, t in enumerate(todo):
        d = fetch_yahoo(t)
        if d:
            fetched[t] = d; union |= set(d)
        prog.progress((i + 1) / len(todo), f"Fetching {t}…")
    if fetched:
        newdates = sorted(union)
        for t in TK:                     # rebuild aligned series on the new union axis
            src = fetched.get(t)
            if src:
                new[t] = {"sub": TK[t]["sub"], "series": [src.get(d) for d in newdates]}
            else:
                old = dict(zip(dates, TK[t]["series"]))
                new[t] = {"sub": TK[t]["sub"], "series": [old.get(d) for d in newdates]}
        st.session_state.prices = {**st.session_state.prices, "dates": newdates,
                                   "tickers": new, "generated": dt.date.today().isoformat()}
        prog.empty(); st.rerun()
    else:
        prog.empty(); st.sidebar.error("Live fetch failed (network blocked?). Using bundled data.")

st.sidebar.caption("Tip: use **Custom** window for a day-level start slider.")


# ----------------------------- header + window controls -----------------------------
st.title("Thematic ETF & Subsector Trend Tracker")
st.caption("Rebase every line to 100 at any start date to isolate short-term relative trends. "
           "Click a ◆ diamond to read the catalyst. Coverage 2024 → June 2026. "
           "Figures approximate — not investment advice.")

last = dates[-1]
WINDOWS = {"1M": 21, "3M": 63, "6M": 126, "1Y": 252, "2Y": 504, "3Y": 756, "Max": 0}
cwin = st.radio("Window", list(WINDOWS) + ["YTD", "Custom"], index=3, horizontal=True)

d0 = dt.date.fromisoformat(dates[0]); dN = dt.date.fromisoformat(dates[-1])
if cwin == "Custom":
    sd = st.slider("Start date (drag by day)", min_value=d0, max_value=dN,
                   value=max(d0, dN - dt.timedelta(days=365)), format="YYYY-MM-DD")
    start = nearest_idx(sd.isoformat())
elif cwin == "YTD":
    start = nearest_idx(f"{last[:4]}-01-01")
else:
    start = max(0, len(dates) - 1 - WINDOWS[cwin])
logscale = st.checkbox("Log scale", value=False)
st.caption(f"**Start:** {dates[start]}  →  {dates[-1]}  ·  {len(selected)} ticker(s) selected")


# ----------------------------- build figure -----------------------------
def build_figure():
    fig = go.Figure()
    for t in selected:
        y = rebase(t, start)
        if not y:
            continue
        isb = (t == "SPY")
        fig.add_trace(go.Scattergl(
            x=dates, y=y, mode="lines", name=label_of[t],
            line=dict(width=2.6 if isb else 1.7, color=color_of[t],
                      dash="dash" if isb else "solid"),
            hovertemplate=f"<b>{t}</b> %{{y:.0f}} · %{{x}}<extra></extra>"))
    shown = []
    ex, ey, etext = [], [], []
    for e in events:
        if e["etf"] not in selected:
            continue
        di = nearest_idx(e["date"])
        if di < start:
            continue
        y = rebase(e["etf"], start)
        if not y or y[di] is None:
            continue
        ex.append(dates[di]); ey.append(y[di]); etext.append(e["headline"]); shown.append(e)
    fig.add_trace(go.Scattergl(
        x=ex, y=ey, mode="markers", name="Key news",
        marker=dict(symbol="diamond", size=11, color="#fff", line=dict(color="#111", width=1.5)),
        text=etext, hovertemplate="◆ %{text}<extra>click for detail</extra>"))
    fig.update_layout(
        template="plotly_dark", height=560, margin=dict(l=50, r=20, t=10, b=30),
        legend=dict(font=dict(size=10)), hovermode="closest",
        yaxis=dict(title="Rebased to 100", type="log" if logscale else "linear"),
        xaxis=dict(range=[dates[start], dates[-1]]))
    return fig, shown


tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Relative performance", "📊 Watchlists & fundamentals", "🗓️ Event timeline", "ℹ️ About"])

with tab1:
    if not selected:
        st.info("Pick one or more tickers in the sidebar.")
    else:
        fig, shown = build_figure()
        ev_curve = len(fig.data) - 1
        state = st.plotly_chart(fig, use_container_width=True, on_select="rerun",
                                selection_mode="points", key="chart")
        pts = (state.get("selection", {}) or {}).get("points", []) if state else []
        clicked = [p for p in pts if p.get("curve_number") == ev_curve]
        if clicked and shown:
            pn = clicked[0].get("point_number", clicked[0].get("point_index", 0))
            if pn < len(shown):
                e = shown[pn]
                st.success(f"**{e['date']} · {e['etf']} ({TK[e['etf']]['sub']})** — "
                           f"{e['headline']}\n\n{e['detail']}")
        with st.expander(f"Catalysts in view ({len(shown)})", expanded=not clicked):
            if shown:
                view_df = pd.DataFrame([
                    {"Date": e["date"], "ETF": e["etf"], "Subsector": TK[e["etf"]]["sub"],
                     "Headline": e["headline"], "Detail": e["detail"]} for e in shown])
                st.dataframe(view_df, hide_index=True, use_container_width=True)
            else:
                st.caption("No catalysts for the selected tickers after this start date.")

with tab2:
    st.caption("EPS g = latest YoY EPS growth · Fwd EPS g = consensus forward growth · "
               "P/E trailing · Fwd P/E forward · GM/OM/NM = gross/operating/net margin · "
               "Backlog = latest disclosed. `*` approx · `N/A (neg)` negative earnings · "
               "`n/r` not reported · `†` distorted by one-time items. As of ~2026-06-26.")
    for pool in funds["pools"]:
        st.subheader(f"{pool['title']}  ·  `{pool['etf']}`")
        st.dataframe(pd.DataFrame(pool["rows"]), hide_index=True, use_container_width=True)

with tab3:
    st.subheader("Curated catalyst timeline")
    df = pd.DataFrame([{"Date": e["date"], "ETF": e["etf"], "Subsector": TK[e["etf"]]["sub"],
                        "Headline": e["headline"], "Detail": e["detail"]} for e in events])
    st.dataframe(df.sort_values("Date"), hide_index=True, use_container_width=True, height=560)

with tab4:
    st.markdown(f"""
**What this is.** A research tracker tying news & government contracts to relative stock-market gains
across the cycle's hottest subsectors (semis, memory, photonics, drones, space, quantum, nuclear,
defense, rare earths, and {len(all_tickers)-1} ETFs total).

**Data.** Prices: Yahoo Finance daily adjusted-close (bundled snapshot {P.get('generated','?')};
use **Refresh from Yahoo** for live). Fundamentals: stockanalysis.com + company IR/SEC filings,
~June 2026 — **approximate**, verify before use. Curated catalysts are mapped to a representative ETF.

**Companion docs:** `STOCK_THEME_TRENDS_TRACKER.md` and `WATCHLISTS_AND_FUNDAMENTALS.md` in the repo.

*Not investment advice.*
""")
