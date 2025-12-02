from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

from ..storage import state_manager as sm

@dataclass
class Trade:
    ticker: str
    side: str   # "BUY" / "SELL"
    quantity: float
    price: float
    reason: str

def rebalance_portfolio(
    state: sm.PortfolioState,
    scores: Dict[str, Dict[str, Any]],
) -> Tuple[sm.PortfolioState, List[Trade], Dict[str, Dict[str, Any]]]:
    total_value = state.total_value()
    target_per_ticker = total_value * 0.3  # 30% each for top 3

    ranked = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    top = ranked[:3]

    trades: List[Trade] = []
    new_positions = dict(state.positions)
    cash = state.cash

    for s in top:
        if s["score"] <= 0:
            continue

        ticker = s["ticker"]
        price = s.get("price") or 100.0
        invest_amount = min(target_per_ticker, cash)
        if invest_amount <= 0:
            continue

        qty = invest_amount / price
        prev = new_positions.get(ticker)
        if prev:
            new_qty = prev.quantity + qty
            new_avg = ((prev.avg_price * prev.quantity) + invest_amount) / new_qty
        else:
            new_qty = qty
            new_avg = price

        new_positions[ticker] = sm.Position(
            ticker=ticker,
            quantity=new_qty,
            avg_price=new_avg,
        )
        cash -= invest_amount

        trades.append(
            Trade(
                ticker=ticker,
                side="BUY",
                quantity=qty,
                price=price,
                reason=s["reason"],
            )
        )

    new_state = sm.PortfolioState(
        cash=cash,
        positions=new_positions,
        last_value=total_value,
    )
    picked_scores = {s["ticker"]: s for s in top}
    return new_state, trades, picked_scores
