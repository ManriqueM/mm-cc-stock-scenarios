# Plan — entry-timing-comparison (Phase 5)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1), `portfolio.py` (Phase 2)

## 1. `entry_timing.py` (new module, project root) — pure logic, no Streamlit import
- `HORIZONS_YEARS = (1, 3, 5, 10)`: the fixed set of comparison horizons.
- `horizon_has_sufficient_history(prices: pd.DataFrame, start: pd.Timestamp) -> bool`: `True` only if every ticker column's `first_valid_index()` is on or before `start` — i.e. every asset in the portfolio actually has data back to the horizon's start date.
- `lump_sum_value_series(prices: pd.DataFrame, weights: pd.Series, total_investment: float = 10_000.0) -> pd.Series`: splits `total_investment` across tickers by weight using the **first row's prices** to compute share counts, then values those fixed share counts at every subsequent day's prices.
- `monthly_investment_dates(index: pd.DatetimeIndex) -> pd.DatetimeIndex`: the first trading day of each calendar month present in `index` (one date per month, real trading days only).
- `dca_value_series(prices: pd.DataFrame, weights: pd.Series, total_investment: float = 10_000.0) -> pd.Series`: splits `total_investment` into `len(monthly_investment_dates(prices.index))` equal installments; on each installment date, allocates that installment across tickers by weight at that day's prices (accumulating share counts); returns the day-by-day value of all shares purchased so far (zero before the first installment).

## 2. `pages/4_Entry_Timing.py` (rewrite the Phase 5 placeholder)
- Same "build a portfolio first" guard as Phases 3-4.
- Fetch the longest horizon (10 years) of price history once via `data.fetch_price_history`.
- For each horizon in `entry_timing.HORIZONS_YEARS` (rendered as `st.tabs`):
  - Compute `start = pd.Timestamp(today) - pd.DateOffset(years=horizon)`; if `not horizon_has_sufficient_history(prices, start)`, show `st.warning` naming the horizon and stop that tab early.
  - Otherwise slice `prices.loc[start:]`, compute `lump_sum_value_series` and `dca_value_series`.
  - `st.columns` showing ending value + total return (%) for both strategies side by side (`st.metric`).
  - A `plotly` line chart with both value-over-time series overlaid.
- Assumptions expander: monthly DCA installments on the first trading day of each month, identical $10,000 total notional for both strategies, no fees/taxes/slippage, horizons skipped when any portfolio ticker lacks sufficient history.

## 3. `tests/test_entry_timing.py`
- `lump_sum_value_series` matches a hand-computed value series for a small 2-asset synthetic price DataFrame and known weights.
- `monthly_investment_dates` returns exactly one date per calendar month (the first trading day of that month) for a synthetic multi-month date range that includes weekends/non-trading gaps.
- `dca_value_series`:
  - Total amount invested across installments sums to `total_investment`.
  - Matches a hand-computed value series for a small synthetic series with 2-3 monthly installments.
  - Value is `0` for any day before the first installment.
- `horizon_has_sufficient_history` correctly returns `False` when one ticker's column starts later than the requested horizon start, and `True` when all columns cover it.
- Single-ticker portfolio works correctly for both strategies (degenerate weights case).

## 4. Verification
- `python -m pytest tests/test_entry_timing.py -v`
- Manual (logic script against real data, same pattern as Phases 3-4): run both strategies for a 100% SPY portfolio and a multi-ticker portfolio across all four horizons, confirm ending values are plausible and that a horizon is correctly skipped for a portfolio containing a ticker younger than that horizon.
- Manual: run the app, open Entry-Timing Comparison with and without a portfolio built, confirm each horizon tab renders correctly (or shows the insufficient-history warning).
