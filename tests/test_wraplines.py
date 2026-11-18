"""Tests for wraplines.wrap (greedy word wrapping)."""

from wraplines import wrap


def test_body_example_quick_brown_fox():
    assert wrap("the quick brown fox", 10) == ["the quick", "brown fox"]


def test_body_example_aaa_bb():
    assert wrap("aaa bb", 3) == ["aaa", "bb"]


def test_greedy_wrapping_starts_new_line_when_word_does_not_fit():
    # "the quick" is 9 chars; adding "brown" (5) would exceed 10.
    lines = wrap("the quick brown fox", 10)
    assert all(len(line) <= 10 for line in lines if len(line.split()) > 1)
    assert lines == ["the quick", "brown fox"]


def test_word_longer_than_width_stands_alone():
    # Single word longer than width: over-length allowed, stands alone.
    assert wrap("abcdefghij", 3) == ["abcdefghij"]
    assert wrap("aa bbbbbbb cc", 4) == ["aa", "bbbbbbb", "cc"]


def test_empty_text_returns_empty_list():
    assert wrap("", 10) == []


def test_whitespace_only_text_returns_empty_list():
    assert wrap("   \t\n  ", 5) == []


def test_exact_width_fits_on_one_line():
    assert wrap("aaa bbb", 7) == ["aaa bbb"]
    assert wrap("aaa bbb", 6) == ["aaa", "bbb"]


def test_multiple_whitespace_is_treated_as_single_separator():
    assert wrap("  a\t\n b   c  ", 10) == ["a b c"]
