import pytest

import money
from money import format, parse, split


def test_parse_single_fractional_digit_is_tenths():
    assert parse("12.3") == 1230


def test_parse_two_fractional_digits():
    assert parse("0.07") == 7


def test_parse_negative_integer_without_fraction():
    assert parse("-5") == -500


def test_parse_integer():
    assert parse("17") == 1700


def test_parse_zero():
    assert parse("0") == 0
    assert parse("0.00") == 0


def test_parse_rejects_thousand_separators():
    with pytest.raises(ValueError):
        parse("1,000.00")


def test_parse_rejects_too_many_fractional_digits():
    with pytest.raises(ValueError):
        parse("12.345")


def test_parse_rejects_plus_sign():
    with pytest.raises(ValueError):
        parse("+5")


def test_parse_rejects_whitespace():
    with pytest.raises(ValueError):
        parse(" 5")
    with pytest.raises(ValueError):
        parse("5 ")
    with pytest.raises(ValueError):
        parse("5.00 ")


def test_parse_rejects_malformed_forms():
    for bad in ("", ".", "-", "5.", ".5", "5..0", "abc", "5e2", "1.2.3", "--5"):
        with pytest.raises(ValueError):
            parse(bad)


def test_format_two_decimal_places():
    assert format(123456) == "1234.56"


def test_format_negative_below_one_unit():
    assert format(-5) == "-0.05"


def test_format_zero():
    assert format(0) == "0.00"


def test_format_round_trips_negative():
    assert format(parse(format(-98765))) == "-987.65"
    assert parse(format(-98765)) == -98765


def test_split_exact_shares():
    assert split(100, 4) == [25, 25, 25, 25]


def test_split_remainder_goes_to_first_parts():
    assert split(100, 3) == [34, 33, 33]


def test_split_negative_amount():
    assert split(-100, 3) == [-34, -33, -33]


def test_split_n_less_than_one_raises():
    with pytest.raises(ValueError):
        split(100, 0)
    with pytest.raises(ValueError):
        split(100, -1)


def test_split_sum_conservation():
    for cents in (100, -100, 1, 0, 7, -7, 999, -100001):
        for n in (1, 2, 3, 7, 100):
            parts = split(cents, n)
            assert len(parts) == n
            assert sum(parts) == cents


def test_split_parts_differ_by_at_most_one():
    parts = split(100, 7)
    assert max(parts) - min(parts) <= 1


def test_roundtrip_format_parse_identity():
    assert parse(format(-98765)) == -98765


def test_module_exposes_helpers():
    for name in ("parse", "format", "split"):
        assert callable(getattr(money, name))
