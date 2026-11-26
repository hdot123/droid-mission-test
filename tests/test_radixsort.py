import random

import pytest

from radixsort import radix_sort


def test_empty():
    assert radix_sort([]) == []


def test_single():
    assert radix_sort([5]) == [5]


def test_three_unsorted():
    assert radix_sort([3, 1, 2]) == [1, 2, 3]


def test_negatives():
    assert radix_sort([-5, 3, -1, 0]) == [-5, -1, 0, 3]


def test_classic_example():
    assert radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [
        2,
        24,
        45,
        66,
        75,
        90,
        170,
        802,
    ]


def test_duplicates():
    assert radix_sort([2, 2, 1]) == [1, 2, 2]


def test_large_integers():
    assert radix_sort([10**18, 1, 10**12]) == [1, 10**12, 10**18]


def test_tuple_input():
    assert radix_sort((3, 1, 2)) == [1, 2, 3]


def test_input_not_modified():
    values = [5, -3, 0, 7, -3, 2]
    snapshot = list(values)
    radix_sort(values)
    assert values == snapshot


def test_random_matches_sorted():
    rng = random.Random(58)
    for _ in range(60):
        length = rng.randint(0, 30)
        values = [rng.randint(-10**6, 10**6) for _ in range(length)]
        snapshot = list(values)
        assert radix_sort(values) == sorted(values)
        assert values == snapshot


def test_bad_element_types():
    with pytest.raises(TypeError):
        radix_sort("321")
    with pytest.raises(TypeError):
        radix_sort([1, 2.0])
    with pytest.raises(TypeError):
        radix_sort([1, True])
    with pytest.raises(TypeError):
        radix_sort(123)
