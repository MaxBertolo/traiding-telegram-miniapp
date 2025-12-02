import os
import requests
from typing import List

from ..portfolio.portfolio_engine import Trade
from ..storage.state_manager import PortfolioState

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/{method}"

def _post(method: str, token: str, payload: dict):
    url = TELEGRAM_API_URL.format(token=token, method=method)
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def send_telegram_notification(
    report_url_suffix: str,
    state_after: PortfolioState,
    trades: List[Trade],
) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    webapp_url = os.environ.get("WEBAPP_URL", "")

    text_lines = [
        "📊 *Traiding Weekly Update*",
        f"Portfolio value: `{state_after.total_value():.2f}`",
        "",
        "*Suggested moves:*",
    ]
    if not trades:
        text_lines.append("_No major changes this week._")
    else:
        for t in trades:
            text_lines.append(
                f"- {t.side} {t.quantity:.2f} {t.ticker} @ {t.price:.2f}"
            )

    text = "\n".join(text_lines)

    buttons = []
    if webapp_url:
        buttons.append([{
            "text": "Open Traiding Mini-App",
            "web_app": {"url": webapp_url},
        }])
        buttons.append([{
            "text": "Open weekly report",
            "url": f"{webapp_url}{report_url_suffix}",
        }])

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    _post("sendMessage", token, payload)
