"""Tests for the bitflags module."""

import pytest

import bitflags


def test_define_flags_maps_names_to_powers_of_two():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert F == {"READ": 1, "WRITE": 2, "EXEC": 4}


def test_define_flags_empty_list():
    assert bitflags.define_flags([]) == {}


def test_define_flags_duplicate_names_raises():
    with pytest.raises(ValueError):
        bitflags.define_flags(["READ", "WRITE", "READ"])


def test_combine_or_of_named_bits():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert bitflags.combine(F, "READ", "EXEC") == 5


def test_combine_no_names_returns_zero():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert bitflags.combine(F) == 0


def test_combine_unknown_name_raises():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    with pytest.raises(ValueError):
        bitflags.combine(F, "READ", "NOPE")


def test_contains_true_when_bit_set():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert bitflags.contains(5, F["READ"]) is True


def test_contains_false_when_bit_clear():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert bitflags.contains(5, F["WRITE"]) is False


def test_names_of_returns_names_ordered_by_bit_value():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert bitflags.names_of(F, 5) == ["READ", "EXEC"]


def test_names_of_zero_returns_empty_list():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    assert bitflags.names_of(F, 0) == []


def test_names_of_undefined_bits_raises():
    F = bitflags.define_flags(["READ", "WRITE", "EXEC"])
    with pytest.raises(ValueError):
        bitflags.names_of(F, 8)
