#!/usr/bin/env bash
# Pick a GitHub token that can post issue comments as a non-GITHUB_ACTIONS actor (triggers team.yml).
# Requires S_GO_GITHUB_RUN_TOKEN and/or S_PROJECTS_STATE_PAT in the environment (do not log values).
set -euo pipefail
if [ -n "${S_GO_GITHUB_RUN_TOKEN:-}" ]; then
  export GH_TOKEN="$S_GO_GITHUB_RUN_TOKEN"
elif [ -n "${S_PROJECTS_STATE_PAT:-}" ]; then
  export GH_TOKEN="$S_PROJECTS_STATE_PAT"
else
  echo "Neither GO_GITHUB_RUN_TOKEN nor PROJECTS_STATE_PAT is available to this workflow." >&2
  exit 1
fi
gh api user --jq .login