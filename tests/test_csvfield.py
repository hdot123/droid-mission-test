import pytest

from csvfield import decode, encode


def test_encode_plain():
    assert encode("plain") == "plain"


def test_encode_comma():
    assert encode("a,b") == '"a,b"'


def test_encode_quote():
    assert encode('a"b') == '"a""b"'


def test_encode_newline():
    assert encode("a\nb") == '"a\nb"'
    assert encode("a\rb") == '"a\rb"'


def test_decode_quoted():
    assert decode('"a""b"') == 'a"b'


def test_decode_plain():
    assert decode("plain") == "plain"


def test_roundtrip():
    original = 'x,"y"\nz'
    assert decode(encode(original)) == original


def test_roundtrip_various():
    for field in ("", "plain", "a,b", 'a"b', "line\nbreak", "carriage\rreturn", '"', '""'):
        assert decode(encode(field)) == field


def test_decode_unclosed_quote():
    with pytest.raises(ValueError):
        decode('"abc')


def test_decode_trailing_after_close():
    with pytest.raises(ValueError):
        decode('"abc"def')
