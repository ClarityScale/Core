import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from openai import OpenAI

from report_engine import EventInput, build_mock_report

DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_ENABLED = bool(os.getenv("DEEPSEEK_API_KEY"))

SYSTEM_PROMPT = """You are an institutional research analyst.
Return ONLY valid JSON that matches this schema:
{
  "headline_summary": string,
  "event_context": {
    "overview": string,
    "timing": string,
    "significance": string,
    "context_points": string[1..4]
  },
  "market_impact": {
    "sentiment": "Bullish"|"Bearish"|"Neutral",
    "macro_themes": string[1..6],
    "sector_outlook": string[1..5],
    "horizon_impacts": [
      {"horizon": "Short-term (0–3 months)", "outlook": string},
      {"horizon": "Medium-term (3–12 months)", "outlook": string},
      {"horizon": "Long-term (1–5 years)", "outlook": string}
    ]
  },
  "opportunities": [
    {
      "ticker": string,
      "company": string,
      "sector": string,
      "country": string,
      "expected_direction": "Bullish"|"Bearish"|"Neutral",
      "time_horizon": "Short-term (0–3 months)"|"Medium-term (3–12 months)"|"Long-term (1–5 years)",
      "mechanism": string,
      "investability_score": number (1-10),
      "rationale": string,
      "sources": string[]
    }
  ],
  "summary_insights": string[1..5],
  "risk_note": string,
  "citations": string[3]
}
Ensure there are at least 20 opportunities covering multiple sectors (global equities, ETFs, commodities, fixed income, crypto, etc.).
"""

USER_TEMPLATE = """Event Headline: {name}
Expected Timing: {timing}
Narrative Summary: {description}
Key Drivers:
{drivers}

Produce concise, evidence-based language. Cite reputable public sources only."""


def _extract_json(raw_text: str) -> Optional[str]:
    if not raw_text:
        return None
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"^```\s*", "", text)
        text = text.strip("`")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def _normalise_opportunities(data: List[Dict[str, object]]) -> List[Dict[str, object]]:
    horizons = {"short": "Short-term (0–3 months)", "medium": "Medium-term (3–12 months)", "long": "Long-term (1–5 years)"}
    results = []
    for item in data:
        entry = {
            "ticker": str(item.get("ticker", "")).upper(),
            "company": item.get("company", ""),
            "sector": item.get("sector", ""),
            "country": item.get("country", ""),
            "expected_direction": item.get("expected_direction", "Neutral"),
            "time_horizon": item.get("time_horizon", "Medium-term (3–12 months)"),
            "mechanism": item.get("mechanism", ""),
            "investability_score": item.get("investability_score", 5),
            "rationale": item.get("rationale", ""),
            "sources": item.get("sources", []),
        }
        horizon_lower = entry["time_horizon"].lower()
        for key, label in horizons.items():
            if key in horizon_lower:
                entry["time_horizon"] = label
                break
        results.append(entry)
    return results


def _ensure_structure(raw: Dict[str, object], event_input: EventInput) -> Dict[str, object]:
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "event_name": event_input.name or raw.get("event_context", {}).get("overview", "Strategic Market Catalyst"),
        "headline_summary": raw.get("headline_summary", ""),
        "event_context": {
            "overview": raw.get("event_context", {}).get("overview", ""),
            "timing": raw.get("event_context", {}).get("timing", event_input.expected_timing),
            "significance": raw.get("event_context", {}).get("significance", ""),
            "context_points": raw.get("event_context", {}).get("context_points", [])[:4],
        },
        "market_impact": raw.get("market_impact", {}),
        "opportunities": _normalise_opportunities(raw.get("opportunities", [])),
        "summary_insights": raw.get("summary_insights", []),
        "risk_note": raw.get("risk_note", ""),
        "citations": raw.get("citations", []),
    }

    # Ensure horizon ordering
    desired_order = [
        "Short-term (0–3 months)",
        "Medium-term (3–12 months)",
        "Long-term (1–5 years)",
    ]
    existing = {item.get("horizon"): item.get("outlook") for item in report["market_impact"].get("horizon_impacts", [])}
    report["market_impact"]["horizon_impacts"] = [
        {"horizon": horizon, "outlook": existing.get(horizon, "")} for horizon in desired_order
    ]

    return report


def _call_deepseek(event_input: EventInput) -> Tuple[Optional[Dict[str, object]], Optional[str]]:
    if not DEEPSEEK_ENABLED:
        return None, "DeepSeek API key not configured."

    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=DEEPSEEK_BASE_URL,
    )

    drivers = event_input.key_drivers or ["Driver details not specified"]
    driver_block = "\n".join(f"- {driver}" for driver in drivers)
    user_message = USER_TEMPLATE.format(
        name=event_input.name or "Unnamed Event",
        timing=event_input.expected_timing or "Timing TBD",
        description=event_input.description or "No narrative provided.",
        drivers=driver_block,
    )

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.35,
        max_tokens=3500,
    )

    content = response.choices[0].message.content
    payload = _extract_json(content)
    if not payload:
        raise ValueError("LLM response did not contain valid JSON.")
    data = json.loads(payload)
    return _ensure_structure(data, event_input), None


def generate_report(event_input: EventInput) -> Tuple[Dict[str, object], str]:
    if not DEEPSEEK_ENABLED:
        report = build_mock_report(event_input)
        return report, "DeepSeek disabled; using rule-based template."

    try:
        report, error = _call_deepseek(event_input)
        if report:
            return report, f"DeepSeek ({DEEPSEEK_MODEL}) response."
        raise RuntimeError(error or "Unknown DeepSeek error.")
    except Exception as exc:
        fallback = build_mock_report(event_input)
        fallback["summary_insights"].append(
            "LLM generation unavailable—displaying deterministic template output for review."
        )
        note = f"DeepSeek request failed ({exc}); reverted to rule-based template."
        return fallback, note
