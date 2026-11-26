"""RGB <-> HSL color conversion.

Public API:
    rgb_to_hsl(r, g, b) -> (h, s, l)
    hsl_to_rgb(h, s, l) -> (r, g, b)

Note the returned tuple order is (h, s, l); this deliberately differs from
the stdlib ``colorsys`` order of (h, l, s).
"""

from __future__ import annotations

import math

__all__ = ["rgb_to_hsl", "hsl_to_rgb"]


def _check_rgb_int(name: str, value: object) -> int:
    # bool is an int subclass, but it is not an acceptable channel value here.
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")
    if value < 0 or value > 255:
        raise ValueError(f"{name} must be in [0, 255], got {value}")
    return value


def _check_hsl_number(name: str, value: object) -> float:
    # bool is an int subclass, but it is not an acceptable numeric parameter.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value}")
    return float(value)


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert an RGB color (each channel 0..255) to (h, s, l).

    h is in [0, 360), s and l are in [0, 1].  Achromatic colors get h = 0.0
    and s = 0.0 by convention.
    """
    r = _check_rgb_int("r", r)
    g = _check_rgb_int("g", g)
    b = _check_rgb_int("b", b)

    rf = r / 255.0
    gf = g / 255.0
    bf = b / 255.0

    mx = max(rf, gf, bf)
    mn = min(rf, gf, bf)
    lightness = (mx + mn) / 2.0

    if mx == mn:
        # Achromatic: hue and saturation are 0 by convention.
        return 0.0, 0.0, lightness

    delta = mx - mn
    saturation = delta / (2.0 - mx - mn) if lightness > 0.5 else delta / (mx + mn)

    if mx == rf:
        hue = (gf - bf) / delta + (6.0 if gf < bf else 0.0)
    elif mx == gf:
        hue = (bf - rf) / delta + 2.0
    else:
        hue = (rf - gf) / delta + 4.0

    hue *= 60.0
    if hue >= 360.0:
        hue -= 360.0
    if hue < 0.0:
        hue += 360.0

    return float(hue), float(saturation), float(lightness)


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """Convert an HSL color to (r, g, b) with channels 0..255.

    h must be in [0, 360) (360 excluded); s and l must be in [0, 1].
    Channel values are rounded half-up: floor(x * 255 + 0.5).
    """
    h = _check_hsl_number("h", h)
    s = _check_hsl_number("s", s)
    l = _check_hsl_number("l", l)

    if not (0.0 <= h < 360.0):
        raise ValueError(f"h must be in [0, 360), got {h}")
    if not (0.0 <= s <= 1.0):
        raise ValueError(f"s must be in [0, 1], got {s}")
    if not (0.0 <= l <= 1.0):
        raise ValueError(f"l must be in [0, 1], got {l}")

    c = (1.0 - abs(2.0 * l - 1.0)) * s
    hp = h / 60.0
    x = c * (1.0 - abs(hp % 2.0 - 1.0))
    m = l - c / 2.0

    if 0.0 <= hp < 1.0:
        rp, gp, bp = c, x, 0.0
    elif 1.0 <= hp < 2.0:
        rp, gp, bp = x, c, 0.0
    elif 2.0 <= hp < 3.0:
        rp, gp, bp = 0.0, c, x
    elif 3.0 <= hp < 4.0:
        rp, gp, bp = 0.0, x, c
    elif 4.0 <= hp < 5.0:
        rp, gp, bp = x, 0.0, c
    else:
        rp, gp, bp = c, 0.0, x

    def to_int(v: float) -> int:
        return int(math.floor(v * 255.0 + 0.5))

    return (to_int(rp + m), to_int(gp + m), to_int(bp + m))
