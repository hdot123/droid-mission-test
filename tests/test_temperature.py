"""Tests for temperature.py — only this module's behavior."""

import pytest

from temperature import c_to_f, f_to_c, c_to_k, k_to_c


def test_examples():
    assert c_to_f(100) == 212.0
    assert f_to_c(32) == 0.0
    assert c_to_k(0) == 273.15
    assert k_to_c(0) == -273.15


def test_returns_float():
    assert isinstance(c_to_f(100), float)
    assert isinstance(f_to_c(32), float)
    assert isinstance(c_to_k(0), float)
    assert isinstance(k_to_c(0), float)


def test_boundary_values():
    # Absolute zero boundary values are accepted.
    assert c_to_k(-273.15) == 0.0
    assert k_to_c(0) == -273.15
    assert f_to_c(-459.67) == pytest.approx(-273.15)
    assert c_to_f(-273.15) == pytest.approx(-459.67)


def test_roundtrip():
    assert f_to_c(c_to_f(100)) == pytest.approx(100.0)
    assert k_to_c(c_to_k(0)) == pytest.approx(0.0)


def test_c_to_k_below_absolute_zero():
    with pytest.raises(ValueError):
        c_to_k(-300)


def test_k_to_c_below_absolute_zero():
    with pytest.raises(ValueError):
        k_to_c(-1)


def test_f_to_c_below_absolute_zero():
    with pytest.raises(ValueError):
        f_to_c(-460)
