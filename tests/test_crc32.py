"""crc32 模块测试（第四十二轮 · 验收要点逐条对应）。"""

import pytest

import crc32 as crc32_mod


def test_empty():
    assert crc32_mod.crc32(b"") == 0


def test_check_value_123456789():
    assert crc32_mod.crc32(b"123456789") == 3421780262


def test_hello():
    assert crc32_mod.crc32(b"hello") == 907060870


def test_single_nul_byte():
    assert crc32_mod.crc32(b"\x00") == 3523407757


def test_a_times_1000():
    assert crc32_mod.crc32(b"a" * 1000) == 2587417091


def test_wikipedia():
    assert crc32_mod.crc32(b"Wikipedia") == 2913648686


def test_str_raises_type_error():
    with pytest.raises(TypeError):
        crc32_mod.crc32("abc")
