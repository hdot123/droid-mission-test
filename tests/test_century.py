"""tests for century.py: year → century / millennium helpers."""

import pytest

from century import century, century_range, millennium


# --- century() acceptance points ---

def test_century_2000():
    assert century(2000) == 20


def test_century_2001():
    assert century(2001) == 21


def test_century_1():
    assert century(1) == 1


def test_century_1900():
    assert century(1900) == 19


def test_century_2026():
    assert century(2026) == 21


def test_century_100():
    assert century(100) == 1


def test_century_101():
    assert century(101) == 2


# --- century_range() acceptance points ---

def test_century_range_2001():
    assert century_range(2001) == (2001, 2100)


def test_century_range_2000():
    assert century_range(2000) == (1901, 2000)


def test_century_range_1():
    assert century_range(1) == (1, 100)


# --- millennium() acceptance points ---

def test_millennium_2000():
    assert millennium(2000) == 2


def test_millennium_2001():
    assert millennium(2001) == 3


def test_millennium_1000():
    assert millennium(1000) == 1


def test_millennium_1001():
    assert millennium(1001) == 2


def test_millennium_1():
    assert millennium(1) == 1


# --- validation: ValueError ---

def test_century_zero_raises_value_error():
    with pytest.raises(ValueError):
        century(0)


def test_century_negative_raises_value_error():
    with pytest.raises(ValueError):
        century(-44)


def test_century_range_zero_raises_value_error():
    with pytest.raises(ValueError):
        century_range(0)


def test_millennium_zero_raises_value_error():
    with pytest.raises(ValueError):
        millennium(0)


# --- validation: TypeError ---

def test_century_float_raises_type_error():
    with pytest.raises(TypeError):
        century(2026.0)


def test_century_str_raises_type_error():
    with pytest.raises(TypeError):
        century("2000")


def test_century_bool_raises_type_error():
    with pytest.raises(TypeError):
        century(True)
