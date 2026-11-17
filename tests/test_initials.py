"""Tests for the initials module."""

from initials import initials


def test_two_words():
    assert initials("Ada Lovelace") == "A.L."


def test_extra_spaces_ignored():
    assert initials("  grace   hopper ") == "G.H."


def test_single_word():
    assert initials("Prince") == "P."


def test_empty_string():
    assert initials("") == ""
