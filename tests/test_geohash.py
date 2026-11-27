"""tests/test_geohash.py —— geohash 编解码验收测试。

独立参考实现（整数位码交织，fractions 精确算术）用于性质对照，
与 geohash.py 的浮点二分实现互不引用。
"""

import random
from fractions import Fraction

import pytest

from geohash import geohash_decode, geohash_encode

_ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"


# ---------------------------------------------------------------------------
# 独立参考实现：先算整数格点索引，再交织成码（与模块实现路径不同）
# ---------------------------------------------------------------------------
def _ref_encode(lat, lon, precision):
    nbits = 5 * precision
    lon_bits = (nbits + 1) // 2  # 经度比特居先，奇数位时多一比特
    lat_bits = nbits // 2

    lon_i = int((Fraction(lon) + 180) * (1 << lon_bits) / 360)
    lon_i = min(lon_i, (1 << lon_bits) - 1)  # 上边界取满格
    lat_i = int((Fraction(lat) + 90) * (1 << lat_bits) / 180)
    lat_i = min(lat_i, (1 << lat_bits) - 1)

    bits = []
    for k in range(nbits):
        if k % 2 == 0:
            pos = lon_bits - 1 - k // 2
            bits.append((lon_i >> pos) & 1)
        else:
            pos = lat_bits - 1 - k // 2
            bits.append((lat_i >> pos) & 1)

    out = []
    for start in range(0, nbits, 5):
        idx = 0
        for b in bits[start:start + 5]:
            idx = (idx << 1) | b
        out.append(_ALPHABET[idx])
    return "".join(out)


def _cell_bounds(code):
    """由码反推单元边界 (lat_lo, lat_hi, lon_lo, lon_hi)，中心容差用。"""
    nbits = 5 * len(code)
    lon_bits = (nbits + 1) // 2
    lat_bits = nbits // 2
    lat, lon = geohash_decode(code)
    lat_step = 180.0 / (1 << lat_bits)
    lon_step = 360.0 / (1 << lon_bits)
    return (
        lat - lat_step / 2, lat + lat_step / 2,
        lon - lon_step / 2, lon + lon_step / 2,
    )


# ---------------------------------------------------------------------------
# 一、公开锚点
# ---------------------------------------------------------------------------
def test_encode_wikipedia_example():
    assert geohash_encode(57.64911, 10.40744, 11) == "u4pruydqqvj"


def test_encode_ezs42_not_ezjmg():
    # (42.6, -5.6) 的真值是 ezs42；坊间 ezjmg 配对为错误配对、已废弃
    assert geohash_encode(42.6, -5.6, 5) == "ezs42"


def test_encode_zero_zero():
    assert geohash_encode(0.0, 0.0, 12) == "s00000000000"


def test_decode_cell_center_u4pruydqqvj():
    lat, lon = geohash_decode("u4pruydqqvj")
    assert lat == pytest.approx(57.64911063, abs=1e-6)
    assert lon == pytest.approx(10.40743969, abs=1e-6)


# ---------------------------------------------------------------------------
# 二、性质：随机点 × precision 1..12
# ---------------------------------------------------------------------------
def test_property_random_agrees_with_reference_roundtrip_and_containment():
    rng = random.Random(59059)
    cases = []
    for _ in range(30):
        cases.append((rng.uniform(-90, 90), rng.uniform(-180, 180)))
    # 边界与中点系坐标的额外样本
    cases += [
        (0.0, 0.0),
        (90.0, 180.0),
        (-90.0, -180.0),
        (90.0, -180.0),
        (-90.0, 180.0),
        (45.0, -135.0),
        (22.5, 11.25),
        (-45.0, 135.0),
    ]
    for lat, lon in cases:
        for precision in range(1, 13):
            code = geohash_encode(lat, lon, precision)
            # 1) 与独立整数码交织实现逐个一致
            assert code == _ref_encode(lat, lon, precision), (
                lat, lon, precision, code,
            )
            # 2) decode 中心回编码恒等
            clat, clon = geohash_decode(code)
            assert geohash_encode(clat, clon, precision) == code
            # 3) 原坐标落在 decode 单元内
            lat_lo, lat_hi, lon_lo, lon_hi = _cell_bounds(code)
            assert lat_lo - 1e-9 <= lat <= lat_hi + 1e-9, (lat, lon, code)
            assert lon_lo - 1e-9 <= lon <= lon_hi + 1e-9, (lat, lon, code)


def test_decode_center_is_inside_alphabet_only():
    lat, lon = geohash_decode("ezs42")
    # ezs42 中心（对照整数索引手算：单元中心在 (42.6±0.0009, -5.6±0.0018) 量级）
    assert -90 <= lat <= 90 and -180 <= lon <= 180
    assert _ref_encode(lat, lon, 5) == "ezs42"


# ---------------------------------------------------------------------------
# 三、ValueError 面
# ---------------------------------------------------------------------------
def test_encode_value_errors():
    with pytest.raises(ValueError):
        geohash_encode(90.1, 0.0)
    with pytest.raises(ValueError):
        geohash_encode(0.0, -180.1)
    with pytest.raises(ValueError):
        geohash_encode(0.0, 0.0, 0)
    with pytest.raises(ValueError):
        geohash_encode(0.0, 0.0, 13)


def test_decode_value_errors():
    with pytest.raises(ValueError):
        geohash_decode("")
    with pytest.raises(ValueError):
        geohash_decode("a")
    with pytest.raises(ValueError):
        geohash_decode("ezjmg!")


# ---------------------------------------------------------------------------
# 四、TypeError 面
# ---------------------------------------------------------------------------
def test_encode_type_errors():
    with pytest.raises(TypeError):
        geohash_encode("0", 0.0)
    with pytest.raises(TypeError):
        geohash_encode(0.0, True)
    with pytest.raises(TypeError):
        geohash_encode(0.0, 0.0, 5.0)


def test_decode_type_errors():
    with pytest.raises(TypeError):
        geohash_decode(123)
