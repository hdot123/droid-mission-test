"""Tests for roman.py (to_roman / from_roman)."""

import pytest

from roman import to_roman, from_roman


def test_to_roman_examples():
    assert to_roman(4) == "IV"
    assert to_roman(1994) == "MCMXCIV"


def test_to_roman_roundtrip_representative_values():
    for n in (1, 3, 4, 9, 40, 44, 90, 400, 999, 3999):
        s = to_roman(n)
        assert from_roman(s) == n


def test_to_roman_out_of_range_raises():
    for n in (0, -1, 4000):
        with pytest.raises(ValueError):
            to_roman(n)


def test_from_roman_empty_string_raises():
    with pytest.raises(ValueError):
        from_roman("")


def test_from_roman_illegal_characters_raise():
    for s in ("ABC", "X2", "I-V", " i"):
        with pytest.raises(ValueError):
            from_roman(s)


def test_from_roman_illegal_repetition_raises():
    for s in ("IIII", "VV", "MMMM", "XXXX", "DD", "LL"):
        with pytest.raises(ValueError):
            from_roman(s)


def test_from_roman_improper_subtraction_raises():
    for s in ("IC", "VX", "IL", "XM", "VC", "LD"):
        with pytest.raises(ValueError):
            from_roman(s)


def test_from_roman_examples():
    assert from_roman("IV") == 4
    assert from_roman("MCMXCIV") == 1994
    assert from_roman("XL") == 40
    assert from_roman("XC") == 90
    assert from_roman("CD") == 400
    assert from_roman("CM") == 900
    assert from_roman("MMMCMXCIX") == 3999
