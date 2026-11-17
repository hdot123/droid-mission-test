"""Tests for clamp.py only."""

from clamp import clamp


def test_clamp_inside_range():
    assert clamp(5, 1, 10) == 5


def test_clamp_below_lo():
    assert clamp(-3, 0, 100) == 0


def test_clamp_above_hi():
    assert clamp(99, 0, 10) == 10


def test_additional_check_v_in_range_returns_v():
    # Spec rule: v in [lo, hi] returns v itself, so clamp(7, 0, 10) is 7.
    assert clamp(7, 0, 10) == 7
