"""Tests for morse.py — only exercises morse's own behavior."""

import pytest

import morse


def test_encode_uppercase_example():
    assert morse.encode("SOS") == "... --- ..."


def test_encode_word_separator_example():
    assert morse.encode("A B") == ".- / -..."


def test_encode_lowercase_equals_uppercase():
    assert morse.encode("sos") == morse.encode("SOS")
    assert morse.encode("AbC") == ".- -... -.-."


def test_encode_digits():
    assert morse.encode("12") == ".---- ..---"
    assert morse.encode("9 0") == "----. / -----"


def test_encode_empty_string():
    assert morse.encode("") == ""


def test_encode_invalid_characters_raise_value_error():
    for bad in ("hi!", "a-b", "a,b", "a.b"):
        with pytest.raises(ValueError):
            morse.encode(bad)


def test_decode_example():
    assert morse.decode("... --- ...") == "SOS"


def test_decode_word_separator_example():
    assert morse.decode(".- / -...") == "A B"


def test_decode_returns_uppercase_and_single_space():
    assert morse.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -..") == "HELLO WORLD"


def test_decode_round_trip():
    assert morse.decode(morse.encode("Hello World 42")) == "HELLO WORLD 42"


def test_decode_empty_string():
    assert morse.decode("") == ""


def test_decode_unknown_code_group_raises_value_error():
    for bad in ("... --- ......", "..- ..-.-.", "..- / -..x."):
        with pytest.raises(ValueError):
            morse.decode(bad)
