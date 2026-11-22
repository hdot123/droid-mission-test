"""Tests for fractionx.Fraction and fractionx.parse (module-level parse)."""

import pytest

from fractionx import Fraction, parse


def test_reduce_on_construction():
    f = Fraction(2, 4)
    assert f.numerator == 1
    assert f.denominator == 2


def test_negative_over_negative_reduces_to_positive():
    assert Fraction(-3, -6) == Fraction(1, 2)


def test_sign_normalizes_to_numerator():
    f = Fraction(3, -6)
    assert f.numerator == -1
    assert f.denominator == 2
    assert f == Fraction(-1, 2)


def test_integer_form_construction():
    f = Fraction(5)
    assert f.numerator == 5
    assert f.denominator == 1


def test_zero_denominator_raises():
    with pytest.raises(ValueError):
        Fraction(1, 0)


def test_addition():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)


def test_subtraction():
    assert Fraction(3, 4) - Fraction(1, 4) == Fraction(1, 2)
    assert Fraction(1, 3) - Fraction(1, 2) == Fraction(-1, 6)


def test_multiplication():
    assert Fraction(3, 4) * Fraction(8, 9) == Fraction(2, 3)


def test_division():
    assert Fraction(1, 2) / Fraction(1, 4) == Fraction(2, 1)
    assert Fraction(3, 4) / Fraction(9, 8) == Fraction(2, 3)


def test_division_by_zero_fraction_raises():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0, 1)


def test_str_integer_denominator():
    assert str(Fraction(6, 3)) == "2"


def test_str_negative_fraction():
    assert str(Fraction(-1, 2)) == "-1/2"


def test_str_general():
    assert str(Fraction(3, 4)) == "3/4"


def test_parse_fraction_form():
    assert parse("3/4") == Fraction(3, 4)


def test_parse_negative_fraction_form():
    assert parse("-3/4") == Fraction(-3, 4)


def test_parse_integer_form():
    assert parse("5") == Fraction(5, 1)
    assert parse("-5") == Fraction(-5, 1)


def test_parse_reduces_result():
    assert parse("2/4") == Fraction(1, 2)


def test_parse_zero_denominator_raises():
    with pytest.raises(ValueError):
        parse("1/0")


def test_parse_rejects_whitespace():
    with pytest.raises(ValueError):
        parse(" 3/4")
    with pytest.raises(ValueError):
        parse("3/4 ")
    with pytest.raises(ValueError):
        parse("5 ")


def test_parse_rejects_malformed_forms():
    for bad in ["", "3/", "/4", "3/4/5", "abc", "3.4", "+5", "1 /2", "3 -/4", "3//4"]:
        with pytest.raises(ValueError):
            parse(bad)


def test_parse_rejects_negative_denominator_form():
    # Only '3/4', '-3/4', and integers are accepted forms.
    with pytest.raises(ValueError):
        parse("3/-4")
