"""Tests for hashtable.py (open-addressing hash table)."""

import pytest

from hashtable import HashTable, djb2


def test_djb2_pinned_value():
    # djb2("a") = 177670, home slot = 177670 % 8 = 6
    assert djb2("a") == 177670
    assert djb2("a") % 8 == 6


def test_fresh_table():
    ht = HashTable()
    assert ht.capacity == 8
    assert len(ht) == 0
    assert ht.probe_sequence("a") == [6]


def test_put_two_keys_probe_sequences_and_get():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
    assert ht.probe_sequence("a") == [6]
    assert ht.probe_sequence("i") == [6, 7]
    assert ht.probe_sequence("q") == [6, 7, 0]
    assert ht.get("a") == 1
    assert ht.get("i") == 2
    assert "a" in ht
    assert "q" not in ht


def test_update_same_key_keeps_size():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
    ht.put("a", 10)
    assert ht.get("a") == 10
    assert len(ht) == 2


def test_delete_sets_tombstone_and_probe_skips_it():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
    ht.put("a", 10)
    ht.delete("a")
    with pytest.raises(KeyError):
        ht.get("a")
    # probing for "i" passes the tombstone at slot 6 but still counts it
    assert ht.probe_sequence("i") == [6, 7]


def test_put_reuses_tombstone():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
    ht.put("a", 10)
    ht.delete("a")
    ht.put("a", 9)
    assert ht.probe_sequence("a") == [6]
    assert ht.get("a") == 9


def test_delete_missing_raises_keyerror():
    ht = HashTable()
    with pytest.raises(KeyError):
        ht.delete("missing")


def test_non_str_key_raises_typeerror():
    ht = HashTable()
    with pytest.raises(TypeError):
        ht.put(1, "x")
    with pytest.raises(TypeError):
        ht.get(None)


def test_contains_non_str_is_false():
    ht = HashTable()
    assert (1 in ht) is False
    assert (None in ht) is False


def test_growth_to_16_after_six_keys():
    ht = HashTable()
    keys = ["k%d" % i for i in range(6)]
    for i, key in enumerate(keys):
        ht.put(key, i)
    assert ht.capacity == 16
    for i, key in enumerate(keys):
        assert ht.get(key) == i


def test_growth_to_32_at_twelve_keys():
    ht = HashTable()
    keys = ["k%d" % i for i in range(12)]
    for i, key in enumerate(keys):
        ht.put(key, i)
    assert ht.capacity == 32
    assert len(ht) == 12
    for i, key in enumerate(keys):
        assert ht.get(key) == i
