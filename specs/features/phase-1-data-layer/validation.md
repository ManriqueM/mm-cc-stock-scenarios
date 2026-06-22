# Validation — data-layer (Phase 1)

1. `python -m pytest tests/test_data.py -v` passes:
   - Fetching `["AAPL", "MSFT", "SPY"]` over a known historical range returns a DataFrame with those 3 columns, no `invalid_tickers`, and rows matching trading days in range.
   - Fetching a mix of valid + obviously-invalid ticker (e.g. `"NOTAREALTICKERXYZ"`) returns the invalid one in `invalid_tickers` and excludes it from the price DataFrame.
   - Lowercase/duplicate input tickers (e.g. `["aapl", "AAPL"]`) normalize to a single `AAPL` column.
   - Calling the function twice with the same arguments returns identical data (cache works, no errors).
2. Manual sanity check: run a short script importing `fetch_price_history` directly and print `.head()`/`.tail()` of the result.
