from datetime import date, timedelta

import plotly.graph_objects as go
import streamlit as st

from data import fetch_price_history
from metrics import daily_returns, weighted_portfolio_returns
from simulation import compute_percentile_bands, simulate_portfolio_paths

LOOKBACK_DAYS = 5 * 365
TRADING_DAYS_PER_YEAR = 252
HORIZON_YEARS = 10
HORIZON_DAYS = HORIZON_YEARS * TRADING_DAYS_PER_YEAR
N_PATHS = 1000
STARTING_VALUE = 10_000.0

st.set_page_config(page_title="Monte Carlo", page_icon="🎲")

st.title("🎲 Monte Carlo Projections")

st.markdown(
    "Run forward-looking Monte Carlo simulations of your portfolio's value, "
    "shown as a range of percentile outcomes rather than a single forecast."
)

if "portfolio" not in st.session_state:
    st.info("Build a portfolio first on the **Portfolio Builder** page.", icon="🧮")
    st.stop()

portfolio = st.session_state["portfolio"]
tickers = portfolio["ticker"].tolist()
weights = portfolio.set_index("ticker")["weight"]

end = date.today()
start = end - timedelta(days=LOOKBACK_DAYS)
prices, invalid_tickers = fetch_price_history(tickers, start, end)

if invalid_tickers:
    st.error(f"Could not fetch data for: {', '.join(invalid_tickers)}.")
    st.stop()

returns = daily_returns(prices)
portfolio_returns = weighted_portfolio_returns(returns, weights).dropna()

paths = simulate_portfolio_paths(
    portfolio_returns.to_numpy(),
    horizon_days=HORIZON_DAYS,
    n_paths=N_PATHS,
    starting_value=STARTING_VALUE,
)
bands = compute_percentile_bands(paths)
years = [day / TRADING_DAYS_PER_YEAR for day in range(HORIZON_DAYS + 1)]

st.subheader(f"Projected value of a ${STARTING_VALUE:,.0f} portfolio over {HORIZON_YEARS} years")
col1, col2, col3 = st.columns(3)
col1.metric("10th percentile", f"${bands['p10'].iloc[-1]:,.0f}")
col2.metric("Median", f"${bands['p50'].iloc[-1]:,.0f}")
col3.metric("90th percentile", f"${bands['p90'].iloc[-1]:,.0f}")

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=years + years[::-1],
        y=list(bands["p90"]) + list(bands["p10"])[::-1],
        fill="toself",
        fillcolor="rgba(99, 110, 250, 0.2)",
        line=dict(color="rgba(255,255,255,0)"),
        name="10th-90th percentile",
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter(
        x=years,
        y=bands["p50"],
        line=dict(color="rgb(99, 110, 250)"),
        name="Median",
    )
)
fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Portfolio value ($)",
    showlegend=True,
)
st.plotly_chart(fig, width="stretch")

with st.expander("Assumptions"):
    st.markdown(
        f"- Simulated by **bootstrap resampling** (with replacement) from the portfolio's "
        f"**trailing 5-year daily returns** — no normal-distribution assumption.\n"
        f"- **{HORIZON_YEARS}-year horizon** ({HORIZON_DAYS} trading days), **{N_PATHS:,} simulated paths**.\n"
        f"- Starting value is a **notional ${STARTING_VALUE:,.0f}**, not a personalized forecast.\n"
        "- Assumes a lump-sum investment with **no contributions, withdrawals, or rebalancing** "
        "during the horizon.\n"
        "- Past performance does not guarantee future results."
    )
