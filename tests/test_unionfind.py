import pytest

from unionfind import UnionFind


def test_initial_state_n5():
    uf = UnionFind(5)
    assert len(uf) == 5
    assert uf.count == 5
    assert uf.groups() == [[0], [1], [2], [3], [4]]


def test_union_sequence_and_count():
    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(0, 2) is False
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


def test_union_3_4_after_prior_merges():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(0, 2)
    assert uf.union(3, 4) is True
    assert uf.groups() == [[0, 1, 2], [3, 4]]
    assert uf.count == 2


def test_n_zero_raises_value_error():
    with pytest.raises(ValueError):
        UnionFind(0)


def test_n_negative_raises_value_error():
    with pytest.raises(ValueError):
        UnionFind(-3)


def test_n_float_raises_type_error():
    with pytest.raises(TypeError):
        UnionFind(2.5)


def test_n_bool_rejected():
    with pytest.raises(TypeError):
        UnionFind(True)


def test_n_non_int_raises_type_error():
    with pytest.raises(TypeError):
        UnionFind("5")


def test_find_out_of_range_raises_index_error():
    uf = UnionFind(5)
    with pytest.raises(IndexError):
        uf.find(5)


def test_union_negative_index_raises_index_error():
    uf = UnionFind(5)
    with pytest.raises(IndexError):
        uf.union(0, -1)


def test_find_non_int_raises_type_error():
    uf = UnionFind(5)
    with pytest.raises(TypeError):
        uf.find("0")


def test_find_bool_rejected():
    uf = UnionFind(5)
    with pytest.raises(TypeError):
        uf.find(True)


def test_union_non_int_raises_type_error():
    uf = UnionFind(5)
    with pytest.raises(TypeError):
        uf.union(0, "1")


def test_single_element():
    uf = UnionFind(1)
    assert len(uf) == 1
    assert uf.count == 1
    assert uf.groups() == [[0]]
    assert uf.union(0, 0) is False
    assert uf.find(0) == 0


def test_groups_ordering_and_ascending_members():
    uf = UnionFind(6)
    uf.union(4, 5)
    uf.union(2, 3)
    uf.union(0, 1)
    assert uf.groups() == [[0, 1], [2, 3], [4, 5]]
    assert uf.count == 3
