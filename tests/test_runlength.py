"""Tests for the runlength module (encode / decode)."""

import pytest

import runlength


def test_encode_example():
    assert runlength.encode("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]


def test_encode_empty_string():
    assert runlength.encode("") == []


def test_decode_example():
    assert runlength.decode([("a", 3), ("b", 2)]) == "aaabb"


def test_decode_zero_count_raises():
    with pytest.raises(ValueError):
        runlength.decode([("a", 0)])


def test_decode_negative_count_raises():
    with pytest.raises(ValueError):
        runlength.decode([("a", -1)])


def test_decode_non_integer_count_raises():
    with pytest.raises(ValueError):
        runlength.decode([("a", 2.5)])
