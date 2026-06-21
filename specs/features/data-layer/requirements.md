# Requirements — data-layer (Phase 1)

## Scope
- A single `data.py` module exposing `fetch_price_history(tickers, start, end)` for fetching historical daily **adjusted close** prices via `yfinance`.
- Ticker validation is folded into the same fetch call (no separate network round-trip): tickers with no data over the requested range are reported as invalid rather than raising.
- Results are cached via `st.cache_data` (24h TTL) keyed on the normalized ticker set + date range, to avoid redundant/rate-limited downloads.

## Key decisions
- **Adjusted close only** (no OHLCV) — sufficient for every metric on the roadmap (returns, volatility, Sharpe, drawdown, Monte Carlo, rebalancing).
- Tickers are normalized (stripped, uppercased, deduplicated) before fetching, so `aapl` and `AAPL` are treated as the same request.
- "Invalid" = no data at all over the requested date range (covers bad symbols, delisted tickers, or symbols with no history in that window). This is necessarily range-dependent — a ticker valid for one range could show as invalid for an earlier range (e.g. pre-IPO).
- Caching is by exact `(tickers, start, end)` — different requested ranges/ticker sets are cached independently.

## Out of scope
- Choosing a default date range / lookback window — deferred to the Phase 2 UI.
- A curated S&P 500/NYSE ticker whitelist — validation here only checks "does yfinance return any data," not "is this actually an S&P 500 constituent."
- OHLCV, volume, or any data beyond adjusted close.
