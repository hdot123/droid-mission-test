"""Tests for the affine cipher component (affine.py)."""

import pytest

from affine import decode, encode


def test_encode_affine_reference():
    assert encode("Affine", 5, 8) == "Ihhwvc"


def test_decode_affine_reference():
    assert decode("Ihhwvc", 5, 8) == "Affine"


def test_encode_identity_key():
    assert encode("abc", 1, 0) == "abc"


def test_encode_hello():
    assert encode("Hello", 25, 3) == "Wzssp"


def test_decode_hello():
    assert decode("Wzssp", 25, 3) == "Hello"


def test_encode_non_coprime_raises():
    with pytest.raises(ValueError):
        encode("Hi", 2, 0)


def test_decode_non_coprime_raises():
    with pytest.raises(ValueError):
        decode("Hi", 2, 0)


def test_round_trip_identity():
    text = "Secret message"
    assert decode(encode(text, 7, 11), 7, 11) == text
