"""Tests for temperature.py."""

import temperature


def test_c_to_f_freezing_point():
    assert temperature.c_to_f(0) == 32.0


def test_c_to_f_boiling_point():
    assert temperature.c_to_f(100) == 212.0


def test_f_to_c_boiling_point():
    assert temperature.f_to_c(212) == 100.0


def test_c_to_k_absolute_zero():
    assert temperature.c_to_k(-273.15) == 0.0


def test_returns_floats():
    assert isinstance(temperature.c_to_f(0), float)
    assert isinstance(temperature.f_to_c(212), float)
    assert isinstance(temperature.c_to_k(0), float)


def test_c_to_f_room_temperature():
    assert temperature.c_to_f(25) == 77.0


def test_f_to_c_freezing_point():
    assert temperature.f_to_c(32) == 0.0


def test_c_to_k_room_temperature():
    assert temperature.c_to_k(25) == 298.15
