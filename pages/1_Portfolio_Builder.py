import pandas as pd
import plotly.express as px
import streamlit as st

import disclosures
from portfolio import build_portfolio, parse_portfolio_csv

st.set_page_config(page_title="Portfolio Builder", page_icon="🧮")

st.title("🧮 Portfolio Builder")

st.markdown(
    "Build a multi-asset portfolio by entering tickers and weights "
    "(manually or via CSV upload). Weights must sum to 100%."
)

if "portfolio" in st.session_state:
    st.subheader("Current portfolio")
    current = st.session_state["portfolio"]
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(current, hide_index=True, width="stretch")
    with col2:
        fig = px.pie(current, names="ticker", values="weight", title="Allocation")
        st.plotly_chart(fig, width="stretch")
    st.divider()

manual_tab, upload_tab = st.tabs(["Manual entry", "Upload CSV"])

with manual_tab:
    starter_rows = pd.DataFrame({"ticker": ["", "", ""], "weight": [0.0, 0.0, 0.0]})
    edited = st.data_editor(
        starter_rows,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "ticker": st.column_config.TextColumn("Ticker"),
            "weight": st.column_config.NumberColumn("Weight %", min_value=0.0, step=1.0),
        },
        key="manual_entry_editor",
    )
    manual_submit = st.button("Build Portfolio", key="manual_submit")

    if manual_submit:
        rows = edited.dropna(subset=["ticker"])
        rows = rows[rows["ticker"].str.strip() != ""]
        portfolio, errors = build_portfolio(
            rows["ticker"].tolist(), rows["weight"].tolist()
        )
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.session_state["portfolio"] = portfolio
            st.success("Portfolio built successfully.")
            st.rerun()

with upload_tab:
    st.markdown("Upload a CSV with `ticker` and `weight` columns.")
    uploaded_file = st.file_uploader("CSV file", type=["csv"], key="csv_uploader")
    csv_submit = st.button("Build Portfolio", key="csv_submit")

    if csv_submit:
        if uploaded_file is None:
            st.error("Please upload a CSV file first.")
        else:
            try:
                rows = parse_portfolio_csv(uploaded_file)
            except ValueError as e:
                st.error(str(e))
            else:
                portfolio, errors = build_portfolio(
                    rows["ticker"].tolist(), rows["weight"].tolist()
                )
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    st.session_state["portfolio"] = portfolio
                    st.success("Portfolio built successfully.")
                    st.rerun()

disclosures.render_footer()
