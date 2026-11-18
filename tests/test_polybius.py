import pytest

from polybius import decode, encode


def test_encode_hello():
    assert encode("hello") == "22 31 41 41 12"


def test_decode_hello():
    assert decode("22 31 41 41 12") == "HELLO"


def test_encode_jupiter_j_shares_cell_with_i():
    assert encode("Jupiter") == "34 51 42 34 45 31 15"


def test_encode_empty_string():
    assert encode("") == ""


def test_encode_no_letters():
    assert encode("123") == ""


def test_decode_out_of_range_coordinate():
    with pytest.raises(ValueError):
        decode("99")


def test_roundtrip_polybius():
    encoded = encode("POLYBIUS")
    assert encoded == "42 12 41 23 24 34 51 44"
    assert decode(encoded) == "POLYBIUS"
