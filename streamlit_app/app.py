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


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "report"


def _split_lines(value: str) -> List[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _render_placeholder():
    st.info(
        "Provide an event headline, expected timing, narrative, and key drivers to generate a templated market "
        "intelligence brief. Replace placeholder sources with validated research before distribution."
    )
    st.markdown(
        """
        **Workflow tips**

        - Capture catalysts, timeline markers, and principal stakeholders.
        - Drivers inform macro themes, sector positioning, and opportunity mapping.
        - Use the export button for Markdown handoff into your research knowledge base.
        """
    )


st.title("Global Event-Driven Market Intelligence Analyst")
st.markdown(
    "Identify a forward catalyst to generate a cross-sector opportunity set aligned with an institutional briefing format."
)

with st.form("event_form"):
    st.subheader("1. Context Gathering")
    st.caption(
        "Summarize the event narrative, expected timeline, and catalysts. The engine returns a sell-side style brief "
        "for analyst refinement."
    )

    name = st.text_input("Event Headline", placeholder="e.g., EU unveils continent-wide AI safety regime")
    expected_timing = st.text_input("Expected Timing", placeholder="e.g., Q2 2026 (formal legislation vote)")
    description = st.text_area(
        "Event Narrative",
        placeholder="Summarize what is happening, key actors, and the policy or technology pivot expected.",
        height=140,
    )
    drivers_text = st.text_area(
        "Key Drivers & Catalysts",
        placeholder="List each driver on a new line (e.g., Subsidy outline, Export control easing, Corporate capex commitments)",
        height=140,
    )

    col_submit, col_reset = st.columns([1, 1])
    generate = col_submit.form_submit_button("Generate Assessment", use_container_width=True)
    reset = col_reset.form_submit_button("Reset", use_container_width=True)

    if reset:
        st.session_state.report = None
        st.experimental_rerun()

    if generate:
        event_input = EventInput(
            name=name,
            expected_timing=expected_timing,
            description=description,
            key_drivers=_split_lines(drivers_text),
        )
        st.session_state.report = build_mock_report(event_input)


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
