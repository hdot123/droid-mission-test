"""tests/test_kelvin.py: kelvin.py 温标换算验收测试。"""

import pytest

from kelvin import c_to_f, c_to_k, f_to_c, k_to_c


def test_c_to_k_freezing():
    assert abs(c_to_k(0) - 273.15) < 1e-9


def test_c_to_k_boiling():
    assert abs(c_to_k(100) - 373.15) < 1e-9


def test_k_to_c_freezing():
    assert abs(k_to_c(273.15) - 0.0) < 1e-9


def test_c_to_f_freezing():
    assert abs(c_to_f(0) - 32.0) < 1e-9


def test_c_to_f_boiling():
    assert abs(c_to_f(100) - 212.0) < 1e-9


def test_f_to_c_freezing():
    assert abs(f_to_c(32) - 0.0) < 1e-9


def test_f_to_c_boiling():
    assert abs(f_to_c(212) - 100.0) < 1e-9


def test_k_to_c_negative_raises():
    with pytest.raises(ValueError):
        k_to_c(-1)


def test_c_f_round_trip_37():
    assert abs(f_to_c(c_to_f(37.0)) - 37.0) < 1e-9
