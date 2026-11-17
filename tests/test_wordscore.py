"""Tests for wordscore.py only.

This file does not import or test any other module.

IMPORTANT: The work order's example set is contradictory. Every example is
recorded here VERBATIM as a hard requirement; no value is chosen between,
changed, dropped, or renumbered. The checks run against the real evidence.

Work order examples, verbatim:
  Deliverable examples:   score("abc") == 6, score("z") == 26, score("a-b") == 3
  Acceptance criteria:    score("bad") == 7, score("abc") == 7
"""

from wordscore import score


# --- Spec-rule tests (derived directly from the written spec rules) --------

def test_empty_string_returns_zero():
    assert score("") == 0


def test_no_letters_returns_zero():
    assert score("123 !?-") == 0


def test_letter_positions_a_to_z():
    assert score("a") == 1
    assert score("z") == 26
    assert score("abcd") == 10


def test_case_insensitive():
    assert score("AbC") == 6
    assert score("Zz") == 52


def test_non_letters_ignored():
    assert score("a-b") == 3
    # h(8)+i(9)+t(20)+h(8)+e(5)+r(18)+e(5) = 73; ",", " ", "!" ignored.
    assert score("hi, there!") == 73


# --- Verbatim example assertions (hard requirement, do not weaken) ---------

def test_verbatim_deliverable_example_abc_is_6():
    # Work order deliverable example, verbatim: score("abc") returns 6.
    assert score("abc") == 6


def test_verbatim_deliverable_example_z_is_26():
    # Work order deliverable example, verbatim: score("z") returns 26.
    assert score("z") == 26


def test_verbatim_deliverable_example_a_dash_b_is_3():
    # Work order deliverable example, verbatim: score("a-b") returns 3.
    assert score("a-b") == 3


def test_verbatim_acceptance_example_bad_is_7():
    # Work order acceptance-criteria example, verbatim: score("bad") == 7.
    assert score("bad") == 7


def test_verbatim_acceptance_example_abc_is_7():
    # Work order acceptance-criteria example, verbatim: score("abc") == 7.
    # This contradicts the deliverable example score("abc") == 6.
    # Per the process card: preserved verbatim, not resolved, not changed.
    assert score("abc") == 7
