"""Tests for caesar.shift — round 40 acceptance criteria (verbatim)."""

from caesar import shift


def test_shift_forward_one():
    assert shift("abc", 1) == "bcd"


def test_shift_wraps_around():
    assert shift("xyz", 3) == "abc"


def test_shift_preserves_case_and_spaces():
    assert shift("Abc XyZ", 2) == "Cde ZaB"


def test_shift_rot13():
    assert shift("Hello, World!", 13) == "Uryyb, Jbeyq!"


def test_shift_full_rotation_is_identity():
    assert shift("abc", 26) == "abc"


def test_shift_negative_moves_backward():
    assert shift("abc", -1) == "zab"


def test_shift_empty_string():
    assert shift("", 5) == ""


def test_shift_non_letters_unchanged():
    assert shift("123 !", 7) == "123 !"
