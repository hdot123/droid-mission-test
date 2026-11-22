"""Tests for binarysearch.search."""

from binarysearch import search


def test_found_returns_index():
    assert search([1, 3, 5, 7, 9], 7) == 3


def test_missing_returns_minus_one():
    assert search([1, 3, 5, 7, 9], 4) == -1


def test_empty_list_returns_minus_one():
    assert search([], 1) == -1
