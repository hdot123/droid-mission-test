import pytest

from paritybit import append_parity, check_parity, strip_parity


# --- append_parity, even mode -------------------------------------------

def test_append_even_single_bit():
    assert append_parity("0") == "00"
    assert append_parity("1") == "11"


def test_append_even_multi_bit():
    assert append_parity("1011") == "10111"
    assert append_parity("1010") == "10100"
    assert append_parity("1111111") == "11111111"


def test_append_odd_mode():
    assert append_parity("0", "odd") == "01"
    assert append_parity("1", "odd") == "10"
    assert append_parity("1011", "odd") == "10110"
    assert append_parity("1010", "odd") == "10101"


# --- check_parity --------------------------------------------------------

def test_check_even_examples():
    assert check_parity("10111") is True
    assert check_parity("10110") is False


def test_check_odd_examples():
    assert check_parity("10110", "odd") is True
    assert check_parity("10111", "odd") is False


# --- round-trip ----------------------------------------------------------

def test_roundtrip_examples():
    for mode in ("even", "odd"):
        for bits in ("0", "1", "1011", "1010", "1111111", "110"):
            coded = append_parity(bits, mode)
            assert check_parity(coded, mode) is True
            assert strip_parity(coded) == bits


def test_roundtrip_exhaustive_short_strings():
    for length in range(1, 6):
        for value in range(2 ** length):
            bits = format(value, f"0{length}b")
            for mode in ("even", "odd"):
                coded = append_parity(bits, mode)
                assert check_parity(coded, mode) is True
                assert strip_parity(coded) == bits


# --- input contract: ValueError -----------------------------------------

def test_append_empty_string_value_error():
    with pytest.raises(ValueError):
        append_parity("")


def test_append_non_binary_value_error():
    with pytest.raises(ValueError):
        append_parity("102")


def test_append_bad_mode_value_error():
    with pytest.raises(ValueError):
        append_parity("10", "x")


def test_strip_too_short_value_error():
    with pytest.raises(ValueError):
        strip_parity("1")


def test_strip_empty_string_value_error():
    with pytest.raises(ValueError):
        strip_parity("")


def test_check_empty_string_value_error():
    with pytest.raises(ValueError):
        check_parity("")


def test_check_non_binary_value_error():
    with pytest.raises(ValueError):
        check_parity("0a1")


def test_check_bad_mode_value_error():
    with pytest.raises(ValueError):
        check_parity("10", "even-o")


# --- input contract: TypeError ------------------------------------------

def test_append_non_str_type_error():
    with pytest.raises(TypeError):
        append_parity(10)


def test_check_non_str_type_error():
    with pytest.raises(TypeError):
        check_parity(10)


def test_strip_non_str_type_error():
    with pytest.raises(TypeError):
        strip_parity(10)


def test_non_str_mode_type_error():
    with pytest.raises(TypeError):
        append_parity("10", 1)
