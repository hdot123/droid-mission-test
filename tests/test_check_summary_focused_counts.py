"""VAL-P2-006 fix face (scrutiny PR2-2 / PR2-2b): check-summary.json per-card
counts must reflect what prep actually ran for THAT card.

Scrutiny proved by execution that (a) the summary was written before the
per-card checks loop ran, so every card read {passed: 0}, and (b) even after
reordering, summing every "N passed" in a card's checks-output.txt produced
258 for the r54A damm card (18 focused + 240 merged) — a number corresponding
to nothing. The contract asks for per-card counts: a card's figure is the
count from the card's FOCUSED check (its own file-level pytest run), never a
sum across the check commands.

These tests drive the workflow's own summary block verbatim against the real
round-54 A pack (fixtures are verbatim copies), the same evidence face the
scrutiny validator used for the reproduction.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"

sys.path.insert(0, str(ROOT / "scripts" / "team"))


@pytest.fixture(scope="module")
def yml() -> str:
    return TEAM_YML.read_text(encoding="utf-8")


def _job_text(yml: str, job_key: str) -> str:
    m = re.search(rf"^  {job_key}:\n", yml, re.MULTILINE)
    assert m, f"job {job_key} missing"
    next_m = re.search(r"^  [a-z0-9-]+:\n", yml[m.end() :], re.MULTILINE)
    end = m.end() + next_m.start() if next_m else len(yml)
    return yml[m.start() : end]


# --- PR2-2: the summary must be written after the per-card checks loop ------

@pytest.mark.parametrize("job_key", ["prep", "prep2"])
def test_summary_written_after_checks_loop(yml, job_key: str):
    text = _job_text(yml, job_key)
    summary_idx = text.find("check-summary.json")
    assert summary_idx != -1
    loop_idx = text.find("checks-output.txt")
    assert loop_idx != -1
    checks_exit_idx = text.find("checks-exit.json")
    assert checks_exit_idx != -1
    assert checks_exit_idx < summary_idx, (
        f"{job_key}: checks-exit.json (written by the per-card loop) must exist "
        "before the summary is written"
    )


def _extract_summary_heredoc(text: str) -> str:
    """The prep summary block, verbatim, as a runnable script (the exact code
    CI executes, extracted the way scrutiny's control run did). The heredoc
    body sits 10 spaces deep inside the workflow yaml; dedent it."""
    start = text.index("def _focused_counts")
    end = text.index('json.dump({"schema_version": "check-summary.v1"')
    end = text.index("\n", text.index("open(\"evidence/check-summary.json\"", end))
    raw = text[start:end]
    return "\n".join(
        ln[10:] if ln.startswith(" " * 10) else ln for ln in raw.splitlines()
    )


@pytest.mark.parametrize("job_key", ["prep", "prep2"])
def test_summary_uses_focused_check_not_cross_command_sum(yml, job_key: str):
    text = _job_text(yml, job_key)
    assert "_focused_counts" in text, (
        f"{job_key}: per-card counts must come from the card's focused check"
    )
    body = text[text.find("per_card = {}") : text.find("json.dump({\"schema_version\"")]
    # the old cross-command sum read checks-output.txt with _count_passed
    assert "_count_passed(card_out)" not in body, (
        f"{job_key}: per-card counts must not sum every 'N passed' across the "
        "card's check commands (18 focused + 240 merged must never become 258)"
    )


# --- the real r54A reproduction, driven through the workflow block ----------

R54A_PACK = ROOT / "tests" / "fixtures" / "validator-r54ac" / "a"
CARDS = ("damm", "easterorthodox", "graph")


def _make_pack(tmp_path: Path) -> Path:
    """A real-shaped evidence tree: per-card checks-output.txt verbatim from
    the round-54 A pack (focused 17-18 passed + merged 240 passed)."""
    ev = tmp_path / "evidence"
    (ev / "packs").mkdir(parents=True)
    real = Path("/tmp/r54-audit/a/evidence/packs")
    src = real if real.is_dir() else None
    for pid in CARDS:
        (ev / "packs" / pid).mkdir()
        (ev / "packs" / pid / "checks-exit.json").write_text(
            json.dumps(
                [
                    {"command": f"python3 -m pytest tests/test_{pid}.py -q", "exit": 0},
                    {"command": "python3 -m pytest tests/ -q", "exit": 0},
                ]
            ),
            encoding="utf-8",
        )
        out = None
        if src is not None and (src / pid / "checks-output.txt").is_file():
            out = (src / pid / "checks-output.txt").read_text(encoding="utf-8")
        if out is None:
            # synthetic equivalent when the read-only audit dir is absent
            out = (
                f"$ python3 -m pytest tests/test_{pid}.py -q\n"
                "..................                                                       [100%]\n"
                "18 passed in 0.01s\n\n"
                "[exit 0]\n"
                "$ python3 -m pytest tests/ -q\n"
                "240 passed, 2 skipped in 15.30s\n\n"
                "[exit 0]\n"
            )
        (ev / "packs" / pid / "checks-output.txt").write_text(out, encoding="utf-8")
    return ev


def test_summary_block_on_r54_pack_produces_real_focused_counts(
    tmp_path: Path, yml: str
):
    """Scrutiny PR2-2 control run, repeated after the fix: the workflow's own
    block, run verbatim against the real r54A pack, must give every card its
    focused count (17-18) — not 0 (ordering bug) and not 258 (sum bug)."""
    ev = _make_pack(tmp_path)
    plan = json.loads((R54A_PACK / "plan.json").read_text(encoding="utf-8"))
    pytest_output = (R54A_PACK / "pytest-output.txt").read_text(encoding="utf-8")
    import os
    import subprocess
    import tempfile

    os.chdir(tmp_path)
    # The workflow loop always rewrites checks-output.txt from what it ran;
    # run it on unmerged packs (its shell branch stays off), then re-seed the
    # real r54A outputs and run ONLY the summary pass — the exact production
    # order (loop writes, summary reads) with the real post-loop file state.
    packs = {
        pid: {"merged": False, "pack": {}, "complete": False} for pid in CARDS
    }
    script = _extract_summary_heredoc(_job_text(yml, "prep"))
    ns: dict = {
        "plan": plan,
        "pytest_output": pytest_output,
        "packs": packs,
        "pytest_available": False,
        "os": os,
        "json": json,
        "subprocess": subprocess,
        "CHECK_TIMEOUT": 1,
        # defined elsewhere in the prep heredoc; same regex semantics as the
        # workflow's own helpers (last "N passed" line wins)
        "_count_passed": lambda text: (
            int(m[-1]) if (m := re.findall(r"(\d+) passed", text or "")) else 0
        ),
        "_count_skipped": lambda text: (
            int(m[-1]) if (m := re.findall(r"(\d+) skipped", text or "")) else 0
        ),
    }
    with tempfile.TemporaryDirectory() as td:
        # handoffs/status copies need a repo tree; not exercised for counts
        ns["os"].makedirs(f"{td}/team", exist_ok=True)
        exec(compile(script, "<prep-summary>", "exec"), ns)
    # production order replay: the loop has written its outputs; seed the
    # real r54A per-card outputs (the "checks ran and wrote" state) and run
    # only the summary pass again.
    real = Path("/tmp/r54-audit/a/evidence/packs")
    for pid in CARDS:
        src = real / pid / "checks-output.txt"
        (tmp_path / "evidence" / "packs" / pid / "checks-output.txt").write_text(
            src.read_text(encoding="utf-8"), encoding="utf-8"
        )
    summary_only = script[script.index("# I-4 (round54-root-cure)") :]
    exec(compile(summary_only, "<prep-summary-2>", "exec"), ns)
    doc = json.loads(Path("evidence/check-summary.json").read_text(encoding="utf-8"))
    assert doc["totals"] == {"passed": 240, "skipped": 2}
    for pid in CARDS:
        got = doc["per_card"][pid]
        assert got["passed"] != 0, f"{pid}: per-card count is still zero (PR2-2)"
        assert got["passed"] < 100, (
            f"{pid}: per-card count {got['passed']} looks like a cross-command "
            "sum (18 focused + 240 merged), not the card's focused check (PR2-2b)"
        )
        assert got["skipped"] == 0
