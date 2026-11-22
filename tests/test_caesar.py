"""Tests for the caesar module only."""

from caesar import decode, encode


def test_encode_required_example_abc_xyz():
    assert encode("Abc XyZ!", 2) == "Cde ZaB!"


def test_encode_negative_shift():
    assert encode("abc", -1) == "zab"


def test_decode_required_example():
    assert decode("Cde", 2) == "Abc"


def test_encode_preserves_case_and_non_letters():
    assert encode("Hello, World! 123", 3) == "Khoor, Zruog! 123"


def test_encode_zero_shift_is_identity():
    assert encode("Abc XyZ!", 0) == "Abc XyZ!"


def test_encode_wraps_around_alphabet():
    assert encode("xyz", 3) == "abc"
    assert encode("XYZ", 3) == "ABC"


def test_encode_modulo_26_equivalent_shifts():
    assert encode("abc", 27) == encode("abc", 1)
    assert encode("abc", -27) == encode("abc", -1)


def test_decode_is_inverse_of_encode():
    text = "The quick brown fox! 42%"
    for shift in (0, 1, 5, -3, 25, 26, -26, 100):
        assert decode(encode(text, shift), shift) == text
        assert encode(decode(text, shift), shift) == text


def test_decode_negative_shift():
    assert decode("zab", -1) == "abc"


def test_empty_and_non_letter_strings():
    assert encode("", 5) == ""
    assert decode("", 5) == ""
    assert encode("123 !@#", 7) == "123 !@#"
