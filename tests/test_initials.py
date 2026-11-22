"""Tests for the initials module."""

import initials


def test_simple_name():
    assert initials.initials("ada lovelace") == "A.L."


def test_hyphenated_name():
    assert initials.initials("jean-luc picard") == "J.L.P."


def test_empty_string():
    assert initials.initials("") == ""
