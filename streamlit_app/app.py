import io
import re
from datetime import datetime
from typing import List

import pandas as pd
import streamlit as st

from report_engine import EventInput, build_mock_report
from report_formatter import format_report_as_markdown


st.set_page_config(
    page_title="Global Event-Driven Market Intelligence Analyst",
    page_icon="📊",
    layout="wide",
)

if "report" not in st.session_state:
    st.session_state.report = None

if "messages" not in st.session_state:
    st.session_state.messages: List[dict] = []


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "report"


def _split_driver_line(text: str) -> List[str]:
    parts = re.split(r"[;,•]", text)
    return [part.strip("-• ").strip() for part in parts if part.strip("-• ").strip()]


def _parse_prompt(prompt: str) -> EventInput:
    lines_raw = prompt.splitlines()
    lines = [line.strip() for line in lines_raw if line.strip()]

    name = ""
    timing = ""
    drivers: List[str] = []
    description_parts: List[str] = []
    capture_drivers = False

    for raw_line in lines_raw:
        line = raw_line.strip()
        if not line:
            capture_drivers = False
            continue

        lower = line.lower()
        if lower.startswith("event:"):
            name = line.split(":", 1)[1].strip()
            capture_drivers = False
            continue
        if lower.startswith("timing:"):
            timing = line.split(":", 1)[1].strip()
            capture_drivers = False
            continue
        if lower.startswith("drivers:"):
            rest = line.split(":", 1)[1].strip()
            drivers.extend(_split_driver_line(rest))
            capture_drivers = True
            continue
        if capture_drivers and (line.startswith("-") or line.startswith("•") or line.startswith("*")):
            drivers.append(line.lstrip("-•*").strip())
            continue

        description_parts.append(line)

    if not name and lines:
        name = lines[0]
        description_parts = lines[1:]

    if not drivers and description_parts:
        # Attempt to infer drivers from semicolon- or comma-separated clauses in description.
        inferred = _split_driver_line("; ".join(description_parts))
        drivers = inferred[:4]

    description = " ".join(description_parts) if description_parts else prompt.strip()

    return EventInput(
        name=name,
        expected_timing=timing,
        description=description,
        key_drivers=drivers,
    )


def _render_placeholder():
    st.info(
        "Describe a forward-looking catalyst using the chat composer below. Include event name, expected timing, "
        "and key drivers (e.g., `Event: ...`, `Timing: ...`, `Drivers: ...`). The engine returns a sell-side style "
        "dashboard for refinement."
    )
    st.markdown(
        """
        **Example prompt**

        ```
        Event: India announces national semiconductor incentive expansion
        Timing: Cabinet approval expected Q1 2025
        Drivers: $10B subsidy pool; anchor fabs from TSMC/Samsung; easing of import tariffs on lithography tools
        Narrative: Delhi accelerates chip sovereignty push to attract global foundries, coordinate with Quad allies, and reduce supply chain risk.
        ```
        """
    )
    st.markdown(
        """
        The latest dashboard appears below the chat window. Use the export controls for Markdown or CSV handoff.
        """
    )


st.title("Global Event-Driven Market Intelligence Analyst")
st.markdown(
    "Describe a forward catalyst to generate a cross-sector opportunity set aligned with a sell-side briefing format."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def _store_report(report_data: dict):
    st.session_state.report = report_data
    ack = (
        f"Generated assessment for **{report_data['event_name']}** "
        f"({report_data['market_impact']['sentiment']} sentiment). Scroll to view the dashboard."
    )
    st.session_state.messages.append({"role": "assistant", "content": ack})


def _trigger_rerun():
    rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
    if rerun_fn:
        rerun_fn()


prompt = st.chat_input("Event, timing, drivers… (use Event:/Timing:/Drivers: for best results)")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    event_input = _parse_prompt(prompt)
    report = build_mock_report(event_input)
    _store_report(report)
    _trigger_rerun()


st.divider()

report = st.session_state.report

if not report:
    _render_placeholder()
    st.stop()


generated_at = datetime.fromisoformat(report["generated_at"]).strftime("%Y-%m-%d %H:%M:%S UTC")
markdown_report = format_report_as_markdown(report)
file_name = f"global-event-driven-market-intelligence-analyst-{_slugify(report['event_name'])}.md"

st.subheader("Export")
st.download_button(
    "Download Markdown",
    data=markdown_report.encode("utf-8"),
    file_name=file_name,
    mime="text/markdown",
    use_container_width=True,
)
st.caption(f"Generated: {generated_at}")

st.divider()

st.subheader("1. Headline Summary")
st.write(report["headline_summary"])

st.subheader("2. Event Context")
context = report["event_context"]
st.write(context["overview"])
context_cols = st.columns(2)
context_cols[0].metric("Timing", context["timing"])
context_cols[1].metric("Significance", context["significance"])
st.markdown("**Key Drivers**")
st.markdown("\n".join(f"- {point}" for point in context["context_points"]))

st.subheader("3. Market Impact Analysis")
impact = report["market_impact"]
impact_cols = st.columns(3)
impact_cols[0].metric("Sentiment", impact["sentiment"])
impact_cols[1].markdown("**Macro Themes**\n" + "\n".join(f"- {theme}" for theme in impact["macro_themes"]))
impact_cols[2].markdown("**Sector Exposure**\n" + "\n".join(f"- {outlook}" for outlook in impact["sector_outlook"]))

horizon_df = pd.DataFrame(impact["horizon_impacts"])
st.table(horizon_df)

st.subheader("4. Investment Opportunity Table (20+ entries)")
opportunities = report["opportunities"]
opportunity_df = pd.DataFrame(opportunities)
opportunity_df["Source(s)"] = opportunity_df["sources"].apply(lambda items: "; ".join(items))
opportunity_df = opportunity_df.drop(columns=["sources"])
opportunity_df = opportunity_df.rename(
    columns={
        "ticker": "Ticker",
        "company": "Company",
        "sector": "Sector",
        "country": "Country",
        "expected_direction": "Expected Direction",
        "time_horizon": "Time Horizon",
        "mechanism": "Mechanism of Impact",
        "investability_score": "Investability Score",
        "rationale": "Rationale",
    }
)
st.dataframe(opportunity_df, use_container_width=True, height=600)

csv_buffer = io.StringIO()
opportunity_df.to_csv(csv_buffer, index=False)
st.download_button(
    "Download Opportunities (CSV)",
    data=csv_buffer.getvalue(),
    file_name=f"opportunities-{_slugify(report['event_name'])}.csv",
    mime="text/csv",
    use_container_width=True,
)

st.subheader("5. Summary Insights")
st.markdown("\n".join(f"- {insight}" for insight in report["summary_insights"]))

st.subheader("6. Risk Note")
st.write(report["risk_note"])

st.subheader("7. Citations")
st.markdown("\n".join(f"- {citation}" for citation in report["citations"]))
