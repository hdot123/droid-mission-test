import pytest

from roman import from_roman, to_roman


def test_to_roman_basic():
    assert to_roman(1) == "I"
    assert to_roman(3) == "III"
    assert to_roman(14) == "XIV"
    assert to_roman(58) == "LVIII"
    assert to_roman(1994) == "MCMXCIV"
    assert to_roman(2026) == "MMXXVI"


def test_to_roman_subtractive():
    assert to_roman(4) == "IV"
    assert to_roman(9) == "IX"
    assert to_roman(40) == "XL"
    assert to_roman(90) == "XC"
    assert to_roman(400) == "CD"
    assert to_roman(900) == "CM"


def test_from_roman_basic():
    assert from_roman("I") == 1
    assert from_roman("XIV") == 14
    assert from_roman("LVIII") == 58
    assert from_roman("MCMXCIV") == 1994
    assert from_roman("MMXXVI") == 2026


def test_roundtrip():
    for n in (1, 7, 42, 90, 444, 999, 2026, 3999):
        assert from_roman(to_roman(n)) == n


def test_boundaries():
    assert to_roman(1) == "I"
    assert to_roman(3999) == "MMMCMXCIX"
    assert from_roman("I") == 1
    assert from_roman("MMMCMXCIX") == 3999


def test_to_roman_out_of_range():
    for bad in (0, -1, 5000):
        with pytest.raises(ValueError):
            to_roman(bad)


def test_from_roman_invalid():
    for bad in ("", "IIII", "IC", "VV", "ABC"):
        with pytest.raises(ValueError):
            from_roman(bad)
