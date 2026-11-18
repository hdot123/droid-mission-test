"""Tests for levenshtein.distance (spec examples and basic cases)."""

import levenshtein


def test_kitten_to_sitting():
    assert levenshtein.distance("kitten", "sitting") == 3


def test_flaw_to_lawn():
    assert levenshtein.distance("flaw", "lawn") == 2


def test_empty_to_abc():
    assert levenshtein.distance("", "abc") == 3


def test_identical_strings():
    assert levenshtein.distance("abc", "abc") == 0


def test_both_empty():
    assert levenshtein.distance("", "") == 0


def test_single_substitution():
    assert levenshtein.distance("a", "b") == 1
