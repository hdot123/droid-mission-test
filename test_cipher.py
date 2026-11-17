"""Pytest checks for cipher.shift_text."""

from cipher import shift_text


def test_work_order_example_shift_2():
    assert shift_text("Abc XyZ!", 2) == "Cde ZaB!"


def test_work_order_example_negative_3():
    assert shift_text("Hello", -3) == "Ebiil"


def test_work_order_example_full_rotation_26():
    assert shift_text("Zebra", 26) == "Zebra"


def test_n_zero_is_identity():
    assert shift_text("Abc XyZ!", 0) == "Abc XyZ!"


def test_n_27_wraps_mod_26():
    # 27 % 26 == 1
    assert shift_text("abc", 27) == "bcd"
    assert shift_text("XYZ", 27) == "YZA"


def test_large_negative_n():
    # -27 % 26 == 25 in Python
    assert shift_text("abc", -27) == "zab"


def test_mixed_punctuation_and_digits_unchanged():
    assert shift_text("Hello, World! 123 _-+@#", 1) == "Ifmmp, Xpsme! 123 _-+@#"


def test_case_preserved_at_alphabet_edges():
    assert shift_text("XYZ", 3) == "ABC"
    assert shift_text("xyz", 3) == "abc"


def test_empty_string():
    assert shift_text("", 5) == ""
