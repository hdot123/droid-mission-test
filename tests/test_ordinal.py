"""Tests for ordinal.py (ordinal suffix formatting)."""

import pytest

from ordinal import ordinal, ordinal_suffix


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, "0th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (14, "14th"),
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (121, "121st"),
        (1000, "1000th"),
    ],
)
def test_ordinal(n, expected):
    assert ordinal(n) == expected


@pytest.mark.parametrize(
    "n,expected",
    [
        (1, "st"),
        (2, "nd"),
        (3, "rd"),
        (11, "th"),
        (23, "rd"),
    ],
)
def test_ordinal_suffix(n, expected):
    assert ordinal_suffix(n) == expected


def test_ordinal_negative_raises_value_error():
    with pytest.raises(ValueError):
        ordinal(-1)


def test_ordinal_non_int_raises_type_error():
    with pytest.raises(TypeError):
        ordinal(1.5)
