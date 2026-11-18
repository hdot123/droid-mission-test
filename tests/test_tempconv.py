"""tempconv 的验收测试（第四十轮 · 并发 D 单）。"""

import tempconv


def test_c_to_f_zero():
    assert tempconv.c_to_f(0) == 32.0


def test_c_to_f_boiling():
    assert tempconv.c_to_f(100) == 212.0


def test_c_to_f_minus_forty():
    assert tempconv.c_to_f(-40) == -40.0


def test_c_to_f_body():
    assert tempconv.c_to_f(37) == 98.6


def test_f_to_c_boiling():
    assert tempconv.f_to_c(212) == 100.0


def test_f_to_c_freezing():
    assert tempconv.f_to_c(32) == 0.0


def test_c_to_k_freezing():
    assert tempconv.c_to_k(0) == 273.15


def test_k_to_c_absolute_zero():
    assert tempconv.k_to_c(0) == -273.15


def test_k_to_c_freezing():
    assert tempconv.k_to_c(273.15) == 0.0


def test_f_to_k_freezing():
    assert tempconv.f_to_k(32) == 273.15


def test_k_to_f_absolute_zero():
    assert tempconv.k_to_f(0) == -459.67
