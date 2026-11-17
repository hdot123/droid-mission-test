"""Tests for ipaddr.py."""

import pytest

from ipaddr import from_int, is_private, is_valid_ipv4, to_int


# --- spec examples --------------------------------------------------------

def test_spec_example_to_int():
    assert to_int("192.168.0.1") == 3232235521


def test_spec_example_from_int():
    assert from_int(3232235521) == "192.168.0.1"


def test_spec_example_leading_zero_rejected():
    assert is_valid_ipv4("01.2.3.4") is False


def test_spec_example_private_within_172_16_block():
    assert is_private("172.31.255.255") is True


def test_spec_example_outside_172_16_block():
    assert is_private("172.32.0.1") is False


# --- is_valid_ipv4 --------------------------------------------------------

def test_valid_addresses():
    assert is_valid_ipv4("0.0.0.0") is True
    assert is_valid_ipv4("1.2.3.4") is True
    assert is_valid_ipv4("192.168.0.1") is True
    assert is_valid_ipv4("255.255.255.255") is True
    assert is_valid_ipv4("8.8.8.8") is True


def test_rejects_wrong_segment_count():
    assert is_valid_ipv4("1.2.3") is False
    assert is_valid_ipv4("1.2.3.4.5") is False
    assert is_valid_ipv4("") is False


def test_rejects_out_of_range_octet():
    assert is_valid_ipv4("256.1.1.1") is False
    assert is_valid_ipv4("1.1.1.999") is False
    assert is_valid_ipv4("1.1.1.-1") is False


def test_rejects_leading_zeros():
    assert is_valid_ipv4("01.2.3.4") is False
    assert is_valid_ipv4("1.02.3.4") is False
    assert is_valid_ipv4("1.1.1.00") is False
    # "0" itself is allowed.
    assert is_valid_ipv4("0.0.0.0") is True


def test_rejects_spaces_and_non_digits():
    assert is_valid_ipv4(" 1.2.3.4") is False
    assert is_valid_ipv4("1.2.3.4 ") is False
    assert is_valid_ipv4("1.2.3.4\n") is False
    assert is_valid_ipv4("1.2.3.a") is False
    assert is_valid_ipv4("1.2.3.+4") is False
    assert is_valid_ipv4("1.2.3.4\x00") is False


def test_rejects_non_string_input():
    assert is_valid_ipv4(None) is False
    assert is_valid_ipv4(3232235521) is False


# --- to_int ---------------------------------------------------------------

def test_to_int_known_values():
    assert to_int("0.0.0.0") == 0
    assert to_int("255.255.255.255") == 0xFFFFFFFF
    assert to_int("1.0.0.0") == 16777216
    assert to_int("192.168.0.1") == 3232235521


def test_to_int_roundtrips_with_from_int():
    for addr in ["0.0.0.0", "1.2.3.4", "10.0.0.1", "172.16.0.1",
                 "192.168.0.1", "255.255.255.255"]:
        assert from_int(to_int(addr)) == addr


def test_to_int_raises_on_invalid():
    with pytest.raises(ValueError):
        to_int("01.2.3.4")
    with pytest.raises(ValueError):
        to_int("256.0.0.1")
    with pytest.raises(ValueError):
        to_int("1.2.3")
    with pytest.raises(ValueError):
        to_int("1.2.3.4.5")
    with pytest.raises(ValueError):
        to_int("")
    with pytest.raises(ValueError):
        to_int(None)


# --- from_int -------------------------------------------------------------

def test_from_int_known_values():
    assert from_int(0) == "0.0.0.0"
    assert from_int(1) == "0.0.0.1"
    assert from_int(0xFFFFFFFF) == "255.255.255.255"
    assert from_int(3232235521) == "192.168.0.1"


def test_from_int_raises_on_out_of_range():
    with pytest.raises(ValueError):
        from_int(-1)
    with pytest.raises(ValueError):
        from_int(2 ** 32)
    with pytest.raises(ValueError):
        from_int(2 ** 64)


def test_from_int_raises_on_bad_type():
    with pytest.raises(ValueError):
        from_int("3232235521")
    with pytest.raises(ValueError):
        from_int(3.14)
    with pytest.raises(ValueError):
        from_int(None)
    with pytest.raises(ValueError):
        from_int(True)


# --- is_private -----------------------------------------------------------

def test_private_addresses():
    assert is_private("10.0.0.0") is True
    assert is_private("10.255.255.255") is True
    assert is_private("172.16.0.1") is True
    assert is_private("172.31.255.255") is True
    assert is_private("192.168.0.1") is True
    assert is_private("192.168.255.255") is True


def test_public_addresses():
    assert is_private("8.8.8.8") is False
    assert is_private("172.15.255.255") is False
    assert is_private("172.32.0.1") is False
    assert is_private("192.169.0.1") is False
    assert is_private("11.0.0.1") is False
    assert is_private("0.0.0.0") is False


def test_is_private_raises_on_invalid_address():
    with pytest.raises(ValueError):
        is_private("01.2.3.4")
    with pytest.raises(ValueError):
        is_private("256.1.1.1")
    with pytest.raises(ValueError):
        is_private("")
    with pytest.raises(ValueError):
        is_private(None)
