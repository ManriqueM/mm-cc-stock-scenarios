# Validation — portfolio-builder (Phase 2)

1. `python -m pytest tests/test_portfolio.py -v` passes:
   - `parse_portfolio_csv` parses a valid CSV and raises a clear error on missing columns.
   - `validate_weights` accepts sums within ±0.5 of 100 and rejects sums outside it.
   - `find_duplicate_tickers` detects repeated tickers (case-insensitive).
   - `build_portfolio` succeeds for a small set of known-good tickers with valid weights.
   - `build_portfolio` reports an invalid ticker and does not return a portfolio.
2. Manual check — run `streamlit run app.py`, open Portfolio Builder:
   - Manual entry: add 3 rows (e.g. AAPL 40, MSFT 30, SPY 30), click "Build Portfolio" → success, table + pie chart shown.
   - Enter weights that don't sum to 100 → clear error showing the current total, no portfolio saved.
   - Enter a duplicate ticker → clear error naming the duplicate.
   - Enter an invalid ticker → clear error naming it as invalid.
   - Upload CSV mode: upload a small CSV with `ticker,weight` columns → same success path.
