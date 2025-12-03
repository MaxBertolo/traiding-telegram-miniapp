from pathlib import Path
from datetime import datetime
from shutil import copyfile

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


def run_weekly_analysis() -> None:
    # 1. Load settings
    settings = load_settings(BASE_DIR / "config" / "settings.yaml")

    # 2. Load or initialize portfolio state
    state = load_portfolio_state(
        DATA_DIR / "portfolio_state.json",
        start_cash=settings["start_cash"],
        start_date=settings["start_date"],
    )

    # 3. Collect raw signals
    social_raw = collect_social_signals(settings)
    news_raw = collect_news_signals(settings)
    market_data = collect_market_data(settings, tickers_hint=state.tickers())

    # 4. Compute sentiment
    social_signals = compute_sentiment(social_raw)
    news_signals = compute_sentiment(news_raw)

    # 5. Build scores by ticker
    scores = build_scores(social_signals, news_signals, market_data)

    # 6. Rebalance portfolio based on scores
    new_state, trades, picked_scores = rebalance_portfolio(state, scores)

    # 7. Build HTML report for today
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

    # 8. Also expose latest report as docs/latest.html for the mini-app
    latest_path = REPORTS_DIR / "latest.html"
    copyfile(report_path, latest_path)

    # 9. Persist new portfolio state
    save_portfolio_state(DATA_DIR / "portfolio_state.json", new_state)

    # 10. Notify via Telegram with links to mini-app and report
    send_telegram_notification(
        report_url_suffix=report_url_rel,
        state_after=new_state,
        trades=trades,
    )


if __name__ == "__main__":
    run_weekly_analysis()
