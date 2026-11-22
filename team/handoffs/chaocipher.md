# Handoff: chaocipher (sub-issue #780, work order #761 并发 A 单)

## What was requested

Process card `chaocipher`: implement `chaocipher.py` (Chaocipher dual-alphabet evolving
substitution cipher) and `tests/test_chaocipher.py`, adding only those two files.
Constraints: standard library only; must not import `centroid`/`base62`; every acceptance
point from the work order must have a corresponding test case; no modification of any
pre-existing file; no commits.

## What I did

- Added `chaocipher.py`:
  - Pinned alphabets: left (ciphertext side) `HXUCZVAMDSLKPEFJRIGTWOBNYQ`, right
    (plaintext side) `PTLNBQDEOYSFAVZKGJRIHWXUMC`, exported as module constants.
  - `_preprocess`: rejects non-`str` with `TypeError`, uppercases, keeps only A–Z.
  - `chaocipher_encrypt(text)` / `chaocipher_decrypt(cipher)`: per letter, index lookup
    in one alphabet drives the other; empty string returns `""`; non-`str` raises
    `TypeError`.
  - Per-letter permutation, same for encrypt and decrypt (decrypt drives it with the
    recovered plaintext letter and the ciphertext letter):
    1. Left: rotate so the just-produced ciphertext letter is at index 0; take the
       letter at index 1; insert it so it lands at index 13 in the pre-removal frame
       (post-pop `insert(12)`).
    2. Right: rotate so the just-consumed plaintext letter is at index 0; rotate the
       alphabet left by one; take the letter at index 2; insert it at index 13 in the
       pre-removal frame (post-pop `insert(12)`).
- Added `tests/test_chaocipher.py`: one test per acceptance point (18 tests) covering
  the pinned alphabets, every named vector (`A`, `AAAA`, `HELLOWORLD`,
  `CHAOCIPHER`, `THEQUICKBROWNFOX`, empty string), preprocessing (`hello world`,
  `HELLO, WORLD!`), all four round trips, and the three `TypeError` cases.

## What I did not do

- Did not touch `centroid.py`, `base62.py`, `tests/test_centroid.py`,
  `tests/test_base62.py`, or any pre-existing file; did not touch anything under
  `team/` other than my own two files.
- Did not add dependencies (stdlib only) and did not import sibling modules.
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_chaocipher.py -q` → **18 passed**
2. `python3 -m pytest tests/ -q` → **155 passed, 1 skipped** (the skip is pre-existing,
   unrelated to this card)

(Dev deps were installed once from `requirements-dev.txt` because pytest was missing
in the environment; no repo files changed for that.)

## Validator must pay attention to

- **Permutation index deviation (important).** The card's literal wording — "把下标 1
  的字母取出、插入到下标 13" / "把下标 2 的字母取出、插入到下标 13" read as
  `lst.insert(13, lst.pop(k))` — does NOT reproduce the pinned acceptance vectors: it
  matches only the first 4 letters of `HELLOWORLD` (yields `WAHQZIUETS`, and
  `QTLVOFTEYS` for `CHAOCIPHER`). The acceptance section states 验收要点逐字为准, and
  the pinned ciphertexts require the removed letter to land *before* the element
  originally at index 13, i.e. `lst.insert(12, lst.pop(k))` (equivalent to `insert(13)`
  in the pre-removal frame). I implemented the variant that satisfies all pinned
  vectors; verified by brute-force search over the small rule space (order of the two
  permutations — left-then-right or right-then-left — gives identical outputs for the
  chosen rule set).
- Everything else follows the card literally (preprocessing, TypeError/empty-string
  behavior, decrypt driven by recovered plaintext + ciphertext letter).
- Test style matches repo conventions: plain `pytest` asserts, `pytest.raises` for the
  error cases, no fixtures needed.
