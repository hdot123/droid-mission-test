"""Tests for caesar.py only."""

from caesar import encode, decode


def test_encode_spec_example_mixed_case_punctuation():
    assert encode("Abc XyZ!", 2) == "Cde ZaB!"


def test_encode_negative_shift():
    assert encode("abc", -1) == "zab"


def test_decode_spec_example():
    assert decode("Cde", 2) == "Abc"


def test_encode_preserves_non_letters():
    assert encode("hello, world! 123", 3) == "khoor, zruog! 123"


def test_shift_modulo_26():
    assert encode("abc", 26) == "abc"
    assert encode("abc", 27) == "bcd"


def test_negative_shift_modulo():
    assert encode("a", -27) == "z"


def test_case_preserved():
    assert encode("AbC", 1) == "BcD"


def test_empty_string():
    assert encode("", 5) == ""


def test_no_letters():
    assert encode("123 !!", 4) == "123 !!"


def test_decode_is_inverse_of_encode():
    text = "The Quick Brown Fox! 42 jumps."
    for shift in range(-25, 26):
        assert decode(encode(text, shift), shift) == text


def test_wrap_around_z_to_a():
    assert encode("xyz", 3) == "abc"
    assert encode("XYZ", 3) == "ABC"
