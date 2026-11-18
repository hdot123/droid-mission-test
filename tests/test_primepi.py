import pytest

from primepi import nthprime, primepi


def test_primepi_zero():
    assert primepi(0) == 0


def test_primepi_one():
    assert primepi(1) == 0


def test_primepi_two():
    assert primepi(2) == 1


def test_primepi_ten():
    assert primepi(10) == 4


def test_primepi_thirty():
    assert primepi(30) == 10


def test_primepi_hundred():
    assert primepi(100) == 25


def test_primepi_thousand():
    assert primepi(1000) == 168


def test_primepi_ten_thousand():
    assert primepi(10000) == 1229


def test_nthprime_one():
    assert nthprime(1) == 2


def test_nthprime_two():
    assert nthprime(2) == 3


def test_nthprime_six():
    assert nthprime(6) == 13


def test_nthprime_twenty_five():
    assert nthprime(25) == 97


def test_nthprime_hundred():
    assert nthprime(100) == 541


def test_nthprime_thousand():
    assert nthprime(1000) == 7919


def test_primepi_negative_raises():
    with pytest.raises(ValueError):
        primepi(-1)


def test_nthprime_zero_raises():
    with pytest.raises(ValueError):
        nthprime(0)


def test_primepi_non_integer_raises():
    with pytest.raises(ValueError):
        primepi(2.5)
