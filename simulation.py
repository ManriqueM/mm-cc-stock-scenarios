import numpy as np
import pandas as pd

DEFAULT_PERCENTILES = (10, 50, 90)


def simulate_portfolio_paths(
    daily_returns: np.ndarray,
    horizon_days: int,
    n_paths: int,
    starting_value: float = 10_000.0,
    seed: int | None = None,
) -> np.ndarray:
    """Bootstrap-simulate `n_paths` compounding portfolio value paths.

    Each simulated day independently resamples (with replacement) from
    `daily_returns`. Returns an array of shape `(n_paths, horizon_days + 1)`;
    column 0 is `starting_value` for every path.
    """
    rng = np.random.default_rng(seed)
    sampled_returns = rng.choice(daily_returns, size=(n_paths, horizon_days), replace=True)
    growth = np.cumprod(1 + sampled_returns, axis=1)
    values = starting_value * growth
    return np.hstack([np.full((n_paths, 1), starting_value), values])


def compute_percentile_bands(
    paths: np.ndarray, percentiles: tuple[float, ...] = DEFAULT_PERCENTILES
) -> pd.DataFrame:
    """Per-day percentiles across simulated `paths`, one column per percentile."""
    bands = np.percentile(paths, percentiles, axis=0)
    columns = [f"p{int(p)}" for p in percentiles]
    return pd.DataFrame(bands.T, columns=columns)
