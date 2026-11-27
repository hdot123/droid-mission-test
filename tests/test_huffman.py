"""tests/test_huffman.py —— huffman.py 的逐验收点测试（第五十九轮 D 单）。"""

import random
from fractions import Fraction

import pytest

from huffman import (
    huffman_code_lengths,
    huffman_codes,
    huffman_decode,
    huffman_encode,
)

ANCHOR = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
ANCHOR_LENGTHS = {"f": 1, "c": 3, "d": 3, "e": 3, "a": 4, "b": 4}
ANCHOR_CODES = {
    "f": "0",
    "c": "100",
    "d": "101",
    "e": "110",
    "a": "1110",
    "b": "1111",
}


# ---------------------------------------------------------------------------
# 参考实现：双队列法（与实现所用的堆构造法独立，用于交叉验证码长）
# ---------------------------------------------------------------------------


def _two_queue_code_lengths(freqs):
    """双队列法：叶子队列 + 合并队列，每步取（权重, 子树最小符号）最小者。"""
    leaves = sorted(freqs.items(), key=lambda kv: (kv[1], kv[0]))
    queue1 = [(w, s, ("leaf", s)) for s, w in leaves]
    queue2 = []
    while len(queue1) + len(queue2) > 1:
        if not queue1:
            pick2 = queue2
        elif not queue2:
            pick2 = queue1
        else:
            pick2 = queue1 if queue1[0][:2] <= queue2[0][:2] else queue2
        w1, min1, n1 = pick2.pop(0)
        if queue1 and queue2:
            pick = queue1 if queue1[0][:2] <= queue2[0][:2] else queue2
        elif queue1:
            pick = queue1
        else:
            pick = queue2
        w2, min2, n2 = pick.pop(0)
        merged_min = min1 if min1 < min2 else min2
        queue2.append((w1 + w2, merged_min, ("node", n1, n2)))
    root = (queue1 + queue2)[0][2]
    lengths = {}
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        if node[0] == "leaf":
            lengths[node[1]] = depth
        else:
            stack.append((node[1], depth + 1))
            stack.append((node[2], depth + 1))
    return lengths


# ---------------------------------------------------------------------------
# 验收要点一：教科书锚
# ---------------------------------------------------------------------------


def test_textbook_anchor_code_lengths():
    assert huffman_code_lengths(ANCHOR) == ANCHOR_LENGTHS


def test_textbook_anchor_codes():
    assert huffman_codes(ANCHOR) == ANCHOR_CODES


def test_empty_freqs():
    assert huffman_code_lengths({}) == {}


def test_single_symbol_length_is_one():
    assert huffman_code_lengths({"x": 7}) == {"x": 1}


def test_two_symbols_canonical():
    assert huffman_codes({"b": 1, "a": 1}) == {"a": "0", "b": "1"}


# ---------------------------------------------------------------------------
# 验收要点二：性质测试（随机频次表 2–12 符号）
# ---------------------------------------------------------------------------


def _random_freqs(rng, n):
    return {chr(ord("a") + i): rng.randint(1, 500) for i in range(n)}


def test_heap_and_two_queue_lengths_identical():
    rng = random.Random(590059)
    for _ in range(60):
        n = rng.randint(2, 12)
        freqs = _random_freqs(rng, n)
        assert huffman_code_lengths(freqs) == _two_queue_code_lengths(freqs)


def test_kraft_sum_equals_one():
    rng = random.Random(590060)
    for _ in range(40):
        n = rng.randint(2, 12)
        freqs = _random_freqs(rng, n)
        lengths = huffman_code_lengths(freqs)
        total = sum((Fraction(1, 2**ln) for ln in lengths.values()), Fraction(0))
        assert total == 1


def test_encode_decode_roundtrip_and_bit_length():
    rng = random.Random(590061)
    for _ in range(40):
        n = rng.randint(2, 12)
        freqs = _random_freqs(rng, n)
        codes = huffman_codes(freqs)
        symbols = sorted(freqs)
        text = "".join(rng.choice(symbols) for _ in range(rng.randint(1, 200)))
        bits = huffman_encode(text, codes)
        assert len(bits) == sum(len(codes[ch]) for ch in text)
        assert huffman_decode(bits, codes) == text


def test_anchor_roundtrip():
    codes = huffman_codes(ANCHOR)
    text = "fabcbaffabc"
    bits = huffman_encode(text, codes)
    assert len(bits) == sum(len(codes[ch]) for ch in text)
    assert huffman_decode(bits, codes) == text


# ---------------------------------------------------------------------------
# 验收要点三：ValueError 面
# ---------------------------------------------------------------------------


def test_code_lengths_nonpositive_freq_value_error():
    with pytest.raises(ValueError):
        huffman_code_lengths({"a": 0})
    with pytest.raises(ValueError):
        huffman_code_lengths({"a": -3})


def test_encode_symbol_without_code_value_error():
    with pytest.raises(ValueError):
        huffman_encode("ab", {"a": "0"})


def test_decode_non_binary_char_value_error():
    with pytest.raises(ValueError):
        huffman_decode("02", {"a": "0", "b": "1"})


def test_decode_trailing_partial_code_value_error():
    with pytest.raises(ValueError):
        huffman_decode("111", dict(ANCHOR_CODES))


def test_decode_nonexistent_path_value_error():
    with pytest.raises(ValueError):
        huffman_decode("10", {"a": "0", "b": "110"})


# ---------------------------------------------------------------------------
# 验收要点四：TypeError 面
# ---------------------------------------------------------------------------


def test_code_lengths_non_int_freq_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths({"a": 1.5})


def test_code_lengths_non_dict_freqs_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths([("a", 1)])


def test_encode_decode_type_error_surface():
    with pytest.raises(TypeError):
        huffman_encode(123, {"a": "0"})
    with pytest.raises(TypeError):
        huffman_encode("ab", [("a", "0")])
    with pytest.raises(TypeError):
        huffman_decode(123, {"a": "0", "b": "1"})
    with pytest.raises(TypeError):
        huffman_decode("01", [("a", "0")])


def test_empty_string_symbol_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths({"": 3})


def test_non_str_symbol_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths({1: 3})


def test_empty_and_single_codes_tables():
    assert huffman_codes({}) == {}
    assert huffman_codes({"x": 7}) == {"x": "0"}
