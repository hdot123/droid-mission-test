"""Tests for luhn.py: Luhn validation helpers."""

import pytest

from luhn import check_digit, generate, is_valid


# --- is_valid: given examples ---------------------------------------------

def test_is_valid_space_grouped_example_true():
    assert is_valid("4539 1488 0343 6467") is True


def test_is_valid_hyphenated_wrong_check_digit_example_false():
    assert is_valid("4539-1488-0343-6468") is False


def test_check_digit_given_example():
    assert check_digit("4539 1488 0343 646") == "7"


# --- is_valid: separators and formatting ----------------------------------

def test_is_valid_hyphenated_valid_number_accepted():
    # Same valid number as the spaced example, hyphen-grouped: must be True.
    assert is_valid("4539-1488-0343-6467") is True


def test_is_valid_mixed_and_absent_separators():
    assert is_valid("4539148803436467") is True
    assert is_valid("4539 1488-0343 6467") is True
    assert is_valid("4539 1488 0343 646 7") is True


def test_is_valid_plain_digits_wrong_check_digit_false():
    assert is_valid("4539148803436468") is False


# --- is_valid: length gate (12-19 inclusive after stripping) ---------------

def test_is_valid_rejects_length_11():
    # 11 digits after stripping; Luhn-valid but out of the allowed range.
    assert is_valid("12345678903") is False


def test_is_valid_rejects_length_20():
    # 20 digits after stripping; Luhn-valid but out of the allowed range.
    assert is_valid("12345678901234567894") is False


def test_is_valid_accepts_boundary_lengths_12_and_19():
    assert len("123456789015") == 12
    assert is_valid("123456789015") is True
    assert len("1234567890123456785") == 19
    assert is_valid("1234567890123456785") is True


def test_is_valid_stripped_length_out_of_range_rejected():
    # 20 digits after stripping spaces/hyphens: still rejected.
    assert is_valid("1234 5678 9012 3456 7890") is False
    # 11 digits after stripping hyphens: still rejected.
    assert is_valid("1234-5678-901") is False


# --- is_valid: malformed input never raises -------------------------------

def test_is_valid_rejects_empty_and_separator_only():
    assert is_valid("") is False
    assert is_valid("   ") is False
    assert is_valid("---") is False


def test_is_valid_rejects_non_digit_content():
    assert is_valid("abcdefghijkl") is False
    assert is_valid("4539 1488 0343 646a") is False
    assert is_valid("4539-1488-0343-646.7") is False


def test_is_valid_never_raises_on_non_string():
    assert is_valid(None) is False
    assert is_valid(4539148803436467) is False


# --- check_digit: errors ---------------------------------------------------

def test_check_digit_rejects_empty_prefix():
    with pytest.raises(ValueError):
        check_digit("")


def test_check_digit_rejects_separator_only_prefix():
    with pytest.raises(ValueError):
        check_digit("   ")
    with pytest.raises(ValueError):
        check_digit("--")


def test_check_digit_rejects_non_digit_prefix():
    with pytest.raises(ValueError):
        check_digit("12a4")
    with pytest.raises(ValueError):
        check_digit("4539 1488 x")
    with pytest.raises(ValueError):
        check_digit("4539.1488")


def test_check_digit_accepts_hyphenated_prefix():
    assert check_digit("4539-1488-0343-646") == "7"
    assert check_digit("453914880343646") == "7"


# --- generate ---------------------------------------------------------------

def test_generate_returns_pure_digit_string():
    assert generate("4539 1488 0343 646") == "4539148803436467"
    assert generate("4539-1488-0343-646") == "4539148803436467"
    assert generate("453914880343646") == "4539148803436467"
    assert generate("12345678901") == "123456789015"
    out = generate("4539 1488 0343 646")
    assert out.isdigit()


def test_generate_round_trip_passes_is_valid():
    for prefix in (
        "12345678901",  # 11 -> 12 digits
        "4539 1488 0343 646",  # 15 -> 16 digits
        "4539-1488-0343-646",  # 15 -> 16 digits
        "123456789012345678",  # 18 -> 19 digits
    ):
        number = generate(prefix)
        assert is_valid(number) is True


def test_generate_rejects_invalid_prefix():
    with pytest.raises(ValueError):
        generate("")
    with pytest.raises(ValueError):
        generate("abc")
