"""Tests for the runlength module."""

import pytest

import runlength


def test_encode_acceptance_example():
    assert runlength.encode("aaabbbbc") == "a3b4c"


def test_encode_no_repeats():
    assert runlength.encode("abc") == "abc"


def test_encode_empty_string():
    assert runlength.encode("") == ""


def test_decode_inverse_of_encode():
    assert runlength.decode("a3b4c") == "aaabbbbc"


def test_decode_no_counts():
    assert runlength.decode("abc") == "abc"


def test_decode_empty_string():
    assert runlength.decode("") == ""


def test_roundtrip_encode_of_decoded():
    assert runlength.encode(runlength.decode("a3b4c")) == "a3b4c"


def test_roundtrip_decode_of_encoded():
    assert runlength.decode(runlength.encode("aaabbbbc")) == "aaabbbbc"


def test_decode_leading_digit_raises():
    with pytest.raises(ValueError):
        runlength.decode("3abc")


def test_decode_zero_count_raises():
    with pytest.raises(ValueError):
        runlength.decode("a0b")
