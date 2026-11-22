"""Tests for luhn.py."""

import pytest

from luhn import check_digit, generate, is_valid


# --- is_valid: spec examples ---------------------------------------------

def test_spec_example_valid_number():
    assert is_valid("4539 1488 0343 6467") is True


def test_spec_example_invalid_number():
    assert is_valid("4539-1488-0343-6468") is False


def test_spec_example_check_digit():
    assert check_digit("4539 1488 0343 646") == "7"


# --- is_valid: formatting and bounds -------------------------------------

def test_strips_spaces_and_hyphens():
    # Same digits as the valid spec example, different separators.
    assert is_valid("4539-1488 0343 6467") is True
    assert is_valid("4539148803436467") is True


def test_rejects_non_digit_characters():
    assert is_valid("4539 1488 0343 646a") is False
    assert is_valid("4539.1488.0343.6467") is False


def test_length_bounds():
    # 11 digits: too short (rejected regardless of checksum).
    assert is_valid("12345678901") is False
    # 12 digits is the minimum accepted length.
    twelve = generate("12345678901")  # 11-digit prefix + check digit
    assert len(twelve) == 12
    assert is_valid(twelve) is True
    # 19 digits is the maximum accepted length.
    nineteen = generate("1" * 18)
    assert len(nineteen) == 19
    assert is_valid(nineteen) is True
    # 20 digits: too long (rejected regardless of checksum).
    assert is_valid(nineteen + "0") is False


def test_rejects_empty_and_whitespace_only():
    assert is_valid("") is False
    assert is_valid("   ") is False
    assert is_valid("--") is False


def test_never_raises_on_bad_types():
    assert is_valid(None) is False
    assert is_valid(4539148803436467) is False
    assert is_valid(b"4539148803436467") is False


def test_all_zeros_passes_luhn():
    # 19 zeros: Luhn sum 0, within length bounds.
    assert is_valid("0000000000000000000") is True


# --- check_digit ----------------------------------------------------------

def test_check_digit_returns_single_digit_string():
    result = check_digit("453914880343646")
    assert isinstance(result, str)
    assert len(result) == 1
    assert result in "0123456789"


def test_check_digit_strips_separators():
    assert check_digit("4539-1488 0343 646") == check_digit("453914880343646")


def test_check_digit_makes_prefix_valid():
    prefix = "4539 1488 0343 646"
    assert is_valid(prefix + check_digit(prefix)) is True
    assert is_valid("4539-1488-0343-646" + check_digit(prefix)) is True


def test_check_digit_rejects_empty_or_non_digits():
    with pytest.raises(ValueError):
        check_digit("")
    with pytest.raises(ValueError):
        check_digit("   ")
    with pytest.raises(ValueError):
        check_digit("--")
    with pytest.raises(ValueError):
        check_digit("12a")
    with pytest.raises(ValueError):
        check_digit(123456789)


# --- generate -------------------------------------------------------------

def test_generate_appends_check_digit():
    assert generate("4539 1488 0343 646") == "4539148803436467"


def test_generate_result_is_pure_digits_and_valid():
    result = generate("4539-1488 0343-646")
    assert result == "4539148803436467"
    assert result.isascii() and result.isdigit()
    assert is_valid(result) is True


def test_generate_roundtrip_matches_check_digit():
    prefix = "5555555555554444"
    assert generate(prefix) == prefix + check_digit(prefix)


def test_generate_rejects_invalid_prefix():
    with pytest.raises(ValueError):
        generate("")
    with pytest.raises(ValueError):
        generate("12 34x")
    with pytest.raises(ValueError):
        generate(None)
