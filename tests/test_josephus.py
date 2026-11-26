"""josephus 模块验收测试。"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from josephus import josephus


def _simulate(n: int, k: int) -> int:
    """逐个淘汰的朴素模拟，作为独立参照实现。"""
    ring = list(range(n))
    idx = 0
    while len(ring) > 1:
        idx = (idx + k - 1) % len(ring)
        ring.pop(idx)
    return ring[0]


def _closed_form_k2(n: int) -> int:
    """k = 2 闭式解：n = 2^m + L 时幸存者 = 2L。"""
    m = 0
    while (1 << m) <= n:
        m += 1
    highest = 1 << (m - 1)
    ell = n - highest
    return 2 * ell


class TestKnownValues:
    def test_josephus_5_2(self):
        assert josephus(5, 2) == 2

    def test_josephus_7_3(self):
        assert josephus(7, 3) == 3

    def test_josephus_10_2(self):
        assert josephus(10, 2) == 4

    def test_josephus_1_9(self):
        assert josephus(1, 9) == 0


class TestProperties:
    def test_k1_is_n_minus_1(self):
        for n in range(1, 41):
            assert josephus(n, 1) == n - 1

    def test_matches_simulation_full_domain(self):
        for n in range(1, 41):
            for k in range(1, 10):
                assert josephus(n, k) == _simulate(n, k), (n, k)

    def test_k2_matches_closed_form(self):
        for n in range(1, 41):
            assert josephus(n, 2) == _closed_form_k2(n), n


class TestValueErrors:
    def test_n_zero(self):
        with pytest.raises(ValueError):
            josephus(0, 2)

    def test_k_zero(self):
        with pytest.raises(ValueError):
            josephus(5, 0)


class TestTypeErrors:
    def test_float_n(self):
        with pytest.raises(TypeError):
            josephus(5.0, 2)

    def test_bool_k(self):
        with pytest.raises(TypeError):
            josephus(5, True)
