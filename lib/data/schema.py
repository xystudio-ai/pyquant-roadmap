from __future__ import annotations

import pandas as pd

OHLCV_COLUMNS = ["date", "code", "open", "high", "low", "close", "volume", "amount"]


def normalize_ohlcv(df: pd.DataFrame, column_map: dict[str, str] | None = None) -> pd.DataFrame:
    """Return a clean OHLCV table with standard columns."""
    out = df.rename(columns=column_map or {}).copy()
    missing = [c for c in OHLCV_COLUMNS if c not in out.columns]
    if missing:
        raise ValueError(f"missing OHLCV columns: {missing}")
    out = out[OHLCV_COLUMNS].copy()
    out["date"] = pd.to_datetime(out["date"])
    out["code"] = out["code"].astype(str)
    for col in ["open", "high", "low", "close", "volume", "amount"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.drop_duplicates(["date", "code"]).sort_values(["date", "code"])
    return out.reset_index(drop=True)

