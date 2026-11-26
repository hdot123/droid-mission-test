"""Tests for a1z26 (A1Z26 letter-index codec)."""

import pytest

from a1z26 import a1z26_decode, a1z26_encode


# --- encode acceptance points -------------------------------------------

def test_encode_empty():
    assert a1z26_encode("") == ""


def test_encode_single_a():
    assert a1z26_encode("A") == "1"


def test_encode_single_z():
    assert a1z26_encode("Z") == "26"


def test_encode_abc():
    assert a1z26_encode("ABC") == "1-2-3"


def test_encode_hello():
    assert a1z26_encode("HELLO") == "8-5-12-12-15"


def test_encode_hello_world():
    assert a1z26_encode("HELLO WORLD") == "8-5-12-12-15 23-15-18-12-4"


# --- decode acceptance points -------------------------------------------

def test_decode_empty():
    assert a1z26_decode("") == ""


def test_decode_123():
    assert a1z26_decode("1-2-3") == "ABC"


def test_decode_hello_world():
    assert (
        a1z26_decode("8-5-12-12-15 23-15-18-12-4") == "HELLO WORLD"
    )


def test_decode_26_1():
    assert a1z26_decode("26-1") == "ZA"


# --- round-trip ----------------------------------------------------------

@pytest.mark.parametrize("s", ["PYTHON", "A B C", "ZZZ AAA"])
def test_roundtrip(s):
    assert a1z26_decode(a1z26_encode(s)) == s


# --- encode errors (ValueError) -----------------------------------------

@pytest.mark.parametrize(
    "bad", ["hello", "A1", "A  B", " A"]
)
def test_encode_value_errors(bad):
    with pytest.raises(ValueError):
        a1z26_encode(bad)


# --- decode errors (ValueError) -----------------------------------------

@pytest.mark.parametrize(
    "bad", ["0", "27", "01", "1--2", "1- 2"]
)
def test_decode_value_errors(bad):
    with pytest.raises(ValueError):
        a1z26_decode(bad)


# --- TypeError for non-str ----------------------------------------------

def test_encode_none_type_error():
    with pytest.raises(TypeError):
        a1z26_encode(None)


def test_decode_none_type_error():
    with pytest.raises(TypeError):
        a1z26_decode(None)
