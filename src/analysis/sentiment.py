from typing import List, Dict, Any

POSITIVE_WORDS = ["strong", "bullish", "growth", "winning", "positive"]
NEGATIVE_WORDS = ["fear", "uncertainty", "investigate", "regulatory"]

def simple_sentiment_score(text: str) -> float:
    text_lower = text.lower()
    score = 0
    for w in POSITIVE_WORDS:
        if w in text_lower:
            score += 1
    for w in NEGATIVE_WORDS:
        if w in text_lower:
            score -= 1
    return max(-1.0, min(1.0, score / 3.0))

def compute_sentiment(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for it in items:
        field = it.get("text") or it.get("summary") or ""
        it["sentiment"] = simple_sentiment_score(field)
        # keep other fields as-is
    return items
