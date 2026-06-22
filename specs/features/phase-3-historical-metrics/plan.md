# Plan — historical-metrics (Phase 3)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1), `portfolio.py` (Phase 2)

## 1. `metrics.py` (new module, project root) — pure logic, no Streamlit import
- `daily_returns(prices: pd.DataFrame) -> pd.DataFrame`: simple daily pct-change returns per ticker, drops the first all-NaN row.
- `annualized_return(returns: pd.Series, periods_per_year: int = 252) -> float`: `returns.mean() * periods_per_year`.
- `annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float`: `returns.std() * sqrt(periods_per_year)`.
- `sharpe_ratio(returns: pd.Series, periods_per_year: int = 252, risk_free_rate: float = 0.0) -> float`: `(annualized_return(returns) - risk_free_rate) / annualized_volatility(returns)`; returns `nan` if volatility is 0.
- `max_drawdown(prices: pd.Series) -> float`: cumulative running-max vs. value, `min((value - running_max) / running_max)`; negative percentage.
- `weighted_portfolio_returns(returns: pd.DataFrame, weights: pd.Series) -> pd.Series`: daily portfolio return series = `returns @ (weights / 100)`, row-wise, aligned on common dates only.
- `correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame`: `returns.corr()`.
- `compute_metrics_table(prices: pd.DataFrame) -> pd.DataFrame`: per-ticker DataFrame with columns `ticker`, `annualized_return`, `annualized_volatility`, `sharpe_ratio`, `max_drawdown`, `history_days` (so the page can flag short-history tickers).
- `compute_portfolio_metrics(prices: pd.DataFrame, weights: pd.Series) -> dict`: single dict with the four portfolio-level headline metrics, computed from `weighted_portfolio_returns` and the portfolio cumulative value series.

## 2. `pages/2_Historical_Metrics.py` (rewrite the Phase 3 placeholder)
- If `st.session_state["portfolio"]` is missing: `st.info` prompting the user to build a portfolio first (link/mention of the Portfolio Builder page), stop here.
- Otherwise:
  - Fetch 5-year price history via `data.fetch_price_history` for the portfolio's tickers (`start = today - 5*365 days`, `end = today`).
  - Compute portfolio-level metrics via `metrics.compute_portfolio_metrics` → display as `st.metric` cards (return, volatility, Sharpe, max drawdown), each formatted as a percentage where applicable.
  - Compute per-asset table via `metrics.compute_metrics_table` → display as `st.dataframe`; flag any ticker with less than 5 years of history (e.g. a caption noting the shorter window used).
  - Compute correlation matrix via `metrics.correlation_matrix` → display as a `plotly` heatmap (`px.imshow`).
  - State the annualization convention (252 trading days, 0% risk-free rate, 5-year fixed lookback) explicitly in a caption/expander on the page — consistent with the mission's "surface assumptions" principle, ahead of the dedicated Phase 8 treatment.

## 3. `tests/test_metrics.py`
- Unit tests for `daily_returns`, `annualized_return`, `annualized_volatility`, `sharpe_ratio`, `max_drawdown`, `weighted_portfolio_returns`, `correlation_matrix` using small hand-constructed price series with known expected values (no network calls).
- One test for `compute_metrics_table` / `compute_portfolio_metrics` end-to-end on a small synthetic multi-asset price DataFrame.
- Edge cases: single-ticker portfolio (correlation matrix is 1x1 = `1.0`), zero-volatility series (Sharpe ratio is `nan`, not an exception).

## 4. Verification
- `python -m pytest tests/test_metrics.py -v`
- Manual: build a portfolio in Portfolio Builder, open Historical Metrics, confirm headline metrics, per-asset table, and correlation heatmap render with sane values (e.g. a 100% SPY portfolio should show a 1x1 correlation matrix of `1.0`).
