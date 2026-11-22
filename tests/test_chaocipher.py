"""Tests for chaocipher.py.

One test case per acceptance point from work order #761 (sub-issue #780).
"""

import pytest

from chaocipher import (
    LEFT_ALPHABET,
    RIGHT_ALPHABET,
    chaocipher_decrypt,
    chaocipher_encrypt,
)


def test_alphabets_pinned_and_permutations():
    assert LEFT_ALPHABET == "HXUCZVAMDSLKPEFJRIGTWOBNYQ"
    assert RIGHT_ALPHABET == "PTLNBQDEOYSFAVZKGJRIHWXUMC"
    abc = sorted("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert sorted(LEFT_ALPHABET) == abc
    assert sorted(RIGHT_ALPHABET) == abc


def test_encrypt_single_a():
    assert chaocipher_encrypt("A") == "P"


def test_encrypt_aaaa():
    assert chaocipher_encrypt("AAAA") == "PKLS"


def test_encrypt_helloworld():
    assert chaocipher_encrypt("HELLOWORLD") == "WAHQVICHTD"


def test_decrypt_helloworld():
    assert chaocipher_decrypt("WAHQVICHTD") == "HELLOWORLD"


def test_encrypt_chaocipher():
    assert chaocipher_encrypt("CHAOCIPHER") == "QTLVOFOEYS"


def test_decrypt_chaocipher():
    assert chaocipher_decrypt("QTLVOFOEYS") == "CHAOCIPHER"


def test_encrypt_thequickbrownfox():
    assert chaocipher_encrypt("THEQUICKBROWNFOX") == "XTVXVJGSTKDBISJS"


def test_encrypt_empty_string():
    assert chaocipher_encrypt("") == ""


def test_decrypt_empty_string():
    assert chaocipher_decrypt("") == ""


def test_encrypt_preprocess_lowercases():
    assert chaocipher_encrypt("hello world") == chaocipher_encrypt("HELLOWORLD")


def test_encrypt_preprocess_strips_non_letters():
    assert chaocipher_encrypt("HELLO, WORLD!") == "WAHQVICHTD"


@pytest.mark.parametrize(
    "t",
    [
        "HELLOWORLD",
        "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
        "A",
        "ZZZZ",
    ],
)
def test_roundtrip(t):
    assert chaocipher_decrypt(chaocipher_encrypt(t)) == t


def test_encrypt_rejects_non_str():
    with pytest.raises(TypeError):
        chaocipher_encrypt(123)
    with pytest.raises(TypeError):
        chaocipher_encrypt(None)


def test_decrypt_rejects_non_str():
    with pytest.raises(TypeError):
        chaocipher_decrypt(b"WAHQ")
