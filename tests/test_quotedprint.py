"""Tests for quotedprint (simplified quoted-printable codec)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import quotedprint


def test_encode_equals_sign():
    assert quotedprint.encode(b"a=b") == "a=3Db"


def test_encode_utf8_non_ascii():
    assert quotedprint.encode("café".encode("utf-8")) == "caf=C3=A9"


def test_encode_space():
    assert quotedprint.encode(b"a b") == "a=20b"


def test_encode_plain_ascii_passthrough():
    assert quotedprint.encode(b"plain") == "plain"


def test_encode_tab_and_control():
    assert quotedprint.encode(b"a\tb") == "a=09b"
    assert quotedprint.encode(b"\x00") == "=00"


def test_decode_equals_escape():
    assert quotedprint.decode("a=3Db") == b"a=b"


def test_decode_plain_ascii():
    assert quotedprint.decode("plain") == b"plain"


def test_roundtrip_identity():
    data = b"\x00\xff abc="
    assert quotedprint.decode(quotedprint.encode(data)) == data


def test_decode_bad_hex_raises():
    with pytest.raises(ValueError):
        quotedprint.decode("=ZZ")


def test_decode_trailing_equals_raises():
    with pytest.raises(ValueError):
        quotedprint.decode("abc=")


def test_decode_incomplete_escape_raises():
    with pytest.raises(ValueError):
        quotedprint.decode("a=3")
