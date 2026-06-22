# Roadmap

- [x] **Phase 0 — Project scaffold**: Streamlit app skeleton (`app.py`), `requirements.txt`, multi-page structure, confirm app runs locally
- [x] **Phase 1 — Data layer**: `yfinance` wrapper for fetching/validating historical price data for S&P 500/NYSE tickers, cached with `st.cache_data`
- [x] **Phase 2 — Portfolio builder**: UI for entering tickers + weights (manual or CSV upload), weight validation, portfolio summary view
- [x] **Phase 3 — Historical metrics**: compute & display returns, volatility, Sharpe ratio, max drawdown, correlation matrix
- [x] **Phase 4 — Monte Carlo projections**: forward-looking simulation engine + percentile-band chart of projected portfolio value
- [ ] **Phase 5 — Entry-timing comparison**: lump-sum vs. DCA, compare outcomes starting from different historical dates
- [ ] **Phase 6 — Drawdown stress tests**: apply historical crash scenarios (2008, 2020, dot-com) to the current portfolio, show impact
- [ ] **Phase 7 — Rebalancing rules**: simulate periodic rebalancing vs. buy-and-hold, compare risk/return impact
- [ ] **Phase 8 — Assumptions & limitations**: dedicated, always-visible disclosure of data limitations, simulation assumptions, and "not financial advice" framing throughout the app
- [ ] **Phase 9 — Deploy**: deploy to Streamlit Community Cloud, smoke-test the public URL
