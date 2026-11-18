import pytest

from ipv4 import is_valid_ipv4, parse_ipv4


# --- spec examples ---------------------------------------------------------

def test_valid_examples():
    assert is_valid_ipv4("192.168.0.1") is True
    assert is_valid_ipv4("0.0.0.0") is True


def test_invalid_examples():
    assert is_valid_ipv4("01.2.3.4") is False
    assert is_valid_ipv4("256.1.1.1") is False
    assert is_valid_ipv4("1.2.3") is False


def test_parse_example():
    assert parse_ipv4("192.168.0.1") == (192, 168, 0, 1)


# --- boundaries ------------------------------------------------------------

def test_leading_zeros_invalid():
    assert is_valid_ipv4("01.2.3.4") is False
    assert is_valid_ipv4("1.02.3.4") is False
    assert is_valid_ipv4("1.2.3.04") is False
    assert is_valid_ipv4("00.0.0.0") is False
    assert is_valid_ipv4("0.0.0.00") is False
    # single "0" is fine
    assert is_valid_ipv4("0.0.0.0") is True


def test_empty_segments_invalid():
    assert is_valid_ipv4(".1.2.3") is False
    assert is_valid_ipv4("1.2.3.") is False
    assert is_valid_ipv4("1..2.3") is False
    assert is_valid_ipv4("") is False


def test_out_of_range_invalid():
    assert is_valid_ipv4("255.255.255.255") is True
    assert is_valid_ipv4("256.1.1.1") is False
    assert is_valid_ipv4("1.1.1.256") is False
    assert is_valid_ipv4("999.999.999.999") is False


def test_non_digit_characters_invalid():
    assert is_valid_ipv4("192.168.0.a") is False
    assert is_valid_ipv4("192.168.-1.1") is False
    assert is_valid_ipv4("192.168.0.+1") is False
    assert is_valid_ipv4("192.168.0.1 ") is False
    assert is_valid_ipv4(" 192.168.0.1") is False


def test_wrong_segment_count_invalid():
    assert is_valid_ipv4("1.2.3") is False
    assert is_valid_ipv4("1.2.3.4.5") is False
    assert is_valid_ipv4("1.2.3.4.") is False


def test_too_many_digits_invalid():
    assert is_valid_ipv4("192.168.0001.1") is False
    assert is_valid_ipv4("0000.0.0.0") is False
    assert is_valid_ipv4("1.1.1.1000") is False


def test_non_string_input_is_false_not_raised():
    assert is_valid_ipv4(None) is False
    assert is_valid_ipv4(12345) is False


# --- parse_ipv4 ------------------------------------------------------------

def test_parse_valid():
    assert parse_ipv4("0.0.0.0") == (0, 0, 0, 0)
    assert parse_ipv4("255.255.255.255") == (255, 255, 255, 255)
    assert parse_ipv4("10.0.0.1") == (10, 0, 0, 1)


@pytest.mark.parametrize(
    "bad",
    [
        "01.2.3.4",
        "256.1.1.1",
        "1.2.3",
        "1.2.3.4.5",
        "",
        ".1.2.3",
        "1.2.3.",
        "a.b.c.d",
        "1.2.3.4x",
        "1.1.1.1000",
        " 1.2.3.4",
    ],
)
def test_parse_invalid_raises_value_error(bad):
    with pytest.raises(ValueError):
        parse_ipv4(bad)
