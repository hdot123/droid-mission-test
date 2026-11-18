import pytest

from factorize import factor_count, prime_factors


def test_prime_factors_2():
    assert prime_factors(2) == [2]


def test_prime_factors_12():
    assert prime_factors(12) == [2, 2, 3]


def test_prime_factors_97():
    assert prime_factors(97) == [97]


def test_prime_factors_360():
    assert prime_factors(360) == [2, 2, 2, 3, 3, 5]


def test_factor_count_12():
    assert factor_count(12) == 3


def test_factor_count_97():
    assert factor_count(97) == 1


def test_factor_count_360():
    assert factor_count(360) == 6


def test_prime_factors_invalid():
    for bad in (1, -10):
        with pytest.raises(ValueError):
            prime_factors(bad)


def test_factor_count_invalid():
    for bad in (1, -10):
        with pytest.raises(ValueError):
            factor_count(bad)


def test_factor_count_matches_len():
    for n in (2, 12, 97, 360):
        assert factor_count(n) == len(prime_factors(n))


def test_factor_count_equals_prime_factors_len_invalid():
    for bad in (0, -1, 1):
        with pytest.raises(ValueError):
            factor_count(bad)
