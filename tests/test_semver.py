import pytest

import semver


def test_acceptance_numeric_ordering():
    assert semver.compare("1.10.0", "1.9.9") == 1


def test_acceptance_padding_equivalence():
    assert semver.compare("2.0", "2.0.0") == 0


def test_ordering_results():
    assert semver.compare("1.0.0", "2.0.0") == -1
    assert semver.compare("2.0.0", "1.0.0") == 1
    assert semver.compare("1.2.3", "1.2.3") == 0


def test_omitted_segment_padding():
    assert semver.compare("1.2", "1.2.0") == 0
    assert semver.compare("1.2", "1.2.1") == -1
    assert semver.compare("1", "1.0.0") == 0
    assert semver.compare("1.2", "1.2.10") == -1


def test_single_segment():
    assert semver.compare("1", "2") == -1
    assert semver.compare("10", "9") == 1


def test_invalid_non_numeric_segment():
    with pytest.raises(ValueError):
        semver.compare("1.a.0", "1.0.0")
    with pytest.raises(ValueError):
        semver.compare("1.0.0", "x")
    with pytest.raises(ValueError):
        semver.compare("1..0", "1.0.0")


def test_invalid_more_than_three_segments():
    with pytest.raises(ValueError):
        semver.compare("1.2.3.4", "1.2.3")
    with pytest.raises(ValueError):
        semver.compare("1.0.0", "1.0.0.0")


def test_invalid_empty_string():
    with pytest.raises(ValueError):
        semver.compare("", "1.0.0")
    with pytest.raises(ValueError):
        semver.compare("1.0.0", "")
    with pytest.raises(ValueError):
        semver.compare("", "")
