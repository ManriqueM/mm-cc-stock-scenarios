# Validation — deploy (Phase 9)

1. **Repo readiness check** (before handoff): `requirements.txt` installs cleanly with plain `pip` (already verified throughout Phases 0-8 via the local `.venv`); no secrets are committed; `main` is pushed and up to date.
2. **Manual deploy** (user): app successfully deploys on Streamlit Community Cloud from `ManriqueM/mm-cc-stock-scenarios`, branch `main`, main file `app.py`, with no build errors in the Community Cloud log.
3. **Smoke test** (Claude, via `WebFetch` against the shared public URL):
   - Home page loads and shows the app title, feature bullet list, and the always-visible "Not financial advice" footer.
   - At least one sub-page (e.g. Historical Metrics) loads via the deployed app's navigation and shows the expected "build a portfolio first" prompt (since no portfolio exists for a fresh visitor) rather than an error.
   - No Streamlit exception/error screen appears on either fetch.
4. **Sign-off**: user confirms the public URL is the one they intend to share, and roadmap Phase 9 is marked complete.
