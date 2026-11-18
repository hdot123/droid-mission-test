"""Tests for iban.py only."""

import pytest

from iban import is_valid


def test_valid_gb_iban():
    assert is_valid("GB29 NWBK 6016 1331 9268 19") is True


def test_invalid_gb_iban_checksum():
    assert is_valid("GB29 NWBK 6016 1331 9268 18") is False


def test_spaces_and_case_ignored():
    assert is_valid("gb29 nwbk 6016 1331 9268 19") is True
    assert is_valid("GB29NWBK60161331926819") is True


def test_non_alphanumeric_returns_false_not_raise():
    assert is_valid("GB29-NWBK-6016-1331-9268-19") is False
    assert is_valid("GB29 NWBK 6016 1331 9268 19!") is False
    assert is_valid("") is False
    assert is_valid("!!!") is False


def test_other_valid_iban():
    # DE IBAN: rearranged digits mod 97 == 1
    assert is_valid("DE89 3704 0044 0532 0130 00") is True
    assert is_valid("DE89 3704 0044 0532 0130 01") is False
