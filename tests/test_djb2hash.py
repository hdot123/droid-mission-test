import pytest

from djb2hash import djb2, djb2_bytes


def test_empty_string():
    assert djb2("") == 5381


def test_single_char_a():
    assert djb2("a") == 177670


def test_abc():
    assert djb2("abc") == 193485963


def test_hello():
    assert djb2("hello") == 261238937


def test_str_and_bytes_agree_ascii():
    assert djb2("Hello") == djb2_bytes(b"Hello")


def test_str_and_bytes_agree_utf8():
    assert djb2("café") == djb2_bytes("café".encode("utf-8"))


def test_bytes_empty():
    assert djb2_bytes(b"") == 5381


def test_bytes_null_byte():
    assert djb2_bytes(b"\x00") == 177573


def test_long_string_in_range():
    text = "lorem ipsum dolor sit amet " * 500
    value = djb2(text)
    assert 0 <= value <= 4294967295
    assert value == djb2_bytes(text.encode("utf-8"))


@pytest.mark.parametrize("bad", [123, None])
def test_djb2_rejects_non_str(bad):
    with pytest.raises(TypeError):
        djb2(bad)


def test_djb2_bytes_rejects_str():
    with pytest.raises(TypeError):
        djb2_bytes("abc")
