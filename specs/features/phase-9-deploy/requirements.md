# Requirements — deploy (Phase 9)

## Scope
- Deploy the app to Streamlit Community Cloud (per `specs/tech-stack.md`) and smoke-test the resulting public URL.
- Deploying itself is an **account-bound, browser-based action** (sign in to share.streamlit.io with GitHub, authorize repo access, click "Deploy") — it can't be done from this CLI session. Claude's part of this phase is: (1) verify the repo is actually deploy-ready, (2) hand the user exact steps to click through, (3) once the app is live, smoke-test the public URL.
- Target: `app.py` on the `main` branch of `github.com/ManriqueM/mm-cc-stock-scenarios` (confirmed via `git remote -v`).

## Current state (verified before writing this plan)
- `requirements.txt` lists unpinned `streamlit`, `yfinance`, `pandas`, `numpy`, `scipy`, `plotly`, `pytest` — valid for Community Cloud's pip-based dependency resolution (per Streamlit docs: dependency file priority is `uv.lock` > `Pipfile` > `environment.yml` > `requirements.txt` > `pyproject.toml`; only one should exist — we only have `requirements.txt`, so no conflict).
- `.gitignore` already excludes `.venv/`, `__pycache__/`, `.env` — no risk of committing the virtualenv or secrets.
- No API keys or secrets are needed — `yfinance` requires none, so Community Cloud's "Secrets" step is a no-op for this app.
- The GitHub repo is **private** (confirmed via `gh repo view`) — Community Cloud supports deploying from private repos, but the user must grant the Streamlit GitHub App access to this specific repo (or all repos) during account connection.
- Python version is **not** set via a repo file (no `runtime.txt`/`.python-version` mechanism on Community Cloud) — it's chosen from a "Python version" dropdown in the "Advanced settings" panel of the deploy dialog. Community Cloud defaults to **3.12**; per current Streamlit docs, all actively-supported Python versions are offered (3.9 through at least 3.14 as of this Streamlit release). Local dev has been on 3.14 throughout this project with no version-specific code, so any offered version is expected to work — recommend selecting the newest available (3.14 if listed, else the 3.12 default) since there's nothing in this codebase pinned to an older Python.

## Key decisions
- **No code changes required for "repo prep"** — the verification above confirms the repo is already deploy-ready as-is. This phase does not introduce a `runtime.txt`, pin `requirements.txt` versions, or add a `packages.txt` (no system-level/apt dependencies are needed by any library this project uses).
- **No README is created in this phase** — a project README is the dedicated `mm-readme` skill's job, not this roadmap phase. Deploy instructions live in this spec and are relayed to the user directly in conversation.
- **Smoke test method**: once the user shares the live public URL, fetch it (`WebFetch`/`curl`) and confirm the home page and at least one data sub-page render expected content with no error text, rather than relying solely on the user's own visual check.

## Out of scope
- Actually performing the GitHub OAuth / Streamlit Community Cloud sign-in and clicking "Deploy" — this must be done by the user in their browser, under their account.
- Custom domains, app analytics, or any Community Cloud settings beyond the basic deploy (repo, branch, main file path, Python version).
- Pinning dependency versions or adding CI for this deployment — not required by the roadmap phase and not requested.
