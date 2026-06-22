# Plan — rebalancing-rules (Phase 7)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1), `metrics.py` (Phase 3), `entry_timing.py` (Phase 5)

## 1. `rebalancing.py` (new module, project root) — pure logic, no Streamlit import
- `rebalance_dates(index: pd.DatetimeIndex, frequency: str) -> pd.DatetimeIndex`: `frequency` is `"quarterly"` or `"annual"`, mapped to pandas period `"Q"`/`"Y"`; returns the first trading day of each period present in `index` (same groupby-first pattern as `entry_timing.monthly_investment_dates`).
- `rebalanced_value_series(prices: pd.DataFrame, weights: pd.Series, frequency: str, total_investment: float = 10_000.0) -> pd.Series`: starts with share counts split by weight at the first row (like `entry_timing.lump_sum_value_series`); at each date from `rebalance_dates(...)` after the first row, recomputes the portfolio's current total value and resets share counts to the target weights at that date's prices; values the (possibly-reset) share counts at every day in `prices.index`.

## 2. `pages/6_Rebalancing.py` (rewrite the Phase 7 placeholder)
- Same "build a portfolio first" guard as Phases 3-6.
- Fetch the trailing 5-year price history via `data.fetch_price_history` (same window as Phase 3/4).
- Build three series: `buy_and_hold = entry_timing.lump_sum_value_series(prices, weights, 10_000)`, `quarterly = rebalancing.rebalanced_value_series(prices, weights, "quarterly", 10_000)`, `annual = rebalancing.rebalanced_value_series(prices, weights, "annual", 10_000)`.
- For each series, compute risk/return metrics by reusing Phase 3's `metrics` module on `series.pct_change().dropna()` (annualized return/volatility/Sharpe) and `metrics.max_drawdown(series)` directly.
- Display a small comparison table (`st.dataframe`) with one row per strategy: ending value, total return, annualized volatility, Sharpe ratio, max drawdown.
- `plotly` line chart overlaying all three value-over-time series.
- Assumptions expander: rebalance dates are the first trading day of each quarter/year, no fees/taxes/slippage, single-ticker portfolios will show identical lines for all three strategies (rebalancing is a no-op).

## 3. `tests/test_rebalancing.py`
- `rebalance_dates` returns the expected dates for `"quarterly"` and `"annual"` on a synthetic multi-year business-day date range.
- `rebalanced_value_series` matches a hand-computed series for a small 2-asset synthetic price DataFrame with one rebalance event partway through (verifies share counts reset to target weights at the rebalance date's prices).
- Single-ticker portfolio: `rebalanced_value_series` is identical to `entry_timing.lump_sum_value_series` for both frequencies (rebalancing no-op).
- A synthetic two-asset series with diverging per-asset returns and at least one rebalance produces a **different** ending value than the buy-and-hold series (confirms rebalancing actually changes the outcome when assets diverge).

## 4. Verification
- `python -m pytest tests/test_rebalancing.py -v`
- Manual (logic script against real data, same pattern as prior phases): run buy-and-hold/quarterly/annual for a multi-ticker portfolio (e.g. AAPL/MSFT/SPY) over the trailing 5 years, confirm ending values and risk metrics are plausible and differ across strategies; confirm a single-ticker portfolio collapses all three series to identical values.
- Manual: run the app, open Rebalancing with and without a portfolio built, confirm the comparison table and chart render correctly.
