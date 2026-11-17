"""Tests for clamp module behavior only."""

from clamp import clamp


def test_in_range_returns_value():
    assert clamp(5, 1, 10) == 5


def test_below_range_returns_lo():
    assert clamp(-3, 0, 100) == 0


def test_above_range_returns_hi():
    assert clamp(99, 0, 10) == 10


def test_in_range_returns_value_seven():
    # 7 is inside [0, 10], so the in-range rule wins: result is 7.
    assert clamp(7, 0, 10) == 7
