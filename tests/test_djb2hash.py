"""Tests for djb2hash (djb2 string hashing, 32-bit wraparound)."""

import pytest

from djb2hash import djb2, djb2_bytes


class TestKnownValues:
    def test_empty_string_is_seed(self):
        assert djb2("") == 5381

    def test_single_char_a(self):
        assert djb2("a") == 177670

    def test_abc(self):
        assert djb2("abc") == 193485963

    def test_hello(self):
        assert djb2("hello") == 261238937

    def test_bytes_empty_is_seed(self):
        assert djb2_bytes(b"") == 5381

    def test_bytes_nul(self):
        assert djb2_bytes(b"\x00") == 177573


class TestStringBytesAgreement:
    def test_hello_matches_bytes(self):
        assert djb2("Hello") == djb2_bytes(b"Hello")

    def test_cafe_utf8_matches_bytes(self):
        assert djb2("café") == djb2_bytes("café".encode("utf-8"))


class TestRange:
    def test_long_string_within_32bit_range(self):
        text = "x" * 10_000
        result = djb2(text)
        assert 0 <= result <= 4294967295

    def test_long_bytes_within_32bit_range(self):
        data = b"\xff" * 10_000
        result = djb2_bytes(data)
        assert 0 <= result <= 4294967295

    def test_various_inputs_within_32bit_range(self):
        for text in ("", "a", "abc", "hello", "café", "z" * 1000):
            assert 0 <= djb2(text) <= 4294967295


class TestTypeErrors:
    def test_djb2_int_raises(self):
        with pytest.raises(TypeError):
            djb2(123)

    def test_djb2_none_raises(self):
        with pytest.raises(TypeError):
            djb2(None)

    def test_djb2_bytes_of_str_raises(self):
        with pytest.raises(TypeError):
            djb2_bytes("abc")

    def test_djb2_bytes_of_int_raises(self):
        with pytest.raises(TypeError):
            djb2_bytes(123)

    def test_djb2_bytes_of_none_raises(self):
        with pytest.raises(TypeError):
            djb2_bytes(None)


class TestBytearrayAccepted:
    def test_bytearray_accepted(self):
        assert djb2_bytes(bytearray(b"abc")) == djb2_bytes(b"abc")
