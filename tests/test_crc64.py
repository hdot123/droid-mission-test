import pytest

from crc64 import crc64


def test_empty():
    assert crc64(b"") == 0


def test_check_value_123456789():
    assert crc64(b"123456789") == 0x995DC9BBDF1939FA


def test_hello():
    assert crc64(b"hello") == 0x9B1EDAE5DBB937B1


def test_abc():
    assert crc64(b"abc") == 0x2CD8094A1A277627


def test_single_null_byte():
    assert crc64(b"\x00") == 0x1FADA17364673F59


def test_eight_ff_bytes():
    assert crc64(b"\xff" * 8) == 0xFFFFFFFFFFFFFFFF


def test_quick_brown_fox():
    assert crc64(b"The quick brown fox jumps over the lazy dog") == 0x5B5EB8C2E54AA1C4


def test_non_bytes_raises_type_error():
    with pytest.raises(TypeError):
        crc64("hello")
