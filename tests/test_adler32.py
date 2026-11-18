"""Tests for the adler32 module (round 41)."""

import pytest

from adler32 import adler32


def test_empty():
    assert adler32(b"") == 1


def test_single_byte_a():
    assert adler32(b"a") == 6422626


def test_abc():
    assert adler32(b"abc") == 38600999


def test_wikipedia():
    assert adler32(b"Wikipedia") == 300286872


def test_digits_123456789():
    assert adler32(b"123456789") == 152961502


def test_hello_world():
    assert adler32(b"hello, world") == 492045449


def test_bytes_range_256():
    assert adler32(bytes(range(256))) == 2918612865


def test_a_times_6000():
    assert adler32(b"a" * 6000) == 2051858921


def test_non_bytes_raises_type_error():
    with pytest.raises(TypeError):
        adler32("abc")
