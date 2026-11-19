"""Tests for partitions.py — integer partition counts p(n)."""

import pytest

from partitions import partitions


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 7),
        (6, 11),
        (7, 15),
        (8, 22),
        (9, 30),
        (10, 42),
        (15, 176),
        (20, 627),
        (25, 1958),
        (30, 5604),
        (50, 204226),
        (100, 190569292),
    ],
)
def test_partitions_values(n, expected):
    assert partitions(n) == expected


def test_partitions_zero_is_one():
    assert partitions(0) == 1


def test_partitions_negative_raises_value_error():
    with pytest.raises(ValueError):
        partitions(-1)


def test_partitions_float_raises_type_error():
    with pytest.raises(TypeError):
        partitions(2.5)


def test_partitions_str_raises_type_error():
    with pytest.raises(TypeError):
        partitions("5")


def test_partitions_bool_raises_type_error():
    with pytest.raises(TypeError):
        partitions(True)
