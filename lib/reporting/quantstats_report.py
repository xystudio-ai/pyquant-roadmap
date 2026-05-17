from __future__ import annotations

from pathlib import Path

import pandas as pd


def generate_quantstats_report(
    returns: pd.Series,
    output_html: str | Path,
    benchmark_returns: pd.Series | None = None,
    title: str = "xyQuant ETF Strategy",
) -> Path:
    try:
        import quantstats as qs
    except ImportError as exc:
        raise RuntimeError("quantstats is not installed. Update the project environment.") from exc

    output = Path(output_html)
    output.parent.mkdir(parents=True, exist_ok=True)
    clean_returns = returns.dropna()
    clean_returns.index = pd.to_datetime(clean_returns.index)
    benchmark = None
    if benchmark_returns is not None:
        benchmark = benchmark_returns.dropna()
        benchmark.index = pd.to_datetime(benchmark.index)
    qs.reports.html(clean_returns, benchmark=benchmark, output=str(output), title=title)
    return output
