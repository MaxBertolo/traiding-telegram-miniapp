from pathlib import Path
from typing import Dict, Any, List

from ..storage.state_manager import PortfolioState
from ..portfolio.portfolio_engine import Trade

def build_html_report(
    output_path: Path,
    state_before: PortfolioState,
    state_after: PortfolioState,
    trades: List[Trade],
    scores: Dict[str, Dict[str, Any]],
    run_date: str,
) -> None:
    html = [
        "<html><head><meta charset='utf-8'>",
        f"<title>Traiding Weekly Report - {run_date}</title>",
        "</head><body>",
        f"<h1>Traiding Weekly Report - {run_date}</h1>",
        f"<h2>Portfolio value before</h2><p>{state_before.total_value():.2f}</p>",
        f"<h2>Portfolio value after</h2><p>{state_after.total_value():.2f}</p>",
        "<h2>Trades</h2><ul>",
    ]

    if trades:
        for t in trades:
            html.append(
                f"<li>{t.side} {t.quantity:.2f} {t.ticker} @ {t.price:.2f} - {t.reason}</li>"
            )
    else:
        html.append("<li>No trades executed this week.</li>")
    html.append("</ul>")

    html.append("<h2>Scores & Links</h2><ul>")
    for ticker, s in scores.items():
        links_html = " | ".join(
            f"<a href='{u}' target='_blank'>link</a>" for u in s.get("links", [])
        )
        html.append(
            f"<li><strong>{ticker}</strong> score={s['score']:.3f}, risk={s['risk']} - {s['reason']}<br>{links_html}</li>"
        )
    html.append("</ul>")

    html.append("</body></html>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html), encoding="utf-8")
