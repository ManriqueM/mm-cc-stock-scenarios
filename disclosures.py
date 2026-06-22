import streamlit as st

NOT_FINANCIAL_ADVICE = (
    "**Not financial advice.** All figures are derived from historical data "
    "and simplifying assumptions — they describe what *could have* happened, "
    "not what *will* happen."
)

DATA_LIMITATIONS = """
- Prices come from the free, unofficial Yahoo Finance API (`yfinance`) — there's no SLA, and fetches can fail, get rate-limited, or silently return incomplete data.
- Only **daily closing prices**, **adjusted for splits and dividends**, are used — there's no intraday data, and raw unadjusted prices aren't available.
- Price data is **cached for 24 hours**, so recent price moves or news may not be reflected immediately.
- Tickers are looked up by their **current symbol only** — delisted, renamed, or merged companies may show incomplete or no history, which can introduce survivorship bias in long lookbacks.
- A ticker with **partial history** (e.g., a recent IPO) is still included with whatever shorter window of data is available.
"""

SIMULATION_ASSUMPTIONS = """
- Notional dollar amounts (e.g., $10,000) used throughout the app are **illustrative**, not your actual account size — outcomes scale linearly with your real investment.
- **No fees, transaction costs, taxes, or slippage** are modeled anywhere in this app.
- Lookback windows and horizons are **fixed** per page, not user-tunable, in this version.
- All scenarios are based on **past prices** — historical performance does not predict or guarantee future results.
- The app does not account for your personal tax situation, time horizon, risk tolerance, or financial goals.
"""


def render_footer() -> None:
    st.divider()
    st.warning(NOT_FINANCIAL_ADVICE, icon="⚠️")
    st.page_link(
        "pages/7_Assumptions_and_Limitations.py",
        label="Full assumptions & data limitations",
        icon="📋",
    )
