"""tests/test_speedconv.py: speedconv.convert_speed 验收测试。"""

import math

import pytest

from speedconv import convert_speed

UNITS = ["m/s", "km/h", "mph", "kn", "ft/s"]
REL_TOL = 1e-9


def approx(actual, expected, rel=REL_TOL):
    assert math.isclose(actual, expected, rel_tol=rel, abs_tol=0.0), (
        "%r !~= %r (rel_tol=%g)" % (actual, expected, rel)
    )


def test_zero_converts_exactly():
    assert convert_speed(0, "m/s", "mph") == 0.0


def test_ms_to_kmh():
    approx(convert_speed(1, "m/s", "km/h"), 3.6)


def test_kmh_to_ms():
    approx(convert_speed(100, "km/h", "m/s"), 27.777777777777779)


def test_mph_to_kmh():
    approx(convert_speed(60, "mph", "km/h"), 96.56064)


def test_kn_to_ms():
    approx(convert_speed(1, "kn", "m/s"), 0.5144444444444445)


def test_ms_to_kn():
    approx(convert_speed(1, "m/s", "kn"), 1.9438444924406048)


def test_ms_to_mph():
    approx(convert_speed(1, "m/s", "mph"), 2.2369362920544025)


def test_ms_to_fts():
    approx(convert_speed(1, "m/s", "ft/s"), 3.280839895013123)


def test_fts_to_ms():
    approx(convert_speed(10, "ft/s", "m/s"), 3.048)


def test_negative_value():
    approx(convert_speed(-5, "m/s", "km/h"), -18.0)


def test_mph_to_fts():
    approx(convert_speed(88, "mph", "ft/s"), 129.06666666666668)


def test_roundtrip_all_unit_pairs():
    for u1 in UNITS:
        for u2 in UNITS:
            forth = convert_speed(37.5, u1, u2)
            back = convert_speed(forth, u2, u1)
            approx(back, 37.5)


def test_unknown_unit_fps():
    with pytest.raises(ValueError):
        convert_speed(1, "m/s", "fps")


def test_unknown_unit_knots():
    with pytest.raises(ValueError):
        convert_speed(1, "knots", "m/s")


def test_case_mismatch_MS():
    with pytest.raises(ValueError):
        convert_speed(1, "MS", "m/s")
