# Plan — drawdown-stress-tests (Phase 6)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1), `metrics.py` (Phase 3), `entry_timing.py` (Phase 5)

## 1. `stress_tests.py` (new module, project root) — pure logic, no Streamlit import
- `Scenario` (`NamedTuple` or small `dataclass`): `name: str`, `peak: pd.Timestamp`, `trough: pd.Timestamp`, `recovery_years: int = 2`.
- `SCENARIOS: list[Scenario]`: the three fixed scenarios (dot-com, 2008 GFC, 2020 COVID) with their peak/trough dates per `requirements.md`.
- `scenario_window_end(scenario: Scenario, today: pd.Timestamp) -> pd.Timestamp`: `min(scenario.trough + pd.DateOffset(years=scenario.recovery_years), today)`.
- `scenario_value_series(prices: pd.DataFrame, weights: pd.Series, scenario: Scenario, today: pd.Timestamp, total_investment: float = 10_000.0) -> pd.Series`: slices `prices.loc[scenario.peak : scenario_window_end(scenario, today)]` and delegates to `entry_timing.lump_sum_value_series` — a stress scenario is structurally identical to a lump-sum investment over a fixed historical window, so no new value-series logic is written.
- Re-export/reuse `entry_timing.horizon_has_sufficient_history(prices, scenario.peak)` directly for the insufficient-history check (no wrapper needed beyond calling it from the page with `scenario.peak`).

## 2. `pages/5_Stress_Tests.py` (rewrite the Phase 6 placeholder)
- Same "build a portfolio first" guard as Phases 3-5.
- Fetch price history once via `data.fetch_price_history`, spanning from the earliest scenario's peak date (`min(s.peak for s in SCENARIOS)`) to today.
- `st.tabs` — one per scenario (`"Dot-com (2000-2002)"`, `"2008 Financial Crisis"`, `"2020 COVID Crash"`):
  - If `not entry_timing.horizon_has_sufficient_history(prices, scenario.peak)`: `st.warning` naming the scenario and the reason, stop that tab early.
  - Otherwise compute `value_series = stress_tests.scenario_value_series(prices, weights, scenario, today)`.
  - `max_dd = metrics.max_drawdown(value_series)`; `dollar_impact = 10_000 * max_dd`.
  - `st.metric` for max drawdown (%) and dollar impact ($), plus the scenario's peak/trough dates as a caption.
  - `plotly` line chart of `value_series` over time.
- Assumptions expander: scenarios replay the portfolio's own historical ticker prices (not a benchmark proxy) over named peak-to-trough windows, $10,000 notional invested at the peak, charts extend 2 years past the trough (capped at today) to show early recovery, a scenario is skipped if any portfolio ticker lacks sufficient history.

## 3. `tests/test_stress_tests.py`
- `scenario_window_end` matches hand-computed dates, including the `today` cap (e.g. for the 2020 scenario when `today` is recent).
- `scenario_value_series` matches a hand-computed lump-sum value series on a small synthetic 2-asset price DataFrame spanning a fake scenario's peak/trough/recovery window (verifies correct slicing + delegation to `entry_timing.lump_sum_value_series`).
- Combined with `metrics.max_drawdown`: a synthetic price series with a known dip during the scenario window produces the expected max-drawdown percentage.
- Insufficient-history case: `entry_timing.horizon_has_sufficient_history(prices, scenario.peak)` returns `False` when a ticker's column starts after the scenario's peak date (reuses the Phase 5 function/tests as the contract; just confirms it's wired correctly for stress-test peak dates).

## 4. Verification
- `python -m pytest tests/test_stress_tests.py -v`
- Manual (logic script against real data, same pattern as prior phases): run all three scenarios for a 100% SPY portfolio and confirm the computed max drawdowns are in the right ballpark vs. well-known historical figures (2008 ~-57%, 2020 ~-34%, dot-com ~-49% for the S&P 500 — SPY-specific numbers should be close). Confirm a scenario is correctly skipped for a portfolio containing a ticker too new for that scenario (e.g. CRWD, IPO'd 2019, skipped for dot-com and 2008).
- Manual: run the app, open Drawdown Stress Tests with and without a portfolio built, confirm each scenario tab renders correctly (or shows the insufficient-history warning).
