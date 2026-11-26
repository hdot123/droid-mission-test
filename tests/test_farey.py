"""farey 模块验收测试：覆盖 #927 B 单 farey 全部验收要点。"""

from fractions import Fraction
from math import gcd

import pytest

from farey import farey


# ---- 验收要点：具体样例 ----


def test_farey_1():
    assert farey(1) == [(0, 1), (1, 1)]


def test_farey_4():
    assert farey(4) == [
        (0, 1),
        (1, 4),
        (1, 3),
        (1, 2),
        (2, 3),
        (3, 4),
        (1, 1),
    ]


def test_farey_5():
    assert farey(5) == [
        (0, 1),
        (1, 5),
        (1, 4),
        (1, 3),
        (2, 5),
        (1, 2),
        (3, 5),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 1),
    ]


def test_farey_8_length():
    assert len(farey(8)) == 23


# ---- 验收要点：性质——与 gcd 过滤枚举逐项一致 ----


def _gcd_filtered(n: int) -> list[tuple[int, int]]:
    """独立参照实现：分母 ≤ n、分子分母互素的分数，按值升序。"""
    fracs = [
        (a, b)
        for b in range(1, n + 1)
        for a in range(0, b + 1)
        if gcd(a, b) == 1
    ]
    fracs.sort(key=lambda p: Fraction(p[0], p[1]))
    return fracs


def test_matches_gcd_filtered_enumeration():
    for n in range(1, 31):
        assert farey(n) == _gcd_filtered(n), f"mismatch at n={n}"


# ---- 验收要点：长度 == 1 + Σ φ(k) ----


def _phi(k: int) -> int:
    return sum(1 for j in range(1, k + 1) if gcd(j, k) == 1)


def test_length_equals_1_plus_totient_sum():
    for n in range(1, 31):
        expected = 1 + sum(_phi(k) for k in range(1, n + 1))
        assert len(farey(n)) == expected, f"length mismatch at n={n}"


# ---- 验收要点：相邻两项行列式 b·c − a·d == 1 ----


def test_adjacent_determinant_is_one():
    for n in range(1, 16):
        seq = farey(n)
        for (a, b), (c, d) in zip(seq, seq[1:]):
            assert b * c - a * d == 1, f"determinant fails at n={n}: {(a, b), (c, d)}"


# ---- 验收要点：入参契约 ----


def test_n_below_1_raises_value_error():
    for bad in (0, -3):
        with pytest.raises(ValueError):
            farey(bad)


def test_non_int_raises_type_error():
    for bad in (2.0, True, False, "2", None):
        with pytest.raises(TypeError):
            farey(bad)


# ---- 验收要点：两端在列、元组约分 ----


def test_endpoints_present_and_reduced():
    for n in (1, 2, 7, 30):
        seq = farey(n)
        assert seq[0] == (0, 1)
        assert seq[-1] == (1, 1)
        for a, b in seq:
            assert 0 <= a <= b <= n
            assert gcd(a, b) == 1, f"not reduced: {(a, b)} at n={n}"
        # 升序
        assert all(
            Fraction(seq[i][0], seq[i][1]) < Fraction(seq[i + 1][0], seq[i + 1][1])
            for i in range(len(seq) - 1)
        )
