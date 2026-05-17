from __future__ import annotations

import pandas as pd


def build_technical_factor_panel(prices: pd.DataFrame, codes: list[str] | None = None) -> pd.DataFrame:
    """Build a compact practical factor panel from OHLCV prices.

    The course shows the same formulas by hand inside notebooks. This function
    is the reusable version used by notebooks and the production-style pipeline.
    """
    try:
        from ta.trend import SMAIndicator
    except ImportError as exc:
        raise RuntimeError("ta is not installed. Install ta or update the project environment.") from exc

    work = prices.copy()
    work["date"] = pd.to_datetime(work["date"])
    work["code"] = work["code"].astype(str)
    if codes is not None:
        work = work[work["code"].isin(codes)]

    frames = []
    for code, group in work.sort_values(["code", "date"]).groupby("code"):
        g = group.copy()
        close = g["close"].astype(float)
        returns = close.pct_change()
        sma20 = SMAIndicator(close, window=20).sma_indicator()
        sma60 = SMAIndicator(close, window=60).sma_indicator()
        g["momentum_60"] = close.pct_change(60).shift(1)
        g["low_vol_20"] = -returns.rolling(20).std().shift(1)
        g["ma_gap_20_60"] = (sma20 / sma60 - 1.0).shift(1)
        frames.append(g[["date", "code", "momentum_60", "low_vol_20", "ma_gap_20_60"]])

    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return out.dropna().sort_values(["date", "code"]).reset_index(drop=True)


def zscore_by_date(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        grouped = out.groupby("date")[col]
        mean = grouped.transform("mean")
        std = grouped.transform(lambda s: s.std(ddof=0))
        out[f"{col}_z"] = ((out[col] - mean) / std.replace(0, pd.NA)).fillna(0.0)
    return out


def combine_score(df: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    out = df.copy()
    out["score"] = 0.0
    for col, weight in weights.items():
        use_col = f"{col}_z" if f"{col}_z" in out.columns else col
        out["score"] += out[use_col].fillna(0.0) * float(weight)
    return out
