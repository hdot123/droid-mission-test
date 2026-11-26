"""错排数（子阶乘）验收测试——覆盖 derange.py 全部验收要点。"""

import itertools

import pytest

from derange import derangements_upto, subfactorial


def test_subfactorial_known_values():
    assert subfactorial(0) == 1
    assert subfactorial(1) == 0
    assert subfactorial(2) == 1
    assert subfactorial(3) == 2
    assert subfactorial(4) == 9
    assert subfactorial(5) == 44
    assert subfactorial(6) == 265
    assert subfactorial(7) == 1854
    assert subfactorial(8) == 14833


def test_subfactorial_ten():
    assert subfactorial(10) == 1334961


def test_subfactorial_twenty_exact_integer():
    # 须精确整数、不得用浮点近似
    result = subfactorial(20)
    assert isinstance(result, int)
    assert result == 895014631192902121


def test_subfactorial_matches_brute_force_permutations():
    for n in range(0, 8):
        brute = sum(
            1
            for perm in itertools.permutations(range(n))
            if all(perm[i] != i for i in range(n))
        )
        assert subfactorial(n) == brute


def test_subfactorial_recurrence():
    for n in range(2, 21):
        assert subfactorial(n) == (n - 1) * (
            subfactorial(n - 1) + subfactorial(n - 2)
        )


def test_derangements_upto_zero():
    assert derangements_upto(0) == [1]


def test_derangements_upto_five():
    assert derangements_upto(5) == [1, 0, 1, 2, 9, 44]


def test_derangements_upto_length_ten():
    assert len(derangements_upto(10)) == 11


def test_derangements_upto_consistent_with_subfactorial():
    values = derangements_upto(10)
    assert len(values) == 11
    for n in range(11):
        assert values[n] == subfactorial(n)


def test_subfactorial_negative_raises_value_error():
    with pytest.raises(ValueError):
        subfactorial(-1)


def test_derangements_upto_negative_raises_value_error():
    with pytest.raises(ValueError):
        derangements_upto(-3)


def test_subfactorial_non_int_raises_type_error():
    with pytest.raises(TypeError):
        subfactorial(2.5)


def test_subfactorial_bool_raises_type_error():
    with pytest.raises(TypeError):
        subfactorial(True)


def test_derangements_upto_non_int_raises_type_error():
    with pytest.raises(TypeError):
        derangements_upto(2.5)


def test_derangements_upto_bool_raises_type_error():
    with pytest.raises(TypeError):
        derangements_upto(False)
