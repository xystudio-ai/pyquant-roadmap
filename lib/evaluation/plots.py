from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from lib.evaluation.metrics import drawdown


def plot_nav(nav: pd.Series, title: str = "Strategy NAV"):
    fig, ax = plt.subplots(figsize=(9, 4))
    nav.plot(ax=ax)
    ax.set_title(title)
    ax.set_ylabel("NAV")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, ax


def plot_drawdown(nav: pd.Series, title: str = "Drawdown"):
    fig, ax = plt.subplots(figsize=(9, 3))
    drawdown(nav).plot(ax=ax, color="tab:red")
    ax.set_title(title)
    ax.set_ylabel("Drawdown")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, ax


def plot_nav_comparison(
    strategy_nav: pd.Series,
    benchmark_nav: pd.Series,
    title: str = "Strategy vs Benchmark NAV",
):
    strategy_name = strategy_nav.name or "Strategy"
    benchmark_name = benchmark_nav.name or "Benchmark"
    aligned = pd.concat(
        [
            strategy_nav.rename(strategy_name),
            benchmark_nav.rename(benchmark_name),
        ],
        axis=1,
    ).dropna()

    fig, ax = plt.subplots(figsize=(9, 4))
    aligned.plot(ax=ax)
    ax.set_title(title)
    ax.set_ylabel("NAV")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, ax
