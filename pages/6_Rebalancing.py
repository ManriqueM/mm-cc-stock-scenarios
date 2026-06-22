from datetime import date, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data import fetch_price_history
from entry_timing import lump_sum_value_series
from metrics import annualized_return, annualized_volatility, max_drawdown, sharpe_ratio
from rebalancing import rebalanced_value_series

LOOKBACK_DAYS = 5 * 365
TOTAL_INVESTMENT = 10_000.0

st.set_page_config(page_title="Rebalancing", page_icon="⚖️")

st.title("⚖️ Rebalancing Rules")

st.markdown(
    "Simulate periodic rebalancing (e.g., quarterly or annual) against "
    "buy-and-hold, and compare the risk/return impact."
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

strategies = {
    "Buy-and-hold": lump_sum_value_series(prices, weights, TOTAL_INVESTMENT),
    "Quarterly rebalance": rebalanced_value_series(prices, weights, "quarterly", TOTAL_INVESTMENT),
    "Annual rebalance": rebalanced_value_series(prices, weights, "annual", TOTAL_INVESTMENT),
}

rows = []
for name, series in strategies.items():
    returns = series.pct_change().dropna()
    rows.append(
        {
            "strategy": name,
            "ending_value": series.iloc[-1],
            "total_return": series.iloc[-1] / TOTAL_INVESTMENT - 1,
            "annualized_volatility": annualized_volatility(returns),
            "sharpe_ratio": sharpe_ratio(returns),
            "max_drawdown": max_drawdown(series),
        }
    )
comparison = pd.DataFrame(rows)

st.subheader("Strategy comparison")
display_table = comparison.copy()
display_table["ending_value"] = display_table["ending_value"].map("${:,.0f}".format)
display_table["total_return"] = display_table["total_return"].map("{:.1%}".format)
display_table["annualized_volatility"] = display_table["annualized_volatility"].map("{:.1%}".format)
display_table["sharpe_ratio"] = display_table["sharpe_ratio"].map("{:.2f}".format)
display_table["max_drawdown"] = display_table["max_drawdown"].map("{:.1%}".format)
st.dataframe(display_table, hide_index=True, width="stretch")

fig = go.Figure()
for name, series in strategies.items():
    fig.add_trace(go.Scatter(x=series.index, y=series, name=name))
fig.update_layout(xaxis_title="Date", yaxis_title="Portfolio value ($)", showlegend=True)
st.plotly_chart(fig, width="stretch")

with st.expander("Assumptions"):
    st.markdown(
        "- Rebalance dates are the **first trading day of each calendar quarter/year**.\n"
        f"- All strategies start with the same **${TOTAL_INVESTMENT:,.0f} notional**, over the "
        "**trailing 5-year window**.\n"
        "- No fees, taxes, or slippage are modeled on rebalancing trades.\n"
        "- For a **single-ticker portfolio**, rebalancing is a no-op — all three strategies "
        "will show identical results."
    )
