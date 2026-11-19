"""Tests for isogram.py."""

import pytest

from isogram import is_isogram, repeated_letters


@pytest.mark.parametrize(
    "word, expected",
    [
        ("background", True),
        ("isogram", True),
        ("hello", False),
        ("subdermatoglyphic", True),
        ("", True),
        ("a", True),
        ("Apple", False),
        ("uncopyrightable", True),
        ("a-b", True),
        ("abc def", True),
        ("noon", False),
        ("lumberjack", True),
        ("AbC", True),
        ("AbA", False),
    ],
)
def test_is_isogram(word, expected):
    assert is_isogram(word) is expected


@pytest.mark.parametrize(
    "word, expected",
    [
        ("hello", ["l"]),
        ("banana", ["a", "n"]),
        ("abc", []),
        ("aabbcc", ["a", "b", "c"]),
        ("Mississippi", ["i", "p", "s"]),
        ("", []),
    ],
)
def test_repeated_letters(word, expected):
    assert repeated_letters(word) == expected


def test_is_isogram_non_str_raises():
    with pytest.raises(TypeError):
        is_isogram(123)


def test_repeated_letters_non_str_raises():
    with pytest.raises(TypeError):
        repeated_letters(None)
