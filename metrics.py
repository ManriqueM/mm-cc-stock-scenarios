import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Simple daily percent-change returns per column, dropping the leading NaN row."""
    return prices.pct_change().dropna(how="all")


def annualized_return(returns: pd.Series, periods_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    return returns.mean() * periods_per_year


def annualized_volatility(returns: pd.Series, periods_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    return returns.std() * np.sqrt(periods_per_year)


def sharpe_ratio(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
    risk_free_rate: float = 0.0,
) -> float:
    """Annualized Sharpe ratio; `nan` if volatility is zero."""
    volatility = annualized_volatility(returns, periods_per_year)
    if volatility == 0:
        return float("nan")
    return (annualized_return(returns, periods_per_year) - risk_free_rate) / volatility


def max_drawdown(prices: pd.Series) -> float:
    """Largest peak-to-trough decline over the series, as a negative fraction."""
    running_max = prices.cummax()
    drawdown = (prices - running_max) / running_max
    return drawdown.min()


def weighted_portfolio_returns(returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Daily portfolio return series from per-asset returns and weights (0-100 scale)."""
    aligned_weights = weights.reindex(returns.columns)
    normalized = aligned_weights / 100
    return returns.mul(normalized, axis=1).sum(axis=1)


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()


def compute_metrics_table(prices: pd.DataFrame) -> pd.DataFrame:
    """Per-ticker headline metrics. `history_days` flags shorter-than-requested windows."""
    returns = daily_returns(prices)
    rows = []
    for ticker in prices.columns:
        ticker_prices = prices[ticker].dropna()
        ticker_returns = returns[ticker].dropna()
        rows.append(
            {
                "ticker": ticker,
                "annualized_return": annualized_return(ticker_returns),
                "annualized_volatility": annualized_volatility(ticker_returns),
                "sharpe_ratio": sharpe_ratio(ticker_returns),
                "max_drawdown": max_drawdown(ticker_prices),
                "history_days": len(ticker_prices),
            }
        )
    return pd.DataFrame(rows)


def compute_portfolio_metrics(prices: pd.DataFrame, weights: pd.Series) -> dict:
    """Headline portfolio-level metrics from the weighted daily return series."""
    returns = daily_returns(prices)
    portfolio_returns = weighted_portfolio_returns(returns, weights).dropna()
    portfolio_value = (1 + portfolio_returns).cumprod()
    return {
        "annualized_return": annualized_return(portfolio_returns),
        "annualized_volatility": annualized_volatility(portfolio_returns),
        "sharpe_ratio": sharpe_ratio(portfolio_returns),
        "max_drawdown": max_drawdown(portfolio_value),
    }
