"""Tests for bracecheck.is_balanced.

Only bracecheck's own behaviour is exercised here; no codecbox interaction
and no shared-state manipulation of any kind.
"""

import bracecheck


def test_acceptance_mixed_text():
    assert bracecheck.is_balanced("a(b[c]d)e") is True


def test_acceptance_mismatched_pair():
    assert bracecheck.is_balanced("(]") is False


def test_acceptance_empty_string():
    assert bracecheck.is_balanced("") is True


def test_acceptance_unclosed_opens():
    assert bracecheck.is_balanced("(((") is False


def test_plain_text_is_ignored():
    assert bracecheck.is_balanced("hello world 123") is True


def test_mismatched_closer_returns_false():
    assert bracecheck.is_balanced("(}") is False
    assert bracecheck.is_balanced("[)") is False
    assert bracecheck.is_balanced("{)") is False


def test_wrong_nesting_returns_false():
    assert bracecheck.is_balanced("([)]") is False
    assert bracecheck.is_balanced("({)}") is False
    assert bracecheck.is_balanced("[(])") is False


def test_unbalanced_leftovers_return_false():
    assert bracecheck.is_balanced(")") is False
    assert bracecheck.is_balanced("]") is False
    assert bracecheck.is_balanced("}") is False
    assert bracecheck.is_balanced("a(b[c") is False
    assert bracecheck.is_balanced("((())") is False


def test_correctly_nested_returns_true():
    assert bracecheck.is_balanced("()") is True
    assert bracecheck.is_balanced("([]{})") is True
    assert bracecheck.is_balanced("{[()]}") is True
    assert bracecheck.is_balanced("a(b[c]d)e{f[g]h}i") is True
