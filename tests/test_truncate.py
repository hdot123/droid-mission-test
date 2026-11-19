"""Tests for truncate (word-boundary-first text truncation)."""

import pytest

from truncate import truncate


# --- acceptance examples: within limit / unchanged ---

def test_full_when_equal_length():
    assert truncate("hello world", 11) == "hello world"


def test_full_when_under_limit():
    assert truncate("hello world", 20) == "hello world"


def test_empty_text():
    assert truncate("", 5) == ""


def test_exact_fit():
    assert truncate("hi", 2) == "hi"


# --- acceptance examples: word-boundary truncation ---

def test_word_boundary_hello():
    assert truncate("hello world", 8) == "hello…"


def test_hard_cut_when_no_space():
    assert truncate("hello world", 5) == "hell…"


def test_hard_cut_single_word():
    assert truncate("helloworld", 8) == "hellowo…"


def test_word_boundary_multi_word():
    assert truncate("a b c d e", 5) == "a b…"


def test_budget_zero_returns_ellipsis_only():
    assert truncate("hello", 1) == "…"


def test_custom_ellipsis_word_boundary():
    assert truncate("hello world", 9, "...") == "hello..."


def test_leading_space_kept_when_candidate_empty():
    assert truncate(" hello world", 6) == " hell…"


def test_word_boundary_at_max_len_minus_ellipsis():
    assert truncate("hello world", 10) == "hello…"


# --- acceptance examples: ValueErrors ---

def test_value_error_when_max_len_below_ellipsis_len():
    with pytest.raises(ValueError):
        truncate("hello", 0)


def test_value_error_when_max_len_below_custom_ellipsis_len():
    with pytest.raises(ValueError):
        truncate("hello", 2, "...")


# --- acceptance examples: TypeErrors ---

def test_type_error_non_str_text():
    with pytest.raises(TypeError):
        truncate(123, 5)


def test_type_error_non_int_max_len():
    with pytest.raises(TypeError):
        truncate("hello", 5.0)


def test_type_error_non_str_ellipsis():
    with pytest.raises(TypeError):
        truncate("hello", 5, None)


# --- result length invariant ---

def test_result_length_always_within_max_len():
    cases = [
        ("hello world", 8),
        ("hello world", 5),
        ("helloworld", 8),
        ("a b c d e", 5),
        ("hello", 1),
        (" hello world", 6),
        ("hello world", 10),
        ("hello world", 9),
        ("", 5),
        ("hi", 2),
    ]
    for text, max_len in cases:
        ellipsis = "..." if max_len == 9 else "…"
        result = truncate(text, max_len, ellipsis)
        assert len(result) <= max_len
