import numpy as np
import pytest

from simulation import compute_percentile_bands, simulate_portfolio_paths

HORIZON_DAYS = 50
N_PATHS = 200


def test_simulate_portfolio_paths_shape_and_starting_value():
    daily_returns = np.array([0.01, -0.01, 0.02, -0.02, 0.0])

    paths = simulate_portfolio_paths(
        daily_returns, horizon_days=HORIZON_DAYS, n_paths=N_PATHS, starting_value=10_000.0, seed=42
    )

    assert paths.shape == (N_PATHS, HORIZON_DAYS + 1)
    assert (paths[:, 0] == 10_000.0).all()


def test_zero_returns_keep_value_constant():
    daily_returns = np.array([0.0, 0.0, 0.0])

    paths = simulate_portfolio_paths(
        daily_returns, horizon_days=HORIZON_DAYS, n_paths=N_PATHS, starting_value=10_000.0, seed=1
    )

    assert np.allclose(paths, 10_000.0)


def test_same_seed_is_reproducible():
    daily_returns = np.array([0.01, -0.01, 0.02, -0.02, 0.0])

    first = simulate_portfolio_paths(
        daily_returns, horizon_days=HORIZON_DAYS, n_paths=N_PATHS, starting_value=10_000.0, seed=7
    )
    second = simulate_portfolio_paths(
        daily_returns, horizon_days=HORIZON_DAYS, n_paths=N_PATHS, starting_value=10_000.0, seed=7
    )

    assert np.array_equal(first, second)


def test_percentile_bands_are_ordered():
    daily_returns = np.array([0.02, -0.015, 0.03, -0.01, 0.0, 0.01])

    paths = simulate_portfolio_paths(
        daily_returns, horizon_days=HORIZON_DAYS, n_paths=N_PATHS, starting_value=10_000.0, seed=3
    )
    bands = compute_percentile_bands(paths)

    assert (bands["p10"] <= bands["p50"]).all()
    assert (bands["p50"] <= bands["p90"]).all()


def test_percentile_bands_ordered_for_zero_returns():
    daily_returns = np.array([0.0, 0.0])

    paths = simulate_portfolio_paths(
        daily_returns, horizon_days=HORIZON_DAYS, n_paths=N_PATHS, starting_value=10_000.0, seed=5
    )
    bands = compute_percentile_bands(paths)

    assert (bands["p10"] == bands["p50"]).all()
    assert (bands["p50"] == bands["p90"]).all()


def test_percentile_bands_column_names():
    daily_returns = np.array([0.01, -0.01])

    paths = simulate_portfolio_paths(daily_returns, horizon_days=5, n_paths=10, seed=9)
    bands = compute_percentile_bands(paths, percentiles=(5, 50, 95))

    assert list(bands.columns) == ["p5", "p50", "p95"]
    assert len(bands) == 6
