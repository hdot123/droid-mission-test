# Handoff: pctform-codec (sub-issue #322)

## What was requested
Process card `pctform-codec` for work order #313 (第三十八轮 · 并发 B 单): implement the percent-form
(application/x-www-form-urlencoded value) codec as two new files only —
`pctform.py` and `tests/test_pctform.py` — owning nothing else.

Spec (verbatim from work order):
- `encode(text: str) -> str`: UTF-8 encode the text first; unreserved characters A–Z, a–z, 0–9, `-`,
  `.`, `_`, `~` pass through as-is; space encodes as `+`; all other bytes encode as `%XX` with
  uppercase hex.
- `decode(text: str) -> str`: inverse (`+` → space, `%XX` → bytes then UTF-8 decode); raise
  `ValueError` if `%` is not followed by exactly two hex digits, or the decoded bytes are not valid
  UTF-8.

Acceptance points: `encode("a b&c") == "a+b%26c"`; `encode("~ok") == "~ok"`; `encode("é") == "%C3%A9"`;
`decode("a+b%26c") == "a b&c"`; round-trip identity for `"x y+z%w"`. Plus ValueError cases
(`%zz`, `%A`, invalid UTF-8 like `%FF`).

## What I did
- Created `pctform.py` (repo root): standard-library only, no imports of other project modules.
  - `encode`: iterates over `text.encode("utf-8")` bytes; unreserved set kept as a frozenset of
    byte values; space → `+`; everything else → `%%%02X` (uppercase hex).
  - `decode: single pass over the string: `+` → 0x20, `%` → require two following chars, both hex
    digits (else `ValueError`), non-`%` chars appended as their UTF-8 bytes; finally the accumulated
    bytes are UTF-8 decoded, with `UnicodeDecodeError` converted to `ValueError`.
- Created `tests/test_pctform.py`: 11 test cases covering every acceptance point (all five, each as
  its own test), plus full unreserved pass-through, uppercase hex output, `+` → space, and the three
  ValueError cases (`%zz`, `%A`, `%FF`).
- Environment note: system `python3` had no pytest; installed `pytest` 9.2.0 via `pip3 install
  pytest` so the mandated checks could run (no repository files affected).

## What I did not do
- Did not touch `quotedprint.py`, `hexcodec.py`, or any test file other than `tests/test_pctform.py`.
- Did not modify any pre-existing repository file; no commits, no pushes.
- No soft-wrapping/line-length handling anywhere (that concern belongs to quotedprint's scope).

## Checks run (both required, verbatim)
- `python3 -m pytest tests/test_pctform.py -q` → **11 passed** in 0.02s.
- `python3 -m pytest tests/ -q` → **22 passed** in 0.03s (full suite, including other processes'
  tests).

Both checks were initially run before fixes: two of my own test expectations were wrong/buggy
(a literal `%` in an error message broke %-formatting; U+00FF encodes to `%C3%BF`, not `%FF`).
Fixed in my two files only; both checks now pass.

## What the validator must pay attention to
- Only two repo files were added by this process: `pctform.py`, `tests/test_pctform.py` (plus the
  two team files under `team/`). Nothing else should show as modified.
- `%XX` output is always uppercase (`encode("\x0b") == "%0B"`, `encode("é") == "%C3%A9"`).
- `decode` is strict: `%` at end of string, `%A` (one hex digit), `%zz` (non-hex) and `%FF`
  (lone byte, invalid UTF-8) all raise `ValueError` — none of these may be silently accepted.
- `decode("a+b") == "a b"`: `+` is space only in decode; encode maps space to `+`.
- Round-trip identity holds for `"x y+z%w"` (test exists).
