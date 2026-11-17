"""Tests for median.py (lower-median rule)."""

import pytest

from median import median


def test_even_length_takes_lower_middle():
    assert median([1, 2, 3, 4]) == 2


def test_unsorted_odd_length():
    assert median([5, 1, 9]) == 5


def test_single_element():
    assert median([7]) == 7


def test_another_even_length_lower_middle_not_average():
    # Sorted [2, 4, 8, 10]: middle values 4 and 8, average would be 6.
    assert median([10, 2, 8, 4]) == 4


def test_unsorted_input_is_sorted_first():
    assert median([3, 1, 2]) == 2


def test_negative_numbers():
    assert median([-5, -1, -3]) == -3
    assert median([-4, -3, -2, -1]) == -3


def test_empty_list_raises_value_error():
    with pytest.raises(ValueError):
        median([])
