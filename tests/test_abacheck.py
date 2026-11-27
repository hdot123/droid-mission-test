"""tests/test_abacheck.py — ABA 路由号校验位验收测试（仅标准库）。"""

import random

import pytest

from abacheck import aba_check_digit, aba_validate


# --- 具体验收点 -----------------------------------------------------------

def test_check_digit_known_examples():
    assert aba_check_digit("02100002") == "1"
    assert aba_check_digit("01100001") == "5"


def test_validate_known_valid_numbers():
    # 公开有效号，加权和 30 / 20
    assert aba_validate("021000021") is True
    assert aba_validate("011000015") is True


def test_validate_known_invalid_number():
    assert aba_validate("021000022") is False


# --- 性质测试 ---------------------------------------------------------------

def _reference_check_digit_right_to_left(first8):
    """右至左逐位提取的参照实现（位权自右起 7/3/1 循环）。"""
    total = 0
    for i, ch in enumerate(reversed(first8)):
        weight = (7, 3, 1)[i % 3]
        total += int(ch) * weight
    return str((10 - total % 10) % 10)


def test_property_random_agrees_with_reference_and_roundtrip():
    rng = random.Random(20261127)
    for _ in range(300):
        first8 = "".join(str(rng.randint(0, 9)) for _ in range(8))
        # 与右至左逐位提取参照实现逐个一致
        assert aba_check_digit(first8) == _reference_check_digit_right_to_left(first8)
        # 拼上校验位的 9 位号 validate 必 True
        number = first8 + aba_check_digit(first8)
        assert aba_validate(number) is True
        # 任一位改动一位后 validate 必 False
        pos = rng.randint(0, 8)
        original = int(number[pos])
        new_digit = (original + rng.randint(1, 9)) % 10
        changed = number[:pos] + str(new_digit) + number[pos + 1:]
        assert aba_validate(changed) is False


# --- 形态错误（ValueError）-------------------------------------------------

def test_value_error_on_bad_shape():
    with pytest.raises(ValueError):
        aba_check_digit("1234567")          # 长度 7
    with pytest.raises(ValueError):
        aba_check_digit("1234567a")         # 含非数字
    with pytest.raises(ValueError):
        aba_validate("0210000210")          # 长度 10


# --- 类型错误（TypeError）--------------------------------------------------

def test_type_error_on_non_str():
    with pytest.raises(TypeError):
        aba_check_digit(2100002)
    with pytest.raises(TypeError):
        aba_validate(None)
