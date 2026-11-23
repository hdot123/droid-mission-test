"""Tests for cssunits.css_convert (process card #830, round 54 concurrency B)."""

import math

import pytest

from cssunits import css_convert


def approx(actual, expected, tol=1e-9):
    assert abs(actual - expected) < tol, "%r != %r" % (actual, expected)


class TestConversions:
    def test_in_to_px(self):
        approx(css_convert(1, "in", "px"), 96.0)

    def test_72pt_to_px(self):
        approx(css_convert(72, "pt", "px"), 96.0)

    def test_1pt_to_px(self):
        approx(css_convert(1, "pt", "px"), 1.3333333333333333)

    def test_cm_to_in(self):
        approx(css_convert(2.54, "cm", "in"), 1.0)

    def test_em_to_px(self):
        approx(css_convert(1, "em", "px"), 16.0)

    def test_rem_to_pt(self):
        approx(css_convert(1, "rem", "pt"), 12.0)

    def test_12pt_to_pc(self):
        approx(css_convert(12, "pt", "pc"), 1.0)

    def test_pc_to_px(self):
        approx(css_convert(1, "pc", "px"), 16.0)

    def test_mm_to_cm(self):
        approx(css_convert(10, "mm", "cm"), 1.0)

    def test_px_to_in(self):
        approx(css_convert(1, "px", "in"), 0.010416666666666666)

    def test_100mm_to_in(self):
        approx(css_convert(100, "mm", "in"), 3.937007874015748)

    def test_1_5in_to_cm(self):
        approx(css_convert(1.5, "in", "cm"), 3.81)

    def test_24px_to_em(self):
        approx(css_convert(24, "px", "em"), 1.5)

    def test_24px_to_em_base_20(self):
        approx(css_convert(24, "px", "em", base_font_px=20.0), 1.2)

    def test_in_to_px_dpi_300(self):
        approx(css_convert(1, "in", "px", dpi=300.0), 300.0)

    def test_zero_pt_to_mm(self):
        approx(css_convert(0, "pt", "mm"), 0.0)

    def test_returns_float_not_rounded(self):
        result = css_convert(1, "pt", "px")
        assert isinstance(result, float)
        assert result == pytest.approx(1.3333333333333333, abs=0)


class TestValueErrors:
    def test_unknown_to_unit(self):
        with pytest.raises(ValueError):
            css_convert(1, "px", "m")

    def test_zero_dpi(self):
        with pytest.raises(ValueError):
            css_convert(1, "px", "px", dpi=0)

    def test_negative_base_font_px(self):
        with pytest.raises(ValueError):
            css_convert(1, "px", "px", base_font_px=-1)

    def test_unknown_from_unit(self):
        with pytest.raises(ValueError):
            css_convert(1, "m", "px")

    def test_zero_base_font_px(self):
        with pytest.raises(ValueError):
            css_convert(1, "em", "px", base_font_px=0)


class TestTypeErrors:
    def test_string_value(self):
        with pytest.raises(TypeError):
            css_convert("1", "px", "in")

    def test_int_from_unit(self):
        with pytest.raises(TypeError):
            css_convert(1, 5, "in")

    def test_bool_value(self):
        with pytest.raises(TypeError):
            css_convert(True, "px", "in")

    def test_none_value(self):
        with pytest.raises(TypeError):
            css_convert(None, "px", "in")

    def test_nan_value(self):
        with pytest.raises(TypeError):
            css_convert(math.nan, "px", "in")

    def test_inf_value(self):
        with pytest.raises(TypeError):
            css_convert(math.inf, "px", "in")

    def test_non_numeric_base_font_px(self):
        with pytest.raises(TypeError):
            css_convert(1, "px", "em", base_font_px="16")

    def test_non_numeric_dpi(self):
        with pytest.raises(TypeError):
            css_convert(1, "px", "in", dpi="96")

    def test_bool_from_unit(self):
        with pytest.raises(TypeError):
            css_convert(1, True, "px")
