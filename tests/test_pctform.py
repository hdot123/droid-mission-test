"""tests/test_pctform.py: pctform 编码组件的验收测试。"""

import pytest

import pctform


def test_encode_space_and_ampersand():
    assert pctform.encode("a b&c") == "a+b%26c"


def test_encode_unreserved_passthrough():
    assert pctform.encode("~ok") == "~ok"


def test_encode_non_ascii_utf8_percent():
    assert pctform.encode("é") == "%C3%A9"


def test_decode_basic():
    assert pctform.decode("a+b%26c") == "a b&c"


def test_roundtrip_identity():
    s = "x y+z%w"
    assert pctform.decode(pctform.encode(s)) == s


def test_encode_unreserved_full_set():
    assert pctform.encode("AZaz09-._~") == "AZaz09-._~"


def test_encode_uppercase_hex():
    # U+00FF → UTF-8 bytes C3 BF → uppercase hex letters in output.
    assert pctform.encode("\xff") == "%C3%BF"
    # Single byte with letter hex digit: vertical tab → "%0B".
    assert pctform.encode("\x0b") == "%0B"


def test_decode_incomplete_escape():
    with pytest.raises(ValueError):
        pctform.decode("%A")


def test_decode_bad_hex():
    with pytest.raises(ValueError):
        pctform.decode("%zz")


def test_decode_invalid_utf8():
    with pytest.raises(ValueError):
        pctform.decode("%FF")


def test_decode_plus_becomes_space():
    assert pctform.decode("a+b") == "a b"
