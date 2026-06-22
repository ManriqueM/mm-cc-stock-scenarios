from typing import NamedTuple

import pandas as pd

from entry_timing import lump_sum_value_series


class Scenario(NamedTuple):
    name: str
    peak: pd.Timestamp
    trough: pd.Timestamp
    recovery_years: int = 2


SCENARIOS: list[Scenario] = [
    Scenario("Dot-com crash", pd.Timestamp("2000-03-24"), pd.Timestamp("2002-10-09")),
    Scenario("2008 Global Financial Crisis", pd.Timestamp("2007-10-09"), pd.Timestamp("2009-03-09")),
    Scenario("2020 COVID crash", pd.Timestamp("2020-02-19"), pd.Timestamp("2020-03-23")),
]


def scenario_window_end(scenario: Scenario, today: pd.Timestamp) -> pd.Timestamp:
    return min(scenario.trough + pd.DateOffset(years=scenario.recovery_years), today)


def scenario_value_series(
    prices: pd.DataFrame,
    weights: pd.Series,
    scenario: Scenario,
    today: pd.Timestamp,
    total_investment: float = 10_000.0,
) -> pd.Series:
    """Value over time of a lump-sum invested at `scenario.peak`, through the scenario's window."""
    window = prices.loc[scenario.peak : scenario_window_end(scenario, today)]
    return lump_sum_value_series(window, weights, total_investment)
