"""tests/test_natsort.py: 自然序排序验收（第五十九轮 D 单 natsort）。"""

import functools
import random
import re

import pytest

from natsort import natural_sort

# ---------------------------------------------------------------------------
# 验收要点：给定样例
# ---------------------------------------------------------------------------


def test_basic_numeric_order():
    assert natural_sort(["a10", "a2", "a1"]) == ["a1", "a2", "a10"]


def test_leading_zero_tie_break():
    # "a01" 与 "a1" 数值同、按位数分先后（钉死项，不许含糊并列）
    assert natural_sort(["a01", "a1", "a001"]) == ["a1", "a01", "a001"]


def test_numeric_segment_sorts_first_and_codepoint_order():
    # "1" 数字段先于非数字段；"a" < "x" 按码点序
    assert natural_sort(["x", "1", "a"]) == ["1", "a", "x"]


def test_empty_list():
    assert natural_sort([]) == []


# ---------------------------------------------------------------------------
# 性质：不改入参
# ---------------------------------------------------------------------------


def test_input_list_unchanged():
    original = ["a10", "a2", "a1", "x", "1", "a", "a01", "a1", "a001"]
    snapshot = list(original)
    natural_sort(original)
    assert original == snapshot
    assert all(a is b for a, b in zip(original, snapshot))


def test_returns_new_list():
    src = ["b", "a"]
    out = natural_sort(src)
    assert out is not src
    assert out == ["a", "b"]


# ---------------------------------------------------------------------------
# 性质：随机词表上键函数排序与显式比较器排序逐个一致
# ---------------------------------------------------------------------------

_SEG = re.compile(r"\d+|\D+")


def _ref_compare(a: str, b: str) -> int:
    """按规范独立实现的显式比较器（不复用被测模块代码）。"""
    segs_a = _SEG.findall(a)
    segs_b = _SEG.findall(b)
    for sx, sy in zip(segs_a, segs_b):
        nx, ny = sx[0].isdigit(), sy[0].isdigit()
        if nx and ny:
            vx, vy = int(sx), int(sy)
            if vx != vy:
                return -1 if vx < vy else 1
            if len(sx) != len(sy):
                return -1 if len(sx) < len(sy) else 1
        elif nx:
            return -1
        elif ny:
            return 1
        else:
            if sx != sy:
                return -1 if sx < sy else 1
    if len(segs_a) != len(segs_b):
        return -1 if len(segs_a) < len(segs_b) else 1
    if a == b:
        return 0
    return -1 if a < b else 1


def _random_words(rng: random.Random, count: int) -> list:
    words = []
    alphabet = "abcxyz_"
    for _ in range(count):
        parts = []
        for _ in range(rng.randint(1, 4)):
            if rng.random() < 0.5:
                parts.append(str(rng.randint(0, 999)))
            else:
                parts.append("".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4))))
        words.append("".join(parts))
    return words


def test_key_sort_and_comparator_sort_agree_on_random_words():
    rng = random.Random(20261127)
    for _ in range(40):
        words = _random_words(rng, rng.randint(2, 30))
        by_key = natural_sort(list(words))
        by_cmp = sorted(words, key=functools.cmp_to_key(_ref_compare))
        assert by_key == by_cmp


# ---------------------------------------------------------------------------
# 入参契约：TypeError（本题无 ValueError 面）
# ---------------------------------------------------------------------------


def test_non_list_container_raises_typeerror():
    with pytest.raises(TypeError):
        natural_sort("a10")


def test_non_str_element_raises_typeerror():
    with pytest.raises(TypeError):
        natural_sort(["a", 1])


def test_none_raises_typeerror():
    with pytest.raises(TypeError):
        natural_sort(None)


# ---------------------------------------------------------------------------
# 补充边界：前缀规则与交替段
# ---------------------------------------------------------------------------


def test_prefix_shorter_first():
    assert natural_sort(["ab", "a"]) == ["a", "ab"]
    assert natural_sort(["a1b", "a1"]) == ["a1", "a1b"]


def test_alternating_segments_compare():
    # 数字段对齐比较：2 vs 10 数值比；非数字段码点比
    assert natural_sort(["2b", "10a", "2a"]) == ["2a", "2b", "10a"]
