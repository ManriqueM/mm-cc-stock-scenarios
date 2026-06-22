from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import disclosures
from data import fetch_price_history
from entry_timing import horizon_has_sufficient_history
from metrics import max_drawdown
from stress_tests import SCENARIOS, scenario_value_series

TOTAL_INVESTMENT = 10_000.0

st.set_page_config(page_title="Stress Tests", page_icon="💥")

st.title("💥 Drawdown Stress Tests")

st.markdown(
    "See how your current portfolio composition would have fared during "
    "historical market crashes (2008, 2020, dot-com, and others)."
)

if "portfolio" not in st.session_state:
    st.info("Build a portfolio first on the **Portfolio Builder** page.", icon="🧮")
    disclosures.render_footer()
    st.stop()

portfolio = st.session_state["portfolio"]
tickers = portfolio["ticker"].tolist()
weights = portfolio.set_index("ticker")["weight"]

today = pd.Timestamp(date.today())
earliest_peak = min(scenario.peak for scenario in SCENARIOS)
prices, invalid_tickers = fetch_price_history(tickers, earliest_peak.date(), today.date())

if invalid_tickers:
    st.error(f"Could not fetch data for: {', '.join(invalid_tickers)}.")
    st.stop()

tabs = st.tabs([scenario.name for scenario in SCENARIOS])

for scenario, tab in zip(SCENARIOS, tabs):
    with tab:
        if not horizon_has_sufficient_history(prices, scenario.peak):
            st.warning(
                f"Skipping {scenario.name}: at least one ticker in the portfolio "
                "doesn't have price history reaching back that far.",
                icon="⚠️",
            )
            continue

        value_series = scenario_value_series(prices, weights, scenario, today, TOTAL_INVESTMENT)
        max_dd = max_drawdown(value_series)
        dollar_impact = TOTAL_INVESTMENT * max_dd

        st.caption(
            f"Peak: {scenario.peak.date()} — Trough: {scenario.trough.date()}"
        )
        col1, col2 = st.columns(2)
        col1.metric("Max drawdown", f"{max_dd:.1%}")
        col2.metric("Dollar impact", f"${dollar_impact:,.0f}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=value_series.index, y=value_series, name="Portfolio value"))
        fig.update_layout(xaxis_title="Date", yaxis_title="Portfolio value ($)", showlegend=False)
        st.plotly_chart(fig, width="stretch")

with st.expander("Assumptions"):
    st.markdown(
        f"- Each scenario replays the portfolio's **own historical ticker prices** "
        "(not a benchmark proxy) over the named peak-to-trough window.\n"
        f"- A **${TOTAL_INVESTMENT:,.0f} notional** is invested at the scenario's peak date, "
        "split by the portfolio's weights.\n"
        "- Charts extend **2 years past the trough** (capped at today) to show the start of recovery.\n"
        "- A scenario is **skipped** if any portfolio ticker lacks price history reaching "
        "back to that scenario's peak date."
    )

disclosures.render_footer()
