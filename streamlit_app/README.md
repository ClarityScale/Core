# Streamlit Interface

This directory contains a Streamlit implementation of the **Global Event-Driven Market Intelligence Analyst** workflow.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

Open the URL that Streamlit prints (usually `http://localhost:8501`) in your browser.

## Features

- Event capture form mirroring the institutional briefing inputs.
- Mock assessment engine that generates:
  - Headline summary
  - Event context
  - Market impact analysis across sentiments, macro themes, and horizons
  - Opportunity table with 20+ cross-sector entries
  - Summary insights, risk note, and citations
- Markdown and CSV export for downstream research workflows.

Replace placeholder sources and narrative language with verified research before distribution.
