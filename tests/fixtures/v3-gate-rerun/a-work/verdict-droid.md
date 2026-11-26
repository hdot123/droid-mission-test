# Validator Report (squad-leader acceptance)

Judged processes: damm, easterorthodox, graph. Verdicts were persisted via
`salvage_verdict` one process at a time, and the final conclusion was sealed
with `--final`. No out-of-card conflicts were found.

## damm — PASS

Evidence relied on:
- `packs/damm/process-card.json` — card scope: only `damm.py` and `tests/test_damm.py`, standard library only, no cross-imports.
- `packs/damm/diff.patch` — new files only; `_TABLE` matches all 10 pinned rows of the quasi-group table exactly; TypeError checked before emptiness; ValueError for empty string and any non-ASCII-digit character; `damm_check_digit` returns `str(final_interim)` with no extra transform (diagonal all zeros), `damm_validate` returns `final_interim == 0`, per spec.
- `packs/damm/handoff.md` — 18 tests, one per acceptance point plus edge guards; all 16 mandated acceptance points mapped to dedicated test functions (verified 1:1 in the diff: `572→"4"`, `5724→True`, `5742→False`, `123→"4"`, `0→"0"`, `42→"7"`, `987654321→"5"`, `2024→"0"`, `1234→True`, `1235→False`, `427→True`, TypeError on `572` int, ValueError on `""`/`"57a"`/`"57 24"`).
- `packs/damm/checks-exit.json` — both mandated checks exit 0.
- `packs/damm/checks-output.txt` — `tests/test_damm.py`: 18 passed; `tests/`: 240 passed, 2 skipped.
- No `checks-failed.marker` present.

Note (bookkeeping, not a conflict): handoff.md and status.json report the full
suite as "205 passed, 2 skipped" while checks-output.txt shows "240 passed,
2 skipped". Per the rules this is a pre-merge count difference; both runs
exited 0 and the merged `pytest-output.txt` (240 passed, 2 skipped) agrees
with checks-output.txt.

## easterorthodox — PASS

Evidence relied on:
- `packs/easterorthodox/process-card.json` — card scope: only `easterorthodox.py` and `tests/test_easterorthodox.py`, standard library only, no cross-imports.
- `packs/easterorthodox/diff.patch` — implements the pinned two-step algorithm verbatim: Julian computus (`a=year%4`, `b=year%7`, `c=year%19`, `d=(19c+15)%30`, `e=(2a+4b−d+34)%7`, Julian month/day from `(d+e+114)`), then Gregorian offset `(year//100 − year//400 − 2)` days; bool rejected as TypeError; range 1583–9999 enforced with ValueError.
- Independent spot-verification of the computus against the pinned dates reproduced: 2024=(5,5), 2025=(4,20), 2016=(5,1), 2010=(4,4), 1900=(4,22), 2000=(4,30), 2100=(5,2). All correct.
- `packs/easterorthodox/handoff.md` — 18 tests; all 17 acceptance points covered in the diff (12 parametrized dates, ValueError for 1582/10000, TypeError for 2024.0/"2024"/True, plus a return-shape test).
- `packs/easterorthodox/checks-exit.json` — both mandated checks exit 0.
- `packs/easterorthodox/checks-output.txt` — `tests/test_easterorthodox.py`: 18 passed; `tests/`: 240 passed, 2 skipped.
- No `checks-failed.marker` present.

Same bookkeeping note as above (handoff/status "205 passed" vs checks-output
"240 passed"): pre-merge count difference, both exit 0, no conflict.

## graph — PASS

Evidence relied on:
- `packs/graph/process-card.json` — card scope: only `graph.py` and `tests/test_graph.py`, standard library only, no cross-imports.
- `packs/graph/diff.patch` — API matches the spec exactly: str-only node names, idempotent `add_node`, `add_edge` with TypeError on non-str endpoints, ValueError on self-loops, auto-add of missing endpoints, duplicate edges as no-op (set-based adjacency), sorted `nodes()`/`neighbors()`, BFS enqueueing unvisited neighbors in lexicographic order at dequeue time, recursive-preorder DFS, `connected_components()` ordered by each component's smallest element (achieved by iterating `nodes()` in sorted order), `has_path` with ValueError on missing endpoints and True for `u == v` in-graph.
- Independent hand-verification of the reference graph G (edges a-b, a-c, b-d, c-d, d-e plus isolated z): `bfs("a")` = [a, b, c, d, e] ✓; `dfs("a")` = [a, b, d, c, e] ✓; `bfs("z")` = [z] ✓; `neighbors("d")` = [b, c, e] ✓; `connected_components()` = [[a..e], [z]] ✓. For G2 (m-n, m-o, n-p, o-p, p-q): `bfs("m")` = [m, n, o, p, q] ✓; `dfs("m")` = [m, n, p, o, q] ✓.
- `packs/graph/handoff.md` — 17 tests covering every acceptance point verbatim, plus consistent hardening tests (empty-graph `has_path`, idempotent `add_node`, non-str on either side of `add_edge`).
- `packs/graph/checks-exit.json` — both mandated checks exit 0.
- `packs/graph/checks-output.txt` — `tests/test_graph.py`: 17 passed; `tests/`: 240 passed, 2 skipped.
- No `checks-failed.marker` present.
- `packs/graph/status.json` lists `team/handoffs/graph.md` and `team/status/graph.json` in its files array: these are whitelisted protocol artifacts maintained by the pipeline, not out-of-card writes, so not a conflict.

Same bookkeeping note (handoff/status "204 passed" vs checks-output "240
passed"): pre-merge count difference, both exit 0, no conflict.

## Merged candidate evidence

`pytest-output.txt` / `pytest-exit.txt`: full merged suite 240 passed,
2 skipped, exit 0. Consistent with each pack's full-suite check output.

## Conflicts

None. No process flagged an out-of-card conflict; the "conflicts" array in
`verdict-droid.json` is empty.
