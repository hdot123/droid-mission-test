"""lfucache 验收测试（第五十七轮 D 单 · 逐条对应验收要点）。"""

import pytest

from lfucache import LFUCache


def test_official_script_capacity_2():
    """官方脚本（capacity = 2）：LFU 淘汰顺序全链路探针。"""
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # 淘汰键 2
    assert cache.get(2) == -1
    assert cache.get(3) == 3
    cache.put(4, 4)  # 淘汰键 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
    assert len(cache) == 2
    assert 2 not in cache
    assert 4 in cache


def test_equal_frequency_tie_break_evicts_least_recently_used():
    """同频破平探针：a、b 同频 1，淘汰最近最少使用的 a。"""
    cache = LFUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.get("a") == -1
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_contains_does_not_count_as_use():
    """contains 不计使用探针：多次 in 不刷新频率与最近序，仍淘汰 a。"""
    cache = LFUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    for _ in range(5):
        assert ("a" in cache) is True
    cache.put("c", 3)
    assert cache.get("a") == -1
    assert cache.get("b") == 2


def test_put_counts_as_use_on_update():
    """put（含更新已有键）计一次使用：刷新频率与最近时刻。"""
    cache = LFUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)  # a 频率升到 2 并刷新最近序
    assert cache.get("a") == 10
    cache.put("c", 3)  # b 频率 1 最低，淘汰 b
    assert cache.get("b") == -1
    assert cache.get("a") == 10
    assert cache.get("c") == 3


def test_get_miss_returns_minus_one_without_side_effects():
    """get 未命中返回 -1 且不落键、不改变现存内容。"""
    cache = LFUCache(2)
    assert cache.get("missing") == -1
    assert len(cache) == 0
    cache.put("x", 1)
    assert cache.get("missing") == -1
    assert len(cache) == 1


def test_len_counts_existing_keys():
    """__len__ 返回现存键数。"""
    cache = LFUCache(3)
    assert len(cache) == 0
    cache.put("a", 1)
    cache.put("b", 2)
    assert len(cache) == 2
    cache.put("c", 3)
    assert len(cache) == 3


def test_capacity_zero_and_negative_raise_value_error():
    """LFUCache(0) 与 LFUCache(-2) 抛 ValueError。"""
    with pytest.raises(ValueError):
        LFUCache(0)
    with pytest.raises(ValueError):
        LFUCache(-2)


def test_non_int_capacity_raises_type_error():
    """LFUCache(2.0) 与 LFUCache(True) 抛 TypeError。"""
    with pytest.raises(TypeError):
        LFUCache(2.0)
    with pytest.raises(TypeError):
        LFUCache(True)
