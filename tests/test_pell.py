"""tests/test_pell.py: pell_minimal 验收测试。

覆盖验收要点：公开锚值、方程回代、[2, 40] 非平方 D 与逐 y 暴力
最小解逐个一致、全部 ValueError／TypeError 入参口径。只用标准库。
"""

import math

import pytest

from pell import pell_minimal


def _brute_force(D: int) -> tuple[int, int]:
    """逐 y 暴力搜索 x² − D·y² = 1 的最小解（y ≥ 1）。"""
    y = 1
    while True:
        rhs = D * y * y + 1
        x = math.isqrt(rhs)
        if x * x == rhs:
            return (x, y)
        y += 1


# --- 验收要点：公开锚值 -------------------------------------------------

def test_d2():
    assert pell_minimal(2) == (3, 2)


def test_d3():
    assert pell_minimal(3) == (2, 1)


def test_d5():
    assert pell_minimal(5) == (9, 4)


def test_d6():
    assert pell_minimal(6) == (5, 2)


def test_d7():
    assert pell_minimal(7) == (8, 3)


def test_d10():
    assert pell_minimal(10) == (19, 6)


def test_d13():
    assert pell_minimal(13) == (649, 180)


def test_d61_public_anchor():
    """Bhaskara II / Fermat 挑战值：D = 61 的最小解为十位数。"""
    x, y = pell_minimal(61)
    assert (x, y) == (1766319049, 226153980)
    # 方程回代验
    assert x * x - 61 * y * y == 1


# --- 性质：[2, 40] 非平方 D --------------------------------------------

def test_range_2_40_equation_and_minimality():
    for D in range(2, 41):
        if math.isqrt(D) ** 2 == D:
            continue
        x, y = pell_minimal(D)
        assert y >= 1
        assert x * x - D * y * y == 1, D
        assert (x, y) == _brute_force(D), D


# --- ValueError --------------------------------------------------------

@pytest.mark.parametrize("D", [1, 0, -5, 4, 16])
def test_value_error(D):
    with pytest.raises(ValueError):
        pell_minimal(D)


# --- TypeError ----------------------------------------------------------

@pytest.mark.parametrize("D", [2.0, True, "7"])
def test_type_error(D):
    with pytest.raises(TypeError):
        pell_minimal(D)
