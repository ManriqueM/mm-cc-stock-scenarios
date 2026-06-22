# Requirements — project-scaffold (Phase 0)

## Scope
- Set up the Streamlit application skeleton using native multi-page structure.
- `app.py` serves as the Home page.
- `pages/` directory holds placeholder stubs for each major roadmap feature area, so future phases (1–7) have an obvious place to build.
- `requirements.txt` pins core dependencies needed across the project (per `specs/tech-stack.md`): streamlit, yfinance, pandas, numpy, scipy, plotly, pytest.
- No real functionality yet — pages are placeholders with a title and short description of what will go there, referencing the roadmap phase that will fill them in.

## Key decisions
- Multi-page approach: Streamlit's native `pages/` directory (auto-discovered sidebar nav), per `specs/tech-stack.md` (Streamlit) and roadmap Phase 0 wording ("multi-page structure").
- Page-to-phase mapping (filenames numbered to control sidebar order):
  - `app.py` → Home (mission summary, "not financial advice" disclaimer per `specs/mission.md`)
  - `pages/1_Portfolio_Builder.py` → Phase 2
  - `pages/2_Historical_Metrics.py` → Phase 3
  - `pages/3_Monte_Carlo.py` → Phase 4
  - `pages/4_Entry_Timing.py` → Phase 5
  - `pages/5_Stress_Tests.py` → Phase 6
  - `pages/6_Rebalancing.py` → Phase 7
- Data layer (Phase 1) is not part of this scaffold — no `yfinance` calls yet.

## Out of scope
- Any actual data fetching, computation, or charts (later phases).
- Deployment config (Phase 9).
- Persistence (explicitly none, per `tech-stack.md`).
