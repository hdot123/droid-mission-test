"""egyptian 贪心埃及分数展开的验收测试。"""

import math
from fractions import Fraction

import pytest

from egyptian import egyptian


def _ref_greedy(p: int, q: int) -> list[int]:
    """测试侧独立的纯整数贪心参考实现。"""
    g = math.gcd(p, q)
    p //= g
    q //= g
    out: list[int] = []
    while p > 0:
        d = -(-q // p)
        out.append(d)
        p, q = p * d - q, q * d
        g = math.gcd(p, q)
        p //= g
        q //= g
    return out


def test_examples_basic():
    assert egyptian(1, 1) == [1]
    assert egyptian(1, 7) == [7]
    assert egyptian(2, 3) == [2, 6]
    assert egyptian(3, 7) == [3, 11, 231]
    assert egyptian(4, 13) == [4, 18, 468]
    assert egyptian(5, 4) == [1, 4]
    assert egyptian(7, 15) == [3, 8, 120]
    assert egyptian(3, 4) == [2, 4]


def test_unreduced_input():
    # 2/6 未约分，先约成 1/3 再展开。
    assert egyptian(2, 6) == [3]


def test_value_errors():
    with pytest.raises(ValueError):
        egyptian(0, 3)
    with pytest.raises(ValueError):
        egyptian(1, 0)
    with pytest.raises(ValueError):
        egyptian(-1, 2)


def test_type_errors():
    with pytest.raises(TypeError):
        egyptian(1.5, 2)
    with pytest.raises(TypeError):
        egyptian(1, True)
    # bool 是 int 子类，也必须拒；其他非 int 形态同理。
    with pytest.raises(TypeError):
        egyptian(True, 2)
    with pytest.raises(TypeError):
        egyptian(1, 2.0)
    with pytest.raises(TypeError):
        egyptian("2", 3)
    with pytest.raises(TypeError):
        egyptian(1, None)


def test_return_type_is_int_list():
    out = egyptian(7, 15)
    assert isinstance(out, list)
    assert all(isinstance(d, int) and not isinstance(d, bool) for d in out)


def test_property_sweep():
    for p in range(1, 13):
        for q in range(1, 31):
            out = egyptian(p, q)

            # (1) 单位分数之和恰 == p/q（Fraction 精确验）。
            total = sum((Fraction(1, d) for d in out), Fraction(0, 1))
            assert total == Fraction(p, q), (p, q, out)

            # (2) 每步所取单位分数是 <= 当步余数的最大者。
            remainder = Fraction(p, q)
            for d in out:
                unit = Fraction(1, d)
                assert unit <= remainder, (p, q, out, d, remainder)
                expected = -(-remainder.denominator // remainder.numerator)
                assert d == expected, (p, q, out, d, expected)
                remainder -= unit
            assert remainder == 0

            # (3) 与纯整数贪心实现逐个一致。
            assert out == _ref_greedy(p, q), (p, q, out)
