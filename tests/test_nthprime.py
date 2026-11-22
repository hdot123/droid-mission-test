import pytest

from nthprime import nth_prime


def test_first_six_primes():
    assert nth_prime(1) == 2
    assert nth_prime(2) == 3
    assert nth_prime(3) == 5
    assert nth_prime(4) == 7
    assert nth_prime(5) == 11
    assert nth_prime(6) == 13


def test_larger_values():
    assert nth_prime(10) == 29
    assert nth_prime(25) == 97
    assert nth_prime(50) == 229
    assert nth_prime(100) == 541
    assert nth_prime(1000) == 7919


def test_non_positive_raises_value_error():
    for bad in (0, -3):
        with pytest.raises(ValueError):
            nth_prime(bad)


def test_non_int_raises_type_error():
    for bad in (2.0, "3", True):
        with pytest.raises(TypeError):
            nth_prime(bad)
