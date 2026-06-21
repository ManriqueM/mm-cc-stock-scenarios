# Tech Stack

## Language & Framework
- Python 3 (using the existing `.venv`)
- Streamlit — single Python codebase, fast to build, strong fit for interactive data/finance dashboards

## Data
- `yfinance` for historical OHLCV price data on S&P 500 / NYSE tickers (free, no API key)
- Cache downloaded data with `st.cache_data` to avoid repeated/rate-limited fetches — this is a performance cache, not user-portfolio persistence

## Computation
- `pandas` / `numpy` — returns, risk metrics, portfolio math
- `numpy` / `scipy.stats` — Monte Carlo simulation sampling
- `pytest` — unit tests for metrics/simulation logic

## Visualization
- `plotly` — interactive charts (return distributions, drawdown curves, Monte Carlo fan charts), integrates natively with Streamlit

## Persistence
- None — portfolios live only in `st.session_state` for the duration of a session; nothing is saved server-side between visits. Revisit if saved-portfolios/accounts become a requirement later.

## Deployment
- Streamlit Community Cloud (free, deploys directly from the GitHub repo, gives a shareable public URL) — default given the "shareable, deployed for others" requirement. Can move host later if usage outgrows the free tier.
