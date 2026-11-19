"""Tests for unionfind.UnionFind (work order #633, process card unionfind)."""

import pytest

from unionfind import UnionFind


# --- construction / basic attributes --------------------------------------

def test_initial_state_n5():
    uf = UnionFind(5)
    assert len(uf) == 5
    assert uf.count == 5
    assert uf.groups() == [[0], [1], [2], [3], [4]]


# --- unions and connectivity ----------------------------------------------

def test_union_sequence_and_count():
    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(0, 2) is False  # already same set
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 3) is False
    assert uf.count == 3
    assert uf.groups() == [[0, 1, 2], [3], [4]]


def test_find_relations():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.find(0) == uf.find(2)
    assert uf.find(0) != uf.find(3)


def test_union_3_4_final_state():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.count == 2
    assert uf.groups() == [[0, 1, 2], [3, 4]]
    assert len(uf) == 5


# --- constructor validation ------------------------------------------------

def test_constructor_zero_and_negative_raise_value_error():
    with pytest.raises(ValueError):
        UnionFind(0)
    with pytest.raises(ValueError):
        UnionFind(-3)


def test_constructor_float_raises_type_error():
    with pytest.raises(TypeError):
        UnionFind(2.5)


def test_constructor_bool_rejected():
    with pytest.raises(TypeError):
        UnionFind(True)


# --- element validation -----------------------------------------------------

def test_find_out_of_range_raises_index_error():
    uf = UnionFind(5)
    with pytest.raises(IndexError):
        uf.find(5)
    with pytest.raises(IndexError):
        uf.find(-1)


def test_union_negative_element_raises_index_error():
    uf = UnionFind(5)
    with pytest.raises(IndexError):
        uf.union(0, -1)


def test_find_non_int_raises_type_error():
    uf = UnionFind(5)
    with pytest.raises(TypeError):
        uf.find("0")
    with pytest.raises(TypeError):
        uf.find(True)


# --- path compression + union by rank behaviour -----------------------------

def test_path_compression_flattens():
    uf = UnionFind(6)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(2, 3)
    uf.union(3, 4)
    root = uf.find(0)
    # after find, every member's parent chain is flat
    assert uf.find(4) == root
    assert uf.count == 2


def test_union_by_rank_attach_small_under_large():
    uf = UnionFind(7)
    # build a set with higher rank on the left
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.union(0, 3) is True
    assert uf.count == 3  # 7 elements, 4 merges
    assert uf.groups() == [[0, 1, 2, 3, 4], [5], [6]]


def test_union_idempotent_returns_false():
    uf = UnionFind(3)
    assert uf.union(2, 2) is False  # same element
    uf.union(0, 2)
    assert uf.union(2, 0) is False  # reverse of existing merge
    assert uf.count == 2


def test_groups_ordering_and_ascending():
    uf = UnionFind(6)
    uf.union(5, 3)
    uf.union(4, 2)
    # groups sorted by first element ascending, members ascending
    assert uf.groups() == [[0], [1], [2, 4], [3, 5]]


def test_single_element():
    uf = UnionFind(1)
    assert len(uf) == 1
    assert uf.count == 1
    assert uf.groups() == [[0]]
    assert uf.find(0) == 0
    assert uf.union(0, 0) is False
