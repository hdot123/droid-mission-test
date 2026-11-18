"""Tests for ean13 only."""

import pytest

from ean13 import check_digit, is_valid


def test_check_digit_example():
    assert check_digit("400638133393") == 1


def test_is_valid_example_true():
    assert is_valid("4006381333931") is True


def test_is_valid_example_false():
    assert is_valid("4006381333932") is False


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "12345678901",       # 11 digits
        "1234567890123",     # 13 digits
        "12345678901a",      # non-digit
        "12345678901 ",      # trailing space
        400638133393,        # not a str
        None,
    ],
)
def test_check_digit_invalid_input_raises_value_error(bad):
    with pytest.raises(ValueError):
        check_digit(bad)


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "400638133393",      # 12 digits
        "40063813339310",    # 14 digits
        "400638133393x",     # non-digit
        "40063813339 1",     # embedded space
        4006381333931,       # not a str
        None,
    ],
)
def test_is_valid_malformed_returns_false_without_raising(bad):
    assert is_valid(bad) is False


def test_odd_even_weighting():
    # Position parity drives the weights: +1 at an odd position (weight 1)
    # must shift the weighted sum by 1, while +1 at an even position
    # (weight 3) must shift it by 3.
    base = "400638133393"
    base_sum = original_sum(base)

    odd_pos = list(base)
    odd_pos[0] = str((int(odd_pos[0]) + 1) % 10)  # position 1, weight 1
    assert check_digit("".join(odd_pos)) == (10 - ((base_sum + 1) % 10)) % 10

    even_pos = list(base)
    even_pos[1] = str((int(even_pos[1]) + 1) % 10)  # position 2, weight 3
    assert check_digit("".join(even_pos)) == (10 - ((base_sum + 3) % 10)) % 10

    # The two positions therefore produce different check digits here.
    assert check_digit("".join(odd_pos)) != check_digit("".join(even_pos))


def original_sum(first12):
    """Weighted sum helper mirroring the spec's weighting scheme."""
    return sum(
        int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(first12)
    )


def test_roundtrip_via_is_valid():
    # Every 12-digit prefix yields a code that is_valid accepts.
    prefix = "987654321098"
    assert is_valid(prefix + str(check_digit(prefix))) is True
