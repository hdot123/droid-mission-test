"""Tests for hslconv: RGB <-> HSL conversion (tuple order h, s, l)."""

import colorsys
import math
import random

import pytest

from hslconv import hsl_to_rgb, rgb_to_hsl


def hue_dist(a: float, b: float) -> float:
    """Circular distance between two hues on the [0, 360) ring."""
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


# --- rgb_to_hsl fixed points -------------------------------------------------

def test_red():
    assert rgb_to_hsl(255, 0, 0) == (0.0, 1.0, 0.5)


def test_green_hue():
    h, s, l = rgb_to_hsl(0, 255, 0)
    assert h == pytest.approx(120.0, abs=1e-9)
    assert s == pytest.approx(1.0, abs=1e-9)
    assert l == pytest.approx(0.5, abs=1e-9)


def test_blue_hue():
    h, s, l = rgb_to_hsl(0, 0, 255)
    assert h == pytest.approx(240.0, abs=1e-9)
    assert s == pytest.approx(1.0, abs=1e-9)
    assert l == pytest.approx(0.5, abs=1e-9)


def test_yellow_hue():
    h, s, l = rgb_to_hsl(255, 255, 0)
    assert h == pytest.approx(60.0, abs=1e-9)
    assert s == pytest.approx(1.0, abs=1e-9)
    assert l == pytest.approx(0.5, abs=1e-9)


def test_black():
    assert rgb_to_hsl(0, 0, 0) == (0.0, 0.0, 0.0)


def test_white():
    assert rgb_to_hsl(255, 255, 255) == (0.0, 0.0, 1.0)


def test_gray():
    h, s, l = rgb_to_hsl(128, 128, 128)
    assert h == 0.0
    assert s == pytest.approx(0.0, abs=1e-12)
    assert l == pytest.approx(128 / 255, abs=1e-12)


# --- hsl_to_rgb fixed points -------------------------------------------------

def test_hsl_red():
    assert hsl_to_rgb(0, 1, 0.5) == (255, 0, 0)


def test_hsl_blue():
    assert hsl_to_rgb(240, 1, 0.5) == (0, 0, 255)


def test_hsl_green_quarter_lightness():
    assert hsl_to_rgb(120, 1, 0.25) == (0, 128, 0)


def test_hsl_black():
    assert hsl_to_rgb(0, 0, 0) == (0, 0, 0)


def test_hsl_white():
    assert hsl_to_rgb(0, 0, 1) == (255, 255, 255)


def test_hsl_output_is_int_tuple():
    result = hsl_to_rgb(0, 1, 0.5)
    assert isinstance(result, tuple)
    assert all(isinstance(v, int) and not isinstance(v, bool) for v in result)


# --- properties --------------------------------------------------------------

def test_rgb_to_hsl_matches_colorsys():
    rng = random.Random(20261126)
    for _ in range(300):
        r = rng.randint(0, 255)
        g = rng.randint(0, 255)
        b = rng.randint(0, 255)
        h, s, l = rgb_to_hsl(r, g, b)
        # colorsys order is (h, l, s), not (h, s, l); its hue is in [0, 1].
        ch, cl, cs = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        ch *= 360.0
        if r == g == b:
            # Achromatic: our convention is h = 0.0, s = 0.0.
            assert s == 0.0
            assert l == pytest.approx(cl, abs=1e-9)
        else:
            assert hue_dist(h, ch) <= 1e-6
            assert s == pytest.approx(cs, abs=1e-9)
            assert l == pytest.approx(cl, abs=1e-9)


def test_round_trip_within_one():
    rng = random.Random(4242)
    for _ in range(300):
        r = rng.randint(0, 255)
        g = rng.randint(0, 255)
        b = rng.randint(0, 255)
        rr, gg, bb = hsl_to_rgb(*rgb_to_hsl(r, g, b))
        assert abs(rr - r) <= 1
        assert abs(gg - g) <= 1
        assert abs(bb - b) <= 1


def test_hsl_to_rgb_matches_colorsys_half_up():
    # Cross-check against colorsys with half-up quantization applied.
    rng = random.Random(777)
    for _ in range(300):
        h = rng.uniform(0.0, 360.0)
        if h >= 360.0:
            h = math.nextafter(360.0, 0.0)
        s = rng.uniform(0.0, 1.0)
        l = rng.uniform(0.0, 1.0)
        got = hsl_to_rgb(h, s, l)
        # colorsys hue is in [0, 1], so convert degrees -> turns.
        hr, lr, sr = colorsys.hls_to_rgb(h / 360.0, l, s)
        expected = tuple(int(math.floor(v * 255.0 + 0.5)) for v in (hr, lr, sr))
        assert got == expected


def test_hue_in_valid_range_for_random_rgb():
    rng = random.Random(1)
    for _ in range(100):
        h, s, l = rgb_to_hsl(rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))
        assert 0.0 <= h < 360.0
        assert 0.0 <= s <= 1.0
        assert 0.0 <= l <= 1.0


# --- ValueError: out of range ------------------------------------------------

@pytest.mark.parametrize(
    "args",
    [
        (256, 0, 0),
        (0, -1, 0),
    ],
)
def test_rgb_to_hsl_value_error(args):
    with pytest.raises(ValueError):
        rgb_to_hsl(*args)


@pytest.mark.parametrize(
    "args",
    [
        (360, 1, 0.5),
        (-1, 1, 0.5),
        (0, 1.5, 0.5),
        (0, 1, -0.1),
    ],
)
def test_hsl_to_rgb_value_error(args):
    with pytest.raises(ValueError):
        hsl_to_rgb(*args)


# --- TypeError: wrong types (bool included) ----------------------------------

@pytest.mark.parametrize(
    "args",
    [
        (1.5, 0, 0),
        (True, 0, 0),
    ],
)
def test_rgb_to_hsl_type_error(args):
    with pytest.raises(TypeError):
        rgb_to_hsl(*args)


def test_hsl_to_rgb_type_error_string():
    with pytest.raises(TypeError):
        hsl_to_rgb("0", 1, 0.5)


def test_hsl_to_rgb_type_error_bool():
    with pytest.raises(TypeError):
        hsl_to_rgb(True, 1, 0.5)


# --- tuple order guard: (h, s, l), not colorsys (h, l, s) --------------------

def test_tuple_order_is_hsl_not_hls():
    h, s, l = rgb_to_hsl(0, 255, 0)
    # In (h, s, l) order, the second element is saturation (1.0), not lightness.
    assert s == pytest.approx(1.0, abs=1e-9)
    assert l == pytest.approx(0.5, abs=1e-9)
