# Plan — data-layer (Phase 1)

Reference: `specs/tech-stack.md` (yfinance, `st.cache_data`, pandas)

## 1. `data.py` (new module, project root)
- `fetch_price_history(tickers: list[str], start: date, end: date) -> tuple[pd.DataFrame, list[str]]`
  - Normalizes tickers (strip, uppercase, dedupe).
  - Delegates to a `st.cache_data`-wrapped internal downloader (`_download_close_prices`), keyed on a sorted tuple of tickers + start/end, TTL 24h.
  - Uses `yfinance.download(..., auto_adjust=True)["Close"]` to get adjusted close prices.
  - Splits results into `(valid_prices_df, invalid_tickers)` — a ticker is invalid if its column is entirely NaN over the requested range.
  - Returns prices with columns = valid tickers, index = trading dates.

## 2. `tests/test_data.py`
- Live yfinance tests (no mocking) using a small fixed set of known tickers (AAPL, MSFT, SPY) plus one deliberately invalid ticker.
- Cases:
  - Valid tickers return non-empty data with the expected columns.
  - An invalid ticker is reported in `invalid_tickers` and excluded from the price DataFrame.
  - Date range is respected.
  - Lowercase/duplicate input tickers normalize to one column.
  - Repeated calls with identical arguments return identical data (cache works, no errors).

## 3. Verification
- `python -m pytest tests/test_data.py -v`
