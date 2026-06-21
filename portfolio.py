from datetime import date, timedelta

import pandas as pd

from data import fetch_price_history


def parse_portfolio_csv(file) -> pd.DataFrame:
    """Parse an uploaded CSV with `ticker` and `weight` columns (case-insensitive)."""
    df = pd.read_csv(file)
    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = {"ticker", "weight"} - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")

    return df[["ticker", "weight"]]


def validate_weights(weights: list[float], tolerance: float = 0.5) -> tuple[bool, float]:
    """Check that `weights` (in percent) sum to 100 within `tolerance` points."""
    total = sum(weights)
    return abs(total - 100) <= tolerance, total


def find_duplicate_tickers(tickers: list[str]) -> list[str]:
    """Return tickers (normalized) that appear more than once."""
    normalized = [t.strip().upper() for t in tickers if t.strip()]
    seen_once = set()
    duplicates = []
    for t in normalized:
        if t in seen_once and t not in duplicates:
            duplicates.append(t)
        seen_once.add(t)
    return duplicates


def build_portfolio(
    tickers: list[str], weights: list[float], lookback_days: int = 30
) -> tuple[pd.DataFrame | None, list[str]]:
    """Validate tickers + weights and assemble a portfolio.

    Returns `(portfolio_df, errors)`. `portfolio_df` has columns `ticker`,
    `weight` and is `None` if any errors were found.
    """
    errors: list[str] = []

    weights_ok, total = validate_weights(weights)
    if not weights_ok:
        errors.append(f"Weights must sum to 100% (currently {total:.2f}%).")

    duplicates = find_duplicate_tickers(tickers)
    if duplicates:
        errors.append(f"Duplicate ticker(s): {', '.join(duplicates)}.")

    if errors:
        return None, errors

    normalized_tickers = [t.strip().upper() for t in tickers]
    end = date.today()
    start = end - timedelta(days=lookback_days)
    _, invalid_tickers = fetch_price_history(normalized_tickers, start, end)
    if invalid_tickers:
        errors.append(f"Invalid ticker(s): {', '.join(invalid_tickers)}.")
        return None, errors

    portfolio = pd.DataFrame({"ticker": normalized_tickers, "weight": weights})
    return portfolio, []
