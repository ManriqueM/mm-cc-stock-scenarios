# Requirements — historical-metrics (Phase 3)

## Scope
- Add a working Historical Metrics page (`pages/2_Historical_Metrics.py`), replacing the Phase 3 placeholder.
- Reads the portfolio from `st.session_state["portfolio"]` (built in Phase 2). If no portfolio exists, show a friendly prompt to build one first instead of erroring.
- Computes, over a fixed trailing 5-year window of daily prices:
  - Annualized return (per-asset and weighted portfolio)
  - Annualized volatility (per-asset and weighted portfolio)
  - Sharpe ratio (per-asset and weighted portfolio)
  - Max drawdown (per-asset and weighted portfolio)
  - Correlation matrix between asset daily returns
- Displays:
  - Headline portfolio-level metrics (return, volatility, Sharpe, max drawdown)
  - A per-asset breakdown table with the same four metrics per ticker
  - A correlation matrix (heatmap via `plotly`)

## Key decisions
- **Lookback window**: fixed trailing 5 years of daily data (`end=today`, `start=today - 5 years`), not user-selectable for now. If a ticker has less than 5 years of price history, use whatever history is available (no error) — flag this per-asset in the breakdown table rather than failing the whole page.
- **Risk-free rate**: fixed at 0% for the Sharpe ratio (`Sharpe = annualized_return / annualized_volatility`). Revisit if/when Phase 8 (assumptions & limitations) wants to surface this as an adjustable, explicitly-stated assumption.
- **Annualization**: daily returns annualized using 252 trading days/year (`mean * 252` for return, `std * sqrt(252)` for volatility) — the standard convention, stated explicitly in the UI as an assumption.
- **Portfolio-level (weighted) metrics**: computed from the *weighted portfolio return series* (daily returns combined using portfolio weights), not by weighting the individual per-asset metrics — this is the financially correct way to account for diversification/correlation effects (a weighted average of per-asset Sharpe ratios is not the portfolio Sharpe ratio).
- **Max drawdown**: computed on the cumulative value series (running peak vs. trough), expressed as a negative percentage.
- **Correlation matrix**: Pearson correlation of each asset's daily returns over the same 5-year window. Degenerate case (single-ticker portfolio): show a 1x1 matrix (trivially 1.0) rather than hiding the section.
- **Pure logic separated from UI**: all metric computations live in a new `metrics.py` module (no Streamlit import), unit-testable in isolation; the page module only handles widgets/display, mirroring the `portfolio.py` / `1_Portfolio_Builder.py` split from Phase 2.
- **Data fetching**: reuse `data.fetch_price_history` (Phase 1) for the 5-year price window — already cached via `st.cache_data`.

## Out of scope
- User-selectable lookback windows or risk-free rate (fixed for this phase, per explicit decision — may revisit later).
- Forward-looking projections (Monte Carlo — Phase 4).
- Rolling/time-varying metrics (e.g. rolling Sharpe) — only a single full-window value per metric.
- Benchmark comparison (e.g. vs. S&P 500) — not part of this phase's scope.
