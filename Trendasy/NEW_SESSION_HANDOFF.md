# Handoff: publish Trendasy from a correctly-scoped session

The session that built this project is scoped to `hunterfischels/linear-algebra` only, so it cannot
push to `hunterfischels/Trendasy` (org policy → 403). Use a **new Claude Code session scoped to BOTH
repos** and paste the prompt below.

## 1) Start the new session with the right scope
Create/start a Claude Code (web) session whose repository access includes **both**:
- `hunterfischels/Trendasy`  (destination)
- `hunterfischels/linear-algebra`  (source of the content)

Both must be in scope — the agent needs to read the content from linear-algebra and write it to Trendasy.

## 2) Paste this prompt into that session

```
You have GitHub access to BOTH hunterfischels/linear-algebra and hunterfischels/Trendasy.

Goal: publish the `Trendasy/` project — currently a subfolder on branch
`claude/stock-theme-trends-tracker-g5o88m` of hunterfischels/linear-algebra — as the ROOT of the
hunterfischels/Trendasy repository, preserving git history. Then report the result.

Do exactly this in the shell:

1. Find the local git proxy base (host:port) from an existing clone so you reuse this session's auth:
   git remote -v
   # take the part before "/git/<owner>/<repo>", e.g. http://local_proxy@127.0.0.1:PORT/git
   # call that PROXYBASE for the steps below.

2. Get the source repo + branch (skip the clone if you are already inside a linear-algebra clone):
   cd /tmp
   git clone -b claude/stock-theme-trends-tracker-g5o88m PROXYBASE/hunterfischels/Linear-Algebra la
   cd la

3. Split the Trendasy subtree into a history-preserving branch whose root IS the Trendasy contents:
   git subtree split --prefix=Trendasy -b _pub

4. Push it to the Trendasy repo's main branch:
   git remote add trendasy PROXYBASE/hunterfischels/Trendasy
   git push trendasy _pub:main
   # If this is rejected as non-fast-forward (the repo already has an initial commit),
   # re-run with:  git push --force trendasy _pub:main

5. Verify and report:
   git ls-remote trendasy
   # Confirm the Trendasy repo root now contains: README.md, STOCK_THEME_TRENDS_TRACKER.md,
   # WATCHLISTS_AND_FUNDAMENTALS.md, index.html, assets/, streamlit_app/app.py,
   # and .github/workflows/deploy-pages.yml

6. Tell me the resulting commit SHA on Trendasy:main and the file tree at the root.

Notes:
- Do NOT modify linear-algebra; it is read-only source here.
- If a push to Trendasy returns 403, that repo is not actually in this session's scope — stop and
  tell me to fix the scope rather than retrying.
- After the push, GitHub Pages for Trendasy is one manual toggle: Settings → Pages → Source =
  "GitHub Actions" (the bundled .github/workflows/deploy-pages.yml then deploys the site at
  https://hunterfischels.github.io/Trendasy/).
```

## 3) After it runs
- The Trendasy repo will have the project at its root (so `streamlit_app/app.py`, `index.html`,
  `README.md`, etc. are top-level), with history preserved.
- Enable Pages (Settings → Pages → Source = GitHub Actions) to publish the site.
- Deploy the Streamlit app on Streamlit Community Cloud with main file `streamlit_app/app.py`.

### Fallback (no scope change, any machine logged into GitHub)
```
git clone https://github.com/hunterfischels/Linear-Algebra.git
cd Linear-Algebra && git checkout claude/stock-theme-trends-tracker-g5o88m
./Trendasy/publish.sh https://github.com/hunterfischels/Trendasy.git main
```
