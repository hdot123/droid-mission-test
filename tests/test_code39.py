"""code39 的验收测试（第五十二轮 · 并发 D 单）。"""

import pytest

from code39 import code39_checksum, code39_encode, code39_verify


# --- 验收要点：校验字符 ---

@pytest.mark.parametrize(
    "text,expected",
    [
        ("A", "A"),
        ("CODE39", "W"),
        ("HELLO", "B"),
        ("123", "6"),
        ("Z", "Z"),
        ("%", "%"),
        (" ", " "),
    ],
)
def test_checksum_acceptance(text, expected):
    assert code39_checksum(text) == expected


# --- 验收要点：编码 ---

@pytest.mark.parametrize(
    "text,expected",
    [
        ("CODE39", "*CODE39W*"),
        ("A", "*AA*"),
        ("123", "*1236*"),
    ],
)
def test_encode_acceptance(text, expected):
    assert code39_encode(text) == expected


# --- 验收要点：校验符号 ---

def test_verify_acceptance_true():
    assert code39_verify("*CODE39W*") is True
    assert code39_verify("*AA*") is True
    assert code39_verify("*1236*") is True


def test_verify_acceptance_false():
    assert code39_verify("*CODE39X*") is False
    assert code39_verify("CODE39W") is False
    assert code39_verify("*A*") is False
    assert code39_verify("") is False
    assert code39_verify("**") is False
    assert code39_verify("*code39W*") is False


# --- 验收要点：往返 ---

@pytest.mark.parametrize("text", ["CODE39", "HELLO", "A", "123", "TEST-1"])
def test_round_trip(text):
    assert code39_verify(code39_encode(text)) is True


# --- 验收要点：ValueError ---

@pytest.mark.parametrize("text", ["", "abc", "HELLO!"])
def test_checksum_value_error(text):
    with pytest.raises(ValueError):
        code39_checksum(text)


def test_encode_value_error():
    with pytest.raises(ValueError):
        code39_encode("")


# --- 验收要点：TypeError ---

def test_checksum_type_error():
    with pytest.raises(TypeError):
        code39_checksum(123)


def test_verify_type_error():
    with pytest.raises(TypeError):
        code39_verify(123)
