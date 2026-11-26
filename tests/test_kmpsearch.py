"""kmpsearch 验收测试：全部出现位置（含重叠）。

逐条对应验收要点：重叠出现、朴素对照性质、入参契约。
"""

import random

import pytest

from kmpsearch import find_all


def _naive(text: str, pattern: str) -> list[int]:
    """朴素逐位扫描（含重叠）作为对照实现。"""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    return [i for i in range(n - m + 1) if text[i : i + m] == pattern]


# ---------------------------------------------------------------- 验收要点


def test_overlapping_ababab():
    assert find_all("ababab", "abab") == [0, 2]


def test_overlapping_aaaa_aa():
    assert find_all("aaaa", "aa") == [0, 1, 2]


def test_abcabc():
    assert find_all("abcabc", "abc") == [0, 3]


def test_mississippi_issi():
    assert find_all("mississippi", "issi") == [1, 4]


def test_no_match():
    assert find_all("abc", "d") == []


def test_empty_text():
    assert find_all("", "a") == []


def test_single_char_match():
    assert find_all("a", "a") == [0]


def test_pattern_longer_than_text():
    assert find_all("ab", "abc") == []


def test_ascending_order_multiple_hits():
    # 结果必须升序且不重复
    res = find_all("aaaa", "a")
    assert res == [0, 1, 2, 3]
    assert res == sorted(set(res))


# ---------------------------------------------------------------- 性质：与朴素扫描一致


def test_property_matches_naive_two_letter_alphabet():
    rng = random.Random(20261126)
    for _ in range(400):
        n = rng.randrange(0, 26)  # text 长 0–25
        m = rng.randrange(1, 6)   # pattern 长 1–5
        text = "".join(rng.choice("ab") for _ in range(n))
        pattern = "".join(rng.choice("ab") for _ in range(m))
        assert find_all(text, pattern) == _naive(text, pattern), (
            text,
            pattern,
        )


def test_property_matches_naive_three_letter_alphabet():
    rng = random.Random(5858)
    for _ in range(400):
        n = rng.randrange(0, 26)
        m = rng.randrange(1, 6)
        text = "".join(rng.choice("abc") for _ in range(n))
        pattern = "".join(rng.choice("abc") for _ in range(m))
        assert find_all(text, pattern) == _naive(text, pattern), (
            text,
            pattern,
        )


def test_property_random_text_from_full_alphabet():
    # 额外覆盖：文本可任意、pattern 限定 1–5 长，仍与朴素一致
    rng = random.Random(932)
    alphabet = "abcd"
    for _ in range(300):
        n = rng.randrange(0, 26)
        m = rng.randrange(1, 6)
        text = "".join(rng.choice(alphabet) for _ in range(n))
        pattern = "".join(rng.choice(alphabet) for _ in range(m))
        assert find_all(text, pattern) == _naive(text, pattern), (
            text,
            pattern,
        )


# ---------------------------------------------------------------- 入参契约


def test_empty_pattern_raises_value_error():
    with pytest.raises(ValueError):
        find_all("abc", "")


def test_non_str_text_raises_type_error():
    with pytest.raises(TypeError):
        find_all(123, "a")


def test_non_str_pattern_raises_type_error():
    with pytest.raises(TypeError):
        find_all("abc", None)


def test_other_non_str_args_raise_type_error():
    with pytest.raises(TypeError):
        find_all("abc", 123)
    with pytest.raises(TypeError):
        find_all(None, "a")
    with pytest.raises(TypeError):
        find_all(["a"], "a")
    with pytest.raises(TypeError):
        find_all("abc", ["a"])
