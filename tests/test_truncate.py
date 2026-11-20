"""Tests for truncate.text truncation (word-boundary preference)."""

import pytest

from truncate import truncate


def test_no_change_when_shorter_or_equal():
    assert truncate("hello world", 11) == "hello world"


def test_no_change_when_well_within_limit():
    assert truncate("hello world", 20) == "hello world"


def test_word_boundary_cut():
    assert truncate("hello world", 8) == "hello…"


def test_hard_cut_when_no_space_in_budget():
    assert truncate("hello world", 5) == "hell…"


def test_hard_cut_single_word():
    assert truncate("helloworld", 8) == "hellowo…"


def test_multiple_words_cut_at_boundary():
    assert truncate("a b c d e", 5) == "a b…"


def test_empty_text():
    assert truncate("", 5) == ""


def test_text_exactly_max_len():
    assert truncate("hi", 2) == "hi"


def test_budget_zero_returns_only_ellipsis():
    assert truncate("hello", 1) == "…"


def test_custom_ellipsis_word_boundary():
    assert truncate("hello world", 9, "...") == "hello..."


def test_leading_space_keeps_hard_cut_when_candidate_empty():
    assert truncate(" hello world", 6) == " hell…"


def test_boundary_cut_at_max_len_ten():
    assert truncate("hello world", 10) == "hello…"


def test_max_len_smaller_than_ellipsis_raises_value_error():
    with pytest.raises(ValueError):
        truncate("hello", 0)


def test_max_len_smaller_than_custom_ellipsis_raises_value_error():
    with pytest.raises(ValueError):
        truncate("hello", 2, "...")


def test_non_str_text_raises_type_error():
    with pytest.raises(TypeError):
        truncate(123, 5)


def test_float_max_len_raises_type_error():
    with pytest.raises(TypeError):
        truncate("hello", 5.0)


def test_non_str_ellipsis_raises_type_error():
    with pytest.raises(TypeError):
        truncate("hello", 5, None)


def test_bool_max_len_rejected():
    with pytest.raises(TypeError):
        truncate("hello", True)
