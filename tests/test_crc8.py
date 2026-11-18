"""CRC-8/SMBUS 校验函数的验收测试。"""

import crc8 as crc8_mod


def test_check_value_123456789():
    """标准校验值：crc8(b'123456789') == 0xF4。"""
    assert crc8_mod.crc8(b"123456789") == 0xF4


def test_empty_input_returns_zero():
    """空输入返回 0。"""
    assert crc8_mod.crc8(b"") == 0


def test_single_zero_byte_returns_zero():
    """单个 0x00 字节返回 0。"""
    assert crc8_mod.crc8(b"\x00") == 0


def test_return_value_always_in_range():
    """返回值恒在 0-255 内（覆盖多种输入）。"""
    inputs = [
        b"",
        b"\x00",
        b"\x01",
        b"\xff",
        b"123456789",
        b"foobar",
        bytes(range(256)),
        b"\x00" * 64,
        b"\xff" * 64,
    ]
    for data in inputs:
        result = crc8_mod.crc8(data)
        assert isinstance(result, int)
        assert 0 <= result <= 255


def test_known_values():
    """规格给出的验收值与可直接推导的参考值。"""
    assert crc8_mod.crc8(b"\x00\x00\x00\x00") == 0x00
    assert crc8_mod.crc8(b"123456789") == 0xF4
    # CRC-8/SMBUS 对单字节 b"\x01" 的结果可直接由算法推出：
    # 0x01 上移八次（0x01 << 8 与多项式折叠）得到 0x07。
    assert crc8_mod.crc8(b"\x01") == 0x07
