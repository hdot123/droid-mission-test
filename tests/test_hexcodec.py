import pytest

from hexcodec import decode, encode, encode_spaced


def test_encode_basic():
    assert encode(b"\x00\xff") == "00ff"
    assert encode(b"plain") == "706c61696e"


def test_encode_empty():
    assert encode(b"") == ""


def test_encode_lowercase_no_separator():
    assert encode(b"\xde\xad\xbe\xef") == "deadbeef"
    assert encode(b"\x01\x23\x45\x67\x89\xab\xcd\xef") == "0123456789abcdef"


def test_decode_mixed_case():
    assert decode("00FF") == b"\x00\xff"
    assert decode("00ff") == b"\x00\xff"
    assert decode("DeAdBeEf") == b"\xde\xad\xbe\xef"


def test_decode_empty():
    assert decode("") == b""


def test_decode_odd_length_raises():
    with pytest.raises(ValueError):
        decode("0")


def test_decode_non_hex_raises():
    with pytest.raises(ValueError):
        decode("zz")
    with pytest.raises(ValueError):
        decode("0g")
    with pytest.raises(ValueError):
        decode("00 00")


def test_encode_spaced():
    assert encode_spaced(b"\x00\xff") == "00 ff"
    assert encode_spaced(b"") == ""
    assert encode_spaced(b"\xde\xad\xbe\xef") == "de ad be ef"


def test_roundtrip_identity():
    data = b"\xde\xad\xbe\xef"
    assert decode(encode(data)) == data
    for sample in (b"", b"\x00", b"\x00\xff", bytes(range(256))):
        assert decode(encode(sample)) == sample
        assert decode(encode_spaced(sample).replace(" ", "")) == sample
