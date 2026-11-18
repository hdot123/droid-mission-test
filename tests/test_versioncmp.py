"""Tests for versioncmp.compare."""

import pytest

import versioncmp


def test_numeric_segment_ordering():
    # "1.10" vs "1.9": second segment 10 > 9
    assert versioncmp.compare("1.10", "1.9") == 1
    assert versioncmp.compare("1.9", "1.10") == -1


def test_trailing_zero_padding():
    # "1.0" vs "1": shorter side padded with 0 -> equal
    assert versioncmp.compare("1.0", "1") == 0
    assert versioncmp.compare("1", "1.0") == 0


def test_extra_segment_makes_greater():
    assert versioncmp.compare("2.0.1", "2.0") == 1
    assert versioncmp.compare("2.0", "2.0.1") == -1


def test_zero_point_comparisons():
    assert versioncmp.compare("0.9", "1.0") == -1
    assert versioncmp.compare("1.0", "0.9") == 1


def test_equal_versions():
    assert versioncmp.compare("1.2.3", "1.2.3") == 0
    assert versioncmp.compare("0", "0.0.0") == 0


def test_lexicographic_is_not_used():
    # Must compare numerically, not as strings.
    assert versioncmp.compare("1.2", "1.11") == -1
    assert versioncmp.compare("10.0", "9.9") == 1


def test_non_numeric_segment_raises():
    with pytest.raises(ValueError):
        versioncmp.compare("1.a", "1.0")
    with pytest.raises(ValueError):
        versioncmp.compare("1.0", "2.b")
    with pytest.raises(ValueError):
        versioncmp.compare("", "1.0")
