import pandas as pd

from lib.paths import SAMPLE_DIR


def load_sample_prices() -> pd.DataFrame:
    """Load cached AKShare ETF OHLCV data for the tutorial mainline."""
    return pd.read_parquet(SAMPLE_DIR / "prices.parquet")


def load_sample_calendar() -> pd.DataFrame:
    return pd.read_parquet(SAMPLE_DIR / "calendar.parquet")


def load_sample_assets() -> pd.DataFrame:
    return pd.read_parquet(SAMPLE_DIR / "assets.parquet")
