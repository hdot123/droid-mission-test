"""Tests for the vowelcount module (count() only)."""

from vowelcount import count


def test_count_banana():
    assert count("banana") == 3


def test_count_sky():
    assert count("sky") == 0


def test_count_aeiou_case_insensitive():
    assert count("AeIoU") == 5


def test_count_empty_string():
    assert count("") == 0


def test_count_non_vowels_ignored():
    assert count("rhythm") == 0
    assert count("bcdfg") == 0


def test_count_mixed_case_word():
    assert count("Hello World") == 3


def test_count_digits_and_punctuation_ignored():
    assert count("a1e2i3o4u!") == 5
