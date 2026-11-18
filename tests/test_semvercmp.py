"""tests for semvercmp: 语义版本三段比较（第三十六轮交付件）。"""

import pytest

import semvercmp


def test_numerical_not_lexical():
    assert semvercmp.compare("1.2.3", "1.2.10") == -1


def test_major_bump_wins():
    assert semvercmp.compare("2.0.0", "1.999.999") == 1


def test_leading_zeros_allowed():
    assert semvercmp.compare("1.02.3", "1.2.3") == 0


def test_patch_numerical_order():
    assert semvercmp.compare("0.0.9", "0.0.10") == -1


def test_equal_versions():
    assert semvercmp.compare("1.2.3", "1.2.3") == 0


def test_segment_count_mismatch_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("1.2", "1.2.0")


def test_prerelease_suffix_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("1.2.3-alpha", "1.2.3")


def test_build_suffix_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("1.2.3+build", "1.2.3")


def test_negative_segment_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("-1.2.3", "1.2.3")


def test_non_digit_segment_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("1.2.x", "1.2.3")


def test_empty_segment_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("1..3", "1.2.3")


def test_empty_string_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("", "1.2.3")


def test_extra_segment_raises():
    with pytest.raises(ValueError):
        semvercmp.compare("1.2.3.4", "1.2.3")
