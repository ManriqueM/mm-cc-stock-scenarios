# Requirements — assumptions-and-limitations (Phase 8)

## Scope
- Today, "Assumptions" are scattered in per-page collapsed `st.expander` blocks (Historical Metrics, Monte Carlo, Entry Timing, Stress Tests, Rebalancing), and the only "not financial advice" framing lives in a single `st.warning` on the home page (`app.py`). General data limitations (how `yfinance` data is fetched, adjusted, and cached) aren't documented anywhere.
- Add a persistent, **always-visible** (not collapsed) disclosure footer rendered at the bottom of every page — home page included.
- Add a new dedicated page, **Assumptions & Limitations**, consolidating:
  - General data limitations (free/unofficial `yfinance` API, daily-only adjusted-close prices, 24-hour cache, current-symbol-only lookups / survivorship bias, partial-history tickers).
  - General simulation assumptions that apply across pages (illustrative notional amounts, no fees/taxes/slippage, fixed lookback windows, past performance disclaimer).
  - A one-line-per-page summary pointing to each existing page's own (page-specific) "Assumptions" expander, so a user gets the full picture in one place without losing the detail already on each page.
- Existing per-page "Assumptions" expanders are kept as-is — they cover page-specific mechanics (e.g., DCA installment timing, rebalance-date convention) that don't belong in a general page.

## Key decisions
- **New shared module `disclosures.py`** (project root, Streamlit-aware — unlike the existing pure-logic modules) holds the disclosure text as constants (`NOT_FINANCIAL_ADVICE`, `DATA_LIMITATIONS`, `SIMULATION_ASSUMPTIONS`) plus one render function, `render_footer()`, called from every page.
- **Footer placement**: bottom of each page (`st.divider()` + a compact, non-collapsed warning line + a `st.page_link` to the new Assumptions & Limitations page). Kept short by design — it's a constant reminder, not a replacement for the detailed page.
- **New page**: `pages/7_Assumptions_and_Limitations.py`, numbered after the existing six pages. No "build a portfolio first" guard — it must be readable without a portfolio in `st.session_state`.
- **`app.py` update**: replace the existing inline `st.warning(...)` block with a call to `disclosures.render_footer()` so the home page uses the same consolidated component as every other page, and add a one-line pointer to the new page in the intro copy.
- **No automated tests for this phase** — `disclosures.py` is static content plus thin Streamlit rendering calls, nothing with branching logic to unit test. Validated by manual review across all pages (per `validation.md`).

## Out of scope
- Per-page data-limitation callouts beyond the existing "Assumptions" expanders — general data limitations live once, on the dedicated page and in the footer link, not duplicated on every page.
- Any new disclosure *content* beyond what's already implied by the current implementation (e.g., no legal/compliance review of wording — this is app-level transparency, not a legal disclaimer).
- Automated UI tests (e.g., Streamlit `AppTest`) — validation is manual for this phase.
