"""Tests for levenshtein.distance — every acceptance item, verbatim."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levenshtein import distance


def test_kitten_sitting():
    assert distance("kitten", "sitting") == 3


def test_flaw_lawn():
    assert distance("flaw", "lawn") == 2


def test_empty_vs_abc():
    assert distance("", "abc") == 3


def test_abc_vs_empty():
    assert distance("abc", "") == 3


def test_abc_vs_abc():
    assert distance("abc", "abc") == 0


def test_abc_vs_abd():
    assert distance("abc", "abd") == 1


def test_abc_vs_abcd():
    assert distance("abc", "abcd") == 1


def test_two_empty_strings():
    assert distance("", "") == 0
