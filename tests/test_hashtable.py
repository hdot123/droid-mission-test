import pytest

from hashtable import HashTable, djb2


def test_djb2_hash_is_pinned():
    # djb2 32-bit over UTF-8 bytes: 5381 * 33 + ord("a") == 177670
    assert djb2("a") == 177670
    # home slot at capacity 8
    assert djb2("a") % 8 == 6


def test_new_table_capacity_len_and_probe():
    ht = HashTable()
    assert ht.capacity == 8
    assert len(ht) == 0
    assert ht.probe_sequence("a") == [6]


def test_probe_sequences_and_lookups_after_two_puts():
    ht = HashTable()
    assert ht.put("a", 1) is None
    assert ht.put("i", 2) is None
    assert ht.probe_sequence("a") == [6]
    assert ht.probe_sequence("i") == [6, 7]
    assert ht.probe_sequence("q") == [6, 7, 0]
    assert ht.get("a") == 1
    assert ht.get("i") == 2
    assert "a" in ht
    assert "q" not in ht


def test_update_existing_key_keeps_size():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
    ht.put("a", 10)
    assert ht.get("a") == 10
    assert len(ht) == 2


def test_delete_tombstones_and_probe_skips_tombstone():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
    assert ht.delete("a") is None
    with pytest.raises(KeyError):
        ht.get("a")
    # probing for "i" walks over the tombstone at slot 6 but still ends at 7
    assert ht.probe_sequence("i") == [6, 7]
    assert len(ht) == 1


def test_reinsert_reuses_first_tombstone():
    ht = HashTable()
    ht.put("a", 1)
    ht.put("i", 2)
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


def test_resize_to_16_after_six_keys():
    ht = HashTable()
    keys = ["k0", "k1", "k2", "k3", "k4", "k5"]
    for n, key in enumerate(keys, start=1):
        ht.put(key, n)
    assert ht.capacity == 16
    for n, key in enumerate(keys, start=1):
        assert ht.get(key) == n


def test_resize_to_32_at_twelve_keys():
    ht = HashTable()
    keys = ["k%d" % n for n in range(12)]
    for n, key in enumerate(keys[:6], start=1):
        ht.put(key, n)
    assert ht.capacity == 16
    for n, key in enumerate(keys[6:], start=7):
        ht.put(key, n)
    assert ht.capacity == 32
    assert len(ht) == 12
    for n, key in enumerate(keys, start=1):
        assert ht.get(key) == n
