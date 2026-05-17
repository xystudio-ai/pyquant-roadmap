from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from lib.data.cache import save_parquet
from lib.data.schema import normalize_ohlcv
from lib.paths import SAMPLE_DIR


AKSHARE_ETF_COLUMN_MAP = {
    "日期": "date",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "成交量": "volume",
    "成交额": "amount",
}


@dataclass(frozen=True)
class EtfSymbol:
    code: str
    name: str


DEFAULT_ETF_UNIVERSE = [
    EtfSymbol("510300", "沪深300ETF"),
    EtfSymbol("510500", "中证500ETF"),
    EtfSymbol("159915", "创业板ETF"),
    EtfSymbol("512100", "中证1000ETF"),
]


def fetch_akshare_etf_daily(
    symbol: str,
    start_date: str,
    end_date: str,
    adjust: str = "qfq",
) -> pd.DataFrame:
    """Fetch one ETF's daily OHLCV data from AKShare and normalize fields."""
    try:
        import akshare as ak
    except ImportError as exc:
        raise RuntimeError("AKShare is not installed. Install akshare or update the project environment.") from exc

    raw = ak.fund_etf_hist_em(
        symbol=symbol,
        period="daily",
        start_date=start_date.replace("-", ""),
        end_date=end_date.replace("-", ""),
        adjust=adjust,
    )
    if raw.empty:
        raise ValueError(f"AKShare returned no ETF daily data for {symbol}")
    raw = raw.assign(code=symbol)
    return normalize_ohlcv(raw, column_map=AKSHARE_ETF_COLUMN_MAP)


def fetch_akshare_etf_pool(
    symbols: list[EtfSymbol] | None = None,
    start_date: str = "2021-01-01",
    end_date: str = "2023-12-31",
    adjust: str = "qfq",
) -> pd.DataFrame:
    """Fetch a small ETF universe from AKShare for the tutorial mainline."""
    symbols = symbols or DEFAULT_ETF_UNIVERSE
    frames = []
    for item in symbols:
        frames.append(fetch_akshare_etf_daily(item.code, start_date, end_date, adjust=adjust))
    prices = pd.concat(frames, ignore_index=True).sort_values(["date", "code"]).reset_index(drop=True)

    # Keep only dates shared by the full ETF universe. This makes the tutorial
    # matrix examples and bt backtests deterministic and free of missing prices.
    common_dates = None
    for code, group in prices.groupby("code"):
        dates = set(pd.to_datetime(group["date"]))
        common_dates = dates if common_dates is None else common_dates & dates
    if not common_dates:
        raise ValueError("no common trading dates found across ETF universe")
    prices = prices[prices["date"].isin(sorted(common_dates))]
    return prices.sort_values(["date", "code"]).reset_index(drop=True)


def build_asset_metadata(symbols: list[EtfSymbol] | None = None) -> pd.DataFrame:
    symbols = symbols or DEFAULT_ETF_UNIVERSE
    return pd.DataFrame(
        {
            "code": [item.code for item in symbols],
            "name": [item.name for item in symbols],
            "asset_type": ["ETF"] * len(symbols),
            "list_date": [pd.Timestamp("2000-01-01")] * len(symbols),
        }
    )


def build_calendar_from_prices(prices: pd.DataFrame) -> pd.DataFrame:
    dates = pd.Series(pd.to_datetime(prices["date"].unique())).sort_values()
    return pd.DataFrame({"date": dates, "is_open": 1})


def save_market_dataset(
    prices: pd.DataFrame,
    assets: pd.DataFrame,
    output_dir: str | Path = SAMPLE_DIR,
) -> dict[str, Path]:
    """Save normalized prices, calendar, and asset metadata as parquet files."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    calendar = build_calendar_from_prices(prices)
    return {
        "prices": save_parquet(prices, output / "prices.parquet"),
        "calendar": save_parquet(calendar, output / "calendar.parquet"),
        "assets": save_parquet(assets, output / "assets.parquet"),
    }


def fetch_and_save_akshare_etf_dataset(
    symbols: list[EtfSymbol] | None = None,
    start_date: str = "2021-01-01",
    end_date: str = "2023-12-31",
    output_dir: str | Path = SAMPLE_DIR,
    adjust: str = "qfq",
) -> dict[str, object]:
    """Fetch the tutorial ETF dataset from AKShare and cache it locally."""
    symbols = symbols or DEFAULT_ETF_UNIVERSE
    prices = fetch_akshare_etf_pool(symbols, start_date=start_date, end_date=end_date, adjust=adjust)
    assets = build_asset_metadata(symbols)
    paths = save_market_dataset(prices, assets, output_dir=output_dir)
    return {"prices": prices, "assets": assets, "paths": paths}
