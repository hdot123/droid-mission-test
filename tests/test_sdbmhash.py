"""Tests for sdbmhash: sdbm string hash and hex representation."""

import pytest

import sdbmhash


def test_empty_string_hash_is_zero():
    assert sdbmhash.sdbm_hash("") == 0


def test_single_char_hash():
    assert sdbmhash.sdbm_hash("a") == 97


def test_abc_hash():
    assert sdbmhash.sdbm_hash("abc") == 807794786


def test_hex_empty():
    assert sdbmhash.sdbm_hex("") == "00000000"


def test_hex_single_char():
    assert sdbmhash.sdbm_hex("a") == "00000061"


def test_order_sensitive():
    assert sdbmhash.sdbm_hash("abc") != sdbmhash.sdbm_hash("acb")
    assert sdbmhash.sdbm_hash("ab") != sdbmhash.sdbm_hash("ba")


def test_range_and_hex_length():
    samples = [
        "",
        "a",
        "abc",
        "acb",
        "ab",
        "ba",
        "hello, world",
        "月历网格",
        "\U0001f600 emoji",
        "0" * 1000,
        "n" * 256,
    ]
    for text in samples:
        h = sdbmhash.sdbm_hash(text)
        assert isinstance(h, int)
        assert 0 <= h <= 0xFFFFFFFF
        hx = sdbmhash.sdbm_hex(text)
        assert len(hx) == 8
        assert all(c in "0123456789abcdef" for c in hx)
        assert int(hx, 16) == h


def test_hex_matches_hash_for_long_input():
    text = "The quick brown fox jumps over the lazy dog " * 50
    h = sdbmhash.sdbm_hash(text)
    assert sdbmhash.sdbm_hex(text) == format(h, "08x")
    assert 0 <= h <= 0xFFFFFFFF


def test_hash_formula_matches_multiplicative_form():
    # h = h * 65599 + b equivalence, checked on a UTF-8 string.
    text = "sdbm-哈希"
    h = 0
    for b in text.encode("utf-8"):
        h = (h * 65599 + b) & 0xFFFFFFFF
    assert sdbmhash.sdbm_hash(text) == h


def test_non_str_raises_type_error():
    with pytest.raises(TypeError):
        sdbmhash.sdbm_hash(b"abc")
    with pytest.raises(TypeError):
        sdbmhash.sdbm_hash(123)
