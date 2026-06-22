import streamlit as st

import disclosures

st.set_page_config(page_title="Assumptions & Limitations", page_icon="📋")

st.title("📋 Assumptions & Limitations")

st.markdown(disclosures.NOT_FINANCIAL_ADVICE)

st.markdown(
    "This page consolidates the data limitations and simulation assumptions "
    "that apply across the whole app. Every page also has its own "
    "**Assumptions** section covering the mechanics specific to that page — "
    "summarized below with links back to each one."
)

st.subheader("Data limitations")
st.markdown(disclosures.DATA_LIMITATIONS)

st.subheader("Simulation assumptions")
st.markdown(disclosures.SIMULATION_ASSUMPTIONS)

st.subheader("Page-specific assumptions")

page_assumptions = [
    (
        "pages/2_Historical_Metrics.py",
        "📊 Historical Metrics",
        "Trailing 5-year window, returns/volatility annualized over 252 trading days, "
        "0% risk-free rate for the Sharpe ratio.",
    ),
    (
        "pages/3_Monte_Carlo.py",
        "🎲 Monte Carlo",
        "Bootstrap-resampled from trailing 5-year daily returns; 10-year horizon, "
        "1,000 paths, notional lump sum with no contributions or rebalancing.",
    ),
    (
        "pages/4_Entry_Timing.py",
        "⏱️ Entry Timing",
        "Lump-sum vs. DCA invest the same total notional; DCA splits it into equal "
        "monthly installments; no fees, taxes, or slippage.",
    ),
    (
        "pages/5_Stress_Tests.py",
        "💥 Stress Tests",
        "Replays the portfolio's own historical prices over each named crash window; "
        "a notional amount is invested at the scenario's peak date.",
    ),
    (
        "pages/6_Rebalancing.py",
        "⚖️ Rebalancing",
        "Rebalance dates are the first trading day of each quarter/year; no fees, "
        "taxes, or slippage; single-ticker portfolios show identical results across strategies.",
    ),
]

for path, label, summary in page_assumptions:
    st.page_link(path, label=label)
    st.caption(summary)
