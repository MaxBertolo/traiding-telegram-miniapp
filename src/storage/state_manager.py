from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List
import json

@dataclass
class Position:
    ticker: str
    quantity: float
    avg_price: float

@dataclass
class PortfolioState:
    cash: float
    positions: Dict[str, Position]
    last_value: float

    def total_value(self) -> float:
        return self.cash + sum(
            p.quantity * p.avg_price for p in self.positions.values()
        )

    def tickers(self) -> List[str]:
        return list(self.positions.keys())

def load_portfolio_state(path: Path, start_cash: float, start_date: str) -> PortfolioState:
    if not path.exists():
        return PortfolioState(
            cash=start_cash,
            positions={},
            last_value=start_cash,
        )
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    positions = {t: Position(**p) for t, p in raw.get("positions", {}).items()}
    return PortfolioState(
        cash=raw.get("cash", start_cash),
        positions=positions,
        last_value=raw.get("last_value", start_cash),
    )

def save_portfolio_state(path: Path, state: PortfolioState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = {
        "cash": state.cash,
        "last_value": state.last_value,
        "positions": {t: asdict(p) for t, p in state.positions.items()},
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)
