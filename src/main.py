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


# Root del progetto = cartella che contiene src/, docs/, data/, config/
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "docs"


def run_weekly_analysis() -> None:
    """
    Pipeline settimanale:

    1. Carica la configurazione
    2. Carica lo stato del portafoglio (o lo inizializza a 5000 cash)
    3. Colleziona segnali social, news e dati di mercato (mock)
    4. Calcola il sentiment
    5. Costruisce uno score per ogni ticker
    6. Ribilancia il portafoglio (decide i BUY)
    7. Genera il report HTML del giorno
    8. Copia il report in latest.html per la mini-app
    9. Salva il nuovo stato del portafoglio
    10. Invia la notifica Telegram con i bottoni
    """
    # 1. Config
    settings_path = BASE_DIR / "config" / "settings.yaml"
    settings = load_settings(settings_path)

    # 2. Stato portafoglio
    state_path = DATA_DIR / "portfolio_state.json"
    state = load_portfolio_state(
        state_path,
        start_cash=settings["start_cash"],
        start_date=settings["start_date"],
    )

    # 3. Raccolta segnali (mock)
    social_raw = collect_social_signals(settings)
    news_raw = collect_news_signals(settings)
    market_data = collect_market_data(settings, tickers_hint=state.tickers())

    # 4. Sentiment
    social_signals = compute_sentiment(social_raw)
    news_signals = compute_sentiment(news_raw)

    # 5. Score per ticker
    scores = build_scores(social_signals, news_signals, market_data)

    # 6. Ribilanciamento portafoglio
    new_state, trades, picked_scores = rebalance_portfolio(state, scores)

    # 7. Report HTML del giorno
    today = datetime.utcnow().date().isoformat()  # es. "2025-12-03"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_filename = f"report_{today}.html"
    report_path = REPORTS_DIR / report_filename

    build_html_report(
        output_path=report_path,
        state_before=state,
        state_after=new_state,
        trades=trades,
        scores=picked_scores,
        run_date=today,
    )

    # 8. Copia come latest.html per la mini-app (index.html → iframe su latest.html)
    latest_path = REPORTS_DIR / "latest.html"
    copyfile(report_path, latest_path)

    # 9. Salva nuovo stato portafoglio
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    save_portfolio_state(state_path, new_state)

    # 10. Notifica Telegram (i link sono relativi alla root di docs/)
    send_telegram_notification(
        report_url_suffix=report_filename,
        state_after=new_state,
        trades=trades,
    )


if __name__ == "__main__":
    run_weekly_analysis()
