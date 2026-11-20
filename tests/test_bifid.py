import pytest

from bifid import bifid_decrypt, bifid_encrypt


def test_encrypt_hello():
    assert bifid_encrypt("HELLO", 5) == "FNNVD"


def test_decrypt_fnnvd():
    assert bifid_decrypt("FNNVD", 5) == "HELLO"


def test_encrypt_single_letter():
    assert bifid_encrypt("A", 5) == "A"


def test_encrypt_empty():
    assert bifid_encrypt("", 5) == ""


def test_encrypt_j_folds_into_i():
    assert bifid_encrypt("J", 5) == "I"


def test_encrypt_jump():
    assert bifid_encrypt("JUMP", 5) == "INUK"


def test_encrypt_cryptography_period_6():
    assert bifid_encrypt("CRYPTOGRAPHY", 6) == "DXSMUTICKGEO"


def test_encrypt_helloworld_period_3():
    assert bifid_encrypt("HELLOWORLD", 3) == "FNVNVROOFD"


def test_roundtrip_thequickbrownfox():
    text, period = "THEQUICKBROWNFOX", 5
    assert bifid_decrypt(bifid_encrypt(text, period), period) == text


def test_roundtrip_attackatdawn():
    text, period = "ATTACKATDAWN", 4
    assert bifid_decrypt(bifid_encrypt(text, period), period) == text


def test_period_changes_result():
    assert bifid_encrypt("HELLOWORLD", 5) != bifid_encrypt("HELLOWORLD", 4)


def test_period_zero_raises_value_error():
    with pytest.raises(ValueError):
        bifid_encrypt("ABC", 0)


def test_period_non_int_raises_type_error():
    with pytest.raises(TypeError):
        bifid_encrypt("ABC", "5")


def test_text_non_str_raises_type_error():
    with pytest.raises(TypeError):
        bifid_encrypt(42, 5)
