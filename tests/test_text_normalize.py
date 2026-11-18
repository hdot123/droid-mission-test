"""Tests for text_normalize.py (this module's own behavior only)."""

import string

import text_normalize


def test_lowercase_lowercases_only():
    assert text_normalize.lowercase("Hello WORLD") == "hello world"
    assert text_normalize.lowercase("MiXeD, PUNCT!") == "mixed, punct!"
    assert text_normalize.lowercase("") == ""


def test_lowercase_preserves_punctuation_and_whitespace():
    assert text_normalize.lowercase("  A  B\tC\n") == "  a  b\tc\n"


def test_strip_punctuation_removes_ascii_punctuation():
    for ch in string.punctuation:
        assert ch not in text_normalize.strip_punctuation("x" + ch + "y")
    assert text_normalize.strip_punctuation("hi, there!") == "hi there"
    assert text_normalize.strip_punctuation("a-b_c.d") == "abcd"


def test_strip_punctuation_does_not_insert_spaces():
    assert text_normalize.strip_punctuation("hi,there") == "hithere"


def test_strip_punctuation_keeps_case_and_whitespace():
    assert text_normalize.strip_punctuation("  Keep CASE  ") == "  Keep CASE  "
    assert text_normalize.strip_punctuation("") == ""


def test_collapse_whitespace_collapses_runs_to_single_space():
    assert text_normalize.collapse_whitespace("  a \t\n b  ") == "a b"
    assert text_normalize.collapse_whitespace("a     b") == "a b"
    assert text_normalize.collapse_whitespace("\n\nx\n\n") == "x"


def test_collapse_whitespace_keeps_case_and_punctuation():
    assert text_normalize.collapse_whitespace("  Hello, WORLD!  ") == "Hello, WORLD!"
    assert text_normalize.collapse_whitespace("") == ""
    assert text_normalize.collapse_whitespace("   ") == ""


def test_normalize_full_pipeline():
    assert text_normalize.normalize("  Hello,   WORLD!\n") == "hello world"
    assert text_normalize.normalize("MiXeD\t CaSe & PuNcT ") == "mixed case punct"
    assert text_normalize.normalize("one...two") == "one two"
    assert text_normalize.normalize("already clean") == "already clean"


def test_normalize_output_is_uniform_clean_form():
    result = text_normalize.normalize("  A,  B!  \t C? \n")
    assert result == "a b c"
    # uniform form: no punctuation, no repeated whitespace, no edge space
    assert not any(ch in string.punctuation for ch in result)
    assert "  " not in result
    assert result == result.strip()
    assert result == result.lower()


def test_normalize_idempotent():
    once = text_normalize.normalize("  Messy,   INPUT!  ")
    assert text_normalize.normalize(once) == once


def test_normalize_empty_and_whitespace_only():
    assert text_normalize.normalize("") == ""
    assert text_normalize.normalize("   \n\t ") == ""
    assert text_normalize.normalize("!!!") == ""
