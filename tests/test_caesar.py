"""Tests for caesar module only."""

import caesar
from caesar import decode, encode


def test_encode_basic_example():
    assert encode("Abc XyZ!", 2) == "Cde ZaB!"


def test_encode_negative_shift():
    assert encode("abc", -1) == "zab"


def test_decode_example():
    assert decode("Cde", 2) == "Abc"


def test_encode_preserves_case_and_other_chars():
    assert encode("Hello, World! 123", 3) == "Khoor, Zruog! 123"


def test_shift_mod_26():
    assert encode("abc", 26) == "abc"
    assert encode("abc", 27) == "bcd"


def test_decode_is_inverse_of_encode():
    text = "The Quick Brown Fox! 42"
    for shift in (0, 1, 5, 13, 25, -3, -26, 27):
        assert decode(encode(text, shift), shift) == text


def test_non_letters_unchanged():
    assert encode("!!!", 5) == "!!!"
    assert decode("123 ab-cd_", 4) == "123 wx-yz_"
