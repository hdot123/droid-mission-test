"""hslconv 测试：RGB ↔ HSL 换算（逐字覆盖验收要点）。

只依赖标准库（colorsys 用于交叉验证）。随机性质测试用固定种子，
保证可复现。
"""

import colorsys
import math
import random

import pytest

from hslconv import hsl_to_rgb, rgb_to_hsl


# ---------------------------------------------------------------------------
# rgb_to_hsl 已知值
# ---------------------------------------------------------------------------


def test_rgb_to_hsl_red():
    assert rgb_to_hsl(255, 0, 0) == (0.0, 1.0, 0.5)


def test_rgb_to_hsl_green():
    h, s, l = rgb_to_hsl(0, 255, 0)
    assert h == pytest.approx(120.0, abs=1e-9)
    assert s == pytest.approx(1.0, abs=1e-9)
    assert l == pytest.approx(0.5, abs=1e-9)


def test_rgb_to_hsl_blue():
    h, _s, _l = rgb_to_hsl(0, 0, 255)
    assert h == pytest.approx(240.0, abs=1e-9)


def test_rgb_to_hsl_yellow():
    h, _s, _l = rgb_to_hsl(255, 255, 0)
    assert h == pytest.approx(60.0, abs=1e-9)


def test_rgb_to_hsl_black():
    assert rgb_to_hsl(0, 0, 0) == (0.0, 0.0, 0.0)


def test_rgb_to_hsl_white():
    assert rgb_to_hsl(255, 255, 255) == (0.0, 0.0, 1.0)


def test_rgb_to_hsl_gray_achromatic():
    h, s, l = rgb_to_hsl(128, 128, 128)
    assert s == pytest.approx(0.0, abs=1e-9)
    assert l == pytest.approx(128 / 255, abs=1e-12)
    # 无色约定：色相按 0.0 处理
    assert h == 0.0


def test_rgb_to_hsl_output_ranges():
    rng = random.Random(7)
    for _ in range(300):
        r, g, b = (rng.randrange(256) for _ in range(3))
        h, s, l = rgb_to_hsl(r, g, b)
        assert 0 <= h < 360
        assert 0 <= s <= 1
        assert 0 <= l <= 1


# ---------------------------------------------------------------------------
# hsl_to_rgb 已知值
# ---------------------------------------------------------------------------


def test_hsl_to_rgb_red():
    assert hsl_to_rgb(0, 1, 0.5) == (255, 0, 0)


def test_hsl_to_rgb_blue():
    assert hsl_to_rgb(240, 1, 0.5) == (0, 0, 255)


def test_hsl_to_rgb_green_half_up_rounding():
    # 120/360 位置的绿：G 通道恰好半值，须按半上取 128（非银行家舍入的 128 也对，
    # 但 254.5 → 255 这类下例才是半上的判据）
    assert hsl_to_rgb(120, 1, 0.25) == (0, 128, 0)


def test_hsl_to_rgb_black():
    assert hsl_to_rgb(0, 0, 0) == (0, 0, 0)


def test_hsl_to_rgb_white():
    assert hsl_to_rgb(0, 0, 1) == (255, 255, 255)


def test_half_up_rounding_is_not_bankers_round():
    """通道值必须四舍五入半上 floor(x*255+0.5)，不得用 round()（银行家舍入）。

    灰色路径（s == 0）下通道值恰好是 floor(l*255+0.5)，故取 l = (k+0.5)/255
    构造精确半值：k 为偶数时 round(k+0.5) 按银行家舍入取 k，半上须取 k+1。
    """
    for k in (0, 2, 126, 128, 130):
        l = (k + 0.5) / 255
        assert l * 255 == k + 0.5, "fixture must be an exact half tie"
        assert hsl_to_rgb(0, 0, l) == (k + 1, k + 1, k + 1)
        assert round(l * 255) == k  # 银行家舍入会取偶数 k（证明两者确实分歧）
    # 半上口径本身：0.5 → 1、127.5 → 128、128.5 → 129
    assert hsl_to_rgb(0, 0, 0.5 / 255)[0] == 1
    assert hsl_to_rgb(0, 0, 127.5 / 255)[0] == 128
    assert hsl_to_rgb(0, 0, 128.5 / 255)[0] == 129


# ---------------------------------------------------------------------------
# 性质测试
# ---------------------------------------------------------------------------


def test_rgb_to_hsl_matches_colorsys_hls_order():
    """与标准库 colorsys（rgb_to_hls，注意其序为 HLS）逐分量一致；色相差按环形距离比。"""
    rng = random.Random(42)
    for _ in range(500):
        r, g, b = (rng.randrange(256) for _ in range(3))
        h, s, l = rgb_to_hsl(r, g, b)
        ch, cl, cs = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        hue_diff = abs(h - ch * 360) % 360
        hue_diff = min(hue_diff, 360 - hue_diff)
        assert hue_diff <= 1e-9, (r, g, b, h, ch * 360)
        assert s == pytest.approx(cs, abs=1e-12)
        assert l == pytest.approx(cl, abs=1e-12)


def test_hsl_to_rgb_matches_colorsys_hls_to_rgb():
    """与 colorsys.hls_to_rgb 逐分量一致（colorsys 返回 float，比较前同样按半上取整）。"""
    rng = random.Random(43)
    for _ in range(500):
        h = rng.random() * 360.0
        s = rng.random()
        l = rng.random()
        ours = hsl_to_rgb(h, s, l)
        expected = tuple(
            math.floor(v * 255.0 + 0.5)
            for v in colorsys.hls_to_rgb(h / 360.0, l, s)
        )
        assert ours == expected, (h, s, l, ours, expected)


def test_roundtrip_within_one_per_channel():
    """hsl_to_rgb(*rgb_to_hsl(r, g, b)) 与原值逐通道差 ≤ 1。"""
    rng = random.Random(44)
    for _ in range(500):
        r, g, b = (rng.randrange(256) for _ in range(3))
        back = hsl_to_rgb(*rgb_to_hsl(r, g, b))
        for orig, restored in zip((r, g, b), back):
            assert abs(orig - restored) <= 1, ((r, g, b), back)


# ---------------------------------------------------------------------------
# 入参契约
# ---------------------------------------------------------------------------


def test_rgb_to_hsl_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        rgb_to_hsl(256, 0, 0)
    with pytest.raises(ValueError):
        rgb_to_hsl(0, -1, 0)


def test_hsl_to_rgb_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        hsl_to_rgb(360, 1, 0.5)  # 360 不含
    with pytest.raises(ValueError):
        hsl_to_rgb(-1, 1, 0.5)
    with pytest.raises(ValueError):
        hsl_to_rgb(0, 1.5, 0.5)
    with pytest.raises(ValueError):
        hsl_to_rgb(0, 1, -0.1)


def test_rgb_to_hsl_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        rgb_to_hsl(1.5, 0, 0)
    with pytest.raises(TypeError):
        rgb_to_hsl(True, 0, 0)


def test_hsl_to_rgb_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        hsl_to_rgb("0", 1, 0.5)
