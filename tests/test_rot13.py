import rot13 as m


def test_rot13_basic_mixed_case_and_non_letters():
    assert m.rot13("Hello, World!") == "Uryyb, Jbeyq!"


def test_rot13_digits_and_symbols_unchanged():
    assert m.rot13("abc123!@#") == "nop123!@#"


def test_rot13_round_trip_identity():
    text = "The Quick Brown Fox! 42 jumps over the lazy dog."
    assert m.rot13(m.rot13(text)) == text


def test_rot13_equals_rot_n_13():
    text = "Mixed CASE with 9 numbers, symbols! and unicode: café"
    assert m.rot13(text) == m.rot_n(text, 13)


def test_rot_n_negative_shift():
    assert m.rot_n("abc", -1) == "zab"
    assert m.rot_n("XYZ", -3) == "UVW"


def test_rot_n_larger_than_26_wraps():
    assert m.rot_n("abc", 27) == m.rot_n("abc", 1)
    assert m.rot_n("Hello", 52) == "Hello"


def test_rot_n_case_preservation():
    assert m.rot_n("AbC", 5) == "FgH"
    assert m.rot_n("AbC", -5) == "VwX"


def test_rot_n_non_letter_invariance():
    assert m.rot_n("a b-c_1!Z", 7) == "h i-j_1!G"


def test_rot13_known_vectors():
    assert m.rot13("python") == "clguba"
    assert m.rot13("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == "NOPQRSTUVWXYZABCDEFGHIJKLM"


def test_rot_n_zero_is_identity():
    assert m.rot_n("No change 123!", 0) == "No change 123!"


def test_empty_string():
    assert m.rot13("") == ""
    assert m.rot_n("", 5) == ""
