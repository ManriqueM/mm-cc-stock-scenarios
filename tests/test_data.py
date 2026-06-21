from datetime import date

import pandas as pd

from data import fetch_price_history

START = date(2024, 1, 1)
END = date(2024, 2, 1)


def test_valid_tickers_return_expected_columns():
    prices, invalid = fetch_price_history(["AAPL", "MSFT", "SPY"], START, END)

    assert invalid == []
    assert set(prices.columns) == {"AAPL", "MSFT", "SPY"}
    assert not prices.empty


def test_invalid_ticker_is_reported_and_excluded():
    prices, invalid = fetch_price_history(["AAPL", "NOTAREALTICKERXYZ"], START, END)

    assert invalid == ["NOTAREALTICKERXYZ"]
    assert "NOTAREALTICKERXYZ" not in prices.columns
    assert "AAPL" in prices.columns


def test_tickers_are_normalized_and_deduped():
    prices, invalid = fetch_price_history(["aapl", "AAPL", " Aapl "], START, END)

    assert invalid == []
    assert list(prices.columns) == ["AAPL"]


def test_date_range_is_respected():
    prices, _ = fetch_price_history(["AAPL"], START, END)

    assert prices.index.min() >= pd.Timestamp(START)
    assert prices.index.max() < pd.Timestamp(END)


def test_repeated_calls_return_identical_data():
    first, _ = fetch_price_history(["AAPL"], START, END)
    second, _ = fetch_price_history(["AAPL"], START, END)

    pd.testing.assert_frame_equal(first, second)
