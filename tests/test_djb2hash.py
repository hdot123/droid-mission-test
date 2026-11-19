import pytest

from djb2hash import djb2, djb2_bytes


def test_djb2_empty_string():
    assert djb2("") == 5381


def test_djb2_a():
    assert djb2("a") == 177670


def test_djb2_abc():
    assert djb2("abc") == 193485963


def test_djb2_hello():
    assert djb2("hello") == 261238937


def test_djb2_matches_bytes_hello():
    assert djb2("Hello") == djb2_bytes(b"Hello")


def test_djb2_matches_utf8_bytes_cafe():
    assert djb2("café") == djb2_bytes("café".encode("utf-8"))


def test_djb2_bytes_empty():
    assert djb2_bytes(b"") == 5381


def test_djb2_bytes_nul_byte():
    assert djb2_bytes(b"\x00") == 177573


def test_long_string_result_within_32_bits():
    for text in ("x" * 1000, "abc" * 5000, "café" * 3000, "\U0001f600" * 2000):
        result = djb2(text)
        assert 0 <= result <= 4294967295
    for data in (b"\xff" * 4096, bytes(range(256)) * 64):
        result = djb2_bytes(data)
        assert 0 <= result <= 4294967295


def test_djb2_rejects_non_str():
    for bad in (123, None, b"abc", 1.5, True, ["a"]):
        with pytest.raises(TypeError):
            djb2(bad)


def test_djb2_bytes_rejects_non_bytes():
    for bad in ("abc", None, 123, 1.5, True, [1, 2]):
        with pytest.raises(TypeError):
            djb2_bytes(bad)


def test_djb2_bytes_accepts_bytearray():
    assert djb2_bytes(bytearray(b"Hello")) == djb2_bytes(b"Hello")
