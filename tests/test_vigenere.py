"""Tests for the Vigenere cipher module (vigenere.py only)."""

import pytest

import vigenere


# --- happy path / required examples ---

def test_encrypt_example_attack_at_dawn():
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_encrypt_example_attack_mixed_case():
    assert vigenere.encrypt("Attack", "LEMON") == "Lxfopv"


def test_decrypt_example():
    assert vigenere.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_roundtrip():
    text = "Attack at dawn! Meet at 0600."
    key = "LEMON"
    assert vigenere.decrypt(vigenere.encrypt(text, key), key) == text


# --- invalid keys raise ValueError ---

@pytest.mark.parametrize("bad_key", ["", " ", "LE MON", "LE1MON", "L3MON", None, 123, b"LEMON"])
def test_invalid_key_raises_value_error(bad_key):
    with pytest.raises(ValueError):
        vigenere.encrypt("ATTACKATDAWN", bad_key)
    with pytest.raises(ValueError):
        vigenere.decrypt("ATTACKATDAWN", bad_key)


# --- key advances only on letters; non-letters kept verbatim ---

def test_non_letter_characters_do_not_advance_key():
    # "A B C" with key "LEMON": letters A, B, C consume L, E, M;
    # the spaces are preserved and do not consume key letters.
    assert vigenere.encrypt("A B C", "LEMON") == "L F O"


def test_punctuation_and_digits_preserved():
    # "hi, there!" with key "key": letters consume K, E, Y, K, E, Y, K;
    # ",", " " and "!" are kept verbatim and consume no key letter.
    assert vigenere.encrypt("hi, there!", "key") == "rm, rripo!"


def test_newlines_and_tabs_preserved():
    assert vigenere.encrypt("a\nb\tc", "LE") == "l\nf\tn"


# --- case preservation ---

def test_case_preserved():
    assert vigenere.encrypt("Attack", "LEMON") == "Lxfopv"
    assert vigenere.encrypt("ATTACK", "LEMON") == "LXFOPV"
    assert vigenere.encrypt("attack", "LEMON") == "lxfopv"


def test_decrypt_case_preserved():
    assert vigenere.decrypt("Lxfopv", "LEMON") == "Attack"
