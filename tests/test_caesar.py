import pytest

import caesar


def test_encrypt_example_hello_world():
    assert caesar.encrypt("Hello, World!", 3) == "Khoor, Zruog!"


def test_encrypt_negative_shift():
    assert caesar.encrypt("abc", -1) == "zab"


def test_encrypt_shift_greater_than_26():
    assert caesar.encrypt("XYZ", 29) == "ABC"


def test_decrypt_example():
    assert caesar.decrypt("Khoor, Zruog!", 3) == "Hello, World!"


def test_case_preservation():
    assert caesar.encrypt("AbC", 1) == "BcD"
    assert caesar.encrypt("AbC", 25) == "ZaB"


def test_non_letter_passthrough():
    text = "Hello, World! 123\t\n"
    assert caesar.encrypt(text, 0) == text
    assert caesar.encrypt("a-b_c d", 5) == "f-g_h i"


@pytest.mark.parametrize("shift", [0, 1, 25, 26, 27, -1, -26, -27, 100])
def test_decrypt_inverts_encrypt(shift):
    text = "Hello, World! xyz ABC 123, ?!"
    assert caesar.decrypt(caesar.encrypt(text, shift), shift) == text


def test_decrypt_negative_and_large_shifts():
    assert caesar.decrypt(caesar.encrypt("Test", -3), -3) == "Test"
    assert caesar.decrypt(caesar.encrypt("Test", 55), 55) == "Test"
