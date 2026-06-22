# Validation — historical-metrics (Phase 3)

1. `python -m pytest tests/test_metrics.py -v` passes:
   - `daily_returns` matches hand-computed pct-change values on a small synthetic price series.
   - `annualized_return` / `annualized_volatility` match hand-computed values (mean/std scaled by 252 / sqrt(252)).
   - `sharpe_ratio` matches `annualized_return / annualized_volatility` on a known series, and returns `nan` (not an exception) when volatility is 0.
   - `max_drawdown` correctly identifies the trough-vs-peak drawdown on a series with a known dip.
   - `weighted_portfolio_returns` matches a hand-computed weighted combination of two synthetic return series.
   - `correlation_matrix` returns `1.0` on the diagonal and the expected off-diagonal value for two known-correlated series; returns a 1x1 matrix of `1.0` for a single ticker.
   - `compute_metrics_table` / `compute_portfolio_metrics` run end-to-end on a small synthetic multi-asset price DataFrame without error and return the expected columns/keys.
2. Manual check — run `streamlit run app.py`:
   - Build a 100% SPY portfolio in Portfolio Builder, open Historical Metrics → headline metrics show sane values, per-asset table shows one row for SPY, correlation matrix is a 1x1 heatmap of `1.0`.
   - Build a 3-ticker portfolio (e.g. AAPL 40 / MSFT 30 / SPY 30) → headline portfolio metrics differ from any single per-asset row (confirms weighting logic), correlation heatmap shows a 3x3 matrix with plausible values (mostly positive, diagonal `1.0`).
   - With no portfolio built yet, visiting Historical Metrics shows the "build a portfolio first" prompt instead of an error/crash.
   - The assumptions caption/expander (252 trading days, 0% risk-free rate, 5-year fixed lookback) is visible on the page.
