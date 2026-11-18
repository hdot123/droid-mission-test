"""Tests for intervals.merge and intervals.total_length."""

import pytest

import intervals


def test_merge_example_overlap():
    assert intervals.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6],
        [8, 10],
        [15, 18],
    ]


def test_total_length_example():
    assert intervals.total_length([[1, 3], [2, 6], [8, 10], [15, 18]]) == 10


def test_merge_endpoint_sharing():
    assert intervals.merge([[1, 3], [3, 5]]) == [[1, 5]]


def test_merge_disjoint():
    assert intervals.merge([[1, 3], [4, 5]]) == [[1, 3], [4, 5]]


def test_merge_sorts_input():
    assert intervals.merge([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]


def test_merge_empty():
    assert intervals.merge([]) == []


def test_merge_tuple_intervals():
    assert intervals.merge([(8, 10), (1, 3), (2, 6)]) == [[1, 6], [8, 10]]


def test_merge_tie_on_start_sorted_by_end():
    assert intervals.merge([[1, 5], [1, 3], [3, 4]]) == [[1, 5]]


def test_merge_contained_interval_absorbed():
    assert intervals.merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]


def test_total_length_empty():
    assert intervals.total_length([]) == 0


def test_total_length_disjoint():
    assert intervals.total_length([[1, 3], [4, 5]]) == 3


def test_merge_start_greater_than_end_raises():
    with pytest.raises(ValueError):
        intervals.merge([[3, 1]])


def test_total_length_start_greater_than_end_raises():
    with pytest.raises(ValueError):
        intervals.total_length([[1, 3], [5, 2]])
