# Handoff: codec-flip (sub-issue #272)

## What was requested (process card #272, "codec-flip")
Implement the `flip` codec plugin for the stock `codecbox` directory, owning exactly two files:

- `codec_flip.py`: on import, register a codec named `"flip"` into `codecbox` by calling `codecbox.add_codec("flip", encode, decode)`, where both `encode` and `decode` simply reverse the string. Acceptance points: after import, `"flip" in codecbox.codec_names()` is True; `codecbox.get_codec("flip")[0]("abc") == "cba"`.
- `tests/test_codec_flip.py`: assert exactly those acceptance points (name present in `codec_names()`, encode `("abc") == "cba"`, decode reversing as specified), plus a roundtrip.

Constraints: Python standard library only; no package directory, no CLI; `codec_flip.py` may depend only on the stock `codecbox` and must not import `codec_rle` or `bracecheck`; the test file must test only `codec_flip`'s behavior. The stock files `codecbox.py` and `tests/test_codecbox.py` (存量两文件) must remain untouched. Attribution ban: no `codecbox.reset()`, no `importlib.reload`/re-import tricks, no delete-then-re-register, no clearing shared state before asserting.

## What I did
- Created `codec_flip.py`: defines module-level `encode(text)` and `decode(text)` both returning `text[::-1]`, then calls `codecbox.add_codec("flip", encode, decode)` at import time. Imports only the stock `codecbox`.
- Created `tests/test_codec_flip.py`: imports `codec_flip` (triggering registration) and `codecbox`, and asserts:
  1. `test_flip_name_in_codec_names` — `"flip" in codecbox.codec_names()`;
  2. `test_flip_encode_reverses` — `codecbox.get_codec("flip")[0]("abc") == "cba"`;
  3. `test_flip_decode_reverses` — `codecbox.get_codec("flip")[1]("abc") == "cba"`;
  4. `test_flip_roundtrip` — `decode(encode("abc")) == "abc"` and `encode(decode("abc")) == "abc"`.
  The test file contains no `reset()`, no `importlib.reload`, no re-registration, no state clearing.

## What I did NOT do
- Did not create or modify `codec_rle.py`, `bracecheck.py`, or any tests for them (owned by other processes).
- Did not modify or delete `codecbox.py` or `tests/test_codecbox.py` (存量两文件原样未动).
- Did not call `codecbox.reset()` or use any reload/re-import isolation in tests or attribution.
- Did not add package directories, CLI entry points, or any non-standard-library dependency.
- Did not commit or push anything.

## Checks I ran and their results
1. `python -m pytest -q tests/test_codec_flip.py` → exit 0, `4 passed in 0.01s`.
2. `git diff --exit-code -- codecbox.py tests/test_codecbox.py` → exit 0, no diff (stock files untouched).

Environment note: `pytest` was not installed in the environment initially (`python -m pytest` failed with "No module named pytest"); I installed it via `python3 -m pip install pytest` (got 9.2.0), then ran both checks verbatim as given on the card. Both passed. The `git diff --exit-code` check also passed before and after pytest installation.

## What the validator must pay attention to
- Registration is import-time: `codec_flip.py` must be imported before the `codec_names()`/`get_codec()` assertions can hold. The test file does this with a top-level `import codec_flip  # noqa: F401`. In a full-suite run, any process whose tests import `codec_flip` first is fine because registration is idempotent-per-name (re-import of the same module is a no-op in Python; `add_codec` with the same name just overwrites with equivalent functions).
- Both `encode` and `decode` are pure reversals, so roundtrip holds regardless of import/registration order of other codecs.
- `pipeline_encode` behavior is not asserted here (that belongs to the `codec_rle` card); no cross-assertions on other codecs exist in this test file.
- The attribution ban was honored: no `reset()`, `reload`, or shared-state clearing appears in `tests/test_codec_flip.py`.
