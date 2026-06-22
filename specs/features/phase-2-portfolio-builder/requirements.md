# Requirements — portfolio-builder (Phase 2)

## Scope
- Add a working Portfolio Builder page (`pages/1_Portfolio_Builder.py`), replacing the Phase 0 placeholder.
- Two input modes, in tabs: **Manual entry** (editable table via `st.data_editor`, add/remove rows) and **CSV upload** (`ticker,weight` columns).
- On submit, validate the entered tickers + weights, and on success store the portfolio in `st.session_state["portfolio"]` for later phases to consume.
- Display a portfolio summary: a ticker/weight table and an allocation pie chart.

## Key decisions
- **Weight validation**: weights must sum to 100% within a ±0.5 percentage-point tolerance (to allow for rounding when entering numbers like 33.33/33.33/33.34). If outside tolerance, show an error with the current total — no auto-normalization, per explicit decision; the user must adjust the numbers themselves.
- **Duplicate tickers**: rejected with an explicit error (e.g. "AAPL entered twice") rather than silently merged/summed — avoids ambiguity about user intent.
- **Ticker validation**: reuses `data.fetch_price_history` (Phase 1) over a short recent window (last 30 calendar days) purely to confirm the ticker has data — not the full historical range (that's for Phase 3+). Validation runs once per "Build Portfolio" click, not on every keystroke, to avoid excessive `yfinance` calls.
- **Storage**: `st.session_state["portfolio"]` — a DataFrame with columns `ticker`, `weight` (0–100 scale). Session-only, per `specs/tech-stack.md` (no DB).
- **Pure logic separated from UI**: validation/parsing logic lives in a new `portfolio.py` module (no Streamlit import) so it's directly unit-testable; the page module only handles widgets/display.

## Out of scope
- Computing any return/risk metrics on the portfolio (Phase 3).
- Editing an existing saved portfolio in place — rebuilding via the same form is sufficient for now.
- Ticker metadata (company name, sector) — not available from the Phase 1 data layer.
