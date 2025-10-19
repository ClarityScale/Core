# Streamlit Interface

This directory contains a Streamlit implementation of the **Global Event-Driven Market Intelligence Analyst** workflow.

## Getting Started

```bash
# optional: create a virtual environment first
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

Open the URL Streamlit prints (typically `http://localhost:8501`) in your browser.

## Features

- LLM-style interface with a single-line composer anchored at the bottom of the screen.
- Mock assessment engine that generates:
  - Headline summary
  - Event context
  - Market impact analysis across sentiments, macro themes, and horizons
  - Opportunity table with 20+ cross-sector entries
  - Summary insights, risk note, and citations
- Markdown and CSV export for downstream research workflows.

Replace placeholder sources and narrative language with verified research before distribution.

### Prompt structure

For the best results, include labelled fields inside your message:

```
Event: India expands semiconductor incentive programme
Timing: Cabinet approval expected Q1 2025
Drivers: $10B subsidy pool; anchor fabs from TSMC/Samsung; easing of import tariffs on lithography tools
Narrative: Delhi accelerates chip sovereignty push to attract global foundries and reduce supply chain risk.
```

The dashboard updates after each submission, and the chat transcript keeps the latest system response.*** End Patch
