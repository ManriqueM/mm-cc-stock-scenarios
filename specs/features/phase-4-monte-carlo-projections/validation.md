# Validation — monte-carlo-projections (Phase 4)

1. `python -m pytest tests/test_simulation.py -v` passes:
   - `simulate_portfolio_paths` returns an array of shape `(n_paths, horizon_days + 1)`, with every path's first value equal to `starting_value`.
   - With an all-zero daily-returns input, every simulated path stays exactly at `starting_value` for the full horizon.
   - Simulation is reproducible given the same seed (two runs with the same seed produce identical paths).
   - `compute_percentile_bands` always satisfies `p10 <= p50 <= p90` for every day in the horizon.
2. Manual check (logic script, real data) — mirroring the Phase 3 sanity check:
   - Derive a portfolio's weighted daily returns over the trailing 5 years (100% SPY, and a 3-ticker portfolio).
   - Run the simulation and confirm the median ending value is in a plausible range relative to the portfolio's Phase 3 historical annualized return compounded over 10 years.
   - Confirm the 10th percentile ending value is below the median and the 90th percentile is above it.
3. Manual check — run `streamlit run app.py`:
   - With no portfolio built, visiting Monte Carlo Projections shows the "build a portfolio first" prompt instead of an error/crash.
   - With a portfolio built, the fan chart renders with a visible shaded band and median line, headline ending-value numbers are shown, and the assumptions expander (bootstrap method, 10-year horizon, 1,000 paths, $10,000 notional) is visible.
