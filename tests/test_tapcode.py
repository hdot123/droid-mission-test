"""Tests for tapcode.py — Tap code (5x5, C/K merged)."""

import pytest

from tapcode import tapcode_decode, tapcode_encode


def test_encode_single_letters():
    assert tapcode_encode("A") == [(1, 1)]
    assert tapcode_encode("C") == [(1, 3)]
    assert tapcode_encode("Z") == [(5, 5)]


def test_encode_k_merges_with_c():
    assert tapcode_encode("K") == [(1, 3)]


def test_encode_hello():
    assert tapcode_encode("HELLO") == [(2, 3), (1, 5), (3, 1), (3, 1), (3, 4)]


def test_encode_empty_string():
    assert tapcode_encode("") == []


def test_encode_preprocessing():
    # uppercase, non-letters dropped, K→C
    assert tapcode_encode("tap code!") == [
        (4, 4),
        (1, 1),
        (3, 5),
        (1, 3),
        (3, 4),
        (1, 4),
        (1, 5),
    ]


def test_decode_hello():
    assert tapcode_decode([(2, 3), (1, 5), (3, 1), (3, 1), (3, 4)]) == "HELLO"


def test_decode_single_pair_returns_c():
    assert tapcode_decode([(1, 3)]) == "C"


def test_decode_empty_list():
    assert tapcode_decode([]) == ""


def test_round_trip_world():
    assert tapcode_decode(tapcode_encode("WORLD")) == "WORLD"


def test_round_trip_tapcode():
    assert tapcode_decode(tapcode_encode("TAPCODE")) == "TAPCODE"


def test_decode_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        tapcode_decode([(0, 3)])
    with pytest.raises(ValueError):
        tapcode_decode([(3, 6)])
    with pytest.raises(ValueError):
        tapcode_decode([(6, 1)])


def test_decode_malformed_raises_type_error():
    with pytest.raises(TypeError):
        tapcode_decode([("1", 3)])
    with pytest.raises(TypeError):
        tapcode_decode([(1,)])
    with pytest.raises(TypeError):
        tapcode_decode("13")


def test_encode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        tapcode_encode(42)
