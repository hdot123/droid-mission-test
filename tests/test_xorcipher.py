"""tests for xorcipher: repeating-key XOR with hex in/out."""

import pytest

from xorcipher import xor_decrypt_hex, xor_encrypt_hex


def test_encrypt_hello_key():
    assert xor_encrypt_hex("hello", "key") == "030015070a"


def test_decrypt_hello_key():
    assert xor_decrypt_hex("030015070a", "key") == "hello"


def test_encrypt_empty_plaintext():
    assert xor_encrypt_hex("", "key") == ""


def test_decrypt_empty_hex():
    assert xor_decrypt_hex("", "key") == ""


def test_encrypt_single_char():
    assert xor_encrypt_hex("A", "k") == "2a"


def test_encrypt_hello_world():
    assert (
        xor_encrypt_hex("Hello, World!", "secret")
        == "3b000f1e0a5853320c00091052"
    )


def test_decrypt_hello_world():
    assert xor_decrypt_hex("3b000f1e0a5853320c00091052", "secret") == "Hello, World!"


def test_round_trip_unicode():
    assert (
        xor_decrypt_hex(xor_encrypt_hex("café ☕", "pässwörd"), "pässwörd")
        == "café ☕"
    )


def test_round_trip_single_byte_key():
    assert (
        xor_decrypt_hex(xor_encrypt_hex("The quick brown fox", "x"), "x")
        == "The quick brown fox"
    )


def test_encrypt_empty_key_raises():
    with pytest.raises(ValueError):
        xor_encrypt_hex("hi", "")


def test_decrypt_invalid_hex_raises():
    with pytest.raises(ValueError):
        xor_decrypt_hex("zz", "key")
    with pytest.raises(ValueError):
        xor_decrypt_hex("abc", "key")


def test_encrypt_non_str_raises():
    with pytest.raises(TypeError):
        xor_encrypt_hex(123, "key")
    with pytest.raises(TypeError):
        xor_encrypt_hex("hi", 5)


def test_decrypt_non_str_raises():
    with pytest.raises(TypeError):
        xor_decrypt_hex(123, "key")
    with pytest.raises(TypeError):
        xor_decrypt_hex("ab", 5)


def test_decrypt_empty_key_raises():
    with pytest.raises(ValueError):
        xor_decrypt_hex("030015070a", "")
