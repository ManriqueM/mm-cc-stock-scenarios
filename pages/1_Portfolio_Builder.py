import streamlit as st

st.set_page_config(page_title="Portfolio Builder", page_icon="🧮")

st.title("🧮 Portfolio Builder")

st.markdown(
    "Build a multi-asset portfolio by entering tickers and weights "
    "(manually or via CSV upload), with validation that weights sum to 100%."
)

st.info("Coming in Phase 2 — Portfolio builder.", icon="🚧")
