"""tests for codec_rle: acceptance via codecbox.get_codec("rle") only."""

import codec_rle  # noqa: F401  (import registers the "rle" codec)
import codecbox


def _pair():
    return codecbox.get_codec("rle")


def test_encode_aaab():
    encode, _ = _pair()
    assert encode("aaab") == "a3b1"


def test_encode_abc():
    encode, _ = _pair()
    assert encode("abc") == "a1b1c1"


def test_encode_empty():
    encode, _ = _pair()
    assert encode("") == ""


def test_decode_a3b1():
    _, decode = _pair()
    assert decode("a3b1") == "aaab"


def test_decode_empty():
    _, decode = _pair()
    assert decode("") == ""


def test_round_trip_examples():
    encode, decode = _pair()
    for text in ("aaab", "abc", ""):
        assert decode(encode(text)) == text
