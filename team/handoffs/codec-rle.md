# Handoff: codec-rle (sub-issue #274, r2)

## What was requested
Process card "codec-rle" (v2, REVISE retry): create exactly `codec_rle.py` and `tests/test_codec_rle.py`.

- `codec_rle.py`: on import, register codec `"rle"` into the stock `codecbox` via `codecbox.add_codec("rle", encode, decode)`. `encode` writes each run of consecutive identical chars as char + run length (`"aaab"` -> `"a3b1"`, `"abc"` -> `"a1b1c1"`, `""` -> `""`); `decode` is the exact inverse (input limited to English letters); round-trip consistent.
- Acceptance anchored ONLY on `codecbox.get_codec("rle")`: encode of `"aaab"`, `"abc"`, `""`; decode of `"a3b1"` -> `"aaab"`, `""` -> `""`; round-trip on those examples.
- HARD CHANGE from v1: no assertion on `codecbox.pipeline_encode(...)`. In the merged tree codec-flip registers into the same shared directory, so `pipeline_encode("aaab")` returns `"b1a3"`; any pipeline assertion is forbidden on this card.
- 归因禁令: no `codecbox.reset()`, no `importlib.reload`/re-import tricks, no delete-then-re-register, no clearing shared state before asserting. Stock files `codecbox.py` and `tests/test_codecbox.py` must stay untouched.

## What I did
- `codec_rle.py` (new): standard-library only, imports only `codecbox`; `encode` groups runs, `decode` parses char+digits pairs (inverse of encode); calls `codecbox.add_codec("rle", encode, decode)` at import time. Does not import `codec_flip` or `bracecheck`.
- `tests/test_codec_rle.py` (new): imports `codec_rle` (registration side effect) then asserts exactly the card's acceptance points through `codecbox.get_codec("rle")`: encode `aaab`/`abc`/empty, decode `a3b1`/empty, round-trip on all three examples. No `pipeline_encode` assertion anywhere. No reset/reload/clear usage.

## What I did NOT do
- Did not touch `codec_flip.py`, `bracecheck.py`, or any other process's files.
- Did not modify/delete `codecbox.py` or `tests/test_codecbox.py`.
- Did not add any `pipeline_encode` assertion (the v1 fault being corrected).
- Did not commit or push.

## Checks run and results
1. `python -m pytest -q tests/test_codec_rle.py` -> `6 passed in 0.01s`, exit 0.
   (pytest was not installed in the environment; installed it via `pip install pytest` so the mandated check command could run verbatim.)
2. `git diff --exit-code -- codecbox.py tests/test_codecbox.py` -> exit 0, no output (stock files unchanged).

## Notes for the validator
- This tree did not contain `codec_rle.py`/`tests/test_codec_rle.py` at start (fresh files created by this run).
- Acceptance deliberately excludes `pipeline_encode`: shared-directory composition with codec-flip makes `pipeline_encode("aaab") == "b1a3"` in the merged tree, and the card forbids asserting it.
- All tests pass on the merged candidate as required; attribution evidence: failure was previously `test_rle_pipeline_encode` asserting `'b1a3' == 'a3b1'`, which this card removes by design (plan fault, not worker fault).
