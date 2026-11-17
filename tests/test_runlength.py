"""Tests for the runlength module (encode/decode only)."""

import pytest

import runlength


def test_encode_example():
    assert runlength.encode("aaabbc") == "a3b2c1"


def test_encode_empty_string():
    assert runlength.encode("") == ""


def test_encode_single_character_run():
    assert runlength.encode("a") == "a1"
    assert runlength.encode("aaaa") == "a4"


def test_encode_alternating_characters():
    assert runlength.encode("abab") == "a1b1a1b1"


def test_encode_preserves_non_letters():
    assert runlength.encode("  11!") == " 212!1"


def test_decode_empty_string():
    assert runlength.decode("") == ""


def test_decode_example():
    assert runlength.decode("a3b2c1") == "aaabbc"


def test_decode_single_character_run():
    assert runlength.decode("a1") == "a"
    assert runlength.decode("z7") == "zzzzzzz"


def test_decode_multi_digit_count():
    assert runlength.decode("a12") == "a" * 12


def test_round_trip_decode_encode():
    # encode(decode(x)) == x for every valid encoding, including
    # encodings whose source text contained digits.
    for valid in ["a1", "a3b2c1", "a1b1", "a10", " 212!1", "15", "a12", "z1x1"]:
        assert runlength.encode(runlength.decode(valid)) == valid


def test_round_trip_encode_decode():
    # decode(encode(y)) == y for text without digit characters (digits in
    # the source would be ambiguous with counts; see runlength docstring).
    for text in ["", "a", "aaabbc", "abcabc", "aaaa", "  ", "!!a!!", "Hello World!"]:
        assert runlength.decode(runlength.encode(text)) == text


def test_decode_missing_count_raises():
    with pytest.raises(ValueError):
        runlength.decode("a")


def test_decode_trailing_symbol_without_count_raises():
    with pytest.raises(ValueError):
        runlength.decode("a3b")


def test_decode_count_position_not_digit_raises():
    # Count must start with a digit where required.
    with pytest.raises(ValueError):
        runlength.decode("ab")
    with pytest.raises(ValueError):
        runlength.decode("a-2")


def test_decode_count_of_zero_raises():
    with pytest.raises(ValueError):
        runlength.decode("a0")


def test_decode_leading_zero_count_raises():
    with pytest.raises(ValueError):
        runlength.decode("a01")
