# Requirements — monte-carlo-projections (Phase 4)

## Scope
- Add a working Monte Carlo Projections page (`pages/3_Monte_Carlo.py`), replacing the Phase 4 placeholder.
- Reads the portfolio from `st.session_state["portfolio"]` (Phase 2). If no portfolio exists, show the same "build a portfolio first" prompt used in Phase 3.
- Runs a bootstrap Monte Carlo simulation of the portfolio's future value over a 10-year horizon, using 1,000 simulated paths.
- Displays a percentile-band ("fan") chart: median path + shaded 10th-90th percentile band, plus headline ending-value numbers (median, 10th percentile, 90th percentile).

## Key decisions
- **Simulation method: bootstrap resampling** of the portfolio's actual trailing 5-year weighted daily returns (computed via Phase 3's `metrics.daily_returns` + `metrics.weighted_portfolio_returns`), not a parametric (Normal) distribution. Each simulated day independently resamples (with replacement) from the historical daily return series and compounds — this captures the real historical fat-tails/skew without assuming normality.
- **Horizon & paths**: fixed 10-year horizon (2,520 trading days at 252/year) and 1,000 simulated paths — not user-selectable for now (mirrors Phase 3's fixed-lookback decision; keeps scope and UI simple).
- **Starting value**: fixed $10,000 notional, clearly labeled as illustrative — results are about the *shape* of the distribution of outcomes, not a personalized dollar forecast. Not user-input for this phase.
- **Chart**: single shaded band between the 10th and 90th percentile across paths, with the median (50th percentile) as a solid line — the standard "fan chart" convention. X-axis in years for readability (converted from trading days).
- **Pure logic separated from UI**: simulation logic lives in a new `simulation.py` module (no Streamlit import; takes a pre-computed daily-returns array as input rather than depending on `metrics.py` directly), unit-testable in isolation with seeded randomness for reproducible tests.
- **Reuse**: reuses `data.fetch_price_history` (Phase 1) for the same 5-year window, and `metrics.daily_returns` / `metrics.weighted_portfolio_returns` (Phase 3) to derive the portfolio's historical daily return series that feeds the bootstrap — no duplicated return-computation logic.

## Out of scope
- User-selectable horizon, path count, or starting value (fixed for this phase, per explicit decision — may revisit later).
- Parametric/Normal-distribution simulation mode.
- Contributions/withdrawals during the horizon (lump-sum-equivalent projection only; entry-timing/DCA comparisons are Phase 5).
- Rebalancing during the simulated horizon (Phase 7).
- Incorporating stress-test/crash scenarios into the simulation (Phase 6 is separate and historical-scenario-based, not bootstrap-based).
