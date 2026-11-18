import pytest

from julian import from_jd, to_jd


def test_to_jd_known_dates():
    assert to_jd(2000, 1, 1) == 2451545
    assert to_jd(1970, 1, 1) == 2440588
    assert to_jd(1999, 12, 31) == 2451544
    assert to_jd(2026, 11, 19) == 2461364
    assert to_jd(2024, 2, 29) == 2460370
    assert to_jd(1582, 10, 15) == 2299161


def test_from_jd_known_values():
    assert from_jd(2451545) == (2000, 1, 1)
    assert from_jd(2461364) == (2026, 11, 19)


def test_to_jd_invalid_inputs():
    with pytest.raises(ValueError):
        to_jd(2026, 2, 29)
    with pytest.raises(ValueError):
        to_jd(2026, 13, 1)
    with pytest.raises(ValueError):
        to_jd(2026, 1, 0)


def test_roundtrip_2026_11_19():
    assert from_jd(to_jd(2026, 11, 19)) == (2026, 11, 19)
