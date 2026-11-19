#!/usr/bin/env bash
# Pick a GitHub token that can post issue comments as a non-GITHUB_ACTIONS actor (triggers team.yml).
# Requires S_GO_GITHUB_RUN_TOKEN and/or S_PROJECTS_STATE_PAT in the environment (do not log values).
set -euo pipefail
# Prefer PROJECTS_STATE_PAT for non-GITHUB_ACTIONS issue comments (triggers team.yml).
if [ -n "${S_PROJECTS_STATE_PAT:-}" ]; then
  export GH_TOKEN="$S_PROJECTS_STATE_PAT"
elif [ -n "${S_I8_TEAM_TRIGGER_PAT:-}" ]; then
  export GH_TOKEN="$S_I8_TEAM_TRIGGER_PAT"
elif [ -n "${S_GO_GITHUB_RUN_TOKEN:-}" ]; then
  export GH_TOKEN="$S_GO_GITHUB_RUN_TOKEN"
else
  echo "No GitHub PAT for I8 team trigger (set PROJECTS_STATE_PAT or a valid GO_GITHUB_RUN_TOKEN gh PAT)." >&2
  exit 1
fi
gh api user --jq .login