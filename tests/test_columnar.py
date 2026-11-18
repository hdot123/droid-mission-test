import pytest

from columnar import columnar_decrypt, columnar_encrypt


def test_encrypt_weare_discovered():
    assert (
        columnar_encrypt("WEAREDISCOVEREDFLEEATONCE", "ZEBRAS")
        == "EVLNXACDTXESEAXROFOXDEECXWIREE"
    )


def test_encrypt_hello_key():
    assert columnar_encrypt("HELLO", "KEY") == "EOHLLX"


def test_encrypt_abcdefgij_balloon():
    assert columnar_encrypt("ABCDEFGHIJ", "BALLOON") == "BIAHCJDXGXEXFX"


def test_encrypt_single_column():
    assert columnar_encrypt("HELLO", "A") == "HELLO"


def test_encrypt_empty_text():
    assert columnar_encrypt("", "KEY") == ""


def test_decrypt_weare_discovered():
    assert (
        columnar_decrypt("EVLNXACDTXESEAXROFOXDEECXWIREE", "ZEBRAS")
        == "WEAREDISCOVEREDFLEEATONCEXXXXX"
    )


def test_decrypt_hello_key():
    assert columnar_decrypt("EOHLLX", "KEY") == "HELLOX"


def test_decrypt_abcdefgij_balloon():
    assert columnar_decrypt("BIAHCJDXGXEXFX", "BALLOON") == "ABCDEFGHIJXXXX"


def test_encrypt_empty_keyword_raises():
    with pytest.raises(ValueError):
        columnar_encrypt("HELLO", "")


def test_encrypt_non_alpha_keyword_raises():
    with pytest.raises(ValueError):
        columnar_encrypt("HELLO", "K3Y")


def test_decrypt_bad_length_raises():
    # ciphertext length 5 is not a multiple of keyword length 3
    with pytest.raises(ValueError):
        columnar_decrypt("HELLO", "KEY")


def test_encrypt_non_str_text_raises():
    with pytest.raises(TypeError):
        columnar_encrypt(123, "KEY")


def test_decrypt_empty_cipher():
    assert columnar_decrypt("", "KEY") == ""


def test_decrypt_non_str_cipher_raises():
    with pytest.raises(TypeError):
        columnar_decrypt(123, "KEY")


def test_encrypt_non_str_keyword_raises():
    with pytest.raises(TypeError):
        columnar_encrypt("HELLO", 123)


def test_decrypt_non_str_keyword_raises():
    with pytest.raises(TypeError):
        columnar_decrypt("EOHLLX", 123)


def test_decrypt_empty_keyword_raises():
    with pytest.raises(ValueError):
        columnar_decrypt("EOHLLX", "")


def test_decrypt_non_alpha_keyword_raises():
    with pytest.raises(ValueError):
        columnar_decrypt("EOHLLX", "K3Y")
