"""Tests for the vigenere module (only this module's behavior)."""

import pytest

import vigenere


def test_encrypt_example_attack():
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_encrypt_example_hello():
    assert vigenere.encrypt("Hello, World!", "key") == "Rijvs, Uyvjn!"


def test_decrypt_round_trip():
    text = "Hello, World!"
    key = "key"
    assert vigenere.decrypt(vigenere.encrypt(text, key), key) == text
    assert vigenere.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_case_preservation():
    assert vigenere.encrypt("AbC", "b") == "BcD"
    assert vigenere.decrypt("BcD", "b") == "AbC"


def test_non_letters_passthrough_without_consuming_key():
    # "!" does not consume a key letter: second A uses key letter E.
    # (If "!" consumed a key letter, the second A would use L again -> "L!L".)
    assert vigenere.encrypt("A!A", "LE") == "L!E"


def test_key_cycles_when_shorter_than_text():
    assert vigenere.encrypt("AAAA", "AB") == "ABAB"
    assert vigenere.decrypt("ABAB", "AB") == "AAAA"


@pytest.mark.parametrize("bad_key", ["", "123", "ab1", "ab c", "ab!", None, 42])
def test_invalid_keys_raise_value_error(bad_key):
    with pytest.raises(ValueError):
        vigenere.encrypt("text", bad_key)
    with pytest.raises(ValueError):
        vigenere.decrypt("text", bad_key)
