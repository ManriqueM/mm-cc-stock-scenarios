from datetime import date, timedelta

import plotly.express as px
import streamlit as st

from data import fetch_price_history
from metrics import compute_metrics_table, compute_portfolio_metrics, correlation_matrix, daily_returns

LOOKBACK_DAYS = 5 * 365

st.set_page_config(page_title="Historical Metrics", page_icon="📊")

st.title("📊 Historical Metrics")

st.markdown(
    "Explore historical return and risk metrics for your portfolio: "
    "returns, volatility, Sharpe ratio, max drawdown, and correlation matrix."
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

portfolio_metrics = compute_portfolio_metrics(prices, weights)

st.subheader("Portfolio metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Annualized return", f"{portfolio_metrics['annualized_return']:.2%}")
col2.metric("Annualized volatility", f"{portfolio_metrics['annualized_volatility']:.2%}")
col3.metric("Sharpe ratio", f"{portfolio_metrics['sharpe_ratio']:.2f}")
col4.metric("Max drawdown", f"{portfolio_metrics['max_drawdown']:.2%}")

st.divider()

st.subheader("Per-asset breakdown")
metrics_table = compute_metrics_table(prices)
display_table = metrics_table.copy()
display_table["annualized_return"] = display_table["annualized_return"].map("{:.2%}".format)
display_table["annualized_volatility"] = display_table["annualized_volatility"].map("{:.2%}".format)
display_table["sharpe_ratio"] = display_table["sharpe_ratio"].map("{:.2f}".format)
display_table["max_drawdown"] = display_table["max_drawdown"].map("{:.2%}".format)
st.dataframe(display_table, hide_index=True, width="stretch")

short_history = metrics_table[metrics_table["history_days"] < LOOKBACK_DAYS * 0.9]
if not short_history.empty:
    st.caption(
        "Note: " + ", ".join(short_history["ticker"]) + " have less than 5 years of "
        "price history; metrics for these tickers use whatever history is available."
    )

st.divider()

st.subheader("Correlation matrix")
returns = daily_returns(prices)
corr = correlation_matrix(returns)
fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
    aspect="auto",
)
st.plotly_chart(fig, width="stretch")

with st.expander("Assumptions"):
    st.markdown(
        "- Metrics use a **fixed trailing 5-year window** of daily prices.\n"
        "- Returns and volatility are **annualized using 252 trading days/year**.\n"
        "- The Sharpe ratio assumes a **0% risk-free rate**.\n"
        "- Portfolio-level metrics are computed from the **weighted daily return series** "
        "(not a weighted average of per-asset metrics), so they account for diversification."
    )
