import numpy as np
import pandas as pd
import pytest

from metrics import (
    annualized_return,
    annualized_volatility,
    compute_metrics_table,
    compute_portfolio_metrics,
    correlation_matrix,
    daily_returns,
    max_drawdown,
    sharpe_ratio,
    weighted_portfolio_returns,
)


def test_daily_returns_matches_pct_change():
    prices = pd.DataFrame({"A": [100.0, 110.0, 99.0]})
    returns = daily_returns(prices)

    assert len(returns) == 2
    assert returns["A"].iloc[0] == pytest.approx(0.10)
    assert returns["A"].iloc[1] == pytest.approx(-0.10)


def test_annualized_return_and_volatility():
    returns = pd.Series([0.01, -0.01, 0.01, -0.01])

    assert annualized_return(returns, periods_per_year=252) == pytest.approx(
        returns.mean() * 252
    )
    assert annualized_volatility(returns, periods_per_year=252) == pytest.approx(
        returns.std() * np.sqrt(252)
    )


def test_sharpe_ratio_matches_return_over_volatility():
    returns = pd.Series([0.02, 0.01, -0.01, 0.03, -0.02])

    expected = annualized_return(returns) / annualized_volatility(returns)
    assert sharpe_ratio(returns) == pytest.approx(expected)


def test_sharpe_ratio_is_nan_when_volatility_is_zero():
    returns = pd.Series([0.0, 0.0, 0.0])

    assert np.isnan(sharpe_ratio(returns))


def test_max_drawdown_identifies_known_trough():
    prices = pd.Series([100.0, 120.0, 60.0, 90.0])

    assert max_drawdown(prices) == pytest.approx((60.0 - 120.0) / 120.0)


def test_weighted_portfolio_returns_combines_assets():
    returns = pd.DataFrame({"A": [0.10, 0.0], "B": [0.0, 0.10]})
    weights = pd.Series({"A": 50.0, "B": 50.0})

    portfolio_returns = weighted_portfolio_returns(returns, weights)

    assert portfolio_returns.iloc[0] == pytest.approx(0.05)
    assert portfolio_returns.iloc[1] == pytest.approx(0.05)


def test_correlation_matrix_perfectly_correlated_series():
    returns = pd.DataFrame({"A": [0.01, 0.02, -0.01], "B": [0.02, 0.04, -0.02]})

    corr = correlation_matrix(returns)

    assert corr.loc["A", "A"] == pytest.approx(1.0)
    assert corr.loc["A", "B"] == pytest.approx(1.0)


def test_correlation_matrix_single_ticker_is_one_by_one():
    returns = pd.DataFrame({"A": [0.01, 0.02, -0.01]})

    corr = correlation_matrix(returns)

    assert corr.shape == (1, 1)
    assert corr.loc["A", "A"] == pytest.approx(1.0)


def test_compute_metrics_table_returns_expected_columns():
    prices = pd.DataFrame(
        {
            "A": [100.0, 101.0, 102.0, 101.0, 103.0],
            "B": [50.0, 49.0, 51.0, 52.0, 50.0],
        }
    )

    table = compute_metrics_table(prices)

    assert set(table["ticker"]) == {"A", "B"}
    assert list(table.columns) == [
        "ticker",
        "annualized_return",
        "annualized_volatility",
        "sharpe_ratio",
        "max_drawdown",
        "history_days",
    ]
    assert (table["history_days"] == 5).all()


def test_compute_portfolio_metrics_runs_end_to_end():
    prices = pd.DataFrame(
        {
            "A": [100.0, 101.0, 102.0, 101.0, 103.0],
            "B": [50.0, 49.0, 51.0, 52.0, 50.0],
        }
    )
    weights = pd.Series({"A": 60.0, "B": 40.0})

    result = compute_portfolio_metrics(prices, weights)

    assert set(result.keys()) == {
        "annualized_return",
        "annualized_volatility",
        "sharpe_ratio",
        "max_drawdown",
    }
    assert all(isinstance(v, float) for v in result.values())
