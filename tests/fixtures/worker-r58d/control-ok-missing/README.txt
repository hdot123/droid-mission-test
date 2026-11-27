control-ok-missing: SYNTHETIC contrast fixture (not verbatim CI evidence).

Contrast target: the verbatim fixture at the parent directory (CI run
45812793849, see ../PROVENANCE.txt). The parent fixture records the real
death: wall-killed session while the machine checks were green. This
control keeps the same run shape — branch merged, checks green, pack
missing handoff/status, complete false — but flips the session outcome to
healthy: worker-delta.json carries session_outcome "ok",
droid_exit_code 0, stream_tail_marker false, and
worker-stream-tail.jsonl is a synthetic normal-completion session tail
written in the same event schema as the real run's stream: an assistant
message that carries no interrupt marker and is not an error result.

Purpose: fail-closed guard replay. A normally-completed session that
still fails to write handoff/status is a true compliance failure — no
machine salvage may paper over it. Consumers (the salvage guard's
negative case, and any future replan attribution branch) must keep this
shape judged blocked, never salvaged, never re-attributed.

Self-consistency is enforced byte-level: manifest.json's sha256 table
attests every other file in this directory (digests written in the same
change that wrote the files; verified by
tests/test_worker_r58d_fixtures.py).
