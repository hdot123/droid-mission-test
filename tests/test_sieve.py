import pytest

from sieve import is_prime, primes_up_to


class TestPrimesUpTo:
    def test_10(self):
        assert primes_up_to(10) == [2, 3, 5, 7]

    def test_30(self):
        assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    def test_2(self):
        assert primes_up_to(2) == [2]

    def test_1(self):
        assert primes_up_to(1) == []

    def test_0(self):
        assert primes_up_to(0) == []

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            primes_up_to(-1)


class TestIsPrime:
    def test_97(self):
        assert is_prime(97) is True

    def test_100(self):
        assert is_prime(100) is False

    def test_2(self):
        assert is_prime(2) is True

    def test_1(self):
        assert is_prime(1) is False

    def test_0(self):
        assert is_prime(0) is False

    def test_negative(self):
        assert is_prime(-7) is False
