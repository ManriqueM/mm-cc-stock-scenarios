# Requirements — rebalancing-rules (Phase 7)

## Scope
- Add a working Rebalancing Rules page (`pages/6_Rebalancing.py`), replacing the Phase 7 placeholder.
- Reads the portfolio from `st.session_state["portfolio"]` (Phase 2). If no portfolio exists, show the same "build a portfolio first" prompt used in Phases 3-6.
- Over the fixed trailing 5-year window (same convention as Phase 3/4), compares three strategies, each investing the same $10,000 notional:
  - **Buy-and-hold**: no rebalancing — weights drift as prices move.
  - **Quarterly rebalancing**: reset to target weights at the start of every calendar quarter.
  - **Annual rebalancing**: reset to target weights at the start of every calendar year.
- Displays for each strategy: ending value, total return, annualized volatility, Sharpe ratio, and max drawdown, plus a single chart overlaying all three value-over-time series.

## Key decisions
- **Lookback**: fixed trailing 5 years, consistent with Phase 3/4 — not user-selectable.
- **Notional**: fixed $10,000, consistent with Phases 4-6.
- **Rebalance dates**: the first trading day of each calendar quarter (quarterly) or calendar year (annual) present in the window — mirrors Phase 5's "first trading day of each calendar period" convention used for DCA installment dates.
- **Rebalancing mechanic**: at each rebalance date, the portfolio's current total value is redistributed across tickers according to the target weights at that date's prices (sell winners/buy laggards back to target); share counts reset at each rebalance date and otherwise drift freely with price moves between rebalances (same as buy-and-hold in between).
- **No fees, taxes, or slippage** modeled on rebalancing trades — consistent with the "pure price-return" simplification used in prior phases.
- **Single-ticker portfolios**: rebalancing is a no-op (there's nothing to rebalance against), so the quarterly/annual series will be identical to buy-and-hold — this is expected, not an error or edge case to special-case away.
- **Reuse**: `data.fetch_price_history` (Phase 1) for the 5-year window; `entry_timing.lump_sum_value_series` (Phase 5) directly as the buy-and-hold series (a lump-sum investment with no further trading is exactly buy-and-hold); `metrics.annualized_return` / `annualized_volatility` / `sharpe_ratio` / `max_drawdown` (Phase 3) for each strategy's risk/return numbers. Only rebalance-date generation and the rebalanced value-series computation are new logic.

## Out of scope
- User-selectable lookback window, rebalancing frequency, or notional (fixed for this phase, per explicit decision).
- Fees, taxes, or slippage on rebalancing trades.
- Threshold-based (vs. calendar-based) rebalancing triggers.
