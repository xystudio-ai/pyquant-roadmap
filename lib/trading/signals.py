from __future__ import annotations

import math

import pandas as pd


def latest_target_weights(weight_matrix: pd.DataFrame) -> pd.DataFrame:
    weights = weight_matrix.fillna(0.0)
    if weights.empty:
        return pd.DataFrame(columns=["date", "code", "target_weight"])
    last_date = weights.index.max()
    latest = weights.loc[last_date]
    out = latest[latest.abs() > 0].rename("target_weight").reset_index()
    out.columns = ["code", "target_weight"]
    out.insert(0, "date", last_date)
    return out.sort_values("code").reset_index(drop=True)


def target_weights_to_orders(
    weight_matrix: pd.DataFrame,
    price_matrix: pd.DataFrame,
    capital: float = 1_000_000,
    current_positions: dict[str, int] | None = None,
    lot_size: int = 100,
) -> pd.DataFrame:
    if capital <= 0:
        raise ValueError("capital must be positive")
    if lot_size <= 0:
        raise ValueError("lot_size must be positive")

    weights = weight_matrix.reindex(index=price_matrix.index, columns=price_matrix.columns).fillna(0.0)
    latest_date = weights.index.max()
    latest_weights = weights.loc[latest_date]
    latest_prices = price_matrix.loc[latest_date]
    current_positions = current_positions or {}

    rows = []
    for code in latest_prices.index:
        price = float(latest_prices[code])
        target_weight = float(latest_weights.get(code, 0.0))
        current_shares = int(current_positions.get(code, 0))
        target_value = capital * target_weight
        target_shares = int(math.floor(target_value / price / lot_size) * lot_size) if price > 0 else 0
        order_shares = target_shares - current_shares
        side = "BUY" if order_shares > 0 else "SELL" if order_shares < 0 else "HOLD"
        current_weight = current_shares * price / capital
        rows.append(
            {
                "signal_date": latest_date,
                "code": code,
                "side": side,
                "price": price,
                "target_weight": target_weight,
                "current_weight": current_weight,
                "delta_weight": target_weight - current_weight,
                "target_shares": target_shares,
                "current_shares": current_shares,
                "order_shares": order_shares,
                "order_value": order_shares * price,
            }
        )
    out = pd.DataFrame(rows)
    return out[out["side"] != "HOLD"].sort_values(["side", "code"]).reset_index(drop=True)

