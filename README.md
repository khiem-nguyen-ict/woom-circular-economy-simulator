# Woom 3: Circular Economy & Remanufacturing Simulator

Enterprise-grade scenario modeling for reverse logistics, operational triage, component-level recovery, and environmental impact — built with [Streamlit](https://streamlit.io).

## Overview

This interactive simulator models the full circular economy lifecycle of the **Woom 3** kids' balance bike. It helps product designers, operations managers, and sustainability teams evaluate trade-in programs, remanufacturing routing strategies, component harvesting, ESG impact, and Design for Remanufacturing (DfRem) readiness.

### Features

- **Executive Dashboard** — KPIs comparing linear vs. circular profit models, revenue waterfall, and asset routing volumes.
- **Operational Triage** — Condition-based quality routing (Light Refurbish / Full Remanufacture / Component Harvest) with real-time margin feedback.
- **Component Recovery** — Material flow planning for harvested bikes (Internal Reuse, Remanufacturing, B2B Secondary Market, Scrap).
- **Idea Bank: 350 Scenarios** — A searchable matrix of B2B repurposing strategies for every harvested component.
- **Scenario Simulation** — Monte Carlo simulation of 100 market scenarios with configurable volatility boundaries.
- **ESG & Impact** — Scope 3 CO₂e avoided and virgin aluminum kept in the loop.
- **DfRem Audit Tool** — Interactive product assessment scoring design for remanufacturing.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Deployment

This project includes a [`render.yaml`](render.yaml) blueprint and a [`requirements.txt`](requirements.txt). Push the repository to GitHub, then deploy on [Render](https://render.com):

1. Sign in to Render and choose **Blueprints**.
2. Paste your repository URL.
3. Render provisions a free-tier Python web service and runs `streamlit run main.py`.

## Dependencies

- [Streamlit](https://streamlit.io) ≥ 1.31
- [Pandas](https://pandas.pydata.org) ≥ 2.1

## License

MIT