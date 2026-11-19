"""tests/test_trifid.py —— trifid.py 的验收测试（逐字对应工作单验收要点）。"""

import pytest

import trifid


# --- 基本向量 -------------------------------------------------------------

def test_encrypt_single_a():
    assert trifid.trifid_encrypt("A", 5) == "A"


def test_encrypt_az():
    assert trifid.trifid_encrypt("AZ", 5) == "GT"


def test_decrypt_gt():
    assert trifid.trifid_decrypt("GT", 5) == "AZ"


def test_encrypt_hello():
    assert trifid.trifid_encrypt("HELLO", 5) == "BOJN+"


def test_encrypt_thequickbrownfox():
    assert trifid.trifid_encrypt("THEQUICKBROWNFOX", 5) == "SPXEOBFA+OQENQRX"


def test_decrypt_thequickbrownfox():
    assert trifid.trifid_decrypt("SPXEOBFA+OQENQRX", 5) == "THEQUICKBROWNFOX"


def test_encrypt_attackatdawn_period3():
    assert trifid.trifid_encrypt("ATTACKATDAWN", 3) == "IAEBAHGBDHEE"


def test_encrypt_xyz_plus_abc_period4():
    assert trifid.trifid_encrypt("XYZ+ABC", 4) == "+X+FAAF"


def test_encrypt_empty_string():
    assert trifid.trifid_encrypt("", 5) == ""


def test_decrypt_empty_string():
    assert trifid.trifid_decrypt("", 5) == ""


# --- 预处理 ---------------------------------------------------------------

def test_encrypt_lowercases_to_upper():
    assert trifid.trifid_encrypt("hello", 5) == "BOJN+"


def test_encrypt_strips_non_alphabet():
    assert trifid.trifid_encrypt("HE LLO!", 5) == "BOJN+"


# --- 往返 -----------------------------------------------------------------

@pytest.mark.parametrize("text,period", [
    ("HELLOWORLDTHISISATEST", 7),
    ("LONGERTEXTWITHPLUS+", 6),
    ("A", 1),
])
def test_roundtrip(text, period):
    assert trifid.trifid_decrypt(trifid.trifid_encrypt(text, period), period) == text


def test_period_affects_result():
    assert trifid.trifid_encrypt("HELLOWORLD", 5) != trifid.trifid_encrypt("HELLOWORLD", 3)


# --- 参数校验 -------------------------------------------------------------

def test_encrypt_period_zero_raises_valueerror():
    with pytest.raises(ValueError):
        trifid.trifid_encrypt("ABC", 0)


def test_encrypt_period_negative_raises_valueerror():
    with pytest.raises(ValueError):
        trifid.trifid_encrypt("ABC", -2)


def test_encrypt_period_float_raises_typeerror():
    with pytest.raises(TypeError):
        trifid.trifid_encrypt("ABC", 2.5)


def test_encrypt_non_str_text_raises_typeerror():
    with pytest.raises(TypeError):
        trifid.trifid_encrypt(123, 5)


def test_decrypt_non_str_cipher_raises_typeerror():
    with pytest.raises(TypeError):
        trifid.trifid_decrypt(None, 5)


def test_decrypt_period_validation():
    with pytest.raises(ValueError):
        trifid.trifid_decrypt("ABC", 0)
    with pytest.raises(ValueError):
        trifid.trifid_decrypt("ABC", -2)
    with pytest.raises(TypeError):
        trifid.trifid_decrypt("ABC", 2.5)
