import pytest

from rangemerge import merge, total


def test_merge_overlapping():
    assert merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]


def test_merge_adjacent():
    assert merge([(1, 3), (4, 6)]) == [(1, 6)]


def test_merge_unsorted():
    assert merge([(5, 5), (1, 2)]) == [(1, 2), (5, 5)]


def test_merge_contained():
    assert merge([(1, 10), (2, 3)]) == [(1, 10)]


def test_merge_empty():
    assert merge([]) == []


def test_merge_single_point():
    assert merge([(7, 7)]) == [(7, 7)]


def test_total_overlapping():
    assert total([(1, 3), (2, 6), (8, 10)]) == 9


def test_total_adjacent():
    assert total([(1, 3), (4, 6)]) == 6


def test_total_empty():
    assert total([]) == 0


def test_merge_invalid_range():
    with pytest.raises(ValueError):
        merge([(3, 1)])


def test_total_invalid_range():
    with pytest.raises(ValueError):
        total([(3, 1)])
