# Mission

## What
An interactive full-stack app for analyzing historical S&P 500 / NYSE stock data and stress-testing real, multi-asset investment portfolios.

## Why
To support actual investment decisions with transparent, explicit assumptions and limitations — not a black-box robo-advisor. Users should be able to see exactly what data and assumptions drive every projection.

## Who
- Individual investors evaluating their own real portfolios.
- The app is deployed and shared with others (not just a personal local tool), so it should be approachable for non-technical users.

## Core capabilities
- Build a multi-asset portfolio (tickers + weights), via manual entry or upload.
- Explore historical return/risk metrics (returns, volatility, Sharpe, drawdown, correlation).
- Run forward-looking scenario analysis:
  - Monte Carlo return projections
  - Entry-timing comparisons (lump sum vs. DCA, different historical start dates)
  - Drawdown stress tests against historical crashes (2008, 2020, dot-com, etc.)
  - Rebalancing rule simulations (e.g., quarterly/annual vs. buy-and-hold)
- Surface all assumptions and limitations explicitly alongside every result, not buried in footnotes.
