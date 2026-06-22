# Validation — assumptions-and-limitations (Phase 8)

1. `python -m pytest` passes — the full existing suite has no regressions from adding `disclosures.py` and wiring it into `app.py` and `pages/1-6`.
2. Manual check — run `streamlit run app.py`:
   - **Home page**: the "not financial advice" warning is visible immediately (no click/expand needed), and there's a working link to the new Assumptions & Limitations page.
   - **Each of the 6 existing pages** (Portfolio Builder, Historical Metrics, Monte Carlo, Entry Timing, Stress Tests, Rebalancing): scrolling to the bottom shows the same always-visible footer warning + link, in addition to (not replacing) that page's existing "Assumptions" expander where one exists.
   - **New "Assumptions & Limitations" page**: accessible from the sidebar and from every footer link; renders fully **without** a portfolio built (no "build a portfolio first" guard); shows data limitations, general simulation assumptions, and one-line summaries linking back to each page's specific assumptions.
3. Manual check — wording review: confirm the footer text is short enough not to dominate any page, and the dedicated page's content accurately reflects current behavior (`auto_adjust=True`, 24-hour cache, current-symbol-only lookups) by spot-checking against `data.py`.
