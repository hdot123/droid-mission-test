"""Tests for the morse module."""

import pytest

import morse


class TestEncode:
    def test_sos(self):
        assert morse.encode("SOS") == "... --- ..."

    def test_hello_world(self):
        assert (
            morse.encode("HELLO WORLD")
            == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        )

    def test_single_letter(self):
        assert morse.encode("E") == "."

    def test_digits(self):
        assert morse.encode("123") == ".---- ..--- ...--"

    def test_word_separator(self):
        assert morse.encode("A B") == ".- / -..."

    def test_multiple_word_separator(self):
        assert morse.encode("A B C") == ".- / -... / -.-."

    def test_lowercase_raises(self):
        with pytest.raises(ValueError):
            morse.encode("sos")

    def test_punctuation_raises(self):
        with pytest.raises(ValueError):
            morse.encode("HI!")

    def test_mixed_case_raises(self):
        with pytest.raises(ValueError):
            morse.encode("HeLLo")


class TestDecode:
    def test_sos(self):
        assert morse.decode("... --- ...") == "SOS"

    def test_hello_world(self):
        assert (
            morse.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
            == "HELLO WORLD"
        )

    def test_single_letter(self):
        assert morse.decode(".") == "E"

    def test_digits(self):
        assert morse.decode(".---- ..--- ...--") == "123"

    def test_unknown_code_group_raises(self):
        with pytest.raises(ValueError):
            morse.decode("... --- ......")

    def test_empty_code_raises(self):
        with pytest.raises(ValueError):
            morse.decode("")

    def test_invalid_symbol_raises(self):
        with pytest.raises(ValueError):
            morse.decode("... x ...")


class TestRoundTrip:
    @pytest.mark.parametrize(
        "text",
        [
            "SOS",
            "HELLO WORLD",
            "A",
            "ABC",
            "0123456789",
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
            "A B C D E",
        ],
    )
    def test_encode_decode_roundtrip(self, text):
        assert morse.decode(morse.encode(text)) == text
