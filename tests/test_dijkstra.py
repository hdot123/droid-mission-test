"""tests/test_dijkstra.py: dijkstra.py 验收要点逐条覆盖。"""

import math

import pytest

from dijkstra import dijkstra, shortest_path

G1 = {"A": {"B": 1, "C": 4}, "B": {"C": 2, "D": 5}, "C": {"D": 1}, "D": {}, "E": {}}
G2 = {"S": {"T": 2.5, "U": 1.5}, "U": {"T": 0.5}, "T": {}}
G3 = {"A": {"B": 7}}


def test_g1_dist_and_prev():
    dist, prev = dijkstra(G1, "A")
    assert dist["A"] == 0
    assert dist["B"] == 1
    assert dist["C"] == 3
    assert dist["D"] == 4
    assert dist["E"] == math.inf
    assert prev == {"B": "A", "C": "B", "D": "C"}


def test_g1_shortest_paths():
    assert shortest_path(G1, "A", "D") == ["A", "B", "C", "D"]
    assert shortest_path(G1, "A", "C") == ["A", "B", "C"]
    assert shortest_path(G1, "A", "E") == []
    assert shortest_path(G1, "A", "A") == ["A"]
    assert shortest_path(G1, "D", "A") == []


def test_g2_float_weights():
    dist, prev = dijkstra(G2, "S")
    assert dist["T"] == 2.0
    assert dist["U"] == 1.5
    assert prev == {"U": "S", "T": "U"}
    assert shortest_path(G2, "S", "T") == ["S", "U", "T"]


def test_g3_single_edge():
    dist, prev = dijkstra(G3, "A")
    assert dist["B"] == 7
    assert prev == {"B": "A"}


def test_negative_weight_raises_value_error():
    with pytest.raises(ValueError):
        dijkstra({"A": {"B": -1}}, "A")


def test_source_not_in_graph_raises_value_error():
    with pytest.raises(ValueError):
        dijkstra(G1, "Z")


def test_target_not_in_graph_raises_value_error():
    with pytest.raises(ValueError):
        shortest_path(G1, "A", "Z")


def test_non_dict_graph_raises_type_error():
    with pytest.raises(TypeError):
        dijkstra([("A", {})], "A")


def test_non_numeric_weight_raises_type_error():
    with pytest.raises(TypeError):
        dijkstra({"A": {"B": "x"}}, "A")


def test_bool_weight_raises_type_error():
    with pytest.raises(TypeError):
        dijkstra({"A": {"B": True}}, "A")
