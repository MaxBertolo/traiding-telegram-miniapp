from typing import List, Dict, Any
from collections import defaultdict

def build_scores(
    social_signals: List[Dict[str, Any]],
    news_signals: List[Dict[str, Any]],
    market_data: Dict[str, Dict[str, float]],
) -> Dict[str, Dict[str, Any]]:
    agg = defaultdict(lambda: {"social": [], "news": []})

    for s in social_signals:
        agg[s["ticker"]]["social"].append(s)
    for n in news_signals:
        agg[n["ticker"]]["news"].append(n)

    results: Dict[str, Dict[str, Any]] = {}

    for ticker, groups in agg.items():
        social_sent = sum(i["sentiment"] for i in groups["social"]) / max(len(groups["social"]), 1)
        news_sent = sum(i["sentiment"] for i in groups["news"]) / max(len(groups["news"]), 1)
        market = market_data.get(ticker, {})

        change_1d = market.get("change_1d", 0.0)
        raw_score = 0.6 * ((social_sent + news_sent) / 2.0) + 0.4 * change_1d

        vol = market.get("volatility", 0.3)
        if vol < 0.2:
            risk = "Low"
        elif vol < 0.5:
            risk = "Medium"
        else:
            risk = "High"

        links = [i["url"] for i in groups["social"]] + [i["url"] for i in groups["news"]]
        reason = f"Social sentiment {social_sent:.2f}, news sentiment {news_sent:.2f}, daily change {change_1d:.2f}"

        results[ticker] = {
            "ticker": ticker,
            "score": raw_score,
            "risk": risk,
            "links": links,
            "reason": reason,
            "price": market.get("price"),
        }

    return results
