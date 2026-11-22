import pytest

from mobius import mobius


def test_one():
    assert mobius(1) == 1


def test_small_primes():
    assert mobius(2) == -1
    assert mobius(3) == -1
    assert mobius(5) == -1
    assert mobius(7) == -1
    assert mobius(97) == -1


def test_powers_of_primes_return_zero():
    assert mobius(4) == 0
    assert mobius(8) == 0
    assert mobius(9) == 0
    assert mobius(12) == 0
    assert mobius(360) == 0


def test_distinct_prime_counts():
    assert mobius(6) == 1
    assert mobius(10) == 1
    assert mobius(30) == -1
    assert mobius(210) == 1
    assert mobius(1001) == -1
    assert mobius(2310) == -1
    assert mobius(30030) == 1


def test_non_positive_raises_value_error():
    with pytest.raises(ValueError):
        mobius(0)
    with pytest.raises(ValueError):
        mobius(-6)


def test_non_int_raises_type_error():
    with pytest.raises(TypeError):
        mobius(2.5)
    with pytest.raises(TypeError):
        mobius("6")
    with pytest.raises(TypeError):
        mobius(True)
