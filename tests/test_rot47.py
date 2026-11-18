import pytest

from rot47 import rot47


def test_hello_world():
    assert rot47("Hello, World!") == "w6==@[ (@C=5P"


def test_abc():
    assert rot47("abc") == "234"


def test_uppercase_abc():
    assert rot47("ABC") == "pqr"


def test_rot47():
    assert rot47("ROT47") == "#~%cf"


def test_empty():
    assert rot47("") == ""


def test_space_preserved():
    assert rot47(" ") == " "


def test_round_trip_identity():
    text = "Hello, World! 123"
    assert rot47(rot47(text)) == text
