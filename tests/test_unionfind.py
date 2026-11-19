import pytest

from unionfind import UnionFind


def test_initial_state_n5():
    uf = UnionFind(5)
    assert len(uf) == 5
    assert uf.count == 5
    assert uf.groups() == [[0], [1], [2], [3], [4]]


def test_union_returns_true_then_false():
    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(0, 2) is False


def test_connected():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 3) is False


def test_count_after_merges():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.count == 3
    assert uf.groups() == [[0, 1, 2], [3], [4]]


def test_find_relationships():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.find(0) == uf.find(2)
    assert uf.find(0) != uf.find(3)


def test_union_3_4_final_groups():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.union(3, 4) is True
    assert uf.groups() == [[0, 1, 2], [3, 4]]
    assert uf.count == 2


def test_constructor_non_positive_raises_value_error():
    with pytest.raises(ValueError):
        UnionFind(0)
    with pytest.raises(ValueError):
        UnionFind(-3)


def test_constructor_non_int_raises_type_error():
    with pytest.raises(TypeError):
        UnionFind(2.5)


def test_constructor_bool_rejected():
    with pytest.raises(TypeError):
        UnionFind(True)


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


def test_index_bool_rejected():
    uf = UnionFind(5)
    with pytest.raises(TypeError):
        uf.find(True)
    with pytest.raises(TypeError):
        uf.union(False, 1)
    with pytest.raises(TypeError):
        uf.connected(0, True)


def test_union_by_rank_and_path_compression():
    uf = UnionFind(4)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(0, 2)
    assert uf.count == 1
    assert uf.groups() == [[0, 1, 2, 3]]
    for x in range(4):
        assert uf.find(x) == uf.find(0)


def test_groups_ordering_with_scattered_sets():
    uf = UnionFind(6)
    uf.union(1, 3)
    uf.union(4, 5)
    assert uf.groups() == [[0], [1, 3], [2], [4, 5]]
    assert uf.count == 4
    assert len(uf) == 6
