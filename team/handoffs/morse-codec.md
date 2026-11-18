# Handoff: morse-codec (sub-issue #307)

## What was requested
Implement process card `morse-codec` from work order #305 (第三十七轮 · 常规组二): create `morse.py` and `tests/test_morse.py` as NEW files only, touching no existing file (including `README.md`, `legacy_stringkit.py`, `roman.py`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`).

Spec (verbatim from the card):
- International Morse code for A–Z and 0–9, mapping table inside the module (no external data).
- `encode(text: str) -> str`: uppercase input, encode letter by letter, letters separated by a single space, words (original spaces) separated by ` / `; any character outside A–Z, 0–9, space raises `ValueError`; empty string returns empty string.
- `decode(code: str) -> str`: inverse, returns uppercase text with words separated by a single space; unknown code groups or malformed forms such as consecutive multiple spaces raise `ValueError`; empty string returns empty string.
- One test case for EVERY acceptance item: `encode("SOS") == "... --- ..."`, `encode("HELLO") == ".... . .-.. .-.. ---"`, `encode("123") == ".---- ..--- ...--"`, `encode("SOS SOS") == "... --- ... / ... --- ..."`, `decode("... --- ...") == "SOS"`, `encode("sos") == "... --- ..."` (lowercase auto-uppercased), `encode("HI!")` raises ValueError, round-trip identity for `"MORSE CODE 2026"`. Standard library only.

## What I did
- Created `morse.py`: module-level `MORSE` dict (A–Z, 0–9 → code strings), derived reverse `DECODE` dict, `encode()` and `decode()` as specified. Validation raises `ValueError` on unsupported characters (encode) and unknown/malformed code groups, consecutive spaces, or empty words (decode). Both functions return `""` for `""`.
- Created `tests/test_morse.py`: 10 tests covering all 8 verbatim acceptance items plus empty-string edge cases for both functions.
- Installed `pytest` (was not present in the environment: `python3: No module named pytest`) so the required checks could run.

## What I did NOT do
- Did not modify any existing file.
- Did not touch `levenshtein.py`, `collatz.py`, or their tests (owned by other processes).
- Did not add imports of any other deliverable module; only the standard library (`pytest` for tests, as the repo's existing tests already use).
- Did not commit or push.

## Checks run and results
- `python3 -m pytest tests/test_morse.py -q` → **10 passed**
- `python3 -m pytest tests/ -q` → **21 passed** (morse 10 + existing roman/legacy_stringkit 11)

## Validator notes
- The module exposes `MORSE` and `DECODE` as public names (the card required the mapping table to live inside the module); only `encode`/`decode` are specified API, the dicts are incidental.
- `encode` splits on single spaces and rejects empty words, so `"A  B"` (double space) raises `ValueError`; `decode` likewise rejects consecutive spaces and empty words, matching the "不合规形态" requirement.
- Case handling: `encode` uppercases via `str.upper()`, so `"sos"` → `"... --- ..."` as required; `decode` output is always uppercase by construction.
- Environment note: pytest had to be pip-installed; if the validator's environment already has it, that is a no-op difference.
