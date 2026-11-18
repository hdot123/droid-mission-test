"""Tests for the temperature conversion module."""

import pytest

import temperature


def test_c_to_f_zero():
    assert temperature.c_to_f(0) == 32.0


def test_c_to_f_boiling():
    assert temperature.c_to_f(100) == 212.0


def test_f_to_c_boiling():
    assert temperature.f_to_c(212) == 100.0


def test_c_to_k_absolute_zero():
    assert temperature.c_to_k(-273.15) == 0.0


def test_return_types_are_float():
    assert isinstance(temperature.c_to_f(0), float)
    assert isinstance(temperature.c_to_f(100), float)
    assert isinstance(temperature.f_to_c(212), float)
    assert isinstance(temperature.c_to_k(-273.15), float)


@pytest.mark.parametrize("c", [-273.15, -40, 0, 37, 100, 1000])
def test_c_f_round_trip(c):
    assert temperature.f_to_c(temperature.c_to_f(c)) == pytest.approx(c)
