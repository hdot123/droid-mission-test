from fractions import Fraction

import pytest

from harmonic import harmonic


def test_harmonic_zero():
    assert harmonic(0) == Fraction(0)


def test_harmonic_one():
    assert harmonic(1) == Fraction(1)


def test_harmonic_two():
    assert harmonic(2) == Fraction(3, 2)


def test_harmonic_three():
    assert harmonic(3) == Fraction(11, 6)


def test_harmonic_four():
    assert harmonic(4) == Fraction(25, 12)


def test_harmonic_five():
    assert harmonic(5) == Fraction(137, 60)


def test_harmonic_six():
    assert harmonic(6) == Fraction(49, 20)


def test_harmonic_ten():
    assert harmonic(10) == Fraction(7381, 2520)


def test_harmonic_twenty():
    assert harmonic(20) == Fraction(55835135, 15519504)


def test_harmonic_returns_fraction():
    assert isinstance(harmonic(7), Fraction)


def test_harmonic_negative_raises_value_error():
    with pytest.raises(ValueError):
        harmonic(-1)


def test_harmonic_float_raises_type_error():
    with pytest.raises(TypeError):
        harmonic(2.5)


def test_harmonic_str_raises_type_error():
    with pytest.raises(TypeError):
        harmonic("5")


def test_harmonic_bool_raises_type_error():
    with pytest.raises(TypeError):
        harmonic(True)
