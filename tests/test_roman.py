import pytest

from roman import to_roman, from_roman


def test_to_roman_examples():
    assert to_roman(4) == "IV"
    assert to_roman(9) == "IX"
    assert to_roman(1994) == "MCMXCIV"


def test_to_roman_boundaries():
    assert to_roman(1) == "I"
    assert to_roman(3999) == "MMMCMXCIX"


def test_to_roman_other_values():
    assert to_roman(3) == "III"
    assert to_roman(40) == "XL"
    assert to_roman(58) == "LVIII"
    assert to_roman(2024) == "MMXXIV"


def test_from_roman_examples():
    assert from_roman("IV") == 4
    assert from_roman("IX") == 9
    assert from_roman("MCMXCIV") == 1994


def test_from_roman_boundaries():
    assert from_roman("I") == 1
    assert from_roman("MMMCMXCIX") == 3999


def test_roundtrip():
    for n in (1, 4, 9, 40, 58, 1994, 2024, 3999):
        assert from_roman(to_roman(n)) == n


@pytest.mark.parametrize("bad", [0, -1, 4000, 4001])
def test_to_roman_out_of_range(bad):
    with pytest.raises(ValueError):
        to_roman(bad)


@pytest.mark.parametrize("bad", [1.5, "3", None, True, 4.0])
def test_to_roman_non_integer(bad):
    with pytest.raises(ValueError):
        to_roman(bad)


@pytest.mark.parametrize(
    "bad", ["", "ABC", "IIII", "VV", "XM", "IXI", "IC", 123, None, 4]
)
def test_from_roman_invalid(bad):
    with pytest.raises(ValueError):
        from_roman(bad)
