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
    html: List[str] = [
        "<html><head><meta charset='utf-8'>",
        f"<title>Traiding Weekly Report - {run_date}</title>",
        "<style>",
        "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 16px; }",
        "h1 { margin-bottom: 4px; }",
        "h2 { margin-top: 24px; }",
        "table { border-collapse: collapse; width: 100%; margin-top: 8px; }",
        "th, td { border: 1px solid #ccc; padding: 6px 8px; font-size: 14px; }",
        "th { background: #f5f5f5; text-align: left; }",
        ".ticker { font-weight: 600; }",
        ".risk { font-weight: 600; }",
        ".links a { margin-right: 8px; }",
        "</style>",
        "</head><body>",
        f"<h1>Traiding Weekly Report - {run_date}</h1>",
        f"<h2>Portfolio value before</h2><p>{state_before.total_value():.2f}</p>",
        f"<h2>Portfolio value after</h2><p>{state_after.total_value():.2f}</p>",
        "<h2>Trades (BUY / SELL)</h2>",
    ]

    if trades:
        html.append("<table>")
        html.append("<tr><th>Ticker</th><th>Side</th><th>Qty</th><th>Price</th><th>Why</th></tr>")
        for t in trades:
            reason = scores.get(t.ticker, {}).get("reason", "")
            html.append(
                "<tr>"
                f"<td class='ticker'>{t.ticker}</td>"
                f"<td>{t.side}</td>"
                f"<td>{t.quantity:.2f}</td>"
                f"<td>{t.price:.2f}</td>"
                f"<td>{reason}</td>"
                "</tr>"
            )
        html.append("</table>")
    else:
        html.append("<p>No trades executed this week.</p>")

    html.append("<h2>Scores & Links</h2>")
    if scores:
        html.append("<table>")
        html.append("<tr><th>Ticker</th><th>Score</th><th>Risk</th><th>Why</th><th>Links</th></tr>")
        for ticker, s in scores.items():
            links_html = " ".join(
                f"<a href='{u}' target='_blank'>link</a>" for u in s.get("links", [])
            )
            html.append(
                "<tr>"
                f"<td class='ticker'>{ticker}</td>"
                f"<td>{s['score']:.3f}</td>"
                f"<td class='risk'>{s['risk']}</td>"
                f"<td>{s['reason']}</td>"
                f"<td class='links'>{links_html}</td>"
                "</tr>"
            )
        html.append("</table>")
    else:
        html.append("<p>No scores computed.</p>")

    html.append("</body></html>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html), encoding="utf-8")
