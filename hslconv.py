"""hslconv: RGB ↔ HSL 颜色换算组件（第五十八轮 D 单）。

- ``rgb_to_hsl(r, g, b)`` 返回 ``(h, s, l)``：h ∈ [0, 360)，s ∈ [0, 1]，
  l ∈ [0, 1]；无色（r == g == b）时按约定 h = 0.0、s = 0.0。
- ``hsl_to_rgb(h, s, l)`` 返回 ``(r, g, b)`` 整数通道；h ∈ [0, 360)
  （不含 360），s、l ∈ [0, 1]；通道值按四舍五入半上
  （``floor(x * 255 + 0.5)`` 口径）取整，不用银行家舍入（``round``）。

注意：返回元组顺序是 ``(h, s, l)``，与标准库 ``colorsys`` 的
``(h, l, s)``（HLS 序）不同。入参越界抛 ``ValueError``；
类型不合（rgb 非 int、hsl 非数值，含 bool）抛 ``TypeError``。
仅依赖标准库。
"""

import math

__all__ = ["rgb_to_hsl", "hsl_to_rgb"]


def _require_int(value, name):
    """rgb 分量必须是 int（bool 不算）。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s must be int, got %s" % (name, type(value).__name__))


def _require_number(value, name):
    """hsl 分量必须是数值（int/float，bool 不算）。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            "%s must be a real number, got %s" % (name, type(value).__name__)
        )


def _hue_to_rgb(p, q, t):
    """把单个色相分量从 [0, 1] 区间换算回 RGB 分量（float）。"""
    if t < 0.0:
        t += 1.0
    if t > 1.0:
        t -= 1.0
    if t < 1.0 / 6.0:
        return p + (q - p) * 6.0 * t
    if t < 1.0 / 2.0:
        return q
    if t < 2.0 / 3.0:
        return p + (q - p) * (2.0 / 3.0 - t) * 6.0
    return p


def rgb_to_hsl(r, g, b):
    """把 RGB 整数通道（各 ∈ [0, 255]）换算成 (h, s, l)。

    无色（r == g == b）时返回 h = 0.0、s = 0.0；h 落在 [0, 360)。
    """
    _require_int(r, "r")
    _require_int(g, "g")
    _require_int(b, "b")
    for value, name in ((r, "r"), (g, "g"), (b, "b")):
        if not 0 <= value <= 255:
            raise ValueError("%s out of range [0, 255]: %r" % (name, value))
    rf = r / 255.0
    gf = g / 255.0
    bf = b / 255.0
    mx = max(rf, gf, bf)
    mn = min(rf, gf, bf)
    lightness = (mx + mn) / 2.0
    if mx == mn:
        # 无色：按约定 h = 0.0、s = 0.0。
        return 0.0, 0.0, lightness
    delta = mx - mn
    if lightness > 0.5:
        saturation = delta / (2.0 - mx - mn)
    else:
        saturation = delta / (mx + mn)
    if mx == rf:
        hue = (gf - bf) / delta
        if gf < bf:
            hue += 6.0
    elif mx == gf:
        hue = (bf - rf) / delta + 2.0
    else:
        hue = (rf - gf) / delta + 4.0
    hue *= 60.0
    hue %= 360.0
    return hue, saturation, lightness


def hsl_to_rgb(h, s, l):
    """把 (h, s, l) 换算回 (r, g, b) 整数通道。

    h ∈ [0, 360)（不含 360），s、l ∈ [0, 1]；
    通道值按四舍五入半上 floor(x * 255 + 0.5) 取整。
    """
    _require_number(h, "h")
    _require_number(s, "s")
    _require_number(l, "l")
    if not 0 <= h < 360:
        raise ValueError("h out of range [0, 360): %r" % (h,))
    if not 0 <= s <= 1:
        raise ValueError("s out of range [0, 1]: %r" % (s,))
    if not 0 <= l <= 1:
        raise ValueError("l out of range [0, 1]: %r" % (l,))
    if s == 0:
        gray = math.floor(l * 255.0 + 0.5)
        return (gray, gray, gray)
    if l < 0.5:
        q = l * (1.0 + s)
    else:
        q = l + s - l * s
    p = 2.0 * l - q
    hue = h / 360.0
    red = _hue_to_rgb(p, q, hue + 1.0 / 3.0)
    green = _hue_to_rgb(p, q, hue)
    blue = _hue_to_rgb(p, q, hue - 1.0 / 3.0)
    return (
        math.floor(red * 255.0 + 0.5),
        math.floor(green * 255.0 + 0.5),
        math.floor(blue * 255.0 + 0.5),
    )
