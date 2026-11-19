"""tests/test_bloom.py:布隆过滤器验收用例（第 46 轮 B 单）。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from bloom import BloomFilter


def test_bit_positions_apple():
    bf = BloomFilter(100, 3)
    assert bf.bit_positions("apple") == [10, 53, 67]


def test_bit_positions_banana():
    bf = BloomFilter(100, 3)
    assert bf.bit_positions("banana") == [36, 52, 94]


def test_bit_positions_cherry():
    bf = BloomFilter(100, 3)
    assert bf.bit_positions("cherry") == [8, 72, 90]


def test_fresh_filter_membership():
    bf = BloomFilter(100, 3)
    assert "apple" not in bf


def test_add_then_contains():
    bf = BloomFilter(100, 3)
    bf.add("apple")
    assert "apple" in bf
    assert "grape" not in bf


def test_multiple_items_membership():
    bf = BloomFilter(100, 3)
    bf.add("apple")
    bf.add("banana")
    bf.add("cherry")
    assert "banana" in bf
    assert "cherry" in bf
    assert "grape" not in bf
    assert "melon" not in bf


def test_set_bits_after_three_items():
    bf = BloomFilter(100, 3)
    bf.add("apple")
    bf.add("banana")
    bf.add("cherry")
    assert bf.set_bits() == [8, 10, 36, 52, 53, 67, 72, 90, 94]


def test_readd_apple_idempotent():
    bf = BloomFilter(100, 3)
    bf.add("apple")
    bf.add("banana")
    bf.add("cherry")
    bf.add("apple")
    assert "apple" in bf
    assert len(bf.set_bits()) == 9


def test_invalid_sizes_raise_value_error():
    with pytest.raises(ValueError):
        BloomFilter(0, 3)
    with pytest.raises(ValueError):
        BloomFilter(100, 0)
    with pytest.raises(ValueError):
        BloomFilter(-5, 3)


def test_non_int_sizes_raise_type_error():
    with pytest.raises(TypeError):
        BloomFilter(100.5, 3)
    with pytest.raises(TypeError):
        BloomFilter(100, "3")


def test_add_non_str_raises_type_error():
    bf = BloomFilter(100, 3)
    with pytest.raises(TypeError):
        bf.add(123)


def test_bit_positions_non_str_raises_type_error():
    bf = BloomFilter(100, 3)
    with pytest.raises(TypeError):
        bf.bit_positions(123)


def test_contains_non_str_raises_type_error():
    bf = BloomFilter(100, 3)
    with pytest.raises(TypeError):
        123 in bf


def test_set_bits_fresh_filter_empty():
    bf = BloomFilter(100, 3)
    assert bf.set_bits() == []


def test_positions_are_sorted_and_deduplicated():
    bf = BloomFilter(100, 3)
    positions = bf.bit_positions("apple")
    assert positions == sorted(positions)
    assert len(positions) == len(set(positions))
