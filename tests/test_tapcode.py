"""Tests for tapcode.py — Tap code (5x5, C/K merged)."""

import pytest

from tapcode import tapcode_decode, tapcode_encode


# --- encode: acceptance value cases ---


def test_encode_a():
    assert tapcode_encode("A") == [(1, 1)]


def test_encode_c():
    assert tapcode_encode("C") == [(1, 3)]


def test_encode_k_merges_with_c():
    assert tapcode_encode("K") == [(1, 3)]


def test_encode_hello():
    assert tapcode_encode("HELLO") == [
        (2, 3),
        (1, 5),
        (3, 1),
        (3, 1),
        (3, 4),
    ]


def test_encode_z():
    assert tapcode_encode("Z") == [(5, 5)]


def test_encode_empty_string():
    assert tapcode_encode("") == []


def test_encode_preprocessing_tap_code():
    # uppercase, non-letters dropped
    assert tapcode_encode("tap code!") == [
        (4, 4),
        (1, 1),
        (3, 5),
        (1, 3),
        (3, 4),
        (1, 4),
        (1, 5),
    ]


# --- decode: acceptance value cases ---


def test_decode_hello():
    assert tapcode_decode([(2, 3), (1, 5), (3, 1), (3, 1), (3, 4)]) == "HELLO"


def test_decode_one_three_is_c():
    assert tapcode_decode([(1, 3)]) == "C"


def test_decode_empty_list():
    assert tapcode_decode([]) == ""


# --- round-trip ---


def test_roundtrip_world():
    assert tapcode_decode(tapcode_encode("WORLD")) == "WORLD"


def test_roundtrip_tapcode():
    assert tapcode_decode(tapcode_encode("TAPCODE")) == "TAPCODE"


# --- decode: ValueError (coordinates outside 1-5) ---


def test_decode_row_zero_raises_value_error():
    with pytest.raises(ValueError):
        tapcode_decode([(0, 3)])


def test_decode_col_six_raises_value_error():
    with pytest.raises(ValueError):
        tapcode_decode([(3, 6)])


def test_decode_row_six_raises_value_error():
    with pytest.raises(ValueError):
        tapcode_decode([(6, 1)])


# --- TypeError cases ---


def test_decode_string_coordinate_raises_type_error():
    with pytest.raises(TypeError):
        tapcode_decode([("1", 3)])


def test_decode_short_pair_raises_type_error():
    with pytest.raises(TypeError):
        tapcode_decode([(1,)])


def test_decode_pairs_str_raises_type_error():
    with pytest.raises(TypeError):
        tapcode_decode("13")


def test_encode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        tapcode_encode(42)
