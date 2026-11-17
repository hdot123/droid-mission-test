"""Tests for the roman module (to_roman / from_roman)."""

import pytest

from roman import to_roman, from_roman


def test_worked_examples():
    assert to_roman(4) == "IV"
    assert to_roman(9) == "IX"
    assert to_roman(1994) == "MCMXCIV"
    assert from_roman("MCMXCIV") == 1994


def test_representative_values():
    cases = [
        (1, "I"),
        (3, "III"),
        (5, "V"),
        (8, "VIII"),
        (10, "X"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (3999, "MMMCMXCIX"),
    ]
    for n, roman in cases:
        assert to_roman(n) == roman
        assert from_roman(roman) == n


def test_round_trip_full_range():
    for n in range(1, 4000):
        assert from_roman(to_roman(n)) == n


@pytest.mark.parametrize("bad", [0, 4000, -1, 1.5, "x", None, True])
def test_to_roman_value_errors(bad):
    with pytest.raises(ValueError):
        to_roman(bad)


@pytest.mark.parametrize(
    "bad",
    ["", "IIII", "VV", "IC", "XM", "abc", "MCMXCIVI", None, 1994],
)
def test_from_roman_value_errors(bad):
    with pytest.raises(ValueError):
        from_roman(bad)
