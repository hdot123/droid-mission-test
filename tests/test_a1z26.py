"""A1Z26 组件验收测试——逐条对应工单验收要点。"""

import pytest

import a1z26


# --- encode 基本要点 ---

def test_encode_empty_string():
    assert a1z26.a1z26_encode("") == ""


def test_encode_single_letters():
    assert a1z26.a1z26_encode("A") == "1"
    assert a1z26.a1z26_encode("Z") == "26"


def test_encode_abc():
    assert a1z26.a1z26_encode("ABC") == "1-2-3"


def test_encode_hello():
    assert a1z26.a1z26_encode("HELLO") == "8-5-12-12-15"


def test_encode_hello_world():
    assert a1z26.a1z26_encode("HELLO WORLD") == "8-5-12-12-15 23-15-18-12-4"


# --- decode 基本要点 ---

def test_decode_empty_string():
    assert a1z26.a1z26_decode("") == ""


def test_decode_123():
    assert a1z26.a1z26_decode("1-2-3") == "ABC"


def test_decode_hello_world():
    assert a1z26.a1z26_decode("8-5-12-12-15 23-15-18-12-4") == "HELLO WORLD"


def test_decode_26_1():
    assert a1z26.a1z26_decode("26-1") == "ZA"


# --- 往返性 ---

@pytest.mark.parametrize("sample", ["PYTHON", "A B C", "ZZZ AAA"])
def test_round_trip(sample):
    assert a1z26.a1z26_decode(a1z26.a1z26_encode(sample)) == sample


# --- encode 非法输入抛 ValueError ---

def test_encode_lowercase_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_encode("hello")


def test_encode_digit_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_encode("A1")


def test_encode_consecutive_spaces_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_encode("A  B")


def test_encode_leading_space_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_encode(" A")


# --- decode 非法输入抛 ValueError ---

def test_decode_zero_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_decode("0")


def test_decode_out_of_range_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_decode("27")


def test_decode_leading_zero_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_decode("01")


def test_decode_double_hyphen_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_decode("1--2")


def test_decode_space_inside_word_raises():
    with pytest.raises(ValueError):
        a1z26.a1z26_decode("1- 2")


# --- 非 str 抛 TypeError ---

def test_encode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        a1z26.a1z26_encode(None)


def test_decode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        a1z26.a1z26_decode(123)
