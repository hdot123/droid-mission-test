# Handoff: soundex (sub-issue #376, process card "soundex")

## What was requested
Implement American Soundex as a new self-contained module `soundex.py` plus
`tests/test_soundex.py`, for work order #373 (第四十一轮 · adler32／soundex／haversine).
Scope: ONLY these two files (plus this handoff and `team/status/soundex.json`).
Do not touch any existing file, nor `adler32.py`, `haversine.py`, or their tests.

Spec (verbatim from the card):
- `soundex(name: str) -> str`: accepts only non-empty pure ASCII letter strings
  (case-insensitive), otherwise raises ValueError.
- First letter kept as-is (uppercased); subsequent letters mapped: bfpv→1,
  cgjkqsxz→2, dt→3, l→4, mn→5, r→6.
- Vowels aeiouy produce no code and BREAK runs of equal codes; h and w produce
  no code and are TRANSPARENT (do not break runs).
- Adjacent equal codes collapse to one; the first letter's own code participates
  in this collapsing.
- Result: first letter + 3 digits, padded with `0`, truncated to 4 characters.

## What I did
- Created `soundex.py`: single function `soundex`, no imports of adler32 or
  haversine (no imports at all). Validation via `isinstance(str)` +
  `str.isascii()` and `str.isalpha()` (rejects `""`, `"A1"`, `"O'Brien"`,
  and non-str inputs). Encoding walk: vowels set `prev = None` (break), `h`/`w`
  are skipped entirely (transparent), other letters append code when it differs
  from `prev`. First letter's code seeds `prev`, so it participates in
  collapsing (e.g. `"BB"` → `B000`, `"Babb"` → `B100`).
- Created `tests/test_soundex.py`: one test case per acceptance item from the
  card (21 tests: 18 positive values incl. `robert` lowercase, plus 3
  ValueError cases `""`, `"A1"`, `"O'Brien"`).

## What I did NOT do
- Did not modify, move, or delete any pre-existing file.
- Did not create `adler32.py`, `haversine.py`, or their tests (other processes own them).
- Did not commit or push anything.
- Did not add tests beyond the acceptance items (scope-limited).

## Checks run and results
From the repository root:
1. `python3 -m pytest tests/test_soundex.py -q` → **21 passed**
2. `python3 -m pytest tests/ -q` → **32 passed** (includes pre-existing
   `test_roman.py` / `test_legacy_stringkit.py`, unchanged)

Note: the environment initially lacked pytest; I installed it with
`python3 -m pip install pytest` (pytest 9.2.0) so the required checks could run.
No repository files were affected by this.

## What the validator must pay attention to
- Both required checks pass as written; the full-suite count (32) includes the
  11 pre-existing tests, so expect the suite total to grow once adler32 and
  haversine land.
- Edge cases encoded by the spec that are easy to get wrong: `"BB"` → `B000`
  (first letter's code collapses with the second B), `"Tymczak"` → `T522`
  (the `y` vowel breaks the `m`/`cz`... i.e. m→5, y breaks, c→2, z collapses
  with c, a breaks, k→2), `"Pfister"` → `P236` (p and f both code 1, collapse
  to one; first-letter P participates).
- Only `soundex.py` and `tests/test_soundex.py` are new from this process;
  `team/handoffs/soundex.md` and `team/status/soundex.json` were also written
  as required by the workflow instructions.
