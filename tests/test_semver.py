"""Tests for semver.py: parse, compare, is_valid."""

import pytest

import semver


class TestParse:
    def test_basic(self):
        assert semver.parse("1.2.3") == (1, 2, 3)

    def test_zeroes(self):
        assert semver.parse("0.0.0") == (0, 0, 0)

    def test_large_segments(self):
        assert semver.parse("10.20.30") == (10, 20, 30)

    @pytest.mark.parametrize(
        "bad",
        [
            "1.2",  # too few segments
            "1.2.3.4",  # too many segments
            "1.2.x",  # non-numeric segment
            "v1.2.3",  # version prefix not allowed
            "01.2.3",  # leading zero in MAJOR
            "1.02.3",  # leading zero in MINOR
            "1.2.03",  # leading zero in PATCH
            "1.2.-3",  # negative not allowed
            "",  # empty
            "1.2.3 ",  # trailing whitespace
            " 1.2.3",  # leading whitespace
        ],
    )
    def test_invalid_raises_value_error(self, bad):
        with pytest.raises(ValueError):
            semver.parse(bad)


class TestCompare:
    def test_equal(self):
        assert semver.compare("2.0.0", "2.0.0") == 0

    def test_numeric_not_lexicographic(self):
        # "1.10.0" > "1.9.9" numerically, but lexicographically "1.10.0" < "1.9.9".
        assert semver.compare("1.10.0", "1.9.9") == 1

    def test_less_than(self):
        assert semver.compare("1.2.3", "1.2.4") == -1

    def test_greater_than(self):
        assert semver.compare("1.3.0", "1.2.9") == 1

    def test_major_dominates(self):
        assert semver.compare("2.0.0", "1.9.9") == 1

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            semver.compare("1.2", "1.2.3")


class TestIsValid:
    def test_valid(self):
        assert semver.is_valid("1.2.3") is True

    def test_invalid(self):
        assert semver.is_valid("1.2") is False

    def test_leading_zero_invalid(self):
        assert semver.is_valid("01.2.3") is False

    def test_returns_bool_type(self):
        assert isinstance(semver.is_valid("1.2.3"), bool)
        assert isinstance(semver.is_valid("nope"), bool)

    @pytest.mark.parametrize("bad", ["1.2", "1.2.x", "v1.2.3", "01.2.3", "", None, 42])
    def test_never_raises(self, bad):
        assert semver.is_valid(bad) is False
