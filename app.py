import streamlit as st

st.set_page_config(
    page_title="Stock Scenarios",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Stock Scenarios")

st.markdown(
    """
An interactive app for analyzing historical S&P 500 / NYSE stock data and
stress-testing real, multi-asset investment portfolios — to support actual
investment decisions, with all assumptions and limitations surfaced
explicitly.
"""
)

st.subheader("What you can do here")
st.markdown(
    """
- **Build a portfolio** — enter tickers and weights, or upload a CSV.
- **Explore historical metrics** — returns, volatility, Sharpe ratio, drawdown, correlation.
- **Run Monte Carlo projections** — simulate a range of forward-looking outcomes.
- **Compare entry timing** — lump sum vs. dollar-cost averaging at different historical dates.
- **Stress-test drawdowns** — see how your portfolio would have fared in past crashes (2008, 2020, dot-com).
- **Test rebalancing rules** — periodic rebalancing vs. buy-and-hold.

Use the sidebar to navigate between sections.
"""
)

st.warning(
    "**Not financial advice.** All figures are derived from historical data "
    "and simplifying assumptions — they describe what *could have* happened, "
    "not what *will* happen. See each page for its specific assumptions and "
    "limitations before making any investment decision.",
    icon="⚠️",
)
