from typing import List, Dict, Any

def collect_social_signals(settings: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    MOCK: fake social posts about some tickers.
    """
    return [
        {
            "source": "twitter",
            "author": "TopTrader",
            "ticker": "NVDA",
            "text": "NVDA still strong on AI chips, huge demand from data centers.",
            "url": "https://twitter.com/example/status/1",
        },
        {
            "source": "twitter",
            "author": "CryptoGuru",
            "ticker": "COIN",
            "text": "Regulatory fears but long term bullish on crypto infrastructure.",
            "url": "https://twitter.com/example/status/2",
        },
        {
            "source": "youtube",
            "author": "TechInvestor",
            "ticker": "MSFT",
            "text": "Microsoft keeps winning in cloud + AI, solid fundamentals.",
            "url": "https://youtube.com/watch?v=abc123",
        },
    ]
