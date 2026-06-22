# Requirements — drawdown-stress-tests (Phase 6)

## Scope
- Add a working Drawdown Stress Tests page (`pages/5_Stress_Tests.py`), replacing the Phase 6 placeholder.
- Reads the portfolio from `st.session_state["portfolio"]` (Phase 2). If no portfolio exists, show the same "build a portfolio first" prompt used in Phases 3-5.
- Defines three fixed historical crash scenarios, each as a peak-to-trough date range on well-known major-index dates:
  - **Dot-com crash**: peak 2000-03-24, trough 2002-10-09.
  - **2008 Global Financial Crisis**: peak 2007-10-09, trough 2009-03-09.
  - **2020 COVID crash**: peak 2020-02-19, trough 2020-03-23.
- For each scenario, replays the **portfolio's actual historical ticker prices** over the peak-to-trough window (plus a short recovery window) to compute a real (not proxy/benchmark) decline for that specific portfolio composition.
- Displays, per scenario: max drawdown (%), dollar impact on a $10,000 notional, and a value-over-time chart spanning the crash and the start of its recovery.

## Key decisions
- **Scenario method: historical replay, not a benchmark shock.** Each scenario invests a $10,000 notional (split by the portfolio's weights) at the scenario's peak date, using the **portfolio's own tickers' actual prices** during that window — consistent with the mission's "transparent, real data" principle, and avoids assuming every asset moves like the S&P 500.
- **Insufficient history**: a scenario is **skipped entirely** (with a clear explanatory note) if any ticker in the portfolio doesn't have price history reaching back to that scenario's peak date — e.g. a stock that IPO'd after 2008 can't be stress-tested against the 2008 crisis. Mirrors the Phase 5 decision: a single consistent date range is required across the whole portfolio, so no partial/reweighted workaround is attempted.
- **Recovery window**: each scenario's chart/value series extends 2 years past the official trough date (capped at today, for the 2020 scenario where that window is now long past) to show the beginning of recovery, not just the bottom.
- **Drawdown calculation**: the max drawdown is computed over the full peak-to-(trough+recovery) value series — not assumed to be exactly `(trough value / peak value) - 1` — since a specific portfolio's own worst point during the window may differ slightly from the named index's official trough date.
- **Total notional**: fixed $10,000, consistent with Phases 4-5's notional convention.
- **Reuse**: reuses `data.fetch_price_history` (Phase 1) for one combined fetch spanning the earliest scenario's peak date to today; `entry_timing.lump_sum_value_series` and `entry_timing.horizon_has_sufficient_history` (Phase 5) for the value-over-time and sufficient-history logic (a stress-test scenario is structurally a lump-sum investment over a fixed historical window); `metrics.max_drawdown` (Phase 3) for the decline calculation. No new return-computation logic is duplicated — only a small `stress_tests.py` module defining the scenarios and wiring this reuse together.

## Out of scope
- User-defined/custom crash date ranges (fixed set of three scenarios for this phase).
- Excluding/reweighting tickers that lack sufficient history (scenario is skipped instead, per explicit decision).
- Applying scenarios on top of Monte Carlo projections or rebalancing simulations (separate phases).
