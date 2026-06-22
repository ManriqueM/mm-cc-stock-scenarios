# Validation — drawdown-stress-tests (Phase 6)

1. `python -m pytest tests/test_stress_tests.py -v` passes:
   - `scenario_window_end` matches hand-computed dates, including the `today` cap.
   - `scenario_value_series` matches a hand-computed lump-sum value series on a small synthetic price DataFrame for a fake scenario's window.
   - A synthetic price series with a known dip produces the expected max-drawdown percentage when combined with `metrics.max_drawdown`.
   - `entry_timing.horizon_has_sufficient_history` correctly returns `False`/`True` when checked against a scenario's peak date.
2. Manual check (logic script, real data) — mirroring prior phases' sanity checks:
   - Run all three scenarios for a 100% SPY portfolio; confirm max drawdowns are roughly in line with well-known historical figures (2008 ~-57%, 2020 ~-34%, dot-com ~-49%).
   - Run the scenarios for a portfolio including a recently-IPO'd ticker (e.g. CRWD) and confirm the dot-com and 2008 scenarios are correctly skipped with a clear note, while the 2020 scenario runs normally.
3. Manual check — run `streamlit run app.py`:
   - With no portfolio built, visiting Drawdown Stress Tests shows the "build a portfolio first" prompt instead of an error/crash.
   - With a portfolio built, each scenario tab shows max drawdown %, dollar impact, a value-over-time chart (or the skip warning), and the assumptions expander is visible.
