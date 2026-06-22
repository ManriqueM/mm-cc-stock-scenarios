# Validation — rebalancing-rules (Phase 7)

1. `python -m pytest tests/test_rebalancing.py -v` passes:
   - `rebalance_dates` returns the expected dates for `"quarterly"` and `"annual"` on a synthetic multi-year date range.
   - `rebalanced_value_series` matches a hand-computed series for a small synthetic 2-asset price DataFrame with one rebalance event.
   - Single-ticker portfolio: `rebalanced_value_series` equals `entry_timing.lump_sum_value_series` for both frequencies.
   - A synthetic two-asset series with diverging returns and a rebalance produces a different ending value than buy-and-hold.
2. Manual check (logic script, real data) — mirroring prior phases' sanity checks:
   - Run buy-and-hold, quarterly, and annual rebalancing for a multi-ticker portfolio (e.g. AAPL 40 / MSFT 30 / SPY 30) over the trailing 5 years; confirm ending values and risk metrics (volatility, Sharpe, max drawdown) are plausible and differ across the three strategies.
   - Run the same for a 100% SPY (single-ticker) portfolio and confirm all three strategies produce identical ending values (rebalancing is a no-op with one asset).
3. Manual check — run `streamlit run app.py`:
   - With no portfolio built, visiting Rebalancing shows the "build a portfolio first" prompt instead of an error/crash.
   - With a portfolio built, the comparison table (ending value, return, volatility, Sharpe, max drawdown per strategy) and the overlaid chart render correctly, and the assumptions expander is visible.
