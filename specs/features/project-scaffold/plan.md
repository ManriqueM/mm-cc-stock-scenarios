# Plan — project-scaffold (Phase 0)

Reference: `specs/mission.md`, `specs/tech-stack.md`

## 1. requirements.txt
- streamlit, yfinance, pandas, numpy, scipy, plotly, pytest

## 2. app.py (Home page)
- Page config (title, icon, `layout="wide"`)
- Title + one-paragraph mission summary (from `specs/mission.md`)
- Bullet list of what the app does (portfolio builder, historical metrics, Monte Carlo, entry timing, stress tests, rebalancing)
- Persistent "not financial advice" disclaimer (sets the pattern that Phase 8 will formalize)

## 3. pages/ — 6 placeholder stub pages
Each stub: page config, title, 1–2 sentence description of what will live there and which roadmap phase implements it, "Coming in Phase N" notice.
- `1_Portfolio_Builder.py`
- `2_Historical_Metrics.py`
- `3_Monte_Carlo.py`
- `4_Entry_Timing.py`
- `5_Stress_Tests.py`
- `6_Rebalancing.py`

## 4. Local verification
- Activate `.venv`, `pip install -r requirements.txt`
- `streamlit run app.py`, confirm it starts, sidebar shows all 6 pages, each loads without error
