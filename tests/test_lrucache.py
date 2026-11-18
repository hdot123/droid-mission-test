"""Tests for lrucache.LRUCache (sub-issue #250)."""

import pytest

from lrucache import LRUCache


def test_capacity_validation_rejects_non_positive_and_non_int():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-1)
    with pytest.raises(ValueError):
        LRUCache(2.5)
    with pytest.raises(ValueError):
        LRUCache("2")
    with pytest.raises(ValueError):
        LRUCache(None)


def test_capacity_validation_accepts_positive_int():
    assert LRUCache(1).capacity == 1
    assert LRUCache(3).capacity == 3


def test_get_hit_refreshes_order():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    assert c.keys_oldest_first() == ["b", "a"]


def test_get_miss_returns_default_and_does_not_change_order():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("missing") is None
    assert c.get("missing", "fallback") == "fallback"
    assert c.keys_oldest_first() == ["a", "b"]


def test_put_insert_and_update_refresh():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.keys_oldest_first() == ["a", "b"]
    c.put("a", 10)  # update refreshes "a" to most recently used
    assert c.get("a") == 10
    assert c.keys_oldest_first() == ["b", "a"]


def test_eviction_of_least_recently_used():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)  # evicts "a" (least recently used)
    assert c.get("a") is None
    assert len(c) == 2
    assert c.keys_oldest_first() == ["b", "c"]


def test_eviction_after_get_refresh():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1  # "a" is now most recently used
    c.put("c", 3)  # evicts "b" (least recently used)
    assert c.get("b") is None
    assert len(c) == 2
    assert c.keys_oldest_first() == ["a", "c"]


def test_put_existing_key_does_not_evict():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 5)  # update within capacity: no eviction
    assert len(c) == 2
    assert c.keys_oldest_first() == ["b", "a"]


def test_len_and_contains():
    c = LRUCache(2)
    assert len(c) == 0
    c.put("a", 1)
    assert len(c) == 1
    assert "a" in c
    assert "z" not in c


def test_contains_does_not_refresh_order():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert "a" in c  # must not move "a" to most recently used
    assert c.keys_oldest_first() == ["a", "b"]
    c.put("c", 3)  # evicts "a", which is still the least recently used
    assert c.get("a") is None
    assert c.get("b") == 2


def test_keys_oldest_first():
    c = LRUCache(3)
    c.put("x", 1)
    c.put("y", 2)
    c.put("z", 3)
    assert c.keys_oldest_first() == ["x", "y", "z"]
    c.get("x")
    assert c.keys_oldest_first() == ["y", "z", "x"]


def test_worked_example_from_spec():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.get("b") is None
    assert len(c) == 2
    assert c.keys_oldest_first() == ["a", "c"]
    c.put("a", 10)
    assert c.get("a") == 10
    assert c.keys_oldest_first() == ["c", "a"]
