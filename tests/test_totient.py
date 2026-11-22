import pytest

from totient import totient


def test_totient_small_values():
    assert totient(1) == 1


def test_totient_nine():
    assert totient(9) == 6


def test_totient_twelve():
    assert totient(12) == 4


def test_totient_prime():
    assert totient(97) == 96


def test_totient_hundred():
    assert totient(100) == 40


def test_totient_million():
    assert totient(1_000_000) == 400000


def test_totient_zero_raises():
    with pytest.raises(ValueError):
        totient(0)


def test_totient_negative_raises():
    with pytest.raises(ValueError):
        totient(-5)
