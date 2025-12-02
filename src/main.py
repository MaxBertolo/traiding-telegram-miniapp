from pathlib import Path
from datetime import datetime

from .config import load_settings
from .storage.state_manager import load_portfolio_state, save_portfolio_state
from .collectors.social_collector import collect_social_signals
from .collectors.news_collector import collect_news_signals
from .collectors.market_collector import collect_market_data
from .analysis.sentiment import compute_sentiment
from .analysis.scoring import build_scores
from .portfolio.portfolio_engine import rebalance_portfolio
from .report.html_report import build_html_report
from .telegram.bot import send_telegram_notification

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "docs"

def run_weekly_analysis():
    settings = load_settings(BASE_DIR / "config" / "settings.yaml")

    state = load_portfolio_state(
        DATA_DIR / "portfolio_state.json",
        start_cash=settings["start_cash"],
        start_date=settings["start_date"],
    )

    social_raw = collect_social_signals(settings)
    news_raw = collect_news_signals(settings)
    market_data = collect_market_data(settings, tickers_hint=state.tickers())

    social_signals = compute_sentiment(social_raw)
    news_signals = compute_sentiment(news_raw)

    scores = build_scores(social_signals, news_signals, market_data)

    new_state, trades, picked_scores = rebalance_portfolio(state, scores)

    today = datetime.utcnow().date().isoformat()
    report_path = REPORTS_DIR / f"report_{today}.html"
    report_url_rel = f"report_{today}.html"

    build_html_report(
        output_path=report_path,
        state_before=state,
        state_after=new_state,
        trades=trades,
        scores=picked_scores,
        run_date=today,
    )

    save_portfolio_state(DATA_DIR / "portfolio_state.json", new_state)

    send_telegram_notification(
        report_url_suffix=report_url_rel,
        state_after=new_state,
        trades=trades,
    )

if __name__ == "__main__":
    run_weekly_analysis()
