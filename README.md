# Stock Scenarios

> An interactive app for analyzing historical S&P 500 / NYSE stock data and stress-testing real, multi-asset investment portfolios.

**🔗 Live app:** [settings-kmexvgtzi9apydplwabwis.streamlit.app](https://settings-kmexvgtzi9apydplwabwis.streamlit.app)

## Overview

Stock Scenarios helps individual investors evaluate their own real portfolios using actual historical price data, rather than relying on a black-box robo-advisor. You build a multi-asset portfolio, then explore its historical risk/return profile and run forward-looking and historical-crash scenario analyses — with every result paired with the assumptions and data limitations behind it, never buried in footnotes.

## Features

- **Portfolio builder** — enter tickers and weights manually, or upload a CSV; validates that weights sum to 100% and tickers have available price data.
- **Historical metrics** — annualized return, volatility, Sharpe ratio, max drawdown, and a correlation matrix, for the portfolio and each individual asset.
- **Monte Carlo projections** — bootstrap-resampled simulation of 1,000 possible 10-year paths, shown as a percentile-band ("fan") chart.
- **Entry-timing comparison** — lump-sum vs. dollar-cost averaging, compared across 1/3/5/10-year historical horizons.
- **Drawdown stress tests** — replays the portfolio's own historical prices through the dot-com crash, the 2008 financial crisis, and the 2020 COVID crash.
- **Rebalancing rules** — compares buy-and-hold against quarterly and annual rebalancing on risk/return.
- **Assumptions & limitations** — a dedicated, always-visible page (plus a footer on every screen) documenting data limitations, simulation assumptions, and a "not financial advice" disclaimer.

## Tech Stack

- **Language/Framework:** Python 3, [Streamlit](https://streamlit.io/)
- **Data:** [`yfinance`](https://github.com/ranaroussi/yfinance) for historical price data, cached with `st.cache_data`
- **Computation:** `pandas`, `numpy`, `scipy.stats`
- **Visualization:** `plotly`
- **Testing:** `pytest`
- **Persistence:** none — portfolios live only in-session (`st.session_state`)
- **Deployment:** Streamlit Community Cloud

## Installation

```bash
git clone https://github.com/ManriqueM/mm-cc-stock-scenarios.git
cd mm-cc-stock-scenarios
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Prefer not to install anything? Use the **[live app](https://settings-kmexvgtzi9apydplwabwis.streamlit.app)** instead.

To run it locally:

```bash
streamlit run app.py
```

Then, in the app:

1. Go to **Portfolio Builder** and enter tickers + weights (or upload a CSV with `ticker` and `weight` columns) — weights must sum to 100%.
2. Use the sidebar to explore **Historical Metrics**, **Monte Carlo**, **Entry Timing**, **Stress Tests**, and **Rebalancing** for your portfolio.
3. Check **Assumptions and Limitations** for the data limitations and simulation assumptions behind every page.

Run the test suite with:

```bash
pytest
```

## Project Structure

```
.
├── app.py                  # Home page — overview + always-visible disclosure footer
├── data.py                 # yfinance wrapper: fetch & cache historical price data
├── portfolio.py            # Portfolio parsing/validation logic (no UI)
├── metrics.py              # Return/risk metric calculations (no UI)
├── simulation.py           # Monte Carlo bootstrap simulation engine (no UI)
├── entry_timing.py         # Lump-sum vs. DCA value-series logic (no UI)
├── stress_tests.py         # Historical crash scenario definitions & replay logic (no UI)
├── rebalancing.py          # Periodic rebalancing simulation logic (no UI)
├── disclosures.py          # Shared disclosure text + footer renderer
├── pages/                  # Streamlit multi-page app screens (1 file per page)
├── tests/                  # pytest unit tests for the pure-logic modules above
├── specs/                  # Project mission, tech stack, roadmap, and feature specs
└── requirements.txt        # Python dependencies
```

## Roadmap

- [x] Phase 0 — Project scaffold
- [x] Phase 1 — Data layer
- [x] Phase 2 — Portfolio builder
- [x] Phase 3 — Historical metrics
- [x] Phase 4 — Monte Carlo projections
- [x] Phase 5 — Entry-timing comparison
- [x] Phase 6 — Drawdown stress tests
- [x] Phase 7 — Rebalancing rules
- [x] Phase 8 — Assumptions & limitations
- [x] Phase 9 — Deploy

## License

MIT License
