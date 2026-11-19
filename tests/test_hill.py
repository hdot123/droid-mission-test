"""tests/test_hill.py —— Hill 2×2 密码（mod 26）验收测试。

覆盖 work order #478 第一节的全部验收要点（21 条），
外加 hill_decrypt 的 key 规则与非 str 输入错误。
"""

import pytest

import hill

K1 = ((3, 3), (2, 5))
K2 = ((11, 8), (3, 7))


# --- 验收要点 1–2 ---
def test_encrypt_help():
    assert hill.hill_encrypt("HELP", K1) == "HIAT"


def test_decrypt_hiat():
    assert hill.hill_decrypt("HIAT", K1) == "HELP"


# --- 验收要点 3–4 ---
def test_encrypt_attack():
    assert hill.hill_encrypt("ATTACK", K1) == "FRFMKC"


def test_decrypt_frfmkc():
    assert hill.hill_decrypt("FRFMKC", K1) == "ATTACK"


# --- 验收要点 5–6（奇数长度补 X，解密保留补位） ---
def test_encrypt_hello_pads_with_x():
    assert hill.hill_encrypt("HELLO", K1) == "HIOZHN"


def test_decrypt_returns_padded_plaintext():
    assert hill.hill_decrypt("HIOZHN", K1) == "HELLOX"


# --- 验收要点 7–8 ---
def test_encrypt_hi_k2():
    assert hill.hill_encrypt("HI", K2) == "LZ"


def test_decrypt_lz_k2():
    assert hill.hill_decrypt("LZ", K2) == "HI"


# --- 验收要点 9–10 ---
def test_encrypt_empty():
    assert hill.hill_encrypt("", K1) == ""


def test_decrypt_empty():
    assert hill.hill_decrypt("", K1) == ""


# --- 验收要点 11 ---
def test_roundtrip_meetmeatnoon():
    assert hill.hill_decrypt(hill.hill_encrypt("MEETMEATNOON", K1), K1) == "MEETMEATNOON"


# --- 验收要点 12（去非字母、转大写） ---
def test_encrypt_strips_non_letters():
    assert hill.hill_encrypt("Help!", K1) == "HIAT"


# --- 验收要点 13 ---
def test_roundtrip_zebra_keeps_padding():
    assert hill.hill_decrypt(hill.hill_encrypt("ZEBRA", K2), K2) == "ZEBRAX"


# --- 验收要点 14–15（行列式与 26 不互素） ---
def test_encrypt_det_not_coprime_raises():
    with pytest.raises(ValueError):
        hill.hill_encrypt("HI", ((2, 0), (0, 2)))


def test_encrypt_det_zero_raises():
    with pytest.raises(ValueError):
        hill.hill_encrypt("HI", ((2, 4), (2, 4)))


# --- 验收要点 16（密文奇数长度） ---
def test_decrypt_odd_length_raises():
    with pytest.raises(ValueError):
        hill.hill_decrypt("ABC", K1)


# --- 验收要点 17–18（类型错误） ---
def test_encrypt_non_str_text_raises():
    with pytest.raises(TypeError):
        hill.hill_encrypt(123, K1)


def test_encrypt_non_matrix_key_raises():
    with pytest.raises(TypeError):
        hill.hill_encrypt("HI", "key")


# --- 验收要点 19（key 元素非 int） ---
def test_encrypt_non_int_element_raises():
    with pytest.raises(TypeError):
        hill.hill_encrypt("HI", ((3, 3.0), (2, 5)))


# --- 验收要点 20（key 元素超出 0–25） ---
def test_encrypt_element_out_of_range_raises():
    with pytest.raises(ValueError):
        hill.hill_encrypt("HI", ((3, 3), (2, 26)))


# --- 验收要点 21（矩阵形状不对） ---
def test_encrypt_wrong_shape_raises():
    with pytest.raises(ValueError):
        hill.hill_encrypt("HI", ((1, 2, 3), (4, 5, 6)))


# --- 26 个字母全保留，J 不并入 I ---
def test_j_not_folded_into_i():
    assert hill.hill_encrypt("J", K1) == "SD"
    assert hill.hill_encrypt("I", K1) == "PB"


# --- hill_decrypt 的 key 规则与非 str 输入（同 encrypt） ---
def test_decrypt_non_str_cipher_raises():
    with pytest.raises(TypeError):
        hill.hill_decrypt(123, K1)


def test_decrypt_non_matrix_key_raises():
    with pytest.raises(TypeError):
        hill.hill_decrypt("HIAT", "key")


def test_decrypt_non_int_element_raises():
    with pytest.raises(TypeError):
        hill.hill_decrypt("HIAT", ((3, 3.0), (2, 5)))


def test_decrypt_element_out_of_range_raises():
    with pytest.raises(ValueError):
        hill.hill_decrypt("HIAT", ((3, 3), (2, 26)))


def test_decrypt_wrong_shape_raises():
    with pytest.raises(ValueError):
        hill.hill_decrypt("HIAT", ((1, 2, 3), (4, 5, 6)))


def test_decrypt_det_not_coprime_raises():
    with pytest.raises(ValueError):
        hill.hill_decrypt("HIAT", ((2, 0), (0, 2)))
