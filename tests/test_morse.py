"""Tests for morse.py only."""

import pytest

import morse


def test_encode_sos_example():
    assert morse.encode("SOS") == "... --- ..."


def test_encode_hi_you_example():
    assert morse.encode("HI YOU") == ".... .. / -.-- --- ..-"


def test_encode_case_insensitive():
    assert morse.encode("sos") == morse.encode("SOS")
    assert morse.encode("hi you") == morse.encode("HI YOU")


def test_encode_digits():
    assert morse.encode("1") == ".----"
    assert morse.encode("a1") == ".- .----"


def test_decode_sos_example():
    assert morse.decode("... --- ...") == "SOS"


def test_decode_hi_you_example():
    assert morse.decode(".... .. / -.-- --- ..-") == "HI YOU"


def test_round_trip():
    for text in ("SOS", "HI YOU", "Hello World", "ABC 123", "Test 42"):
        assert morse.decode(morse.encode(text)) == text.upper()


def test_decode_output_uppercase_and_single_space():
    assert morse.decode(morse.encode("a b c")) == "A B C"


def test_encode_illegal_characters():
    with pytest.raises(ValueError):
        morse.encode("café")
    with pytest.raises(ValueError):
        morse.encode("HI, YOU")
    with pytest.raises(ValueError):
        morse.encode("sos!")


def test_decode_illegal_input():
    with pytest.raises(ValueError):
        morse.decode("... --- ......")
    with pytest.raises(ValueError):
        morse.decode(".... ..-..")
