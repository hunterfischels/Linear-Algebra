#!/usr/bin/env bash
#
# Publish the Trendasy/ project as the ROOT of its own GitHub repository,
# preserving git history (via `git subtree split`).
#
# WHY THIS SCRIPT EXISTS: the cloud session that generated Trendasy has GitHub
# access scoped to the Linear-Algebra repo only, so it cannot push to the new
# Trendasy repo (org policy returns 403). Run this from a machine where you ARE
# authenticated to push to your Trendasy repo.
#
# USAGE (from the root of a local clone of the Linear-Algebra repo):
#   ./Trendasy/publish.sh [REMOTE_URL] [BRANCH]
#
# Examples:
#   ./Trendasy/publish.sh https://github.com/hunterfischels/Trendasy.git main
#   ./Trendasy/publish.sh git@github.com:hunterfischels/Trendasy.git main
#
set -euo pipefail

REMOTE="${1:-https://github.com/hunterfischels/Trendasy.git}"
BRANCH="${2:-main}"
TMP="_trendasy_publish_tmp"

echo "==> Splitting Trendasy/ into standalone history (root = Trendasy contents)…"
git branch -D "$TMP" 2>/dev/null || true
git subtree split --prefix=Trendasy -b "$TMP"

echo "==> Pushing to $REMOTE ($BRANCH)…"
# Use --force only if you intend to overwrite an existing branch.
git push "$REMOTE" "$TMP:$BRANCH"

git branch -D "$TMP"
echo "==> Done. Trendasy is now the root of $REMOTE on branch '$BRANCH'."
echo "    Next: in that repo, Settings → Pages → Source = GitHub Actions (the bundled"
echo "    .github/workflows/deploy-pages.yml will then publish the site)."
