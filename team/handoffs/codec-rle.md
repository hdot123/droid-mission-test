# Handoff: codec-rle (sub-issue #271)

## What was requested
Process card "Implement codec_rle plugin and its tests" under work order #269 (round 34, foreman v2.6.5):
- Own exactly `codec_rle.py` and `tests/test_codec_rle.py`.
- `codec_rle.py` must register a codec named `"rle"` into the stock `codecbox` directory **on import** via `codecbox.add_codec("rle", encode, decode)`.
- `encode(text)` writes each run of consecutive identical characters as character + run length: `"aaab"` -> `"a3b1"`, `"abc"` -> `"a1b1c1"`, `""` -> `""`.
- `decode(text)` is the exact inverse of encode (input limited to English letters); encode/decode round-trip consistently.
- Acceptance points the tests must assert verbatim: `codecbox.get_codec("rle")` pair satisfies the examples with round-trip consistency; after importing this module, `codecbox.pipeline_encode("aaab") == "a3b1"`.
- Python standard library only; no package directory, no CLI; `codec_rle.py` may depend only on stock `codecbox` and must not import `codec_flip` or `bracecheck`; the test file must test only `codec_rle`'s behavior.
- 归因禁令 (hard rule): no `codecbox.reset()`, no `importlib.reload` / re-import tricks, no delete-then-re-register, no clearing shared state before asserting; never modify `codecbox.py` or `tests/test_codecbox.py`.

## What I did
- Created `codec_rle.py`:
  - `import codecbox` (standard library / stock module only; no imports of `codec_flip` or `bracecheck`).
  - `encode(text)`: iterates runs of consecutive identical characters, appends `char + str(len)` per run; `""` returns `""` directly.
  - `decode(text)`: parses `char + digits` pairs and reconstructs the run; `""` returns `""`.
  - Calls `codecbox.add_codec("rle", encode, decode)` at module level (bottom of file), so importing the module registers the codec.
- Created `tests/test_codec_rle.py` with 5 tests:
  - `test_rle_encode_examples` — asserts verbatim: `encode("aaab") == "a3b1"`, `encode("abc") == "a1b1c1"`, `encode("") == ""`.
  - `test_rle_decode_examples` — asserts verbatim: `decode("a3b1") == "aaab"`, `decode("a1b1c1") == "abc"`, `decode("") == ""`.
  - `test_rle_roundtrip` — round-trip consistency on `""`, `"a"`, `"aaab"`, `"abc"`, `"aabbccca"`, `"zzzzz"`.
  - `test_rle_registered` — asserts `"rle" in codecbox.codec_names()`.
  - `test_rle_pipeline_encode` — asserts `codecbox.pipeline_encode("aaab") == "a3b1"` (imports `codec_rle` so the codec is registered before the pipeline assertion).
  - Tests use only `codecbox.get_codec` / `codecbox.codec_names` / `codecbox.pipeline_encode`; **no** `reset()`, **no** `importlib.reload`, **no** state-clearing of any kind.

## What I did not do
- Did not create, modify, or delete `codec_flip.py`, `tests/test_codec_flip.py`, `bracecheck.py`, `tests/test_bracecheck.py`, or any other process's files.
- Did not modify or delete the stock files `codecbox.py` and `tests/test_codecbox.py` (verified unmodified by check below).
- Did not commit or push anything.
- Did not touch the shared directory state (`codecbox.reset()` never called by me or my tests).

## Checks I ran and their results
1. `python -m pytest -q tests/test_codec_rle.py` — **5 passed in 0.02s** (exit 0).
2. `git diff --exit-code -- codecbox.py tests/test_codecbox.py` — **exit 0**, no diff (stock files unchanged).

Note: `pytest` was not preinstalled in this environment; I installed it with `pip install pytest` (pytest 9.2.0) to run the mandated check command. This only affects the local tooling, not the repository.

## What the validator must pay attention to
- Import order matters: `tests/test_codec_rle.py` does `import codec_rle` at module level, which registers `"rle"` before any test runs, so `pipeline_encode("aaab") == "a3b1"` holds because `rle` is the only codec registered at that point in a fresh process (stock codecs are registered by the stock test file, which runs in its own test session/process under the acceptance commands).
- The acceptance commands in the card are per-file; I ran exactly those two verbatim commands with the results above.
- 归因禁令 was honored: no isolation tricks appear anywhere in my code or tests; any future failure must be attributed from in-process evidence only (failure output, test file, source text, import/registration order).
- The pipeline assertion depends on `rle` being registered exactly once on import; `codecbox.add_codec` overwrites same-name entries but keeps registration order, so re-import is idempotent for the pipeline result.
