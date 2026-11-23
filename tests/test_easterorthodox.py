"""Tests for easterorthodox.orthodox_easter (acceptance points, verbatim)."""

import pytest

from easterorthodox import orthodox_easter


# --- acceptance dates ------------------------------------------------------
@pytest.mark.parametrize(
    "year, expected",
    [
        (2010, (4, 4)),
        (2016, (5, 1)),
        (2020, (4, 19)),
        (2021, (5, 2)),
        (2022, (4, 24)),
        (2023, (4, 16)),
        (2024, (5, 5)),
        (2025, (4, 20)),
        (2026, (4, 12)),
        (2000, (4, 30)),
        (1900, (4, 22)),
        (2100, (5, 2)),
    ],
)
def test_orthodox_easter_dates(year, expected):
    assert orthodox_easter(year) == expected


# --- boundary years --------------------------------------------------------
def test_1582_raises_value_error():
    with pytest.raises(ValueError):
        orthodox_easter(1582)


def test_10000_raises_value_error():
    with pytest.raises(ValueError):
        orthodox_easter(10000)


# --- type errors -----------------------------------------------------------
def test_float_rejected():
    with pytest.raises(TypeError):
        orthodox_easter(2024.0)


def test_string_rejected():
    with pytest.raises(TypeError):
        orthodox_easter("2024")


def test_bool_rejected():
    with pytest.raises(TypeError):
        orthodox_easter(True)


# --- return type -----------------------------------------------------------
def test_returns_int_tuple():
    result = orthodox_easter(2024)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(part, int) for part in result)
