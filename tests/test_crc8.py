import pytest

from crc8 import crc8, crc8_hex


def test_empty_input_is_zero():
    assert crc8(b"") == 0


def test_check_value():
    # CRC-8/SMBUS check value of the ASCII string "123456789" is 0xF4.
    assert crc8(b"123456789") == 0xF4
    assert crc8(b"123456789") == 244


def test_single_byte_examples():
    assert crc8(b"\x01") == 0x07
    assert crc8(b"A") == 0xC0


def test_returns_int_in_range():
    for payload in (b"", b"A", b"123456789", b"\x00", bytes(range(256))):
        value = crc8(payload)
        assert isinstance(value, int)
        assert 0 <= value <= 255


def test_empty_and_single_zero_byte():
    assert crc8(b"") == 0
    assert crc8(b"\x00") == 0


def test_crc8_hex_matches_crc8():
    assert crc8_hex(b"123456789") == "F4"
    assert crc8_hex(b"123456789") == "%02X" % crc8(b"123456789")
    assert crc8_hex(b"") == "00"
    assert crc8_hex(b"\x01") == "07"
    assert crc8_hex(b"A") == "C0"


def test_crc8_hex_is_uppercase_two_chars():
    for payload in (b"", b"\x01", b"A", b"123456789", b"\xff", b"\x10\x20"):
        text = crc8_hex(payload)
        assert len(text) == 2
        assert text == text.upper()
        assert text == "%02X" % crc8(payload)


def test_crc8_hex_invalid_input_raises():
    with pytest.raises(TypeError):
        crc8_hex("123456789")


def test_crc8_invalid_input_raises():
    with pytest.raises(TypeError):
        crc8("123456789")


def test_deterministic():
    payload = b"the quick brown fox jumps over the lazy dog"
    assert crc8(payload) == crc8(payload)
    assert crc8_hex(payload) == crc8_hex(payload)
