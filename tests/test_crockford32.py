import pytest

from crockford32 import decode, encode


def test_encode_known_value():
    assert encode(123456789) == "3NQK8N"


def test_decode_known_value():
    assert decode("3NQK8N") == 123456789


def test_decode_case_insensitive():
    assert decode("3nqk8n") == 123456789


def test_decode_alias_o():
    assert decode("O") == 0


def test_decode_alias_l():
    assert decode("L") == 1


def test_decode_u_rejected():
    with pytest.raises(ValueError):
        decode("U")


def test_encode_negative_rejected():
    with pytest.raises(ValueError):
        encode(-1)


def test_roundtrip_identity():
    for n in (0, 1, 31, 32, 1024):
        assert decode(encode(n)) == n


def test_encode_zero():
    assert encode(0) == "0"


def test_decode_empty_string():
    with pytest.raises(ValueError):
        decode("")
