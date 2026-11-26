"""tests/test_eulerian.py — Eulerian 数验收测试（逐字覆盖验收要点）。"""

import itertools
import math

import pytest

from eulerian import eulerian, eulerian_row


def test_row_1():
    assert eulerian_row(1) == [1]


def test_row_4():
    assert eulerian_row(4) == [1, 11, 11, 1]


def test_row_5():
    assert eulerian_row(5) == [1, 26, 66, 26, 1]


def test_row_6():
    assert eulerian_row(6) == [1, 57, 302, 302, 57, 1]


def test_value_10_3():
    assert eulerian(10, 3) == 455192


def test_row_sum_is_factorial():
    for n in range(1, 13):
        assert sum(eulerian_row(n)) == math.factorial(n)


def test_symmetry():
    for n in range(1, 13):
        for m in range(n):
            assert eulerian(n, m) == eulerian(n, n - 1 - m)


def test_worpitzky_identity():
    for n in range(1, 13):
        for m in range(n):
            total = 0
            for k in range(m + 2):
                term = ((-1) ** k) * math.comb(n + 1, k) * (m + 1 - k) ** n
                total += term
            assert eulerian(n, m) == total


def test_brute_force_descents_n_le_7():
    for n in range(1, 8):
        counts = [0] * n
        for perm in itertools.permutations(range(n)):
            descents = sum(1 for i in range(n - 1) if perm[i] > perm[i + 1])
            counts[descents] += 1
        assert eulerian_row(n) == counts


def test_value_error_cases():
    for args in ((0, 0), (5, 5), (5, -1)):
        with pytest.raises(ValueError):
            eulerian(*args)
    with pytest.raises(ValueError):
        eulerian_row(0)


def test_type_error_cases():
    with pytest.raises(TypeError):
        eulerian(5.0, 2)
    with pytest.raises(TypeError):
        eulerian(5, True)
    with pytest.raises(TypeError):
        eulerian_row("5")
