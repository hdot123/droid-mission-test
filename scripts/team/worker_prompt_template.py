"""Single-source worker prompt template (both execution rounds).

The round-1 and round-2 worker session steps in team.yml carried
byte-identical inline f-strings (the same L-4 double-copy disease the
validator face was cured of by validator_prompt_template.py). This module
is the one true source: the workflow embeds it (both session steps import
and render it), and tests read the prompt from here. The rounds are
byte-identical for the same card — the retry note already rides on the
card itself (``retry_note``), so no round parameter exists.

Template deltas versus the inline-heredoc era (r58 cure, layer 2):

- Incremental persistence guidance (P-2-capped): write the status.json
  skeleton before doing anything else, and update both team files as each
  part completes, so a killed session leaves richer intermediate state for
  the prep salvage packer (worker_salvage.py). Per the P-2 verdict this
  wording has no runtime force; its value is the intermediate artifacts.
- The "at most 20 tool calls" arithmetic cap is replaced by I-1-style
  milestone-ordering wording: work the card as an ordered sequence of
  milestones, one milestone per tool call, persisting the completed part
  before moving on (I-1 lesson: a numeric budget is one more arithmetic
  question for the model to reason over, not a mechanism).

The standing discipline lines ("Do not commit or push", the two team-file
instructions, the checks instruction, the by-products cleanup note) are
unchanged verbatim from the era they were written in.
"""
from __future__ import annotations

import json


def build_worker_prompt(
    proc: dict,
    *,
    issue_number: int | str,
    issue_title: str,
    issue_body: str = "",
) -> str:
    """Render the full worker prompt for one process card.

    ``proc`` is the process card as dispatched (the workflow passes
    ``toJSON(matrix.process)``); ``issue_*`` describe the work order. The
    optional ``retry_note`` on the card adds the retry-context block, the
    only conditional section.
    """
    retry = proc.get("retry_note") or ""
    retry_block = (
        f"\n          Retry context (this card was re-dispatched after validation):\n"
        f"          {retry}\n"
        if retry
        else ""
    )
    return f"""You are a WORKER on a development team under the foreman pattern. Execute exactly one process card (your sub-issue #{proc.get('sub_issue_number', '?')}). Do not do any other process. Do not expand scope.

          Work order: #{issue_number} {issue_title}
          Work order body:
          {issue_body}

          Your process card:
          {json.dumps(proc, ensure_ascii=False, indent=2)}
          {retry_block}
          Instructions:
          - Create or edit only these files: {', '.join(proc['files'])}
          - Also write exactly these two team files:
            1. team/handoffs/{proc['id']}.md — a self-contained handoff with: what was requested, what you did, what you did not do, checks you ran and their results, and anything the validator must pay attention to.
            2. team/status/{proc['id']}.json — valid JSON with keys: id, title, state ("done"), files (array), checks (array of objects with command and result).
          - SESSION DISCIPLINE (mandatory, do first): before doing anything else, write team/status/{proc['id']}.json as a status skeleton with every required key (state "in_progress", checks still empty) — then update both team files as you complete each part of the card, and do not leave both to the end. The files survive a session timeout; a session killed before its final write still leaves the intermediate state on disk.
          - Work through the card as an ordered sequence of milestones (read the pinned spec, write each file, run each check); aim at one tool call per milestone and persist the completed part (update the team files) before starting the next.
          - Run your process checks before finishing: {'; '.join(proc['checks'])}
          - Checks may run tests across the whole repo. Files like verdict.json or verdict.md that appear in the repo root because of those checks are pipeline by-products of the test suite, not your deliverables. They are outside your card, so delete them before finishing (e.g. rm -f verdict.json verdict.md).
          - Do not commit or push; the workflow will do that.
          - Do not modify files owned by other processes.
          """
