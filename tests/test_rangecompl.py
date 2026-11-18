"""Tests for rangecompl.complement."""

import pytest

from rangecompl import complement


def test_basic_gaps():
    assert complement([(2, 3), (5, 5)], 0, 7) == [(0, 1), (4, 4), (6, 7)]


def test_empty_ranges():
    assert complement([], 1, 3) == [(1, 3)]


def test_fully_covered():
    assert complement([(0, 10)], 0, 7) == []


def test_unordered_adjacent_coverage_merged():
    # (1,2) and (3,4) are adjacent; the merged coverage leaves only the ends.
    assert complement([(3, 4), (1, 2)], 0, 5) == [(0, 0), (5, 5)]


def test_range_extends_outside_window():
    assert complement([(-5, 1)], 0, 3) == [(2, 3)]


def test_invalid_interval_raises():
    with pytest.raises(ValueError):
        complement([(5, 2)], 0, 7)


def test_lo_greater_than_hi_raises():
    with pytest.raises(ValueError):
        complement([], 5, 4)


def test_overlapping_ranges_merged():
    assert complement([(1, 3), (2, 5)], 0, 7) == [(0, 0), (6, 7)]


def test_full_window_uncovered_single_point():
    assert complement([], 0, 0) == [(0, 0)]


def test_adjacent_gaps_not_split():
    # Coverage (2,4) leaves gaps [0,1] and [5,7]; nothing to merge here.
    assert complement([(2, 4)], 0, 7) == [(0, 1), (5, 7)]


def test_ranges_entirely_outside_window():
    assert complement([(-10, -1), (10, 20)], 0, 5) == [(0, 5)]


def test_point_gap_between_covered_blocks():
    # Coverage (0,0) and (2,2) leaves [1,1]; the single point is a real gap.
    assert complement([(0, 0), (2, 2)], 0, 3) == [(1, 1), (3, 3)]


def test_negative_window():
    # Covered: [-2, -1]; uncovered inside [-5, -1] is [-5, -3].
    assert complement([(-2, 0)], -5, -1) == [(-5, -3)]
