# Plan — portfolio-builder (Phase 2)

Reference: `specs/mission.md`, `specs/tech-stack.md`, `data.py` (Phase 1)

## 1. `portfolio.py` (new module, project root) — pure logic, no Streamlit import
- `parse_portfolio_csv(file) -> pd.DataFrame`: reads an uploaded CSV, case-insensitive `ticker`/`weight` columns, returns a 2-column DataFrame (raises `ValueError` with a clear message on missing columns).
- `validate_weights(weights: list[float], tolerance: float = 0.5) -> tuple[bool, float]`: returns `(is_valid, total)`.
- `find_duplicate_tickers(tickers: list[str]) -> list[str]`: returns any tickers entered more than once (after normalization).
- `build_portfolio(tickers: list[str], weights: list[float], lookback_days: int = 30) -> tuple[pd.DataFrame | None, list[str]]`: normalizes tickers, checks weight sum and duplicates first (no network call needed for those), then calls `data.fetch_price_history` over a recent window to confirm each ticker has data. Returns `(portfolio_df, errors)` — `portfolio_df` is `None` if there are any errors.

## 2. `pages/1_Portfolio_Builder.py` (rewrite the Phase 0 placeholder)
- `st.tabs(["Manual entry", "Upload CSV"])`:
  - Manual entry: `st.data_editor` with `Ticker`/`Weight %` columns, `num_rows="dynamic"`, a few empty starter rows.
  - Upload CSV: `st.file_uploader`, parsed via `parse_portfolio_csv`.
- A single "Build Portfolio" button triggers validation (via `portfolio.build_portfolio`) for whichever tab is active.
- On error: `st.error` listing every problem found (weight sum, duplicates, invalid tickers).
- On success: save to `st.session_state["portfolio"]`, show a confirmation, a summary table, and a `plotly` pie chart of allocation.
- If a portfolio already exists in session state, show it at the top of the page before the input form.

## 3. `tests/test_portfolio.py`
- Unit tests for `parse_portfolio_csv`, `validate_weights`, `find_duplicate_tickers` (pure logic, no network).
- One live-network test for `build_portfolio` happy path + one for an invalid ticker, reusing the Phase 1 testing pattern.

## 4. Verification
- `python -m pytest tests/test_portfolio.py -v`
- Manual: run the app, build a portfolio both ways (manual entry and CSV upload), confirm validation errors and the success summary/chart.
