import os
from typing import List

import requests

from ..portfolio.portfolio_engine import Trade
from ..storage.state_manager import PortfolioState

# Base URL per le API di Telegram
TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/{method}"


def _post(method: str, token: str, payload: dict):
    """
    Wrapper per le chiamate HTTP a Telegram con log degli errori.
    """
    url = TELEGRAM_API_URL.format(token=token, method=method)
    r = requests.post(url, json=payload, timeout=10)

    # Se qualcosa va storto, stampiamo la risposta di Telegram nei log
    if not r.ok:
        print("Telegram error response:", r.text)

    r.raise_for_status()
    return r.json()


def _format_message(state_after: PortfolioState, trades: List[Trade]) -> str:
    """
    Costruisce il testo del messaggio da inviare su Telegram.
    """
    lines: List[str] = [
        "📊 *Traiding Weekly Update*",
        f"Portfolio value: `{state_after.total_value():.2f}`",
        "",
        "*Suggested moves:*",
    ]

    if not trades:
        lines.append("_No major changes this week._")
    else:
        for t in trades:
            lines.append(
                f"- {t.side} {t.quantity:.2f} {t.ticker} @ {t.price:.2f}"
            )

    return "\n".join(lines)


def send_telegram_notification(
    report_url_suffix: str,
    state_after: PortfolioState,
    trades: List[Trade],
) -> None:
    """
    Invia il messaggio settimanale con:
    - riepilogo del portafoglio
    - lista delle operazioni
    - bottoni per aprire la Mini-App (latest.html) e il report del giorno
    """
    # Variabili d'ambiente passate dal workflow GitHub Actions
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    webapp_url = os.environ.get("WEBAPP_URL", "").strip()

    # Normalizza: se non è vuota, assicurati che finisca con "/"
    if webapp_url and not webapp_url.endswith("/"):
        webapp_url = webapp_url + "/"

    text = _format_message(state_after, trades)

    inline_keyboard: List[List[dict]] = []

    if webapp_url:
        # Bottone che apre la mini-app (index.html → iframe su latest.html)
        inline_keyboard.append(
            [
                {
                    "text": "Open Traiding Mini-App",
                    "web_app": {"url": webapp_url},
                }
            ]
        )

        # Bottone che apre direttamente il report del giorno
        inline_keyboard.append(
            [
                {
                    "text": "Open weekly report",
                    "url": f"{webapp_url}{report_url_suffix}",
                }
            ]
        )

    payload: dict = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }

    if inline_keyboard:
        payload["reply_markup"] = {"inline_keyboard": inline_keyboard}

    _post("sendMessage", token, payload)

