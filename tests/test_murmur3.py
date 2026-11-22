"""Tests for murmur3.py — MurmurHash3 x86_32 acceptance items."""

import pytest

from murmur3 import murmur3_32


def test_empty():
    assert murmur3_32(b"") == 0


def test_hello_default_seed():
    assert murmur3_32(b"hello") == 613153351


def test_hello_seed_1():
    assert murmur3_32(b"hello", 1) == 3142237357


def test_foo():
    assert murmur3_32(b"foo") == 4138058784


def test_digits():
    assert murmur3_32(b"123456789") == 3036607362


def test_a():
    assert murmur3_32(b"a") == 1009084850


def test_ab():
    assert murmur3_32(b"ab") == 2613040991


def test_abc():
    assert murmur3_32(b"abc") == 3017643002


def test_abcd():
    assert murmur3_32(b"abcd") == 1139631978


def test_abcde():
    assert murmur3_32(b"abcde") == 3902511862


def test_hello_seed_42():
    assert murmur3_32(b"hello", 42) == 3806057185


def test_str_input_raises_type_error():
    with pytest.raises(TypeError):
        murmur3_32("hello")


def test_negative_seed_raises_value_error():
    with pytest.raises(ValueError):
        murmur3_32(b"x", -1)


def test_seed_too_large_raises_value_error():
    with pytest.raises(ValueError):
        murmur3_32(b"x", 2**32)


def test_non_int_seed_raises_type_error():
    with pytest.raises(TypeError):
        murmur3_32(b"x", "0")


def test_result_in_range():
    for payload in (b"", b"a", b"hello", b"123456789", b"abcdefgh"):
        for seed in (0, 1, 42, 0xFFFFFFFF):
            value = murmur3_32(payload, seed)
            assert isinstance(value, int)
            assert 0 <= value <= 4294967295
