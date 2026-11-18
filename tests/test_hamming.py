"""tests for hamming.distance."""

import pytest

from hamming import distance


def test_karolin_kathrin():
    assert distance("karolin", "kathrin") == 3


def test_binary_strings():
    assert distance("1011101", "1001001") == 2


def test_toned_roses():
    assert distance("toned", "roses") == 3


def test_empty_strings():
    assert distance("", "") == 0


def test_identical_strings():
    assert distance("abc", "abc") == 0


def test_single_difference():
    assert distance("abc", "abd") == 1


def test_unequal_lengths_raise():
    with pytest.raises(ValueError):
        distance("a", "ab")
