"""speedconv 的验收测试（第五十五轮并发 C 单，逐字覆盖验收要点）。

所有 approx 断言统一使用相对误差 1e-9。
"""

import math

import pytest

import speedconv

REL_TOL = 1e-9

ALL_UNITS = ["m/s", "km/h", "mph", "kn", "ft/s"]


def convert(value, from_unit, to_unit):
    return speedconv.convert_speed(value, from_unit, to_unit)


def approx(expected):
    return pytest.approx(expected, rel=REL_TOL)


class TestAcceptanceExamples:
    def test_zero_conversion_exact(self):
        assert convert(0, "m/s", "mph") == 0.0

    def test_ms_to_kmh(self):
        assert convert(1, "m/s", "km/h") == approx(3.6)

    def test_kmh_to_ms(self):
        assert convert(100, "km/h", "m/s") == approx(27.777777777777779)

    def test_mph_to_kmh(self):
        assert convert(60, "mph", "km/h") == approx(96.56064)

    def test_kn_to_ms(self):
        assert convert(1, "kn", "m/s") == approx(0.5144444444444445)

    def test_ms_to_kn(self):
        assert convert(1, "m/s", "kn") == approx(1.9438444924406048)

    def test_ms_to_mph(self):
        assert convert(1, "m/s", "mph") == approx(2.2369362920544025)

    def test_ms_to_fts(self):
        assert convert(1, "m/s", "ft/s") == approx(3.280839895013123)

    def test_fts_to_ms(self):
        assert convert(10, "ft/s", "m/s") == approx(3.048)

    def test_negative_value(self):
        assert convert(-5, "m/s", "km/h") == approx(-18.0)

    def test_mph_to_fts(self):
        assert convert(88, "mph", "ft/s") == approx(129.06666666666668)


class TestRoundTripAllPairs:
    @pytest.mark.parametrize("u1", ALL_UNITS)
    @pytest.mark.parametrize("u2", ALL_UNITS)
    def test_round_trip_restores_37_5(self, u1, u2):
        there = convert(37.5, u1, u2)
        back = convert(there, u2, u1)
        assert back == approx(37.5)


class TestUnknownUnits:
    def test_fps_rejected(self):
        with pytest.raises(ValueError):
            convert(1, "m/s", "fps")

    def test_knots_rejected(self):
        with pytest.raises(ValueError):
            convert(1, "knots", "m/s")

    def test_case_mismatch_rejected(self):
        with pytest.raises(ValueError):
            convert(1, "MS", "m/s")

    def test_unknown_target_unit_rejected(self):
        with pytest.raises(ValueError):
            convert(1, "m/s", "knots")


class TestCoefficientPinning:
    @pytest.mark.parametrize("unit", ALL_UNITS)
    def test_unit_to_itself_is_identity(self, unit):
        for value in (0.0, 1.0, -5.0, 37.5, 123.456):
            assert convert(value, unit, unit) == approx(value)

    def test_coefficients_match_spec(self):
        for unit in ALL_UNITS:
            assert convert(1, unit, "m/s") == approx(
                speedconv._TO_METERS_PER_SECOND[unit]
            )

    def test_relative_error_within_1e9(self):
        result = convert(1, "m/s", "km/h")
        assert math.isclose(result, 3.6, rel_tol=REL_TOL)
