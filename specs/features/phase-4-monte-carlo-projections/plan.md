# Plan — monte-carlo-projections (Phase 4)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1), `metrics.py` (Phase 3)

## 1. `simulation.py` (new module, project root) — pure logic, no Streamlit import
- `simulate_portfolio_paths(daily_returns: np.ndarray, horizon_days: int, n_paths: int, starting_value: float = 10_000.0, seed: int | None = None) -> np.ndarray`: bootstrap-resamples (with replacement) from `daily_returns` to build `n_paths` independent compounding paths over `horizon_days`. Returns an array of shape `(n_paths, horizon_days + 1)` — column 0 is `starting_value` for every path.
- `compute_percentile_bands(paths: np.ndarray, percentiles: tuple[float, ...] = (10, 50, 90)) -> pd.DataFrame`: per-day percentiles across paths; one column per percentile (e.g. `p10`, `p50`, `p90`), one row per day (`0..horizon_days`).

## 2. `pages/3_Monte_Carlo.py` (rewrite the Phase 4 placeholder)
- Same "build a portfolio first" guard as `pages/2_Historical_Metrics.py` (Phase 3).
- Fetch 5-year price history via `data.fetch_price_history` (same window as Phase 3), then derive the portfolio's weighted daily return series via `metrics.daily_returns` + `metrics.weighted_portfolio_returns` — no new return-computation logic.
- Run `simulation.simulate_portfolio_paths` with `horizon_days = 10 * 252 = 2520`, `n_paths = 1000`, `starting_value = 10_000.0`.
- Compute percentile bands (10/50/90) via `simulation.compute_percentile_bands`.
- Plot a `plotly` fan chart: shaded area between `p10` and `p90`, median (`p50`) as a solid line on top; x-axis converted from trading days to years (`day / 252`).
- Headline numbers via `st.metric`: median ending value, 10th percentile ending value, 90th percentile ending value (formatted as currency).
- Assumptions expander (mirrors Phase 3's): bootstrap resampling from the trailing 5-year daily return history, 10-year horizon, 1,000 simulated paths, $10,000 notional starting value, no contributions/withdrawals/rebalancing during the horizon, and a "past performance doesn't guarantee future results" note.

## 3. `tests/test_simulation.py`
- Unit tests with seeded RNG for reproducibility:
  - `simulate_portfolio_paths` output shape is `(n_paths, horizon_days + 1)`; every path's first column equals `starting_value`.
  - All-zero daily-returns input → every path stays exactly at `starting_value` for the whole horizon.
  - Same seed → identical paths across two separate calls (reproducibility).
  - `compute_percentile_bands` satisfies `p10 <= p50 <= p90` for every day, on both a synthetic returns array and the zero-returns case.

## 4. Verification
- `python -m pytest tests/test_simulation.py -v`
- Manual (logic script against real data, same pattern as the Phase 3 sanity check): derive a portfolio's weighted daily returns (100% SPY, and a multi-ticker portfolio), run the simulation, confirm the median ending value is in a plausible range relative to the portfolio's Phase 3 historical annualized return compounded over 10 years, and that `p10 < p50 < p90` holds.
- Manual: run the app, open Monte Carlo Projections with and without a portfolio built, confirm the fan chart, headline numbers, and assumptions expander render correctly.
