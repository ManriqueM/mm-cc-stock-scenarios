import pandas as pd

HORIZONS_YEARS = (1, 3, 5, 10)


def horizon_has_sufficient_history(prices: pd.DataFrame, start: pd.Timestamp) -> bool:
    """True if every ticker column has price data reaching back to `start`."""
    return all(prices[ticker].first_valid_index() <= start for ticker in prices.columns)


def lump_sum_value_series(
    prices: pd.DataFrame, weights: pd.Series, total_investment: float = 10_000.0
) -> pd.Series:
    """Value over time of `total_investment` split by weight at the first row's prices."""
    aligned_weights = weights.reindex(prices.columns)
    first_prices = prices.iloc[0]
    shares = (total_investment * aligned_weights / 100) / first_prices
    return (prices * shares).sum(axis=1)


def monthly_investment_dates(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """The first trading day of each calendar month present in `index`."""
    series = pd.Series(index, index=index)
    return pd.DatetimeIndex(series.groupby(index.to_period("M")).first())


def dca_value_series(
    prices: pd.DataFrame, weights: pd.Series, total_investment: float = 10_000.0
) -> pd.Series:
    """Value over time of `total_investment` split into equal monthly installments."""
    aligned_weights = weights.reindex(prices.columns)
    install_dates = monthly_investment_dates(prices.index)
    installment = total_investment / len(install_dates)

    cumulative_shares = pd.Series(0.0, index=prices.columns)
    values = []
    install_set = set(install_dates)
    for current_date, row in prices.iterrows():
        if current_date in install_set:
            allocation = installment * aligned_weights / 100
            cumulative_shares = cumulative_shares + allocation / row
        values.append((cumulative_shares * row).sum())

    return pd.Series(values, index=prices.index)
