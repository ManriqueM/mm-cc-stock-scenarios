import numpy as np
import pandas as pd
import pytest

from entry_timing import horizon_has_sufficient_history, lump_sum_value_series
from metrics import max_drawdown
from stress_tests import Scenario, scenario_value_series, scenario_window_end


def test_scenario_window_end_adds_recovery_years():
    scenario = Scenario("Fake crash", pd.Timestamp("2010-01-01"), pd.Timestamp("2010-06-01"), recovery_years=2)
    today = pd.Timestamp("2030-01-01")

    end = scenario_window_end(scenario, today)

    assert end == pd.Timestamp("2012-06-01")


def test_scenario_window_end_caps_at_today():
    scenario = Scenario("Recent crash", pd.Timestamp("2024-01-01"), pd.Timestamp("2024-06-01"), recovery_years=2)
    today = pd.Timestamp("2025-01-01")

    end = scenario_window_end(scenario, today)

    assert end == today


def test_scenario_value_series_matches_lump_sum_on_sliced_window():
    index = pd.date_range("2010-01-01", periods=10, freq="D")
    prices = pd.DataFrame(
        {"A": np.linspace(100, 50, 10), "B": np.linspace(50, 80, 10)}, index=index
    )
    weights = pd.Series({"A": 70.0, "B": 30.0})
    scenario = Scenario("Fake crash", index[2], index[5], recovery_years=0)
    today = index[-1]

    series = scenario_value_series(prices, weights, scenario, today, total_investment=1000.0)

    window_end = scenario_window_end(scenario, today)
    expected_window = prices.loc[scenario.peak : window_end]
    expected = lump_sum_value_series(expected_window, weights, 1000.0)

    pd.testing.assert_series_equal(series, expected)


def test_scenario_value_series_max_drawdown_matches_known_dip():
    index = pd.date_range("2020-01-01", periods=6, freq="D")
    prices = pd.DataFrame({"A": [100.0, 90.0, 60.0, 70.0, 95.0, 100.0]}, index=index)
    weights = pd.Series({"A": 100.0})
    scenario = Scenario("Fake crash", index[0], index[2], recovery_years=0)
    today = index[-1]

    series = scenario_value_series(prices, weights, scenario, today, total_investment=1000.0)
    dd = max_drawdown(series)

    assert dd == pytest.approx((60.0 - 100.0) / 100.0)


def test_insufficient_history_is_detected_for_scenario_peak():
    index = pd.date_range("2000-01-01", periods=5, freq="YS")
    prices = pd.DataFrame(
        {"OLD": [1.0, 2.0, 3.0, 4.0, 5.0], "NEW": [np.nan, np.nan, 3.0, 4.0, 5.0]},
        index=index,
    )
    scenario = Scenario("Fake crash", index[0], index[2])

    assert horizon_has_sufficient_history(prices, scenario.peak) is False

    later_scenario = Scenario("Later crash", index[2], index[4])
    assert horizon_has_sufficient_history(prices, later_scenario.peak) is True
