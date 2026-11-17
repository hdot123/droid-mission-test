"""Tests for brackets.is_balanced only (this file never imports other modules)."""

from brackets import is_balanced


def test_empty_string_is_balanced():
    assert is_balanced("") is True


def test_simple_correct_nesting():
    assert is_balanced("()") is True
    assert is_balanced("[]") is True
    assert is_balanced("{}") is True
    assert is_balanced("({[]})") is True
    assert is_balanced("(a[b]{c}d)e") is True


def test_mismatched_pairs():
    assert is_balanced("(]") is False
    assert is_balanced("[)") is False
    assert is_balanced("{)") is False


def test_reversed_order():
    assert is_balanced(")(") is False
    assert is_balanced("][") is False
    assert is_balanced("}{") is False


def test_unclosed_and_extra_closers():
    assert is_balanced("(()") is False
    assert is_balanced("())") is False
    assert is_balanced("(") is False
    assert is_balanced("]") is False


def test_brackets_inside_single_quotes_ignored():
    assert is_balanced("'('") is True
    assert is_balanced("'([{}])'") is True
    assert is_balanced("')('") is True


def test_brackets_inside_double_quotes_ignored():
    assert is_balanced('"["') is True
    assert is_balanced('"[(])"') is True
    assert is_balanced('")("') is True


def test_quotes_across_lines_and_multiple_quotes():
    assert is_balanced("('a'\n[b])") is True
    assert is_balanced("'(' + ')'") is True
    assert is_balanced("\"[\" and ']' and ()") is True
    assert is_balanced("'a'('b')'c'") is True


def test_unclosed_quote_swallows_following_brackets():
    assert is_balanced("'(") is True
    assert is_balanced("'([{'") is True
    assert is_balanced('"(]') is True
    # The unclosed quote swallows the rest, but a bracket opened *before*
    # the quote still counts, so this stays unbalanced.
    assert is_balanced("('") is False
    assert is_balanced("')'(") is False


def test_cross_quote_kind_does_not_close():
    # A single quote must not close a double-quoted region.
    assert is_balanced('"it\'s ("') is True


def test_non_bracket_chars_outside_quotes_ignored():
    assert is_balanced("hello world 123 !@#$%^&*") is True
    assert is_balanced("a(b)c") is True
    assert is_balanced("a)b(c") is False
