from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from lib.evaluation.metrics import perf_stats
from lib.evaluation.plots import plot_drawdown, plot_nav, plot_nav_comparison


def _metrics_to_markdown(metrics: pd.DataFrame) -> str:
    lines = ["| metric | value |", "|---|---:|"]
    for row in metrics.itertuples(index=False):
        lines.append(f"| {row.metric} | {row.value} |")
    return "\n".join(lines) + "\n"


def save_strategy_results(
    returns: pd.Series,
    nav: pd.Series,
    target_weights: pd.DataFrame,
    orders: pd.DataFrame,
    output_dir: str | Path,
    benchmark_returns: pd.Series | None = None,
) -> dict[str, Path]:
    """Save reusable tutorial outputs: charts, metrics, weights, and orders."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    stats = perf_stats(returns, benchmark_returns)
    metrics = pd.DataFrame([stats]).T.reset_index()
    metrics.columns = ["metric", "value"]

    nav_path = output / "nav_curve.png"
    dd_path = output / "drawdown_curve.png"
    benchmark_path = output / "benchmark_comparison.png"
    metrics_csv = output / "performance_metrics.csv"
    metrics_md = output / "performance_metrics.md"
    weights_csv = output / "target_weights.csv"
    orders_csv = output / "trade_orders.csv"

    fig, _ = plot_nav(nav, title="Strategy NAV")
    fig.savefig(nav_path, dpi=160)
    plt.close(fig)

    fig, _ = plot_drawdown(nav, title="Drawdown")
    fig.savefig(dd_path, dpi=160)
    plt.close(fig)

    metrics.to_csv(metrics_csv, index=False, encoding="utf-8-sig")
    metrics_md.write_text(_metrics_to_markdown(metrics), encoding="utf-8")
    target_weights.to_csv(weights_csv, index=False, encoding="utf-8-sig")
    orders.to_csv(orders_csv, index=False, encoding="utf-8-sig")

    paths = {
        "nav_curve": nav_path,
        "drawdown_curve": dd_path,
        "metrics_csv": metrics_csv,
        "metrics_md": metrics_md,
        "target_weights": weights_csv,
        "trade_orders": orders_csv,
    }
    if benchmark_returns is not None:
        benchmark_nav = (1.0 + benchmark_returns.dropna()).cumprod()
        benchmark_nav.name = benchmark_returns.name or "Benchmark"
        fig, _ = plot_nav_comparison(
            nav.rename(nav.name or "Strategy"),
            benchmark_nav,
            title="Strategy vs Benchmark NAV",
        )
        fig.savefig(benchmark_path, dpi=160)
        plt.close(fig)
        paths["benchmark_comparison"] = benchmark_path

    return paths
