"""Tests for the glob_match module only."""

import pytest

from glob_match import match


# --- Required examples -----------------------------------------------------

def test_example_star_py_matches():
    assert match("*.py", "a.py") is True


def test_example_star_py_rejects_pyc():
    assert match("*.py", "a.pyc") is False


def test_example_question_mark():
    assert match("a?c", "abc") is True


def test_example_negated_class_match():
    assert match("[!a-c]x", "dx") is True


def test_example_negated_class_reject():
    assert match("[!a-c]x", "bx") is False


# --- Literal characters ----------------------------------------------------

def test_literal_match():
    assert match("abc", "abc") is True


def test_literal_mismatch():
    assert match("abc", "abd") is False


def test_literal_longer_name():
    assert match("abc", "abcd") is False


def test_literal_longer_pattern():
    assert match("abcd", "abc") is False


def test_special_chars_are_literal():
    assert match("a.b", "a.b") is True
    assert match("a.b", "axb") is False


# --- '*' -------------------------------------------------------------------

def test_star_matches_empty_sequence():
    assert match("a*b", "ab") is True


def test_star_matches_any_sequence():
    assert match("a*b", "axyzb") is True


def test_star_matches_full_name():
    assert match("*", "anything") is True


def test_star_matches_empty_name():
    assert match("*", "") is True


def test_star_requires_prefix_and_suffix():
    assert match("a*b", "b") is False


def test_multiple_stars():
    assert match("a*b*c", "axxbyyc") is True
    assert match("a*b*c", "abc") is True
    assert match("a*b*c", "abbcx") is False
    assert match("a*b*c", "ac") is False  # literal 'b' is required


def test_star_with_path():
    assert match("*.py", "dir/mod.py") is True


# --- '?' -------------------------------------------------------------------

def test_question_matches_exactly_one():
    assert match("?", "x") is True


def test_question_rejects_empty():
    assert match("?", "") is False


def test_question_rejects_two_chars():
    assert match("?", "xy") is False


def test_question_in_middle():
    assert match("a?c", "a.c") is True
    assert match("a?c", "ac") is False
    assert match("a?c", "abbc") is False


# --- Character classes -----------------------------------------------------

def test_class_membership():
    assert match("[abc]", "b") is True
    assert match("[abc]", "d") is False


def test_class_matches_exactly_one_char():
    assert match("[abc]", "ab") is False
    assert match("[abc]", "") is False


def test_class_range():
    assert match("[a-c]x", "ax") is True
    assert match("[a-c]x", "cx") is True
    assert match("[a-c]x", "dx") is False


def test_class_range_digit():
    assert match("[0-9]", "7") is True
    assert match("[0-9]", "a") is False


def test_class_multiple_ranges():
    assert match("[a-c0-2]x", "1x") is True
    assert match("[a-c0-2]x", "9x") is False


def test_negated_class_membership():
    assert match("[!a-c]x", "ax") is False
    assert match("[!a-c]x", "zx") is True


def test_negated_class_rejects_outside_char():
    assert match("[!a-c]x", "dx") is True


def test_class_literal_dash_at_end():
    assert match("[a-]", "-") is True
    assert match("[a-]", "a") is True
    assert match("[a-]", "b") is False


def test_class_inside_star_pattern():
    assert match("*[0-9].txt", "file7.txt") is True
    assert match("*[0-9].txt", "filex.txt") is False


# --- Case sensitivity ------------------------------------------------------

def test_case_sensitive_literal():
    assert match("ABC", "abc") is False
    assert match("abc", "ABC") is False


def test_case_sensitive_star_pattern():
    assert match("*.PY", "a.py") is False
    assert match("*.py", "a.PY") is False


def test_case_sensitive_class():
    assert match("[a-c]", "B") is False
    assert match("[A-C]", "b") is False


# --- Empty pattern / empty name --------------------------------------------

def test_empty_pattern_matches_empty_name():
    assert match("", "") is True


def test_empty_pattern_rejects_nonempty_name():
    assert match("", "x") is False


def test_nonempty_pattern_rejects_empty_name():
    assert match("a", "") is False
    assert match("*a", "") is False


# --- Unclosed '[' raises ValueError ----------------------------------------

def test_unclosed_class_raises():
    with pytest.raises(ValueError):
        match("[abc", "abc")


def test_unclosed_class_alone_raises():
    with pytest.raises(ValueError):
        match("[", "")


def test_unclosed_negated_class_raises():
    with pytest.raises(ValueError):
        match("[!a-z", "q")


def test_unclosed_class_raises_even_on_no_match_name():
    with pytest.raises(ValueError):
        match("a[bc", "zzz")
