import pytest

import vigenere


def test_encrypt_required_example():
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_encrypt_preserves_case():
    assert vigenere.encrypt("Attack", "LEMON") == "Lxfopv"


def test_decrypt_required_example():
    assert vigenere.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_roundtrip():
    text = "Attack at dawn! #42"
    key = "LEMON"
    assert vigenere.decrypt(vigenere.encrypt(text, key), key) == text


def test_non_alpha_characters_pass_through_and_do_not_advance_key():
    # Key advances only on letters; punctuation/spaces/digits stay unchanged.
    assert vigenere.encrypt("A A", "LE") == "L E"
    assert vigenere.encrypt("A1A", "LE") == "L1E"


def test_key_cycles():
    assert vigenere.encrypt("AAAA", "AB") == "ABAB"


def test_empty_text():
    assert vigenere.encrypt("", "KEY") == ""
    assert vigenere.decrypt("", "KEY") == ""


@pytest.mark.parametrize("bad_key", ["", "LE MON", "LE1", "123", None, 42, "LÉMON"])
def test_invalid_key_raises_value_error(bad_key):
    with pytest.raises(ValueError):
        vigenere.encrypt("A", bad_key)
    with pytest.raises(ValueError):
        vigenere.decrypt("A", bad_key)
