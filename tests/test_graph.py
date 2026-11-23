import pytest

from graph import Graph


def build_g() -> Graph:
    """Graph G: edges (a,b) (a,c) (b,d) (c,d) (d,e) plus isolated node z."""
    g = Graph()
    for u, v in [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e")]:
        g.add_edge(u, v)
    g.add_node("z")
    return g


def build_g2() -> Graph:
    """Graph G2: edges (m,n) (m,o) (n,p) (o,p) (p,q)."""
    g = Graph()
    for u, v in [("m", "n"), ("m", "o"), ("n", "p"), ("o", "p"), ("p", "q")]:
        g.add_edge(u, v)
    return g


def test_empty_graph():
    assert Graph().nodes() == []
    assert Graph().connected_components() == []


def test_nodes_sorted():
    assert build_g().nodes() == ["a", "b", "c", "d", "e", "z"]


def test_neighbors():
    g = build_g()
    assert g.neighbors("d") == ["b", "c", "e"]
    assert g.neighbors("z") == []


def test_bfs():
    assert build_g().bfs("a") == ["a", "b", "c", "d", "e"]


def test_dfs():
    assert build_g().dfs("a") == ["a", "b", "d", "c", "e"]


def test_bfs_from_isolated_node():
    assert build_g().bfs("z") == ["z"]


def test_connected_components():
    assert build_g().connected_components() == [["a", "b", "c", "d", "e"], ["z"]]


def test_has_path():
    g = build_g()
    assert g.has_path("a", "e") is True
    assert g.has_path("a", "z") is False
    assert g.has_path("a", "a") is True


def test_g2_bfs():
    assert build_g2().bfs("m") == ["m", "n", "o", "p", "q"]


def test_g2_dfs():
    assert build_g2().dfs("m") == ["m", "n", "p", "o", "q"]


def test_self_loop_raises_value_error():
    with pytest.raises(ValueError):
        build_g().add_edge("a", "a")


def test_unknown_node_raises_value_error():
    g = build_g()
    with pytest.raises(ValueError):
        g.neighbors("q")
    with pytest.raises(ValueError):
        g.bfs("q")
    with pytest.raises(ValueError):
        g.has_path("a", "q")


def test_non_str_node_raises_type_error():
    g = build_g()
    with pytest.raises(TypeError):
        g.add_node(1)
    with pytest.raises(TypeError):
        g.add_edge("a", 2)


def test_duplicate_edge_is_noop():
    g = build_g()
    g.add_edge("a", "b")
    assert g.neighbors("a") == ["b", "c"]
    assert g.neighbors("b") == ["a", "d"]


def test_add_node_is_idempotent():
    g = Graph()
    g.add_node("x")
    g.add_node("x")
    assert g.nodes() == ["x"]


def test_duplicate_edge_endpoints_non_str_type_error():
    with pytest.raises(TypeError):
        Graph().add_edge(1, "a")
    with pytest.raises(TypeError):
        Graph().add_edge("a", 1)


def test_has_path_nonexistent_endpoint_raises():
    with pytest.raises(ValueError):
        build_g().has_path("q", "a")
    with pytest.raises(ValueError):
        Graph().has_path("a", "a")
