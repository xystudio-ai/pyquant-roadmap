from __future__ import annotations

import pandas as pd


def top_n_equal_weight(scores: pd.DataFrame, n: int = 3, score_col: str = "score") -> pd.DataFrame:
    if n <= 0:
        raise ValueError("n must be positive")
    rows = []
    for dt, group in scores.dropna(subset=[score_col]).groupby("date"):
        top = group.sort_values(score_col, ascending=False).head(n)
        if top.empty:
            continue
        weight = 1.0 / len(top)
        rows.append(pd.DataFrame({"date": dt, "code": top["code"].to_numpy(), "weight": weight}))
    if not rows:
        return pd.DataFrame(columns=["date", "code", "weight"])
    return pd.concat(rows, ignore_index=True).sort_values(["date", "code"]).reset_index(drop=True)


def weights_to_matrix(
    weights: pd.DataFrame,
    index: pd.Index,
    columns: pd.Index,
    carry_forward: bool = False,
) -> pd.DataFrame:
    matrix = weights.pivot(index="date", columns="code", values="weight")
    matrix = matrix.reindex(columns=columns).fillna(0.0)
    matrix = matrix.reindex(index=index)
    if carry_forward:
        matrix = matrix.ffill()
    return matrix.fillna(0.0)


def calculate_turnover(weight_matrix: pd.DataFrame) -> pd.Series:
    turnover = weight_matrix.diff().abs().sum(axis=1)
    if not turnover.empty:
        turnover.iloc[0] = weight_matrix.iloc[0].abs().sum()
    return turnover.fillna(0.0)
