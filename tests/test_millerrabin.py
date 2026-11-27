"""tests/test_millerrabin.py: millerrabin.is_prime 的验收测试。

覆盖工作单全部验收要点：边界、梅森素数、2^32 以下最大素数、强伪素数锚、
[0, 3000] 全域与试除法逐个一致、10^7 以下随机数与试除法及手写平方乘
Miller-Rabin 两路逐个一致、入参约定（ValueError / TypeError）。
只用标准库（pytest、固定种子 random）。
"""

import random

import pytest

from millerrabin import is_prime


# ---------- 边界与普通素数/合数 ----------

def test_zero_and_one_are_not_prime():
    assert is_prime(0) is False
    assert is_prime(1) is False


def test_two_is_prime():
    assert is_prime(2) is True


def test_mersenne_prime_2_31_minus_1():
    assert is_prime(2147483647) is True


def test_largest_prime_below_2_32():
    assert is_prime(4294967291) is True


def test_large_primes_below_10_7():
    assert is_prime(999999937) is True
    assert is_prime(104729) is True


def test_2_32_minus_1_is_composite():
    assert is_prime(4294967295) is False


# ---------- 强伪素数锚（钉死项） ----------

@pytest.mark.parametrize(
    "n",
    [561, 1105, 1729, 2047, 41041, 825265, 3215031751],
    ids=str,
)
def test_pseudoprime_anchors_are_composite(n):
    assert is_prime(n) is False


def test_3215031751_fools_base_2_3_5_7_but_not_61():
    """3215031751 是基 2/3/5/7 的强伪素数，必须被基 61 判伪。"""
    def strong_probable_prime(n, a):
        d, r = n - 1, 0
        while d % 2 == 0:
            d //= 2
            r += 1
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    n = 3215031751
    assert all(strong_probable_prime(n, a) for a in (2, 3, 5, 7))
    assert not strong_probable_prime(n, 61)
    assert is_prime(n) is False


# ---------- 性质一：[0, 3000] 全域与试除法逐个一致 ----------

def _trial_division(n):
    if n < 2:
        return False
    f = 2
    while f * f <= n:
        if n % f == 0:
            return False
        f += 1
    return True


def test_full_range_0_to_3000_matches_trial_division():
    for n in range(0, 3001):
        assert is_prime(n) == _trial_division(n), n


# ---------- 性质二：< 10^7 随机数与试除法及手写平方乘 MR 两路一致 ----------

def _handwritten_miller_rabin(n):
    """手写平方乘 Miller-Rabin：基 2/3/5/7/11/13（对 < 10^7 数完备性由
    与试除法的双路交叉验证保证），仅作测试参照。"""
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def test_random_below_10_7_agrees_with_two_reference_paths():
    rng = random.Random(20261127)
    for _ in range(500):
        n = rng.randrange(0, 10_000_000)
        expected = _trial_division(n)
        assert is_prime(n) == expected, ("trial", n)
        assert _handwritten_miller_rabin(n) == expected, ("mr-ref", n)


# ---------- 入参约定 ----------

def test_negative_and_ge_2_32_raise_value_error():
    with pytest.raises(ValueError):
        is_prime(-3)
    with pytest.raises(ValueError):
        is_prime(2**32)


def test_non_int_including_bool_raises_type_error():
    with pytest.raises(TypeError):
        is_prime(7.0)
    with pytest.raises(TypeError):
        is_prime(True)
