# Requirements — entry-timing-comparison (Phase 5)

## Scope
- Add a working Entry-Timing Comparison page (`pages/4_Entry_Timing.py`), replacing the Phase 5 placeholder.
- Reads the portfolio from `st.session_state["portfolio"]` (Phase 2). If no portfolio exists, show the same "build a portfolio first" prompt used in Phases 3-4.
- For each of a fixed set of historical horizons (1, 3, 5, 10 years ago), compares two entry strategies investing the same total notional amount:
  - **Lump-sum**: the full amount invested at the start of the horizon.
  - **DCA (dollar-cost averaging)**: the same total amount split into equal monthly installments from the start of the horizon to today.
- Displays, per horizon: ending value and total return (%) for both strategies side by side, plus a line chart of portfolio value over time for both.

## Key decisions
- **Horizons**: fixed set — 1, 3, 5, 10 years ago — not user-selectable, mirroring the fixed-window decisions in Phases 3-4. Each horizon's start date is `today - N years`.
- **Total notional investment**: fixed at $10,000, identical for both strategies in a given horizon, so the comparison is fair and consistent with the Monte Carlo page's (Phase 4) notional convention.
- **DCA structure**: 12 equal installments/year, invested on the first trading day of each calendar month within the horizon — not weekly, to keep the number of simulated transactions modest and the "monthly" framing intuitive for non-technical users.
- **Multi-asset handling**: each installment (lump-sum's single investment, or each DCA installment) is split across tickers by the portfolio's weights at that installment's prices; per-ticker share counts accumulate over time and are valued at each subsequent day's price to build the value-over-time series.
- **Insufficient history**: a horizon is skipped (with an explanatory note, not an error) if any ticker in the portfolio doesn't have price history reaching back to that horizon's start date (e.g. a 10-year horizon for a stock that IPO'd 4 years ago) — a lump-sum/DCA comparison requires a single consistent start date across the whole portfolio, so partial-history workarounds aren't attempted.
- **No fees, taxes, or slippage** modeled — purely a price-return comparison, consistent with the "transparent simplifying assumptions" approach used in Phases 3-4.
- **Pure logic separated from UI**: strategy simulation lives in a new `entry_timing.py` module (no Streamlit import), unit-testable in isolation; the page module only handles widgets/display and horizon looping.
- **Reuse**: reuses `data.fetch_price_history` (Phase 1) for a single 10-year price fetch (the longest horizon), then slices that DataFrame per horizon rather than re-fetching per horizon.

## Out of scope
- User-selectable horizons, notional amount, or DCA frequency (fixed for this phase, per explicit decision — may revisit later).
- Fees, taxes, or transaction costs.
- Rebalancing during the horizon (Phase 7).
- Benchmark comparison beyond the user's own portfolio.
