"""Single-source validator prompt template (both validation rounds).

L-4: the round-1 and round-2 validator prompts in team.yml were byte-identical
duplicates maintained as two inline f-strings, and tests sliced them back out
of the workflow with string indices. This module is the one true source: the
workflow embeds it (both droid_validate steps import and render it), and tests
read the prompt from here.

The rounds differ in exactly two parametric points:
- the intro sentence (round 2 announces it is the final round after a replan);
- the recorder discipline stamps ``--round 2`` on the salvage CLI (adopt2
  reads verdict-partial.json with --round 2; a missing stamp makes read_salvage
  return None — the 52B loss shape on the round-2 path).

Round-2 prompt rewrite policy (I-1..I-4, PR-2) lands by editing THIS module:
both rounds get the fix, and the diff against the prompt-in-yml era stays
auditable here.
"""
from __future__ import annotations

ROUND1_INTRO = (
    "You are the VALIDATOR on a development team, working in the squad-leader "
    "acceptance style. You only judge pre-packed evidence. You have no GitHub "
    "access and must not try to fetch anything else."
)
ROUND2_INTRO = (
    "You are the VALIDATOR on a development team, working in the squad-leader "
    "acceptance style. This is the final validation round after a replan. You "
    "only judge pre-packed evidence. You have no GitHub access and must not "
    "try to fetch anything else."
)


def _recorder_line(round_num: int) -> str:
    stamp = " --round 2" if round_num == 2 else ""
    return (
        "          python3 -m salvage_verdict --work-dir . --process <process-id> "
        f'--verdict pass|fail --reason "<one line evidence-based reason>"{stamp}'
    )


def build_validator_prompt(judgeable: list[str], *, round_num: int = 1) -> str:
    """Render the full validator prompt for a judgeable process-id list."""
    intro = ROUND2_INTRO if round_num == 2 else ROUND1_INTRO
    ids = ", ".join(judgeable)
    packs = "\n".join(
        f"- packs/{pid}/ (process-card.json, handoff.md, status.json, diff.patch, "
        "checks-output.txt, checks-exit.json, checks-failed.marker (present only "
        "when the worker's own checks failed))"
        for pid in judgeable
    )
    plan_line = (
        "- plan.json (the effective plan: revised cards for re-dispatched "
        "processes, original cards otherwise)"
        if round_num == 2
        else "- plan.json (the plan and process cards)"
    )
    evidence_line = (
        "pytest-output.txt and pytest-exit.txt (full test evidence for the "
        "final merged candidate)"
        if round_num == 2
        else "pytest-output.txt and pytest-exit.txt (full test evidence for the "
        "merged candidate)"
    )
    return f"""{intro}

          Judge ONLY these processes: {ids}

          Evidence available in this directory:
          - {plan_line}
          - {evidence_line}
          {packs}

          SESSION DISCIPLINE (mandatory, do first): after you finish analyzing each process, IMMEDIATELY persist that one conclusion by running the verdict-recorder tool, then move on to the next process:
          {_recorder_line(round_num)}
          Run it once per judged process as soon as its analysis is done — never batch all conclusions at the end. The recorder file survives a session timeout; conclusions that live only in your reasoning are lost when the session is killed.

          Write exactly two files in this directory at the END (after every process has been recorded above):
          1. verdict-droid.json with this shape:
          {{
            "processes": [
              {{"id": "process-id", "verdict": "pass" or "fail", "reason": "evidence-based reason"}}
            ],
            "conflicts": [
              {{"process": "process-id", "summary": "what conflicts, both values/sections named", "evidence": "where it is flagged (handoff/status) with a short quote"}}
            ]
          }}
          The top-level "conflicts" array is required in verdict-droid.json: write an empty array when no judged process flagged an out-of-card conflict.
          It must contain exactly one verdict for each judged process listed above, no more, no fewer.
          2. verdict-droid.md — a human-readable report, one section per judged process, naming the evidence you relied on.

          Rules:
          - Pass a process only when its card, handoff, status, diff, and check outputs line up.
          - HARD RULE — a red mandated check is never a pass: if any entry in packs/<id>/checks-exit.json has a non-zero "exit", or packs/<id>/checks-failed.marker exists, you MUST judge that process "fail", however well the five artifacts line up. Alignment proves the evidence is honest, not that the work passed. In the reason, cite the failed check command(s) and exit code(s) from checks-exit.json. One exception: exit 127 recorded because pytest was unavailable does not count under this rule (that is an environment failure, judged via the pack/manifest evidence).
          - If a process's status.json or handoff.md explicitly flags a conflict outside its card or inside the work order itself (for example a body-vs-acceptance mismatch) and neither the card nor the plan addresses it, you MUST record it in the top-level "conflicts" array — do not bury it in a reason and do not silently pass over it. Recording a conflict does not by itself change that process's verdict: judge the card as written; the conflict is escalated for a human to see, and a verdict carrying any escalated conflict is treated as fail by the machine gates.
          - Judge only from the evidence in this directory. Do not modify any evidence file.
          - Be efficient: at most 12 tool calls, then write the verdict files.
          """


def render_validator_prompt(judgeable: list[str], *, round_num: int = 1) -> str:
    """Alias kept for step-code readability; build_validator_prompt is canonical."""
    return build_validator_prompt(judgeable, round_num=round_num)
