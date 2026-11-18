"""Tests for euclid.py."""

import pytest

import euclid


def test_gcd_basic_examples():
    assert euclid.gcd(48, 36) == 12


def test_gcd_negative_input():
    assert euclid.gcd(-48, 36) == 12


def test_gcd_both_negative():
    assert euclid.gcd(-48, -36) == 12


def test_gcd_zero_zero():
    assert euclid.gcd(0, 0) == 0


def test_gcd_with_zero():
    assert euclid.gcd(0, 7) == 7
    assert euclid.gcd(7, 0) == 7


def test_lcm_basic_example():
    assert euclid.lcm(4, 6) == 12


def test_lcm_zero_input():
    assert euclid.lcm(0, 5) == 0
    assert euclid.lcm(5, 0) == 0


def test_lcm_negative_is_non_negative():
    assert euclid.lcm(-4, 6) == 12
    assert euclid.lcm(-4, -6) == 12
    assert euclid.lcm(4, -6) >= 0


def _assert_extended(a, b):
    g, x, y = euclid.extended_gcd(a, b)
    assert g == euclid.gcd(a, b)
    assert a * x + b * y == g


def test_extended_gcd_example():
    g, x, y = euclid.extended_gcd(30, 18)
    assert g == 6
    assert 30 * x + 18 * y == 6


@pytest.mark.parametrize(
    "a, b",
    [
        (30, 18),
        (48, 36),
        (-48, 36),
        (48, -36),
        (-48, -36),
        (0, 5),
        (0, -5),
        (7, 0),
        (-7, 0),
        (17, 13),
        (0, 0),
    ],
)
def test_extended_gcd_properties(a, b):
    _assert_extended(a, b)


def test_extended_gcd_zero_zero():
    g, x, y = euclid.extended_gcd(0, 0)
    assert g == 0
    assert 0 * x + 0 * y == g
