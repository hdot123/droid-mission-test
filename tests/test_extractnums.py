"""Acceptance tests for extractnums.extract_numbers (pinned token grammar)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from extractnums import extract_numbers  # noqa: E402


# ---------------------------------------------------------------- 基本形状

def test_empty_string():
    assert extract_numbers("") == []


def test_no_numbers():
    assert extract_numbers("abc") == []


def test_digits_between_letters():
    assert extract_numbers("a1b2") == [1, 2]


def test_plain_decimal():
    assert extract_numbers("3.14") == [3.14]


def test_leading_dot_fraction():
    assert extract_numbers(".5") == [0.5]


def test_trailing_dot_is_int():
    assert extract_numbers("5.") == [5]


def test_leading_zeros():
    assert extract_numbers("007") == [7]


# ------------------------------------------------- 无符号/无指数/无千分位

def test_no_exponent():
    assert extract_numbers("1e5") == [1, 5]


def test_no_sign():
    assert extract_numbers("-5") == [5]


def test_no_thousands_separator():
    assert extract_numbers("1,000") == [1, 0]


# ------------------------------------------------- 头号文法关键例（逐字）

def test_key_example_version_string():
    # "2.0" maximally consumed, following ".1" is its OWN token (0.1).
    assert extract_numbers("v2.0.1 build 45") == [2.0, 0.1, 45]


def test_same_shaped_example():
    assert extract_numbers("3.14.15") == [3.14, 0.15]


def test_mixed_sentence():
    assert extract_numbers("price 12.50 and 3 items") == [12.5, 3]


def test_double_dots_around_digit():
    assert extract_numbers("..7..") == [0.7]


def test_zero_zero_zero():
    assert extract_numbers("0.0.0") == [0.0, 0.0]


def test_large_integer():
    assert extract_numbers("1000000") == [1000000]


def test_trailing_dot_after_digit():
    assert extract_numbers("9.") == [9]


def test_lone_dot():
    assert extract_numbers(".") == []


def test_dot_between_letters():
    assert extract_numbers("a.b") == []


def test_embedded_decimal():
    assert extract_numbers("x0.25y") == [0.25]


# ---------------------------------------------------------------- 类型逐项

def test_per_item_types_version_example():
    got = extract_numbers("v2.0.1 build 45")
    assert got == [2.0, 0.1, 45]
    assert [type(v) for v in got] == [float, float, int]


def test_per_item_types_mixed():
    got = extract_numbers("a1b2")
    assert [type(v) for v in got] == [int, int]
    got = extract_numbers("price 12.50 and 3 items")
    assert [type(v) for v in got] == [float, int]
    got = extract_numbers("3.14.15")
    assert [type(v) for v in got] == [float, float]
    got = extract_numbers("5.")
    assert [type(v) for v in got] == [int]
    got = extract_numbers(".5")
    assert [type(v) for v in got] == [float]


# ---------------------------------------------------------------- 入参约定

def test_non_str_int_raises_typeerror():
    with pytest.raises(TypeError):
        extract_numbers(12)


def test_non_str_none_raises_typeerror():
    with pytest.raises(TypeError):
        extract_numbers(None)
