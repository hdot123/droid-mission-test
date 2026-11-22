"""Tests for ipaddr.py strict IPv4 utilities."""

import pytest

from ipaddr import is_valid_ipv4, to_int, from_int, is_private


# --- is_valid_ipv4 ---------------------------------------------------------

def test_is_valid_ipv4_accepts_addresses():
    assert is_valid_ipv4("0.0.0.0") is True
    assert is_valid_ipv4("255.255.255.255") is True
    assert is_valid_ipv4("192.168.0.1") is True
    assert is_valid_ipv4("10.0.0.1") is True
    assert is_valid_ipv4("01.2.3.4") is False


def test_is_valid_ipv4_rejects_wrong_octet_count():
    assert is_valid_ipv4("1.2.3") is False
    assert is_valid_ipv4("1.2.3.4.5") is False
    assert is_valid_ipv4("1.2.3.") is False
    assert is_valid_ipv4(".1.2.3.4") is False


def test_is_valid_ipv4_rejects_bad_octets():
    assert is_valid_ipv4("1.2.3.256") is False
    assert is_valid_ipv4("256.0.0.1") is False
    assert is_valid_ipv4("1.2..4") is False
    assert is_valid_ipv4("01.2.3.4") is False
    assert is_valid_ipv4("1.02.3.4") is False
    assert is_valid_ipv4("1.2.3.007") is False


def test_is_valid_ipv4_rejects_spaces_and_non_digits():
    assert is_valid_ipv4(" 1.2.3.4") is False
    assert is_valid_ipv4("1.2.3.4 ") is False
    assert is_valid_ipv4("1.2. 3.4") is False
    assert is_valid_ipv4("1.2.3.4.") is False
    assert is_valid_ipv4("") is False
    assert is_valid_ipv4("1.2.3.a") is False
    assert is_valid_ipv4("1.2.3.-4") is False


def test_is_valid_ipv4_never_raises_for_garbage():
    for junk in (None, 123, b"1.2.3.4", ["1.2.3.4"], object()):
        assert is_valid_ipv4(junk) is False


# --- to_int ---------------------------------------------------------------

def test_to_int_examples():
    assert to_int("192.168.0.1") == 3232235521
    assert to_int("0.0.0.0") == 0
    assert to_int("255.255.255.255") == 4294967295


def test_to_int_rejects_invalid():
    for bad in ("01.2.3.4", "1.2.3", "1.2.3.4.5", "1.2.3.256", "1.2.3.4 ",
                " 1.2.3.4", "", "1.2..4", "a.b.c.d"):
        with pytest.raises(ValueError):
            to_int(bad)


def test_to_int_from_int_roundtrip():
    for addr in ("0.0.0.0", "192.168.0.1", "10.255.255.255",
                 "255.255.255.255", "8.8.8.8", "172.16.0.1"):
        assert from_int(to_int(addr)) == addr


# --- from_int -------------------------------------------------------------

def test_from_int_examples():
    assert from_int(3232235521) == "192.168.0.1"
    assert from_int(0) == "0.0.0.0"
    assert from_int(4294967295) == "255.255.255.255"


def test_from_int_rejects_out_of_range_and_bad_types():
    for bad in (-1, 2 ** 32, 2 ** 32 + 1, 1.5, True, "3232235521", None,
                4294967295.0, False, complex(1, 0)):
        with pytest.raises(ValueError):
            from_int(bad)


def test_from_int_boundaries_valid():
    assert from_int(2 ** 32 - 1) == "255.255.255.255"
    assert from_int(1) == "0.0.0.1"
    assert from_int(16777216) == "1.0.0.0"


# --- is_private -----------------------------------------------------------

def test_is_private_examples():
    assert is_private("172.31.255.255") is True
    assert is_private("172.32.0.1") is False
    assert is_private("10.0.0.1") is True
    assert is_private("10.255.255.255") is True
    assert is_private("11.0.0.1") is False
    assert is_private("192.168.1.1") is True
    assert is_private("192.169.0.1") is False


def test_is_private_boundaries():
    assert is_private("172.16.0.1") is True
    assert is_private("172.15.255.255") is False
    assert is_private("10.255.255.255") is True
    assert is_private("9.255.255.255") is False
    assert is_private("192.168.255.255") is True
    assert is_private("192.167.255.255") is False
    assert is_private("0.0.0.0") is False
    assert is_private("8.8.8.8") is False


def test_is_private_raises_on_invalid_address():
    for bad in ("01.2.3.4", "1.2.3", "1.2.3.4.5", "1.2.3.256", "1.2.3.4 ",
                "", "10.0.0", "10..0.1"):
        with pytest.raises(ValueError):
            is_private(bad)
