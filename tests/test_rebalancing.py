import numpy as np
import pandas as pd
import pytest

from entry_timing import lump_sum_value_series
from rebalancing import rebalance_dates, rebalanced_value_series


def test_rebalance_dates_quarterly():
    index = pd.date_range("2022-01-01", "2022-12-31", freq="B")

    dates = rebalance_dates(index, "quarterly")

    assert len(dates) == 4
    quarters = {(d.year, d.quarter) for d in dates}
    assert quarters == {(2022, 1), (2022, 2), (2022, 3), (2022, 4)}
    for d in dates:
        quarter_start = index[(index.year == d.year) & (index.quarter == d.quarter)].min()
        assert d == quarter_start


def test_rebalance_dates_annual():
    index = pd.date_range("2020-01-01", "2023-12-31", freq="B")

    dates = rebalance_dates(index, "annual")

    assert len(dates) == 4
    years = {d.year for d in dates}
    assert years == {2020, 2021, 2022, 2023}


def test_rebalanced_value_series_resets_to_target_weights():
    # One row per month, spanning Q1 (Jan-Mar) and Q2 (Apr-Jun); only the first
    # day of each quarter (Jan 1, Apr 1) should trigger a rebalance.
    index = pd.to_datetime(
        ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01", "2024-05-01", "2024-06-01"]
    )
    prices = pd.DataFrame(
        {"A": [100.0, 150.0, 200.0, 200.0, 300.0, 400.0], "B": [100.0] * 6}, index=index
    )
    weights = pd.Series({"A": 50.0, "B": 50.0})

    series = rebalanced_value_series(prices, weights, "quarterly", total_investment=1000.0)

    # After the Jan 1 rebalance: 5 shares of each.
    assert series.iloc[0] == pytest.approx(5.0 * 100.0 + 5.0 * 100.0)
    assert series.iloc[1] == pytest.approx(5.0 * 150.0 + 5.0 * 100.0)
    assert series.iloc[2] == pytest.approx(5.0 * 200.0 + 5.0 * 100.0)
    # Apr 1 rebalance resets to 3.75 shares of A, 7.5 shares of B.
    assert series.iloc[3] == pytest.approx(3.75 * 200.0 + 7.5 * 100.0)
    assert series.iloc[4] == pytest.approx(3.75 * 300.0 + 7.5 * 100.0)
    assert series.iloc[5] == pytest.approx(3.75 * 400.0 + 7.5 * 100.0)


def test_rebalancing_is_noop_for_single_ticker():
    index = pd.date_range("2022-01-01", "2023-12-31", freq="B")
    prices = pd.DataFrame({"A": np.linspace(100, 250, len(index))}, index=index)
    weights = pd.Series({"A": 100.0})

    buy_and_hold = lump_sum_value_series(prices, weights, total_investment=10_000.0)
    quarterly = rebalanced_value_series(prices, weights, "quarterly", total_investment=10_000.0)
    annual = rebalanced_value_series(prices, weights, "annual", total_investment=10_000.0)

    pd.testing.assert_series_equal(buy_and_hold, quarterly)
    pd.testing.assert_series_equal(buy_and_hold, annual)


def test_rebalancing_changes_outcome_for_diverging_assets():
    index = pd.date_range("2022-01-01", periods=3, freq="QS")
    prices = pd.DataFrame(
        {"A": [100.0, 300.0, 300.0], "B": [100.0, 100.0, 300.0]}, index=index
    )
    weights = pd.Series({"A": 50.0, "B": 50.0})

    buy_and_hold = lump_sum_value_series(prices, weights, total_investment=1000.0)
    quarterly = rebalanced_value_series(prices, weights, "quarterly", total_investment=1000.0)

    assert quarterly.iloc[-1] != pytest.approx(buy_and_hold.iloc[-1])
