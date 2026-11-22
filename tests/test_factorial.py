"""tests/test_factorial.py: factorial 模块验收测试（第四十二轮 C 单）。"""

import pytest

from factorial import binom, factorial


# --- factorial 验收要点 ---

def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_five():
    assert factorial(5) == 120


def test_factorial_ten():
    assert factorial(10) == 3628800


def test_factorial_twenty():
    assert factorial(20) == 2432902008176640000


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)


# --- binom 验收要点 ---

def test_binom_5_2():
    assert binom(5, 2) == 10


def test_binom_10_3():
    assert binom(10, 3) == 120


def test_binom_10_0():
    assert binom(10, 0) == 1


def test_binom_7_7():
    assert binom(7, 7) == 1


def test_binom_k_greater_than_n_raises():
    with pytest.raises(ValueError):
        binom(5, 6)


def test_binom_negative_n_raises():
    with pytest.raises(ValueError):
        binom(-1, 0)
