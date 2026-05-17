from __future__ import annotations

from pathlib import Path

import pandas as pd

from lib.backtest.bt_adapter import returns_from_weights, run_bt_from_weights
from lib.data.sample import load_sample_assets, load_sample_prices
from lib.factors import build_technical_factor_panel, combine_score, zscore_by_date
from lib.paths import RESULTS_DIR
from lib.portfolio import top_n_equal_weight, weights_to_matrix
from lib.reporting.quantstats_report import generate_quantstats_report
from lib.reporting.results import save_strategy_results
from lib.trading.signals import latest_target_weights, target_weights_to_orders


def _price_matrix(prices: pd.DataFrame, value_col: str = "close") -> pd.DataFrame:
    return prices.pivot(index="date", columns="code", values=value_col).sort_index().astype(float).ffill().dropna()


def _period_end_trading_dates(dates: pd.Series, freq: str = "M") -> pd.Series:
    clean_dates = pd.Series(pd.to_datetime(dates.dropna().unique())).sort_values()
    try:
        periods = clean_dates.dt.to_period(freq)
    except ValueError as exc:
        raise ValueError(f"invalid rebalance_freq={freq!r}") from exc
    return clean_dates.groupby(periods).max()


def run_etf_strategy_pipeline(
    top_n: int = 3,
    cost_bps: float = 8.0,
    capital: float = 1_000_000,
    lot_size: int = 100,
    factor_weights: dict[str, float] | None = None,
    asset_type: str = "ETF",
    output_dir: str | Path = RESULTS_DIR,
    start_date: str | pd.Timestamp | None = None,
    end_date: str | pd.Timestamp | None = None,
    rebalance_freq: str = "M",
    current_positions: dict[str, int] | None = None,
) -> dict[str, object]:
    prices = load_sample_prices()
    assets = load_sample_assets()
    etf_codes = assets.loc[assets["asset_type"].eq(asset_type), "code"].astype(str).tolist()
    if not etf_codes:
        raise ValueError(f"no assets found for asset_type={asset_type!r}")
    prices = prices[prices["code"].isin(etf_codes)].copy()
    prices["date"] = pd.to_datetime(prices["date"])
    if prices.empty:
        raise ValueError(f"no price rows found for asset_type={asset_type!r}")

    factor_cols = ["momentum_60", "low_vol_20", "ma_gap_20_60"]
    factor_weights = factor_weights or {"momentum_60": 0.45, "low_vol_20": 0.35, "ma_gap_20_60": 0.20}
    factors = build_technical_factor_panel(prices, etf_codes)
    if start_date is not None:
        start = pd.Timestamp(start_date)
        prices = prices[prices["date"].ge(start)]
        factors = factors[factors["date"].ge(start)]
    if end_date is not None:
        end = pd.Timestamp(end_date)
        prices = prices[prices["date"].le(end)]
        factors = factors[factors["date"].le(end)]
    if prices.empty:
        raise ValueError("no price rows found after applying start_date/end_date")
    if factors.empty:
        raise ValueError("factor panel is empty; check sample data length and factor windows")
    close = _price_matrix(prices, "close")
    scored = combine_score(
        zscore_by_date(factors, factor_cols),
        factor_weights,
    )
    rebalance_dates = _period_end_trading_dates(scored["date"], rebalance_freq)
    rebalance_scores = scored[scored["date"].isin(rebalance_dates)]
    sparse_weights = top_n_equal_weight(rebalance_scores, n=top_n)
    target_weights = weights_to_matrix(sparse_weights, close.index, close.columns, carry_forward=True)
    bt_result = run_bt_from_weights(close, target_weights, name="etf_multi_factor")
    report = returns_from_weights(close, target_weights, cost_bps=cost_bps)

    benchmark_returns = close.iloc[:, 0].pct_change().fillna(0.0)
    orders = target_weights_to_orders(
        target_weights,
        close,
        capital=capital,
        current_positions=current_positions,
        lot_size=lot_size,
    )
    latest_weights = latest_target_weights(target_weights)
    latest_scores = scored.sort_values(["code", "date"]).groupby("code").tail(1)[["code", "score"]]
    latest_weights = latest_weights.merge(latest_scores, on="code", how="left")

    output = Path(output_dir)
    assets_paths = save_strategy_results(
        report["strategy_return"],
        report["nav"],
        latest_weights,
        orders,
        output,
        benchmark_returns=benchmark_returns,
    )
    html_path = generate_quantstats_report(
        report["strategy_return"],
        output / "quantstats_report.html",
        benchmark_returns=benchmark_returns,
    )
    factor_scores_path = output / "factor_scores.csv"
    returns_path = output / "strategy_returns.csv"
    scored.to_csv(factor_scores_path, index=False, encoding="utf-8-sig")
    report.to_csv(returns_path, index=True, index_label="date", encoding="utf-8-sig")
    assets_paths["quantstats_report"] = html_path
    assets_paths["factor_scores"] = factor_scores_path
    assets_paths["strategy_returns"] = returns_path

    return {
        "prices": prices,
        "factors": scored,
        "sparse_rebalance_weights": sparse_weights,
        "target_weights": target_weights,
        "latest_target_weights": latest_weights,
        "orders": orders,
        "report": report,
        "bt_result": bt_result,
        "assets": assets_paths,
    }
