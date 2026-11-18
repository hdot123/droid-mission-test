import pytest

from roman import from_roman, to_roman, validate_roman


def test_from_roman_case_insensitive():
    assert from_roman("xiv") == 14
    assert from_roman("Xiv") == 14
    assert from_roman("mmmcmxcix") == 3999


def test_from_roman_uppercase_unchanged():
    assert from_roman("I") == 1
    assert from_roman("XIV") == 14
    assert from_roman("LVIII") == 58
    assert from_roman("MCMXCIV") == 1994
    assert from_roman("MMXXVI") == 2026
    assert from_roman("MMMCMXCIX") == 3999


def test_to_roman_output_always_uppercase():
    assert to_roman(14) == "XIV"
    assert to_roman(4000) == "MMMM"
    assert to_roman(4999) == "MMMMCMXCIX"


def test_validate_roman_true():
    assert validate_roman("XIV") is True
    assert validate_roman("xiv") is True
    assert validate_roman("MMMM") is True
    assert validate_roman("mmmm") is True
    assert validate_roman("MMMMCMXCIX") is True
    assert validate_roman("MMMMD") is True
    assert validate_roman("MMMCMXCIX") is True


def test_validate_roman_false():
    assert validate_roman("IIII") is False
    assert validate_roman("IC") is False
    assert validate_roman("") is False
    assert validate_roman("MMMMM") is False
    assert validate_roman("vv") is False
    assert validate_roman("abc") is False
    assert validate_roman("MMMMCMXCIXX") is False
    assert validate_roman(None) is False
    assert validate_roman(123) is False


def test_extended_range_conversions():
    assert to_roman(4000) == "MMMM"
    assert to_roman(4500) == "MMMMD"
    assert to_roman(4999) == "MMMMCMXCIX"
    assert from_roman("MMMMCMXCIX") == 4999
    assert from_roman("mmmm") == 4000
    assert from_roman("MMMMD") == 4500


def test_extended_range_roundtrip():
    for n in (1, 999, 3999, 4000, 4001, 4444, 4500, 4888, 4999):
        assert from_roman(to_roman(n)) == n


def test_extended_range_out_of_range():
    for bad in (0, -1, 5000, 10000):
        with pytest.raises(ValueError):
            to_roman(bad)


def test_extended_range_invalid_input():
    for bad in ("", "IIII", "IC", "VV", "ABC", "MMMMM", "MMMMCMXCIXX"):
        with pytest.raises(ValueError):
            from_roman(bad)
        assert validate_roman(bad) is False
