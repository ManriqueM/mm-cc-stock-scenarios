from datetime import date, timedelta

import pandas as pd
import streamlit as st
import yfinance as yf


@st.cache_data(ttl=timedelta(hours=24), show_spinner="Fetching price data...")
def _download_close_prices(
    tickers: tuple[str, ...], start: date, end: date
) -> pd.DataFrame:
    raw = yf.download(list(tickers), start=start, end=end, auto_adjust=True, progress=False)
    if "Close" not in raw.columns.get_level_values(0):
        return pd.DataFrame(columns=list(tickers))
    return raw["Close"]


def fetch_price_history(
    tickers: list[str], start: date, end: date
) -> tuple[pd.DataFrame, list[str]]:
    """Fetch daily adjusted-close prices for `tickers` between `start` and `end`.

    Returns a `(prices, invalid_tickers)` tuple: `prices` has one column per
    valid ticker, and `invalid_tickers` lists requested tickers with no data
    over the given range (bad symbol, delisted, or no history yet).
    """
    unique_tickers = tuple(sorted({t.strip().upper() for t in tickers if t.strip()}))
    if not unique_tickers:
        return pd.DataFrame(), []

    closes = _download_close_prices(unique_tickers, start, end)
    invalid = [
        t for t in unique_tickers if t not in closes.columns or closes[t].isna().all()
    ]
    valid_prices = closes.drop(columns=invalid, errors="ignore").dropna(how="all")
    return valid_prices, invalid
