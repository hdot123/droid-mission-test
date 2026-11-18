"""fnv1a 的验收测试（第四十三轮 · A 单）。"""

import pytest

from fnv1a import fnv1a32


def test_empty_input_returns_offset_basis():
    assert fnv1a32(b"") == 2166136261


def test_hello():
    assert fnv1a32(b"hello") == 1335831723


def test_foobar():
    assert fnv1a32(b"foobar") == 3214735720


def test_digits_123456789():
    assert fnv1a32(b"123456789") == 3146166556


def test_thousand_a():
    assert fnv1a32(b"a" * 1000) == 500786573


def test_non_bytes_raises_type_error():
    with pytest.raises(TypeError):
        fnv1a32("x")
