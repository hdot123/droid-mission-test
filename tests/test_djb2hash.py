import pytest

from djb2hash import djb2, djb2_bytes


def test_djb2_empty_string():
    assert djb2("") == 5381


def test_djb2_single_char():
    assert djb2("a") == 177670


def test_djb2_abc():
    assert djb2("abc") == 193485963


def test_djb2_hello():
    assert djb2("hello") == 261238937


def test_djb2_matches_djb2_bytes_for_ascii():
    assert djb2("Hello") == djb2_bytes(b"Hello")


def test_djb2_matches_djb2_bytes_for_utf8():
    assert djb2("café") == djb2_bytes("café".encode("utf-8"))


def test_djb2_bytes_empty():
    assert djb2_bytes(b"") == 5381


def test_djb2_bytes_null_byte():
    assert djb2_bytes(b"\x00") == 177573


def test_djb2_long_string_in_32bit_range():
    for text in ("x" * 1000, "ab" * 5000, "你好" * 300, "z" * 100_000):
        result = djb2(text)
        assert isinstance(result, int)
        assert 0 <= result <= 4294967295


def test_djb2_bytes_long_in_32bit_range():
    result = djb2_bytes(bytes(range(256)) * 50)
    assert 0 <= result <= 4294967295


def test_djb2_rejects_non_str():
    with pytest.raises(TypeError):
        djb2(123)
    with pytest.raises(TypeError):
        djb2(None)


def test_djb2_bytes_rejects_non_bytes():
    with pytest.raises(TypeError):
        djb2_bytes("abc")


def test_djb2_bytes_accepts_bytearray():
    assert djb2_bytes(bytearray(b"Hello")) == djb2_bytes(b"Hello")
