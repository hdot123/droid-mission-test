"""Extract lead-plan segment fixtures from round-51 droid lead streams.

Turns the successful Create/Write tool calls aimed at
team/lead-plan-segments/*.json in a droid stream JSONL into on-disk segment
files, plus a writes.json protocol log. Used to build the r51A-D replay
fixtures (real round-51 artifacts) and to cross-check them against the
adversarial-review reconstructions.

Run standalone:
    python3 extract_lead_segments.py <stream.jsonl> <out-dir> [meta.json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SEGMENT_PATH_RE = re.compile(r"team/lead-plan-segments/([^/]+\.json)$")
SEGMENT_BASENAME_RE = re.compile(r"^(?:00-header|process-[a-z0-9][a-z0-9-]*)\.json$")


def extract_segments(stream_path: Path) -> dict:
    writes: list[dict] = []
    ok_call_ids: set[str] = set()
    for line in stream_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        etype = event.get("type")
        if etype == "tool_result" and not event.get("isError"):
            ok_call_ids.add(str(event.get("id")))
        elif etype == "tool_call":
            tool = str(event.get("toolName"))
            params = event.get("parameters") or {}
            match = SEGMENT_PATH_RE.search(str(params.get("file_path", "")))
            if tool not in ("Create", "Write") or not match:
                continue
            writes.append(
                {
                    "tool": tool,
                    "basename": match.group(1),
                    "tool_call_id": str(event.get("id")),
                    "call_ok": False,
                    "content": params.get("content"),
                }
            )
    for write in writes:
        write["call_ok"] = write["tool_call_id"] in ok_call_ids

    files: dict[str, dict] = {}
    for write in writes:  # stream order; last successful write wins
        if not write["call_ok"]:
            continue
        try:
            doc = json.loads(write["content"])
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(doc, dict):
            files[write["basename"]] = doc

    return {
        "files": files,
        "writes": [
            {k: v for k, v in w.items() if k != "content"} for w in writes
        ],
    }


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(__doc__, file=sys.stderr)
        return 2
    stream_path = Path(argv[1])
    out_dir = Path(argv[2])
    result = extract_segments(stream_path)
    seg_dir = out_dir / "team" / "lead-plan-segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    for basename, doc in result["files"].items():
        if not SEGMENT_BASENAME_RE.fullmatch(basename):
            print(f"skip non-segment basename: {basename}", file=sys.stderr)
            continue
        (seg_dir / basename).write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if len(argv) == 4:
        Path(argv[3]).write_text(
            json.dumps(result["writes"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"{stream_path.name}: {len(result['files'])} segment file(s) -> {seg_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
