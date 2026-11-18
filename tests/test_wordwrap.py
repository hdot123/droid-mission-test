"""tests for wordwrap: greedy word wrapping."""

import pytest

from wordwrap import wrap


def test_greedy_fill_basic():
    assert wrap("the quick brown fox", 10) == ["the quick", "brown fox"]


def test_empty_string_returns_empty_list():
    assert wrap("", 10) == []


def test_fits_on_single_line():
    assert wrap("hello", 10) == ["hello"]


def test_overlong_word_occupies_own_line_untruncated():
    assert wrap("a verylongword here", 5) == ["a", "verylongword", "here"]


def test_zero_width_raises_value_error():
    with pytest.raises(ValueError):
        wrap("x", 0)


def test_negative_width_raises_value_error():
    with pytest.raises(ValueError):
        wrap("x", -3)


def test_full_whitespace_returns_empty_list():
    assert wrap("   ", 10) == []
    assert wrap("\t\n  \r\n", 5) == []


def test_consecutive_whitespace_is_single_separator():
    # collapsed to one separator: joined with a single space
    assert wrap("a  \t\n   b", 3) == ["a b"]
    assert wrap("one    two", 6) == ["one", "two"]
    # and it does not count toward the width as raw whitespace
    assert wrap("a  \t\n   b", 1) == ["a", "b"]


def test_line_length_never_exceeds_width():
    text = "alpha beta gamma delta epsilon zeta eta theta"
    for width in range(1, 20):
        for line in wrap(text, width):
            if len(line) > width:
                # only an over-long single word may exceed the width
                assert " " not in line
