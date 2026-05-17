from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


def _as_period_list(periods: int | Iterable[int]) -> list[int]:
    if isinstance(periods, int):
        out = [periods]
    else:
        out = list(periods)
    if not out:
        raise ValueError("periods must not be empty")
    if any(period <= 0 for period in out):
        raise ValueError("all forward-return periods must be positive")
    return sorted(set(int(period) for period in out))


def add_forward_returns(
    factor_df: pd.DataFrame,
    prices: pd.DataFrame,
    periods: int | Iterable[int] = 5,
    price_col: str = "close",
) -> pd.DataFrame:
    """Attach future close-to-close returns to a date/code factor panel."""
    period_list = _as_period_list(periods)

    close = prices.copy()
    close["date"] = pd.to_datetime(close["date"])
    close["code"] = close["code"].astype(str)
    close = close.pivot(index="date", columns="code", values=price_col).sort_index().astype(float)

    forward_frames = []
    for period in period_list:
        col = f"fwd_ret_{period}d"
        future_return = close.shift(-period) / close - 1.0
        stacked = (
            future_return.stack(future_stack=True)
            .rename(col)
            .rename_axis(index=["date", "code"])
            .reset_index()
        )
        forward_frames.append(stacked)

    forward = forward_frames[0]
    for frame in forward_frames[1:]:
        forward = forward.merge(frame, on=["date", "code"], how="outer")

    out = factor_df.copy()
    out["date"] = pd.to_datetime(out["date"])
    out["code"] = out["code"].astype(str)
    return out.merge(forward, on=["date", "code"], how="left")


def ic_by_date(
    df: pd.DataFrame,
    factor_cols: str | Iterable[str],
    return_col: str,
    method: str = "spearman",
    min_periods: int = 3,
) -> pd.DataFrame:
    """Calculate cross-sectional IC for each date and factor."""
    if isinstance(factor_cols, str):
        factors = [factor_cols]
    else:
        factors = list(factor_cols)
    if method not in {"spearman", "pearson", "kendall"}:
        raise ValueError("method must be one of: spearman, pearson, kendall")

    rows = []
    for date, group in df.groupby("date"):
        for factor in factors:
            valid = group[[factor, return_col]].dropna()
            n = len(valid)
            if n < min_periods:
                ic = np.nan
            else:
                ic = valid[factor].corr(valid[return_col], method=method)
            rows.append({"date": date, "factor": factor, "method": method, "ic": ic, "n": n})

    return (
        pd.DataFrame(rows, columns=["date", "factor", "method", "ic", "n"])
        .dropna(subset=["ic"])
        .sort_values(["factor", "date"])
        .reset_index(drop=True)
    )


def summarize_ic(ic: pd.DataFrame) -> pd.DataFrame:
    """Summarize an IC table returned by ``ic_by_date``."""
    rows = []
    for (factor, method), group in ic.dropna(subset=["ic"]).groupby(["factor", "method"]):
        values = group["ic"].astype(float)
        count = int(values.count())
        std = values.std(ddof=1) if count > 1 else np.nan
        t_stat = values.mean() / (std / np.sqrt(count)) if count > 1 and std and not np.isnan(std) else np.nan
        rows.append(
            {
                "factor": factor,
                "method": method,
                "ic_count": count,
                "ic_mean": values.mean(),
                "ic_std": std,
                "ic_t_stat": t_stat,
                "ic_positive_rate": (values > 0).mean(),
                "ic_abs_mean": values.abs().mean(),
                "avg_cross_section_n": group["n"].mean(),
            }
        )

    return pd.DataFrame(rows).sort_values(["method", "factor"]).reset_index(drop=True)


def layer_forward_returns(
    df: pd.DataFrame,
    factor_col: str,
    return_col: str,
    n_layers: int = 4,
) -> pd.DataFrame:
    """Assign same-date factor ranks to layers and average future returns."""
    if n_layers < 2:
        raise ValueError("n_layers must be at least 2")

    rows = []
    for date, group in df[["date", "code", factor_col, return_col]].dropna().groupby("date"):
        if len(group) < n_layers:
            continue
        ranked = group.copy()
        ranked["layer"] = pd.qcut(
            ranked[factor_col].rank(method="first"),
            q=n_layers,
            labels=range(1, n_layers + 1),
        ).astype(int)
        grouped = ranked.groupby("layer", observed=True)[return_col].agg(["mean", "count"]).reset_index()
        grouped["date"] = date
        grouped["factor"] = factor_col
        rows.append(grouped.rename(columns={"mean": "mean_forward_return", "count": "asset_count"}))

    if not rows:
        return pd.DataFrame(columns=["date", "factor", "layer", "mean_forward_return", "asset_count"])

    return (
        pd.concat(rows, ignore_index=True)[["date", "factor", "layer", "mean_forward_return", "asset_count"]]
        .sort_values(["factor", "date", "layer"])
        .reset_index(drop=True)
    )


def summarize_layer_returns(layer_returns: pd.DataFrame) -> pd.DataFrame:
    """Average layer returns by factor and layer."""
    if layer_returns.empty:
        return pd.DataFrame(columns=["factor", "layer", "mean_forward_return", "date_count", "avg_asset_count"])

    return (
        layer_returns.groupby(["factor", "layer"], as_index=False)
        .agg(
            mean_forward_return=("mean_forward_return", "mean"),
            date_count=("date", "nunique"),
            avg_asset_count=("asset_count", "mean"),
        )
        .sort_values(["factor", "layer"])
        .reset_index(drop=True)
    )
