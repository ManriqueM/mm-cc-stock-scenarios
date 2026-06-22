import pandas as pd

_PERIOD_CODES = {"quarterly": "Q", "annual": "Y"}


def rebalance_dates(index: pd.DatetimeIndex, frequency: str) -> pd.DatetimeIndex:
    """The first trading day of each calendar quarter/year present in `index`."""
    period_code = _PERIOD_CODES[frequency]
    series = pd.Series(index, index=index)
    return pd.DatetimeIndex(series.groupby(index.to_period(period_code)).first())


def rebalanced_value_series(
    prices: pd.DataFrame, weights: pd.Series, frequency: str, total_investment: float = 10_000.0
) -> pd.Series:
    """Value over time of `total_investment`, reset to target weights at each rebalance date."""
    aligned_weights = weights.reindex(prices.columns)
    rebalance_set = set(rebalance_dates(prices.index, frequency))

    shares = (total_investment * aligned_weights / 100) / prices.iloc[0]

    values = []
    for current_date, row in prices.iterrows():
        if current_date in rebalance_set:
            current_value = (shares * row).sum()
            shares = (current_value * aligned_weights / 100) / row
        values.append((shares * row).sum())

    return pd.Series(values, index=prices.index)
