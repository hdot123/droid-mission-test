import pytest

from morse import decode, encode


def test_encode_sos():
    assert encode("SOS") == "... --- ..."


def test_encode_hello():
    assert encode("HELLO") == ".... . .-.. .-.. ---"


def test_encode_123():
    assert encode("123") == ".---- ..--- ...--"


def test_encode_two_words():
    assert encode("SOS SOS") == "... --- ... / ... --- ..."


def test_decode_sos():
    assert decode("... --- ...") == "SOS"


def test_encode_lowercase_uppercased():
    assert encode("sos") == "... --- ..."


def test_encode_invalid_character_raises():
    with pytest.raises(ValueError):
        encode("HI!")


def test_roundtrip_identity():
    text = "MORSE CODE 2026"
    assert decode(encode(text)) == text


def test_encode_empty():
    assert encode("") == ""


def test_decode_empty():
    assert decode("") == ""
