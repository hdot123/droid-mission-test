"""Tests for caesar.py (this module only)."""

from caesar import decode, encode


# HARD REQUIREMENT examples, verbatim from the process card.
def test_example_1():
    assert encode("Abc XyZ!", 2) == "Cde ZaB!"


def test_example_2():
    assert encode("abc", -1) == "zab"


def test_example_3():
    assert decode("Cde", 2) == "Abc"


def test_decode_inverse():
    assert decode(encode("Hello, World! 123", 13), 13) == "Hello, World! 123"


def test_case_preserved_and_nonletters_unchanged():
    assert encode("Abc XyZ!", 2) == "Cde ZaB!"
    assert encode("Hello, World! 123", 0) == "Hello, World! 123"
    assert encode("a1b2c3", 1) == "b1c2d3"


def test_shift_modulo_26():
    assert encode("abc", 26) == "abc"
    assert encode("abc", 27) == "bcd"
    assert encode("abc", -27) == "zab"


def test_roundtrip():
    text = "The Quick Brown Fox! 42 jumps."
    for shift in (1, 13, -5, 26, -26):
        assert decode(encode(text, shift), shift) == text


def test_empty_string():
    assert encode("", 3) == ""
    assert decode("", 3) == ""
