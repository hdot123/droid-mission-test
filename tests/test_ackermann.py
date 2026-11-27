"""tests/test_ackermann.py: Ackermann–Péter 函数验收测试（第五十九轮 A 单）。"""

import pytest

from ackermann import ackermann


# ---------------------------------------------------------------- 验收要点：值


def test_value_row0():
    assert ackermann(0, 0) == 1


def test_value_row1():
    assert ackermann(1, 10) == 12


def test_value_row2():
    assert ackermann(2, 100) == 203


def test_value_row3_small():
    assert ackermann(3, 5) == 253


def test_value_row3():
    assert ackermann(3, 10) == 8189


def test_value_row4_base():
    assert ackermann(4, 0) == 13


# ---------------------------------------------------------------- 验收要点：性质


def _closed(m, n):
    """逐行闭式参照实现（独立于被测模块的直算）。"""
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return 2 ** (n + 3) - 3
    if m == 4 and n == 0:
        return 13
    raise AssertionError("reference out of domain: (%r, %r)" % (m, n))


def test_grid_rows0_to_2_matches_closed_form():
    for m in range(0, 3):
        for n in range(0, 13):
            assert ackermann(m, n) == _closed(m, n), (m, n)


def test_grid_row3_matches_closed_form():
    for n in range(0, 11):
        assert ackermann(3, n) == _closed(3, n), n


def test_returns_int():
    assert isinstance(ackermann(2, 4), int)


# ------------------------------------------------- 验收要点：越界抛 ValueError


@pytest.mark.parametrize("m, n", [(5, 0), (-1, 0), (0, -1), (4, 1), (4, 2)])
def test_out_of_domain_value_error(m, n):
    with pytest.raises(ValueError):
        ackermann(m, n)


def test_m4_n_ge_1_all_value_error():
    for n in range(1, 20):
        with pytest.raises(ValueError):
            ackermann(4, n)


# --------------------------------------------------- 验收要点：类型抛 TypeError


@pytest.mark.parametrize("m, n", [(1.0, 0), (0, True)])
def test_bad_type_type_error(m, n):
    with pytest.raises(TypeError):
        ackermann(m, n)


@pytest.mark.parametrize("m, n", [(True, 0), (0, "1"), (0, 2.5), (None, 0), (0, [1])])
def test_more_bad_types_type_error(m, n):
    with pytest.raises(TypeError):
        ackermann(m, n)
