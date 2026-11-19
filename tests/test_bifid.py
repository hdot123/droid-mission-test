"""Tests for bifid.py (Bifid cipher)."""

import pytest

from bifid import bifid_decrypt, bifid_encrypt


class TestEncrypt:
    def test_hello(self):
        assert bifid_encrypt("HELLO", 5) == "FNNVD"

    def test_single_char(self):
        assert bifid_encrypt("A", 5) == "A"

    def test_empty(self):
        assert bifid_encrypt("", 5) == ""

    def test_j_merges_to_i(self):
        assert bifid_encrypt("J", 5) == "I"

    def test_jump(self):
        assert bifid_encrypt("JUMP", 5) == "INUK"

    def test_cryptography_period_6(self):
        assert bifid_encrypt("CRYPTOGRAPHY", 6) == "DXSMUTICKGEO"

    def test_helloworld_period_3(self):
        assert bifid_encrypt("HELLOWORLD", 3) == "FNVNVROOFD"

    def test_period_affects_result(self):
        assert bifid_encrypt("HELLOWORLD", 5) != bifid_encrypt("HELLOWORLD", 4)


class TestDecrypt:
    def test_hello(self):
        assert bifid_decrypt("FNNVD", 5) == "HELLO"

    def test_empty(self):
        assert bifid_decrypt("", 5) == ""


class TestRoundTrip:
    @pytest.mark.parametrize(
        "text,period",
        [("THEQUICKBROWNFOX", 5), ("ATTACKATDAWN", 4)],
    )
    def test_round_trip(self, text, period):
        assert bifid_decrypt(bifid_encrypt(text, period), period) == text


class TestValidation:
    def test_period_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            bifid_encrypt("ABC", 0)

    def test_period_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            bifid_decrypt("ABC", -1)

    def test_period_non_int_raises_type_error(self):
        with pytest.raises(TypeError):
            bifid_encrypt("ABC", "5")

    def test_text_non_str_raises_type_error(self):
        with pytest.raises(TypeError):
            bifid_encrypt(42, 5)

    def test_decrypt_cipher_non_str_raises_type_error(self):
        with pytest.raises(TypeError):
            bifid_decrypt(42, 5)

    def test_period_bool_rejected(self):
        with pytest.raises(TypeError):
            bifid_encrypt("ABC", True)
