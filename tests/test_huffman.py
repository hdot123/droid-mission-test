"""huffman.py 的验收测试：教科书锚、入参契约、随机性质（第五十九轮 D 单）。"""

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
ANCHOR_CODES = {"f": "0", "c": "100", "d": "101", "e": "110", "a": "1110", "b": "1111"}


# ---------------------------------------------------------------- 教科书锚

def test_anchor_code_lengths():
    assert huffman_code_lengths(dict(ANCHOR)) == ANCHOR_LENGTHS


def test_anchor_codes():
    assert huffman_codes(dict(ANCHOR)) == ANCHOR_CODES


def test_empty_table():
    assert huffman_code_lengths({}) == {}
    assert huffman_codes({}) == {}


def test_single_symbol_length_one():
    assert huffman_code_lengths({"x": 7}) == {"x": 1}


def test_two_equal_symbols_canonical_codes():
    assert huffman_codes({"b": 1, "a": 1}) == {"a": "0", "b": "1"}


# ---------------------------------------------------------------- 入参契约：ValueError

def test_nonpositive_freq_raises_value_error():
    with pytest.raises(ValueError):
        huffman_code_lengths({"a": 0})
    with pytest.raises(ValueError):
        huffman_code_lengths({"a": -3})


def test_encode_missing_symbol_raises_value_error():
    with pytest.raises(ValueError):
        huffman_encode("ab", {"a": "0"})


def test_decode_non_bit_char_raises_value_error():
    with pytest.raises(ValueError):
        huffman_decode("02", {"a": "0", "b": "1"})


def test_decode_trailing_partial_code_raises_value_error():
    with pytest.raises(ValueError):
        huffman_decode(
            "111",
            {"f": "0", "c": "100", "d": "101", "e": "110", "a": "1110", "b": "1111"},
        )


def test_decode_nonexistent_path_raises_value_error():
    with pytest.raises(ValueError):
        huffman_decode("10", {"a": "0", "b": "110"})


# ---------------------------------------------------------------- 入参契约：TypeError

def test_non_int_freq_raises_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths({"a": 1.5})


def test_non_dict_freqs_raises_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths([("a", 1)])


def test_non_str_or_empty_symbol_raises_type_error():
    with pytest.raises(TypeError):
        huffman_code_lengths({1: 5})
    with pytest.raises(TypeError):
        huffman_code_lengths({"": 5})


def test_encode_decode_type_errors():
    with pytest.raises(TypeError):
        huffman_encode(123, {"a": "0"})
    with pytest.raises(TypeError):
        huffman_encode("a", ["a", "0"])
    with pytest.raises(TypeError):
        huffman_decode(1010, {"a": "0"})
    with pytest.raises(TypeError):
        huffman_decode("0", ["a", "0"])


# ---------------------------------------------------------------- 钉死合并序 / 规范码

def _two_queue_lengths(freqs):
    """双队列法独立实现，与堆构造逐个对照（合并序口径一致）。"""
    leaves = [
        [freq, sym, None]
        for sym, freq in sorted(freqs.items(), key=lambda kv: (kv[1], kv[0]))
    ]
    internal = []  # 元素可能为 None 表示已消费
    li = 0

    def remaining():
        return (len(leaves) - li) + sum(1 for n in internal if n is not None)

    if len(leaves) == 1:
        return {leaves[0][1]: 1}

    while remaining() > 1:
        # 全局最小 (权重, 最小符号)：叶队首 vs 未消费内部节点中的最小者
        pick_int = None
        for idx, n in enumerate(internal):
            if n is None:
                continue
            if pick_int is None or (n[0], n[1]) < (internal[pick_int][0], internal[pick_int][1]):
                pick_int = idx
        take_int = pick_int is not None and (
            li >= len(leaves)
            or (internal[pick_int][0], internal[pick_int][1])
            <= (leaves[li][0], leaves[li][1])
        )
        if take_int:
            a = internal[pick_int]
            internal[pick_int] = None
        else:
            a = leaves[li]
            li += 1

        pick_int = None
        for idx, n in enumerate(internal):
            if n is None:
                continue
            if pick_int is None or (n[0], n[1]) < (internal[pick_int][0], internal[pick_int][1]):
                pick_int = idx
        take_int = pick_int is not None and (
            li >= len(leaves)
            or (internal[pick_int][0], internal[pick_int][1])
            <= (leaves[li][0], leaves[li][1])
        )
        if take_int:
            b = internal[pick_int]
            internal[pick_int] = None
        else:
            b = leaves[li]
            li += 1

        internal.append([a[0] + b[0], a[1] if a[1] < b[1] else b[1], (a, b)])

    root = None
    if li < len(leaves):
        root = leaves[li]
    else:
        for n in internal:
            if n is not None:
                root = n

    depths = {}
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        if node[2] is None:
            depths[node[1]] = depth if depth > 0 else 1
        else:
            stack.append((node[2][0], depth + 1))
            stack.append((node[2][1], depth + 1))
    return depths


def test_random_heap_vs_two_queue_lengths_and_kraft_and_roundtrip():
    rng = random.Random(20261127)
    for _ in range(200):
        n = rng.randint(2, 12)
        symbols = [chr(ord("a") + i) for i in range(n)]
        rng.shuffle(symbols)
        freqs = {sym: rng.randint(1, 1000) for sym in symbols}

        lengths = huffman_code_lengths(freqs)
        assert lengths == _two_queue_lengths(freqs), freqs

        # Kraft 和 == 1（有理数精确比较）
        kraft = sum(Fraction(1, 2 ** lengths[sym]) for sym in freqs)
        assert kraft == 1, freqs

        codes = huffman_codes(freqs)
        # 码长与码表一致、前缀自由
        assert {sym: len(code) for sym, code in codes.items()} == lengths
        sorted_codes = sorted(codes.values())
        for i, c1 in enumerate(sorted_codes):
            for c2 in sorted_codes[i + 1:]:
                assert not c2.startswith(c1), (freqs, codes)

        # encode／decode 回环恒等且比特长 == Σ len(codes[ch])
        text = "".join(rng.choice(symbols) for _ in range(rng.randint(1, 50)))
        bits = huffman_encode(text, codes)
        assert bits == "".join(codes[ch] for ch in text)
        assert len(bits) == sum(len(codes[ch]) for ch in text)
        assert huffman_decode(bits, codes) == text


def test_anchor_roundtrip():
    codes = huffman_codes(dict(ANCHOR))
    text = "fababaefcd"
    bits = huffman_encode(text, codes)
    assert len(bits) == sum(len(codes[ch]) for ch in text)
    assert huffman_decode(bits, codes) == text
    assert huffman_decode("", codes) == ""
