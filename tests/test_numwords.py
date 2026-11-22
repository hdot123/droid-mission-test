"""Tests for numwords.number_to_words (R52 concurrent D card, sub-issue #775)."""

import pytest

from numwords import number_to_words


# --- Acceptance value examples (each acceptance item gets a case) ----------

@pytest.mark.parametrize(
    "n,expected",
    [
        (0, "zero"),
        (5, "five"),
        (13, "thirteen"),
        (20, "twenty"),
        (40, "forty"),
        (42, "forty-two"),
        (99, "ninety-nine"),
        (100, "one hundred"),
        (115, "one hundred fifteen"),  # no "and"
        (999, "nine hundred ninety-nine"),
        (1000, "one thousand"),
        (1001, "one thousand one"),
        (1100, "one thousand one hundred"),
        (12345, "twelve thousand three hundred forty-five"),
        (100000, "one hundred thousand"),
        (1000000, "one million"),
        (2000000, "two million"),
        (100000000, "one hundred million"),
        (
            999999999,
            "nine hundred ninety-nine million nine hundred ninety-nine "
            "thousand nine hundred ninety-nine",
        ),
    ],
)
def test_number_to_words_values(n, expected):
    assert number_to_words(n) == expected


def test_no_and_in_output():
    assert "and" not in number_to_words(115)
    assert number_to_words(115) == "one hundred fifteen"


@pytest.mark.parametrize("n", [-1, 1000000000])
def test_out_of_range_raises_valueerror(n):
    with pytest.raises(ValueError):
        number_to_words(n)


@pytest.mark.parametrize("n", [2.5, "42", True])
def test_non_int_raises_typeerror(n):
    with pytest.raises(TypeError):
        number_to_words(n)
