"""Tests for the wordscore module (covers only wordscore's behavior).

The work order contains an internal contradiction about score("abc"), carried
here verbatim as a hard requirement on both sides (not reconciled by this
process):

- Deliverable examples (work order body): score("abc") returns 6,
  score("z") returns 26, score("a-b") returns 3.
- Acceptance examples (work order acceptance criteria): score("bad") must
  equal 7; score("abc") must equal 7.

Both sets are asserted below exactly as stated. Provisional value recorded by
the process card: 7 (acceptance criteria are the hard gate this round); this
process does not pick a side, drop, or renumber either example.
"""

from wordscore import score


# --- deliverable examples (work order body, verbatim) ---
def test_deliverable_example_abc_returns_6():
    assert score("abc") == 6


def test_deliverable_example_z_returns_26():
    assert score("z") == 26


def test_deliverable_example_a_dash_b_returns_3():
    assert score("a-b") == 3


# --- acceptance examples (work order acceptance criteria, verbatim) ---
def test_acceptance_example_bad_equals_7():
    assert score("bad") == 7


def test_acceptance_example_abc_equals_7():
    # Conflict preserved verbatim: deliverable says 6, acceptance says 7.
    assert score("abc") == 7


# --- spec behavior ---
def test_empty_string_returns_0():
    assert score("") == 0


def test_no_letters_returns_0():
    assert score("123!@#") == 0


def test_case_insensitive():
    assert score("AbC") == 6
