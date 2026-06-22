# Validation — entry-timing-comparison (Phase 5)

1. `python -m pytest tests/test_entry_timing.py -v` passes:
   - `lump_sum_value_series` matches a hand-computed value series on a small synthetic 2-asset price DataFrame.
   - `monthly_investment_dates` returns exactly one date per calendar month (the first trading day of that month) on a synthetic date range spanning several months with non-trading-day gaps.
   - `dca_value_series`: total invested across installments equals `total_investment`; matches a hand-computed series for 2-3 installments; value is `0` before the first installment.
   - `horizon_has_sufficient_history` correctly distinguishes sufficient vs. insufficient per-ticker history.
   - Single-ticker portfolio works correctly for both strategies.
2. Manual check (logic script, real data) — mirroring the Phase 3/4 sanity checks:
   - Run lump-sum and DCA for a 100% SPY portfolio across all four horizons (1/3/5/10y); confirm ending values are plausible and lump-sum vs. DCA ordering makes sense given SPY's historical trajectory (DCA typically lags lump-sum in a rising market, since later installments buy fewer cheap shares).
   - Run the same for a multi-ticker portfolio (e.g. AAPL/MSFT/SPY) and confirm a horizon is correctly skipped (with a clear note) if any ticker lacks sufficient history for that horizon.
3. Manual check — run `streamlit run app.py`:
   - With no portfolio built, visiting Entry-Timing Comparison shows the "build a portfolio first" prompt instead of an error/crash.
   - With a portfolio built, each horizon tab shows ending value/return for both strategies and a value-over-time chart, and the assumptions expander is visible.
