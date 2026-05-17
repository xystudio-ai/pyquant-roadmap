from __future__ import annotations

import numpy as np
import pandas as pd


def drawdown(nav: pd.Series) -> pd.Series:
    return nav / nav.cummax() - 1.0


def _clean_returns(returns: pd.Series) -> pd.Series:
    return returns.dropna().astype(float)


def _total_return(returns: pd.Series) -> float:
    return float((1.0 + returns).prod() - 1.0)


def _annual_return(returns: pd.Series, periods_per_year: int) -> float:
    if returns.empty:
        return np.nan
    total_growth = float((1.0 + returns).prod())
    if total_growth < 0:
        return np.nan
    return float(total_growth ** (periods_per_year / len(returns)) - 1.0)


def _annual_volatility(returns: pd.Series, periods_per_year: int) -> float:
    return float(returns.std(ddof=0) * np.sqrt(periods_per_year))


def _annualized_ratio(returns: pd.Series, periods_per_year: int) -> float:
    std = returns.std(ddof=0)
    if std == 0 or np.isclose(std, 0):
        return np.nan
    return float(returns.mean() / std * np.sqrt(periods_per_year))


def perf_stats(returns: pd.Series, benchmark_returns: pd.Series | None = None, periods_per_year: int = 252) -> dict[str, float]:
    returns = _clean_returns(returns)
    if returns.empty:
        return {}
    nav = (1.0 + returns).cumprod()
    ann_return = _annual_return(returns, periods_per_year)
    ann_vol = _annual_volatility(returns, periods_per_year)
    sharpe = _annualized_ratio(returns, periods_per_year)
    stats = {
        "ann_return": float(ann_return),
        "ann_vol": float(ann_vol),
        "sharpe": float(sharpe) if pd.notna(sharpe) else np.nan,
        "max_drawdown": float(drawdown(nav).min()),
        "total_return": _total_return(returns),
        "win_rate": float(returns.gt(0).mean()),
    }
    if benchmark_returns is not None:
        aligned = pd.concat([returns, _clean_returns(benchmark_returns)], axis=1).dropna()
        aligned.columns = ["strategy", "benchmark"]
        if not aligned.empty:
            strategy = aligned["strategy"]
            benchmark = aligned["benchmark"]
            active = strategy - benchmark
            strategy_ann_return = _annual_return(strategy, periods_per_year)
            benchmark_ann_return = _annual_return(benchmark, periods_per_year)
            stats["benchmark_total_return"] = _total_return(benchmark)
            stats["benchmark_ann_return"] = benchmark_ann_return
            stats["excess_total_return"] = _total_return(strategy) - stats["benchmark_total_return"]
            stats["excess_ann_return"] = strategy_ann_return - benchmark_ann_return
            stats["active_return"] = _total_return(active)
            stats["tracking_error"] = _annual_volatility(active, periods_per_year)
            stats["information_ratio"] = _annualized_ratio(active, periods_per_year)
    return stats
