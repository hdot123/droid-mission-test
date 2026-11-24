import pytest

from bacon import bacon_decode, bacon_encode


# --- 验收要点：编码 ---

def test_encode_single_letters():
    assert bacon_encode("A") == "aaaaa"
    assert bacon_encode("Z") == "bbaab"


def test_encode_hello():
    assert bacon_encode("HELLO") == "aabbb aabaa ababb ababb abbba"


def test_encode_mixed_case():
    assert bacon_encode("Hi") == "aabbb abaaa"


def test_encode_empty():
    assert bacon_encode("") == ""


# --- 验收要点：解码 ---

def test_decode_single_letters():
    assert bacon_decode("aaaaa") == "A"
    assert bacon_decode("bbaab") == "Z"


def test_decode_hello():
    assert bacon_decode("aabbb aabaa ababb ababb abbba") == "HELLO"


def test_decode_empty():
    assert bacon_decode("") == ""


# --- 验收要点：编码非法输入 ---

def test_encode_non_letter_raises():
    with pytest.raises(ValueError):
        bacon_encode("A1")
    with pytest.raises(ValueError):
        bacon_encode("HELLO!")


# --- 验收要点：解码非法输入 ---

def test_decode_bad_group_length_raises():
    with pytest.raises(ValueError):
        bacon_decode("aaaa")


def test_decode_non_binary_group_raises():
    with pytest.raises(ValueError):
        bacon_decode("aabbc")


def test_decode_double_space_raises():
    with pytest.raises(ValueError):
        bacon_decode("aabbb  aabaa")


# --- 验收要点：非 str 输入 TypeError ---

def test_encode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        bacon_encode(123)


def test_decode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        bacon_decode(123)


# --- 补充：全字母表与往返一致性 ---

def test_full_alphabet_roundtrip():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = bacon_encode(alphabet)
    assert len(code.split(" ")) == 26
    assert bacon_decode(code) == alphabet


def test_lowercase_roundtrip():
    assert bacon_encode("hello") == bacon_encode("HELLO")
    assert bacon_decode(bacon_encode("hello")) == "HELLO"
