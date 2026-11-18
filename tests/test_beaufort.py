"""Beaufort 密码验收测试（第四十三轮 · 并发 B 单）。"""

import pytest

from beaufort import beaufort


def test_hello_with_key():
    assert beaufort("Hello", "key") == "Danzq"


def test_attack_at_dawn():
    assert beaufort("ATTACK AT DAWN", "lemon") == "LLTOLB ET LNPR"


def test_empty_text():
    assert beaufort("", "k") == ""


def test_digits_passthrough():
    assert beaufort("123", "k") == "123"


def test_punctuation_and_case_preserved():
    assert beaufort("Hello, World!", "key") == "Danzq, Cwnnh!"


def test_roundtrip_identity():
    # Beaufort 自逆：对同一 key 加密两次回到原文。
    text = "Hello, World!"
    key = "key"
    assert beaufort(beaufort(text, key), key) == text


def test_empty_key_raises_valueerror():
    with pytest.raises(ValueError):
        beaufort("Hi", "")
