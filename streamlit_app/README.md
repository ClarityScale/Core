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

### LLM integration

Set the following environment variables before launching Streamlit to enable DeepSeek:

```bash
export DEEPSEEK_API_KEY="your_api_key"
# optional overrides:
# export DEEPSEEK_MODEL="deepseek-chat"
# export DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

If the key is absent or the API call fails, the app automatically falls back to the deterministic mock engine and annotates the dashboard accordingly.

### Prompt structure

For the best results, include labelled fields inside your message:

```
Event: India expands semiconductor incentive programme
Timing: Cabinet approval expected Q1 2025
Drivers: $10B subsidy pool; anchor fabs from TSMC/Samsung; easing of import tariffs on lithography tools
Narrative: Delhi accelerates chip sovereignty push to attract global foundries and reduce supply chain risk.
```

The dashboard updates after each submission, and the chat transcript keeps the latest system response.*** End Patch
