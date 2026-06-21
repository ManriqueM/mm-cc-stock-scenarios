from io import StringIO

import pytest

from portfolio import (
    build_portfolio,
    find_duplicate_tickers,
    parse_portfolio_csv,
    validate_weights,
)


def test_parse_portfolio_csv_valid():
    csv = StringIO("Ticker,Weight\nAAPL,50\nMSFT,50\n")

    df = parse_portfolio_csv(csv)

    assert list(df.columns) == ["ticker", "weight"]
    assert df["ticker"].tolist() == ["AAPL", "MSFT"]


def test_parse_portfolio_csv_missing_column():
    csv = StringIO("ticker,amount\nAAPL,50\n")

    with pytest.raises(ValueError, match="weight"):
        parse_portfolio_csv(csv)


def test_validate_weights_within_tolerance():
    is_valid, total = validate_weights([33.33, 33.33, 33.34])

    assert is_valid
    assert total == pytest.approx(100, abs=0.01)


def test_validate_weights_outside_tolerance():
    is_valid, total = validate_weights([50, 40])

    assert not is_valid
    assert total == 90


def test_find_duplicate_tickers_detects_case_insensitive_dupes():
    duplicates = find_duplicate_tickers(["AAPL", "aapl", "MSFT"])

    assert duplicates == ["AAPL"]


def test_find_duplicate_tickers_no_dupes():
    assert find_duplicate_tickers(["AAPL", "MSFT"]) == []


def test_build_portfolio_happy_path():
    portfolio, errors = build_portfolio(["AAPL", "MSFT", "SPY"], [40, 30, 30])

    assert errors == []
    assert portfolio is not None
    assert set(portfolio["ticker"]) == {"AAPL", "MSFT", "SPY"}


def test_build_portfolio_invalid_ticker():
    portfolio, errors = build_portfolio(["AAPL", "NOTAREALTICKERXYZ"], [50, 50])

    assert portfolio is None
    assert any("NOTAREALTICKERXYZ" in error for error in errors)


def test_build_portfolio_bad_weights_skips_network_call():
    portfolio, errors = build_portfolio(["AAPL", "MSFT"], [50, 40])

    assert portfolio is None
    assert any("100%" in error for error in errors)
