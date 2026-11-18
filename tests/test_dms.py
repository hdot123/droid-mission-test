import pytest

from dms import from_dms, to_dms


def test_to_dms_eiffel_tower():
    assert to_dms(48.8584) == (48, 51, 30.24)


def test_to_dms_west_longitude_sign_in_degrees():
    assert to_dms(-118.2437) == (-118, 14, 37.32)


def test_to_dms_zero():
    assert to_dms(0) == (0, 0, 0.0)


def test_from_dms_positive():
    assert from_dms(48, 51, 30.24) == 48.8584


def test_from_dms_negative():
    assert from_dms(-118, 14, 37.32) == -118.2437


def test_from_dms_zero():
    assert from_dms(0, 0, 0) == 0.0


def test_from_dms_rejects_minutes_out_of_range():
    with pytest.raises(ValueError):
        from_dms(0, 60, 0)


def test_from_dms_rejects_negative_minutes():
    with pytest.raises(ValueError):
        from_dms(1, -1, 0)


def test_round_trip_positive():
    d, m, s = to_dms(48.8584)
    assert abs(from_dms(d, m, s) - 48.8584) < 1e-9


def test_round_trip_negative():
    d, m, s = to_dms(-118.2437)
    assert abs(from_dms(d, m, s) - (-118.2437)) < 1e-9


def test_to_dms_seconds_rounded_to_six_decimals():
    assert to_dms(48.858436111111) == (48, 51, 30.37)


def test_to_dms_rounding_carries_into_minutes():
    assert to_dms(59.9999996 / 3600) == (0, 1, 0.0)


def test_to_dms_rounding_carries_into_degrees():
    assert to_dms(0.9999999999) == (1, 0, 0.0)
    assert to_dms(-0.9999999999) == (-1, 0, 0.0)


def test_from_dms_accepts_seconds_of_sixty_as_carry():
    assert from_dms(0, 0, 60.0) == 60 / 3600
    assert from_dms(0, 59, 60.0) == 1.0


def test_from_dms_rejects_bad_seconds():
    for bad in (-1.0, 60.5):
        with pytest.raises(ValueError):
            from_dms(0, 0, bad)
