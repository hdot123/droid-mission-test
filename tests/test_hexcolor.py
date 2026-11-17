import pytest

from hexcolor import is_valid, parse, to_hex


# --- required examples (verbatim from the work order) ---
def test_example_parse_short_f80():
    assert parse("#f80") == (255, 136, 0)


def test_example_parse_long_FF8800():
    assert parse("#FF8800") == (255, 136, 0)


def test_example_to_hex():
    assert to_hex(255, 136, 0) == "#FF8800"


# --- parse behavior ---
def test_parse_short_form_expansion():
    assert parse("#FFF") == (255, 255, 255)
    assert parse("#000") == (0, 0, 0)


def test_parse_case_insensitive():
    assert parse("#abc") == parse("#ABC")
    assert parse("#AbC123") == parse("#abc123")


def test_parse_missing_hash_raises():
    with pytest.raises(ValueError):
        parse("f80")


def test_parse_wrong_length_raises():
    with pytest.raises(ValueError):
        parse("#ff")
    with pytest.raises(ValueError):
        parse("#ffff")
    with pytest.raises(ValueError):
        parse("#ff88000")


def test_parse_non_hex_characters_raises():
    with pytest.raises(ValueError):
        parse("#fg0")
    with pytest.raises(ValueError):
        parse("#xyz880")
    with pytest.raises(ValueError):
        parse("#8 8000")


def test_parse_empty_and_non_string_raises():
    with pytest.raises(ValueError):
        parse("")
    with pytest.raises(ValueError):
        parse("#")


# --- to_hex behavior ---
def test_to_hex_roundtrip():
    for color in ("#FF8800", "#000000", "#FFFFFF", "#1A2B3C"):
        r, g, b = parse(color)
        assert to_hex(r, g, b) == color


def test_to_hex_is_uppercase():
    assert to_hex(1, 2, 3) == "#010203"
    assert to_hex(10, 11, 12) == "#0A0B0C"


def test_to_hex_out_of_range_raises():
    with pytest.raises(ValueError):
        to_hex(256, 0, 0)
    with pytest.raises(ValueError):
        to_hex(0, -1, 0)
    with pytest.raises(ValueError):
        to_hex(0, 0, 300)


def test_to_hex_non_int_raises():
    with pytest.raises(ValueError):
        to_hex("1", 2, 3)
    with pytest.raises(ValueError):
        to_hex(1.0, 2, 3)
    with pytest.raises(ValueError):
        to_hex(1, 2, None)


# --- is_valid behavior ---
def test_is_valid_true_cases():
    assert is_valid("#f80") is True
    assert is_valid("#FF8800") is True
    assert is_valid("#000000") is True


def test_is_valid_false_cases_never_raise():
    assert is_valid("f80") is False
    assert is_valid("#ff") is False
    assert is_valid("#fg0") is False
    assert is_valid("") is False
    assert is_valid(None) is False
