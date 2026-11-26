import pytest

from kruskal import kruskal_mst


def test_single_node():
    assert kruskal_mst(1, []) == (0, [])


def test_single_edge():
    assert kruskal_mst(2, [(0, 1, 7)]) == (7, [(0, 1, 7)])


def test_three_nodes_triangle():
    assert kruskal_mst(3, [(0, 1, 1), (1, 2, 2), (0, 2, 3)]) == (
        3,
        [(0, 1, 1), (1, 2, 2)],
    )


def test_textbook_graph():
    edges = [
        (0, 1, 4),
        (0, 7, 8),
        (1, 2, 8),
        (1, 7, 11),
        (2, 3, 7),
        (2, 5, 4),
        (2, 8, 2),
        (3, 4, 9),
        (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1),
        (6, 8, 6),
        (7, 8, 7),
    ]
    total, mst = kruskal_mst(9, edges)
    assert total == 37
    assert mst == [
        (6, 7, 1),
        (2, 8, 2),
        (5, 6, 2),
        (0, 1, 4),
        (2, 5, 4),
        (2, 3, 7),
        (0, 7, 8),
        (3, 4, 9),
    ]


def test_equal_weight_tie_broken_by_canonical_order():
    _, mst = kruskal_mst(3, [(1, 2, 5), (0, 2, 5), (0, 1, 5)])
    assert mst == [(0, 1, 5), (0, 2, 5)]


def test_unordered_endpoints_normalized():
    _, mst = kruskal_mst(3, [(2, 0, 1), (1, 0, 1), (2, 1, 9)])
    assert mst == [(0, 1, 1), (0, 2, 1)]


def test_parallel_edges_pick_the_smaller():
    assert kruskal_mst(2, [(0, 1, 5), (0, 1, 3)]) == (3, [(0, 1, 3)])


def test_num_nodes_zero_raises_value_error():
    with pytest.raises(ValueError):
        kruskal_mst(0, [])


def test_disconnected_graph_raises_value_error():
    with pytest.raises(ValueError):
        kruskal_mst(3, [(0, 1, 1)])


def test_self_loop_raises_value_error():
    with pytest.raises(ValueError):
        kruskal_mst(2, [(0, 0, 1)])


def test_node_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        kruskal_mst(2, [(0, 2, 1)])


def test_bool_num_nodes_raises_type_error():
    with pytest.raises(TypeError):
        kruskal_mst(True, [])


def test_float_num_nodes_raises_type_error():
    with pytest.raises(TypeError):
        kruskal_mst(2.0, [])


def test_bool_node_index_raises_type_error():
    with pytest.raises(TypeError):
        kruskal_mst(2, [(0, True, 1)])


def test_non_numeric_weight_raises_type_error():
    with pytest.raises(TypeError):
        kruskal_mst(2, [(0, 1, "x")])


def test_negative_num_nodes_raises_value_error():
    with pytest.raises(ValueError):
        kruskal_mst(-1, [])
