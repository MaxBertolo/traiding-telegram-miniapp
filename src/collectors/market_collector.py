from typing import Dict, Any, List

def collect_market_data(settings: Dict[str, Any], tickers_hint: List[str]) -> Dict[str, Dict[str, float]]:
    """
    MOCK: fake market data.
    """
    prices = {
        "NVDA": 130.0,
        "MSFT": 430.0,
        "COIN": 280.0,
    }
    result: Dict[str, Dict[str, float]] = {}
    for t, p in prices.items():
        result[t] = {
            "price": p,
            "change_1d": 0.02,   # +2%
            "volatility": 0.3,
        }
    return result
