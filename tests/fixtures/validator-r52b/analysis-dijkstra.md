
### dijkstra
- Card: files dijkstra.py, tests/test_dijkstra.py; spec detailed; checks: two pytest commands.
- Diff: only creates dijkstra.py (84 lines) and tests/test_dijkstra.py (73 lines). No other files. Good.
- Does the implementation match spec?
  - Validation walks whole graph: non-dict graph → TypeError; non-str node → TypeError; non-dict adjacency → TypeError; bool/non-numeric weight → TypeError; negative → ValueError. ✓
  - dist contains every node (key or neighbor) ✓; unreachable = math.inf ✓; source = 0 ✓.
  - prev contains only reachable non-source → predecessor ✓ (only set on relaxation).
  - source not in graph → ValueError ✓ (checks `source not in nodes`).
  - shortest_path: both ends included ✓, unreachable → [] ✓, source == target → [source] ✓ (after endpoint existence checks), either endpoint missing → ValueError ✓.
  - No cross-imports (only `math`) ✓; tests import pytest only ✓.
- Tests cover acceptance items:
  - G1 dist/prev: A=0, B=1, C=3, D=4, E=inf, prev ✓  - G1 paths: A→D, A→C, A→E=[], A→A=[A], D→A=[] ✓
  - G2: T=2.0, U=1.5, prev, path ✓
  - G3: B=7, prev ✓
  - ValueError cases: negative weight, source Z, target Z ✓
  - TypeError cases: list graph, "x" weight, True weight ✓
  - That's 10 test functions → matches "10 passed" in checks-output ✓
- Checks: `10 passed` exit 0; full suite `192 passed, 1 skipped` exit 0 ✓- status.json: says `python3 -m pytest tests/ -q` → "147 passed, 1 skipped" while checks-output.txt says "192 passed, 1 skipped". Hmm — this is a mismatch between status.json and checks-output.txt.

Wait, is this a "conflict"? The rule about conflicts: "If a process's status.json or handoff.md explicitly flags a conflict outside its card or inside the work order itself (for example a body-vs-acceptance mismatch)". The status.json's stale full-suite count (147) vs the pack's checks-output (192) — that's an internal artifact inconsistency, not an out-of-card conflict explicitly flagged. The handoff itself explains: "the full-suite run includes other workers' concurrent files if they landed, so a full-suite count above 148 may reflect their additions, not mine." So the handoff explains that the full-suite count varies. The status says 147 while checks-output says 192. That's a discrepancy but it's not an explicitly-flagged out-of-card conflict. It's an alignment nuance.

The pass rule: "Pass a process only when its card, handoff, status, diff, and check outputs line up."

Hmm. For dijkstra: status.json claims `147 passed, 1 skipped` for full suite, but the pack's checks-output.txt (the pack evidence) shows `192 passed, 1 skipped`. The handoff also says `147 passed, 1 skipped`. So handoff and status agree with each other (147) but disagree with checks-output (192).

Actually wait — let me think about this more carefully. The checks-output.txt is the pack's actual recorded run. The handoff/status reported147 (their own run at their time). The merged candidate's pytest-output shows 192 passed, 1 skipped — which matches the pack checks-output full-suite runs (192). So the worker's own full-suite run in the pack recorded 192, but handoff/status claimed 147.

Hmm, but is that a genuine misalignment? Let's consider: the worker ran checks, output captured in checks-output.txt shows 192. The handoff says 147. So there's an inconsistency between handoff/status numbers and the check output.

But is this material? The key hard facts:
- Per-test counts (10 passed for dijkstra's own test file) match between status (10 passed), handoff (10 passed), checks-output (10 passed). ✓
- Full-suite count differs: status/handoff 147 vs checks-output 192.

Interesting: for nthprime: status/handoff say `141 passed, 1 skipped`, checks-output says `192 passed, 1 skipped`. Again mismatch.
For windscale: status/handoff say `178 passed, 1 skipped`, checks-output says `192 passed, 1 skipped`. Mismatch again.

So all three have the same pattern: handoff/status report a lower full-suite count (their own run time, before other workers' files landed), while checks-output.txt records 192 (consistent across all three, and matching the merged candidate pytest-output of 192).

Hmm wait — but that's odd. checks-output.txt for all three shows exactly192 passed, 15.41/15.42/15.44s — these look like the same run re-recorded per pack. Actually the times differ slightly (15.41, 15.42, 15.44) — three separate runs, all after merge presumably, all showing 192.

Actually, the checks-output.txt is the pack's evidence of running the mandated checks. It shows exit 0 for both commands. The full-suite count of 192 matches the merged pytest-output (192 passed, 1 skipped). The handoff/status numbers (147/141/178) were the worker's own earlier runs when fewer concurrent files existed.

Is that a "conflict" to record in the top-level conflicts array? The rule says: status.json or handoff.md must "explicitly flag a conflict outside its card or inside the work order itself (for example a body-vs-acceptance mismatch)". The workers did not flag a conflict; they just reported numbers from their own run time, and the handoff for dijkstra explicitly notes the full-suite count may vary: "the full-suite run includes other workers' concurrent files if they landed, so a full-suite count above 148 may reflect their additions, not mine."

So no process explicitly flags an out-of-card conflict. The conflicts array should be empty... unless there's something else.

Wait — let me check for body-vs-acceptance mismatches. Let me re-check the acceptance items vs tests carefully.

**dijkstra acceptance items:**
- G1 dist: A=0, B=1, C=3, D=4, E=math.inf ✓ test
- prev == {"B": "A", "C": "B", "D": "C"} ✓
- shortest_path(G1, "A", "D") == ["A", "B", "C", "D"] ✓
- shortest_path(G1, "A", "C") == ["A", "B", "C"] ✓
- shortest_path(G1, "A", "E") == [] ✓
- shortest_path(G1, "A", "A") == ["A"] ✓
- shortest_path(G1, "D", "A") == [] ✓
- G2: dist["T"] == 2.0, dist["U"] == 1.5, prev, path ✓
- G3: dist["B"] == 7, prev == {"B": "A"} ✓
- dijkstra({"A": {"B": -1}}, "A") ValueError ✓; dijkstra(G1, "Z") ValueError ✓; shortest_path(G1, "A", "Z") ValueError ✓
- dijkstra([("A", {})], "A") TypeError ✓; {"A": {"B": "x"}} ✓; {"A": {"B": True}} ✓

All 10 test functions cover everything. Card says "10 test functions" claim in handoff — checks-output says 10 passed ✓.

Implementation correctness: Let me think about the Dijkstra implementation. `dist = {node: math.inf for node in nodes}; dist[source] = 0`. Loop: pick unvisited with min dist; if current is None (all remaining have inf), break. Relax neighbors. Looks correct.

One subtlety: `if candidate < dist[neighbor]` — with source dist 0 and non-negative weights, fine.

`prev` only set when relaxing — source never in prev ✓; unreachable never relaxed → not in prev ✓.

shortest_path: validates graph, checks source/target in nodes → ValueError; source == target → [source]; then dijkstra; if inf → []; walk prev. Correct.

Edge: `nodes, _ = _validate_graph(graph)` then `if source not in nodes`. Note `source not in nodes` — nodes is a set of str. If source is unhashable (e.g., list), `in` raises TypeError — but spec doesn't cover that. Fine.
