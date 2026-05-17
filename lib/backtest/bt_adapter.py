from __future__ import annotations

import pandas as pd


def run_bt_from_weights(price: pd.DataFrame, target_weights: pd.DataFrame, name: str = "strategy"):
    """Run the same target-weight strategy with bt.

    The dependency is optional at runtime so notebooks can explain the fallback clearly.
    """
    try:
        import bt
    except ImportError as exc:
        raise RuntimeError("bt is not installed. Install it or use the vector backtest.") from exc

    weights = target_weights.reindex(index=price.index, columns=price.columns).fillna(0.0)
    strategy = bt.Strategy(
        name,
        [
            bt.algos.RunDaily(),
            bt.algos.SelectAll(),
            bt.algos.WeighTarget(weights),
            bt.algos.Rebalance(),
        ],
    )
    return bt.run(bt.Backtest(strategy, price))


def returns_from_weights(price: pd.DataFrame, target_weights: pd.DataFrame, cost_bps: float = 8.0) -> pd.DataFrame:
    """Deterministic return series for reporting and signal checks.

    bt is used as the practical backtest framework, while this small helper
    creates transparent returns and cost series for report assets.
    """
    returns = price.pct_change().fillna(0.0)
    weights = target_weights.reindex(index=price.index, columns=price.columns).fillna(0.0)
    positions = weights.shift(1).fillna(0.0)
    gross = (positions * returns).sum(axis=1)
    turnover = weights.diff().abs().sum(axis=1)
    if not turnover.empty:
        turnover.iloc[0] = weights.iloc[0].abs().sum()
    cost = turnover.fillna(0.0) * cost_bps / 10000.0
    net = gross - cost
    nav = (1.0 + net).cumprod()
    return pd.DataFrame(
        {
            "gross_return": gross,
            "cost": cost,
            "strategy_return": net,
            "nav": nav,
            "turnover": turnover.fillna(0.0),
        }
    )

