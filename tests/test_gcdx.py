import pytest

import gcdx


def test_gcd_worked_example():
    assert gcdx.gcd(12, 18) == 6


def test_gcd_zero_zero():
    assert gcdx.gcd(0, 0) == 0


def test_gcd_with_zero():
    assert gcdx.gcd(0, 5) == 5
    assert gcdx.gcd(5, 0) == 5


def test_gcd_coprime():
    assert gcdx.gcd(7, 13) == 1


def test_lcm_worked_example():
    assert gcdx.lcm(4, 6) == 12


def test_lcm_zero_argument_returns_zero():
    assert gcdx.lcm(0, 6) == 0
    assert gcdx.lcm(4, 0) == 0
    assert gcdx.lcm(0, 0) == 0


def test_lcm_matches_gcd_identity():
    a, b = 12, 18
    assert gcdx.gcd(a, b) * gcdx.lcm(a, b) == a * b


def test_gcd_negative_raises_value_error():
    with pytest.raises(ValueError):
        gcdx.gcd(-1, 2)
    with pytest.raises(ValueError):
        gcdx.gcd(1, -2)


def test_lcm_negative_raises_value_error():
    with pytest.raises(ValueError):
        gcdx.lcm(-1, 2)
    with pytest.raises(ValueError):
        gcdx.lcm(1, -2)
