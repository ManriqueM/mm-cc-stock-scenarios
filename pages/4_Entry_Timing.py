from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data import fetch_price_history
from entry_timing import (
    HORIZONS_YEARS,
    dca_value_series,
    horizon_has_sufficient_history,
    lump_sum_value_series,
)

TOTAL_INVESTMENT = 10_000.0
MAX_HORIZON_YEARS = max(HORIZONS_YEARS)

st.set_page_config(page_title="Entry Timing", page_icon="⏱️")

st.title("⏱️ Entry-Timing Comparison")

st.markdown(
    "Compare lump-sum vs. dollar-cost-averaging entry strategies starting "
    "from different historical dates."
)

if "portfolio" not in st.session_state:
    st.info("Build a portfolio first on the **Portfolio Builder** page.", icon="🧮")
    st.stop()

portfolio = st.session_state["portfolio"]
tickers = portfolio["ticker"].tolist()
weights = portfolio.set_index("ticker")["weight"]

end = date.today()
start = pd.Timestamp(end) - pd.DateOffset(years=MAX_HORIZON_YEARS)
prices, invalid_tickers = fetch_price_history(tickers, start.date(), end)

if invalid_tickers:
    st.error(f"Could not fetch data for: {', '.join(invalid_tickers)}.")
    st.stop()

tabs = st.tabs([f"{horizon} year{'s' if horizon != 1 else ''}" for horizon in HORIZONS_YEARS])

for horizon, tab in zip(HORIZONS_YEARS, tabs):
    with tab:
        horizon_start = pd.Timestamp(end) - pd.DateOffset(years=horizon)

        if not horizon_has_sufficient_history(prices, horizon_start):
            st.warning(
                f"Skipping the {horizon}-year horizon: at least one ticker in the "
                "portfolio doesn't have price history reaching back that far.",
                icon="⚠️",
            )
            continue

        window = prices.loc[horizon_start:]
        lump_sum = lump_sum_value_series(window, weights, TOTAL_INVESTMENT)
        dca = dca_value_series(window, weights, TOTAL_INVESTMENT)

        col1, col2 = st.columns(2)
        col1.metric(
            "Lump-sum ending value",
            f"${lump_sum.iloc[-1]:,.0f}",
            f"{(lump_sum.iloc[-1] / TOTAL_INVESTMENT - 1):.1%}",
        )
        col2.metric(
            "DCA ending value",
            f"${dca.iloc[-1]:,.0f}",
            f"{(dca.iloc[-1] / TOTAL_INVESTMENT - 1):.1%}",
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=lump_sum.index, y=lump_sum, name="Lump-sum"))
        fig.add_trace(go.Scatter(x=dca.index, y=dca, name="DCA"))
        fig.update_layout(xaxis_title="Date", yaxis_title="Portfolio value ($)", showlegend=True)
        st.plotly_chart(fig, width="stretch")

with st.expander("Assumptions"):
    st.markdown(
        f"- Both strategies invest the same **total notional ${TOTAL_INVESTMENT:,.0f}** "
        "for a fair comparison.\n"
        "- **DCA** splits the total into equal installments invested on the **first trading "
        "day of each month** from the horizon's start date to today.\n"
        "- A horizon is **skipped** if any portfolio ticker lacks price history reaching "
        "back to that horizon's start date.\n"
        "- No fees, taxes, or slippage are modeled — this is a pure price-return comparison."
    )
