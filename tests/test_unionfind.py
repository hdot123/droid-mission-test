"""Tests for unionfind.UnionFind (acceptance points from work order #701)."""

import pytest

from unionfind import UnionFind


def test_new_instance_n5():
    uf = UnionFind(5)
    assert len(uf) == 5
    assert uf.count == 5
    assert uf.groups() == [[0], [1], [2], [3], [4]]


def test_union_merges_and_reports():
    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(0, 2) is False  # already same set


def test_connected_and_count_after_merges():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 3) is False
    assert uf.count == 3
    assert uf.groups() == [[0, 1, 2], [3], [4]]


def test_find_consistency():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.find(0) == uf.find(2)
    assert uf.find(0) != uf.find(3)


def test_union_3_4_groups_and_count():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.union(3, 4) is True
    assert uf.groups() == [[0, 1, 2], [3, 4]]
    assert uf.count == 2


def test_non_positive_n_raises_value_error():
    with pytest.raises(ValueError):
        UnionFind(0)
    with pytest.raises(ValueError):
        UnionFind(-3)


def test_non_int_n_raises_type_error():
    with pytest.raises(TypeError):
        UnionFind(2.5)
    with pytest.raises(TypeError):
        UnionFind(True)


def test_out_of_range_raises_index_error():
    uf = UnionFind(5)
    with pytest.raises(IndexError):
        uf.find(5)
    with pytest.raises(IndexError):
        uf.union(0, -1)


def test_non_int_element_raises_type_error():
    uf = UnionFind(5)
    with pytest.raises(TypeError):
        uf.find("0")
    with pytest.raises(TypeError):
        uf.union(0, 1.5)
