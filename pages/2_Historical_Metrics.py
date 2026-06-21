import streamlit as st

st.set_page_config(page_title="Historical Metrics", page_icon="📊")

st.title("📊 Historical Metrics")

st.markdown(
    "Explore historical return and risk metrics for your portfolio: "
    "returns, volatility, Sharpe ratio, max drawdown, and correlation matrix."
)

st.info("Coming in Phase 3 — Historical metrics.", icon="🚧")
