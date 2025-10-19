from __future__ import annotations

from datetime import datetime
from typing import Dict, List


def _escape_pipes(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def _format_opportunity_row(row: Dict[str, object]) -> str:
    cells: List[str] = [
        str(row["ticker"]),
        str(row["company"]),
        str(row["sector"]),
        str(row["country"]),
        str(row["expected_direction"]),
        str(row["time_horizon"]),
        str(row["mechanism"]),
        str(row["investability_score"]),
        str(row["rationale"]),
        "; ".join(row.get("sources", [])),
    ]
    return "| " + " | ".join(_escape_pipes(cell) for cell in cells) + " |"


def format_report_as_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []

    lines.append("# Headline Summary")
    lines.append(str(report["headline_summary"]).strip())
    lines.append("")

    event_context = report["event_context"]
    lines.append("## Event Context")
    lines.append(str(event_context["overview"]).strip())
    lines.append("")
    lines.append(f"- **Timing:** {event_context['timing']}")
    lines.append(f"- **Significance:** {event_context['significance']}")
    context_points = event_context.get("context_points", [])
    if context_points:
        lines.append("- **Key Drivers:**")
        for point in context_points:
            lines.append(f"  - {point}")
    lines.append("")

    market_impact = report["market_impact"]
    lines.append("## Market Impact Analysis")
    lines.append(f"- **Sentiment:** {market_impact['sentiment']}")
    lines.append(f"- **Macro Themes:** {'; '.join(market_impact['macro_themes'])}")
    lines.append(f"- **Sector Exposure:** {'; '.join(market_impact['sector_outlook'])}")
    lines.append("- **Time Horizons:**")
    for item in market_impact["horizon_impacts"]:
        lines.append(f"  - {item['horizon']}: {item['outlook']}")
    lines.append("")

    lines.append("## Investment Opportunity Table")
    lines.append("| Ticker | Company | Sector | Country | Expected Direction | Time Horizon | Mechanism of Impact | Investability Score | Rationale | Source(s) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in report["opportunities"]:
        lines.append(_format_opportunity_row(row))
    lines.append("")

    lines.append("## Summary Insights")
    for insight in report["summary_insights"]:
        lines.append(f"- {insight}")
    lines.append("")

    lines.append("## Risk Note")
    lines.append(str(report["risk_note"]).strip())
    lines.append("")

    lines.append("## Citations")
    for citation in report["citations"]:
        lines.append(f"- {citation}")
    lines.append("")

    generated_at = report.get("generated_at")
    if generated_at:
        dt = datetime.fromisoformat(generated_at)
        lines.append(f"_Generated {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}_")

    return "\n".join(lines)
