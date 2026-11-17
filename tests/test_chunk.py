"""Tests for chunk.py: chunk() and flatten() behavior only."""

import pytest

import chunk


def test_chunk_example():
    assert chunk.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_flatten_example():
    assert chunk.flatten([[1, 2], [3], []]) == [1, 2, 3]


def test_chunk_size_zero_raises():
    with pytest.raises(ValueError):
        chunk.chunk([1], 0)


def test_chunk_negative_size_raises():
    with pytest.raises(ValueError):
        chunk.chunk([1, 2], -3)


def test_chunk_empty_list():
    assert chunk.chunk([], 3) == []


def test_chunk_size_one():
    assert chunk.chunk(["a", "b", "c"], 1) == [["a"], ["b"], ["c"]]


def test_chunk_size_larger_than_list():
    assert chunk.chunk([1, 2, 3], 10) == [[1, 2, 3]]


def test_flatten_ignores_empty_sublists():
    assert chunk.flatten([[], [1], [], [2, 3], []]) == [1, 2, 3]


def test_flatten_empty_input():
    assert chunk.flatten([]) == []


@pytest.mark.parametrize(
    "xs, n",
    [
        ([1, 2, 3, 4, 5], 2),
        ([], 4),
        (list(range(10)), 3),
        (["only"], 7),
        (list(range(6)), 1),
    ],
)
def test_flatten_chunk_round_trip(xs, n):
    assert chunk.flatten(chunk.chunk(xs, n)) == xs
