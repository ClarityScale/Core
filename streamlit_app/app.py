import re
from datetime import datetime
from typing import List

import pandas as pd
import streamlit as st

from llm_client import generate_report
from report_engine import EventInput


st.set_page_config(
    page_title="Global Event-Driven Market Intelligence Analyst",
    page_icon="📊",
    layout="wide",
)

if "report" not in st.session_state:
    st.session_state.report = None

if "messages" not in st.session_state:
    st.session_state.messages: List[dict] = []


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
        The latest dashboard appears below the chat window.
        """
    )


st.title("Global Event-Driven Market Intelligence Analyst")
st.markdown(
    "Describe a forward catalyst to generate a cross-sector opportunity set aligned with a sell-side briefing format."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def _store_report(report_data: dict, source_note: str):
    st.session_state.report = report_data
    ack = (
        f"Generated assessment for **{report_data['event_name']}** "
        f"({report_data['market_impact']['sentiment']} sentiment). Scroll to view the dashboard."
    )
    if source_note:
        ack += f"\n\n_{source_note}_"
    st.session_state.messages.append({"role": "assistant", "content": ack})


def _trigger_rerun():
    rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
    if rerun_fn:
        rerun_fn()


prompt = st.chat_input("Event, timing, drivers… (use Event:/Timing:/Drivers: for best results)")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    event_input = _parse_prompt(prompt)
    report, source = generate_report(event_input)
    _store_report(report, source)
    _trigger_rerun()


st.divider()

report = st.session_state.report

if not report:
    _render_placeholder()
    st.stop()


generated_at = datetime.fromisoformat(report["generated_at"]).strftime("%Y-%m-%d %H:%M:%S UTC")
st.caption(f"Generated: {generated_at}")

st.divider()

context = report["event_context"]
impact = report["market_impact"]

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Headline Summary")
    st.write(report["headline_summary"])

    st.subheader("Event Context")
    st.write(context["overview"])
    if context["timing"]:
        st.markdown(f"**Timing:** {context['timing']}")
    if context["significance"]:
        st.markdown(f"**Significance:** {context['significance']}")
    if context["context_points"]:
        st.markdown("**Key Drivers**")
        st.markdown("\n".join(f"- {point}" for point in context["context_points"]))

with col_right:
    st.subheader("Market Impact Analysis")
    st.metric("Sentiment", impact["sentiment"])
    if impact["macro_themes"]:
        st.markdown("**Macro Themes**")
        st.markdown("\n".join(f"- {theme}" for theme in impact["macro_themes"]))
    if impact["sector_outlook"]:
        st.markdown("**Sector Exposure**")
        st.markdown("\n".join(f"- {outlook}" for outlook in impact["sector_outlook"]))

    horizon_df = pd.DataFrame(impact["horizon_impacts"])
    st.markdown("**Horizon Outlook**")
    st.table(horizon_df)

st.divider()

st.subheader("Investment Opportunity Table (20+ entries)")
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
