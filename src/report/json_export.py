from pathlib import Path
from typing import Dict, Any

from ..storage.state_manager import PortfolioState
import json


def export_portfolio_json(
    output_path: Path,
    state_after: PortfolioState,
    scores: Dict[str, Dict[str, Any]],
    run_date: str,
) -> None:
    data = {
        "run_date": run_date,
        "cash": state_after.cash,
        "positions": [
            {
                "ticker": p.ticker,
                "quantity": p.quantity,
                "avg_price": p.avg_price,
            }
            for p in state_after.positions.values()
        ],
        # punteggio e rischio per ogni ticker
        "scores": scores,
    }
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
