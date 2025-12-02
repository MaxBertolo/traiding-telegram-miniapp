from typing import List, Dict, Any

def collect_news_signals(settings: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    MOCK: fake news articles about some tickers.
    """
    return [
        {
            "source": "news",
            "ticker": "NVDA",
            "headline": "Nvidia reports strong data center revenue growth",
            "summary": "Data center and AI chip demand remain very strong.",
            "url": "https://example.com/nvda-news",
        },
        {
            "source": "news",
            "ticker": "MSFT",
            "headline": "Microsoft expands cloud AI offerings",
            "summary": "More investment in AI and cloud, positive for long term.",
            "url": "https://example.com/msft-news",
        },
        {
            "source": "news",
            "ticker": "COIN",
            "headline": "Regulators investigate crypto exchanges",
            "summary": "Short term uncertainty, long term adoption still debated.",
            "url": "https://example.com/coin-news",
        },
    ]
