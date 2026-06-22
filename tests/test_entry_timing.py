import numpy as np
import pandas as pd
import pytest

from entry_timing import (
    dca_value_series,
    horizon_has_sufficient_history,
    lump_sum_value_series,
    monthly_investment_dates,
)


def test_lump_sum_value_series_matches_hand_computed():
    prices = pd.DataFrame(
        {"A": [100.0, 110.0, 120.0], "B": [50.0, 55.0, 45.0]},
        index=pd.date_range("2024-01-01", periods=3, freq="D"),
    )
    weights = pd.Series({"A": 60.0, "B": 40.0})

    series = lump_sum_value_series(prices, weights, total_investment=1000.0)

    shares_a = 600.0 / 100.0
    shares_b = 400.0 / 50.0
    expected = [
        shares_a * 100.0 + shares_b * 50.0,
        shares_a * 110.0 + shares_b * 55.0,
        shares_a * 120.0 + shares_b * 45.0,
    ]
    np.testing.assert_allclose(series.to_numpy(), expected)


def test_lump_sum_single_ticker():
    prices = pd.DataFrame(
        {"A": [100.0, 200.0]}, index=pd.date_range("2024-01-01", periods=2, freq="D")
    )
    weights = pd.Series({"A": 100.0})

    series = lump_sum_value_series(prices, weights, total_investment=500.0)

    np.testing.assert_allclose(series.to_numpy(), [500.0, 1000.0])


def test_monthly_investment_dates_one_per_month():
    index = pd.date_range("2024-01-01", "2024-03-31", freq="B")

    dates = monthly_investment_dates(index)

    assert len(dates) == 3
    assert all(d in index for d in dates)
    months = {(d.year, d.month) for d in dates}
    assert months == {(2024, 1), (2024, 2), (2024, 3)}
    for d in dates:
        month_start = index[(index.year == d.year) & (index.month == d.month)].min()
        assert d == month_start


def test_dca_value_series_invests_total_amount():
    index = pd.date_range("2024-01-01", "2024-03-31", freq="B")
    prices = pd.DataFrame({"A": np.linspace(100, 130, len(index))}, index=index)
    weights = pd.Series({"A": 100.0})

    series = dca_value_series(prices, weights, total_investment=900.0)

    install_dates = monthly_investment_dates(index)
    installment = 900.0 / len(install_dates)
    expected_shares = sum(installment / prices.loc[d, "A"] for d in install_dates)
    expected_ending_value = expected_shares * prices["A"].iloc[-1]

    assert series.iloc[-1] == pytest.approx(expected_ending_value)


def test_dca_value_series_zero_before_first_installment():
    index = pd.date_range("2024-01-02", "2024-01-31", freq="B")
    prices = pd.DataFrame({"A": np.linspace(100, 110, len(index))}, index=index)
    weights = pd.Series({"A": 100.0})

    series = dca_value_series(prices, weights, total_investment=1000.0)

    first_install_date = monthly_investment_dates(index)[0]
    before = series.loc[series.index < first_install_date]
    assert (before == 0).all()


def test_horizon_has_sufficient_history():
    index = pd.date_range("2020-01-01", periods=5, freq="YS")
    prices = pd.DataFrame(
        {"OLD": [1.0, 2.0, 3.0, 4.0, 5.0], "NEW": [np.nan, np.nan, 3.0, 4.0, 5.0]},
        index=index,
    )

    assert horizon_has_sufficient_history(prices, index[0]) is False
    assert horizon_has_sufficient_history(prices, index[2]) is True
