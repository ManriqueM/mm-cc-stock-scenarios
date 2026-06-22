# Plan — deploy (Phase 9)

Reference: `specs/mission.md`, `specs/tech-stack.md`

## 1. Verify deploy-readiness (Claude, no code changes expected)
- Confirm `requirements.txt` only lists pip-installable packages with no local/private index references.
- Confirm no secrets are required (`yfinance` is keyless) and none are accidentally committed (`git grep` for obvious key-like strings, spot-check `.gitignore` covers `.env`).
- Confirm `app.py` is at the repo root and `pages/*.py` use the numbered-prefix convention Community Cloud's multipage auto-discovery expects.
- Confirm the `main` branch on `origin` is up to date with everything from Phases 0–8 (the commit that will actually be deployed).

## 2. Hand off the manual deploy steps (user, in browser)
1. Go to https://share.streamlit.io and sign in with the GitHub account that owns `ManriqueM/mm-cc-stock-scenarios`.
2. If prompted, authorize the Streamlit Community Cloud GitHub App for this repo (it's private, so explicit access is required).
3. Click **Create app** → choose "Deploy a public app from GitHub" (or equivalent current wording).
4. Fill in: repository `ManriqueM/mm-cc-stock-scenarios`, branch `main`, main file path `app.py`.
5. Open **Advanced settings** and pick a Python version (recommend the newest offered, e.g. 3.14; fall back to the 3.12 default if 3.14 isn't listed). No secrets need to be entered.
6. Click **Deploy** and wait for the build log to finish.
7. Copy the resulting public URL (`https://<app-name>.streamlit.app`) and share it back so the smoke test can run.

## 3. Smoke test (Claude, once the URL is shared)
- `WebFetch` the public URL; confirm the page contains the app title, the "What you can do here" bullet list, and the always-visible "Not financial advice" footer (Phase 8) — confirms Phase 0 and Phase 8 both shipped correctly to prod.
- `WebFetch` one data sub-page reachable from the deployed app — confirms multipage routing works on Community Cloud (note: pages that require `st.session_state["portfolio"]` will correctly show the "build a portfolio first" prompt rather than data, since a fresh visitor has no portfolio yet — that's expected, not a failure).
- Confirm no Streamlit error page / stack trace / "Oh no" exception screen appears anywhere fetched.
- Report back: URL live, what rendered, any warnings (e.g., cold-start spin-up delay, which is normal on the free tier after inactivity).

## 4. Verification
- See `validation.md`.
