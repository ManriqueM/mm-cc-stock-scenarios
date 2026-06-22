# Plan — assumptions-and-limitations (Phase 8)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1), `app.py` and `pages/1-6` (Phases 0-7)

## 1. `disclosures.py` (new module, project root) — Streamlit-aware, no business logic
- `NOT_FINANCIAL_ADVICE: str` — short one-liner used in the footer ("Not financial advice. All figures are derived from historical data and simplifying assumptions...").
- `DATA_LIMITATIONS: str` (markdown) — based on the actual behavior of `data.fetch_price_history`:
  - Free, unofficial Yahoo Finance API (`yfinance`) — no SLA; fetches can fail, rate-limit, or silently return incomplete data.
  - Only **daily closing prices**, **adjusted for splits and dividends** (`auto_adjust=True`) — no intraday data, no access to raw unadjusted prices.
  - Price data is **cached for 24 hours** (`st.cache_data(ttl=timedelta(hours=24))`) — recent moves may not be reflected immediately.
  - Tickers are looked up by their **current symbol only** — delisted/renamed/merged companies may show incomplete or no history, which can introduce survivorship bias in long lookbacks.
  - Tickers with **partial history** (e.g., recent IPOs) are still included with whatever shorter window is available.
- `SIMULATION_ASSUMPTIONS: str` (markdown) — general, cross-page assumptions that aren't already covered by an existing per-page expander: illustrative notional amounts, no fees/taxes/slippage anywhere in the app, fixed (non-user-tunable) lookback windows/horizons per page, past performance does not guarantee future results, no personalization (tax situation, goals, risk tolerance).
- `render_footer() -> None`: renders `st.divider()`, then a non-collapsed `st.warning(NOT_FINANCIAL_ADVICE, icon="⚠️")`, then `st.page_link("pages/7_Assumptions_and_Limitations.py", label="Full assumptions & data limitations", icon="📋")`. Called at the bottom of every page.

## 2. `pages/7_Assumptions_and_Limitations.py` (new page)
- No portfolio guard — must render standalone.
- Title + one-paragraph intro reinforcing `disclosures.NOT_FINANCIAL_ADVICE`.
- "Data limitations" section: render `disclosures.DATA_LIMITATIONS`.
- "Simulation assumptions" section: render `disclosures.SIMULATION_ASSUMPTIONS`.
- "Page-specific assumptions" section: one bullet per existing page (Historical Metrics, Monte Carlo, Entry Timing, Stress Tests, Rebalancing) summarizing that page's own "Assumptions" expander in a single line, each with an `st.page_link` back to that page for full detail.

## 3. Wire the footer into every existing page
- `app.py`: remove the existing inline `st.warning(...)` block at the bottom; add a one-line pointer to the new page in the intro markdown; call `disclosures.render_footer()` at the end.
- `pages/1_Portfolio_Builder.py` through `pages/6_Rebalancing.py`: add `import disclosures` and a single `disclosures.render_footer()` call at the end of each file (after the existing "Assumptions" expander where one exists). No other changes to these files — existing page-specific expanders are untouched.

## 4. Verification
- No automated tests added (per `requirements.md` — `disclosures.py` is static content + thin rendering, nothing with branching logic).
- Manual: `streamlit run app.py`, visit every page (home + all 7 sub-pages) and confirm:
  - The footer warning is visible **without clicking anything** on every page.
  - The `st.page_link` in the footer navigates to the new Assumptions & Limitations page.
  - The new page renders fully without a portfolio built, and its per-page links navigate correctly.
  - Existing per-page "Assumptions" expanders and all prior functionality (Phases 0-7) are unchanged.
- `python -m pytest` — full existing suite still passes (no regressions from the new import/footer call added to each page).
