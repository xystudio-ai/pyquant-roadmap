from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import pandas as pd


PRICE_COLUMNS = ["date", "code", "open", "high", "low", "close", "volume", "amount"]
NUMERIC_PRICE_COLUMNS = ["open", "high", "low", "close", "volume", "amount"]


@dataclass(frozen=True)
class AlignedMarketData:
    prices: pd.DataFrame
    close: pd.DataFrame
    volume: pd.DataFrame
    returns: pd.DataFrame
    quality: pd.DataFrame


def clean_price_data(prices: pd.DataFrame) -> pd.DataFrame:
    """Normalize dtypes, remove duplicate date/code rows, and sort an OHLCV panel."""
    missing = [col for col in PRICE_COLUMNS if col not in prices.columns]
    if missing:
        raise ValueError(f"missing price columns: {missing}")

    out = prices.copy()
    out["_row_order"] = range(len(out))
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out = out.dropna(subset=["date", "code"])
    out["code"] = out["code"].astype(str)
    for col in NUMERIC_PRICE_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out.sort_values(["date", "code", "_row_order"])
    out = out.drop_duplicates(["date", "code"], keep="last")
    out = out.drop(columns="_row_order")
    return out.sort_values(["date", "code"]).reset_index(drop=True)


def open_trading_dates(calendar: pd.DataFrame) -> pd.DatetimeIndex:
    """Return sorted open dates from a calendar table with date and optional is_open."""
    if "date" not in calendar.columns:
        raise ValueError("calendar must contain a date column")

    out = calendar.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    if "is_open" in out.columns:
        out = out[out["is_open"].eq(1)]
    dates = pd.DatetimeIndex(out["date"].dropna().drop_duplicates())
    return dates.sort_values()


def align_to_common_dates(
    prices: pd.DataFrame,
    calendar: pd.DataFrame | None = None,
    codes: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Keep only open dates where every requested code has one price row."""
    clean = clean_price_data(prices)
    code_order = [str(code) for code in codes] if codes is not None else sorted(clean["code"].unique())
    if not code_order:
        return clean.iloc[0:0].copy()

    work = clean[clean["code"].isin(code_order)].copy()
    missing_codes = sorted(set(code_order) - set(work["code"].unique()))
    if missing_codes:
        raise ValueError(f"codes not found in prices: {missing_codes}")

    if calendar is not None:
        dates = open_trading_dates(calendar)
        work = work[work["date"].isin(dates)]

    counts = work.groupby("date")["code"].nunique()
    common_dates = counts[counts.eq(len(code_order))].index
    out = work[work["date"].isin(common_dates)].copy()
    return out.sort_values(["date", "code"]).reset_index(drop=True)


def make_value_matrix(
    prices: pd.DataFrame,
    value_col: str,
    codes: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Pivot a long date/code price table into a date by code matrix."""
    if value_col not in prices.columns:
        raise ValueError(f"{value_col!r} is not a column in prices")

    work = clean_price_data(prices)
    code_order = [str(code) for code in codes] if codes is not None else sorted(work["code"].unique())
    matrix = work.pivot(index="date", columns="code", values=value_col).sort_index()
    return matrix.reindex(columns=code_order).astype(float)


def compute_simple_returns(close: pd.DataFrame, fill_initial: bool = True) -> pd.DataFrame:
    """Compute close-to-close simple returns while leaving internal gaps visible."""
    returns = close.astype(float).pct_change(fill_method=None)
    if fill_initial and not returns.empty:
        returns.iloc[0] = returns.iloc[0].fillna(0.0)
    return returns


def missing_value_report(
    prices: pd.DataFrame,
    columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Summarize date coverage and missing values by asset code."""
    work = clean_price_data(prices)
    value_cols = list(columns) if columns is not None else NUMERIC_PRICE_COLUMNS
    rows = []
    for code, group in work.groupby("code"):
        row = {
            "code": code,
            "start": group["date"].min(),
            "end": group["date"].max(),
            "rows": int(len(group)),
        }
        for col in value_cols:
            if col in group.columns:
                row[f"{col}_na"] = int(group[col].isna().sum())
        rows.append(row)
    return pd.DataFrame(rows)


def build_aligned_market_data(
    prices: pd.DataFrame,
    calendar: pd.DataFrame | None = None,
    codes: Sequence[str] | None = None,
    fill_initial_return: bool = True,
) -> AlignedMarketData:
    """Build aligned long prices, close matrix, volume matrix, and simple returns."""
    clean = clean_price_data(prices)
    code_order = [str(code) for code in codes] if codes is not None else sorted(clean["code"].unique())
    aligned = align_to_common_dates(clean, calendar=calendar, codes=code_order)
    close = make_value_matrix(aligned, "close", codes=code_order)
    volume = make_value_matrix(aligned, "volume", codes=code_order)
    returns = compute_simple_returns(close, fill_initial=fill_initial_return)
    quality = missing_value_report(aligned)
    return AlignedMarketData(
        prices=aligned,
        close=close,
        volume=volume,
        returns=returns,
        quality=quality,
    )
