"""Tests for wordcount module."""

from wordcount import char_count, word_count


def test_word_count_basic():
    assert word_count("Hello, World!") == 2


def test_word_count_multiple_spaces():
    assert word_count("  A  B  ") == 2


def test_word_count_empty_string():
    assert word_count("") == 0


def test_char_count_default_includes_spaces():
    assert char_count("ab cd") == 5


def test_char_count_include_spaces_true_is_default():
    assert char_count("Hello, World!") == len("Hello, World!")


def test_char_count_include_spaces_false_excludes_spaces():
    assert char_count("ab cd", include_spaces=False) == 4


def test_char_count_include_spaces_false_excludes_tabs():
    assert char_count("a\tb\tc", include_spaces=False) == 3


def test_char_count_include_spaces_false_empty_string():
    assert char_count("", include_spaces=False) == 0


def test_char_count_empty_string():
    assert char_count("") == 0
