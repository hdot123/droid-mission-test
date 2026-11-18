"""vigenere 验收测试（第四十轮 · E 单 · 子卡 #367）。

工单验收要点逐条对应一个用例；冲突项见
test_encrypt_hello_world_conflict_records_both_values。
"""

import pytest

from vigenere import decrypt, encrypt


def test_encrypt_attack_uppercase_key():
    assert encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_decrypt_attack_uppercase_key():
    assert decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"


def test_encrypt_attack_mixed_case_lowercase_key():
    assert encrypt("Attack at dawn!", "lemon") == "Lxfopv ef rnhr!"


def test_decrypt_attack_mixed_case_lowercase_key():
    assert decrypt("Lxfopv ef rnhr!", "lemon") == "Attack at dawn!"


def test_encrypt_hello_world_conflict_records_both_values():
    """冲突记录（子卡 #367）：两个候选值都记录，断言 provisional 值。

    验收值（provisional value，逐字为准）："Rijvs, Uyvjn!"。
    子卡记录的另一候选值："Rijvs, Gspvh!"。
    工单正文规则：非字母字符不推进 key 位置。按该规则手工推演：
    "Hello" 用 key 前 5 个字母 k,e,y,k,e -> "Rijvs"；
    "World" 续接 y,k,e,y -> "Uyvjn"；逗号与空格原样保留。
    即实现遵循正文规则的结果与验收值一致，断言验收值。
    """
    alternative = "Rijvs, Gspvh!"  # 子卡记录的另一候选值，仅作留痕
    assert alternative != "Rijvs, Uyvjn!"
    assert encrypt("Hello, World!", "key") == "Rijvs, Uyvjn!"


def test_encrypt_empty_key_raises_value_error():
    with pytest.raises(ValueError):
        encrypt("abc", "")


def test_encrypt_key_with_non_letter_raises_value_error():
    with pytest.raises(ValueError):
        encrypt("abc", "a1")


def test_decrypt_invalid_keys_raise_value_error():
    # key 校验对 decrypt 同样生效
    for bad in ("", "a1", "ab-"):
        with pytest.raises(ValueError):
            decrypt("abc", bad)


def test_non_letters_do_not_advance_key_position():
    # key = "ky" 循环使用；' ' 与 '1' 不推进 key 位置：
    # 'a'+k -> 'k'，'b'+y -> 'z'
    assert encrypt("a b", "ky") == "k z"
    assert encrypt("a1b", "ky") == "k1z"
    assert decrypt("k z", "ky") == "a b"
    assert decrypt("k1z", "ky") == "a1b"


def test_key_case_insensitive():
    assert encrypt("Attack at dawn!", "LEMON") == encrypt("Attack at dawn!", "lemon")
    assert encrypt("Attack at dawn!", "leMoN") == encrypt("Attack at dawn!", "lemon")


def test_non_ascii_letters_untouched():
    # 'é' (precomposed U+00E9) 不是 ASCII 字母：原样保留且不推进 key。
    # 用转义写法，避免 NFC/NFD 归一化差异影响断言。
    text = "h" + "é" + "llo"
    out = encrypt(text, "key")
    assert out[1] == "é"
    assert decrypt(out, "key") == text


def test_empty_text():
    assert encrypt("", "key") == ""
    assert decrypt("", "key") == ""


def test_roundtrip():
    for text, key in (
        ("ATTACKATDAWN", "LEMON"),
        ("Attack at dawn!", "lemon"),
        ("Hello, World!", "key"),
        ("The quick brown fox jumps over the lazy dog.", "Secret"),
        ("12345 !@#", "xyz"),
        ("", "key"),
    ):
        assert decrypt(encrypt(text, key), key) == text
