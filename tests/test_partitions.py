"""Tests for partitions.py: integer partition count p(n)."""

import pytest

from partitions import partitions


@pytest.mark.parametrize(
    "n, expected",
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


def test_partitions_negative_raises_value_error():
    with pytest.raises(ValueError):
        partitions(-1)


@pytest.mark.parametrize("bad", [2.5, "5", True])
def test_partitions_non_int_raises_type_error(bad):
    with pytest.raises(TypeError):
        partitions(bad)
