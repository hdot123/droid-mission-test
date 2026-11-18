"""Tests for graycode module."""

import pytest

import graycode


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 3),
        (3, 2),
        (4, 6),
        (5, 7),
        (6, 5),
        (7, 4),
        (8, 12),
        (10, 15),
        (255, 128),
    ],
)
def test_encode(n, expected):
    assert graycode.encode(n) == expected


@pytest.mark.parametrize(
    "g,expected",
    [
        (15, 10),
        (128, 255),
        (3, 2),
    ],
)
def test_decode(g, expected):
    assert graycode.decode(g) == expected


def test_encode_negative_raises():
    with pytest.raises(ValueError):
        graycode.encode(-1)


def test_decode_negative_raises():
    with pytest.raises(ValueError):
        graycode.decode(-1)


def test_roundtrip_0_to_255():
    for i in range(256):
        assert graycode.decode(graycode.encode(i)) == i
