"""dijkstra: 有向图 Dijkstra 最短路径与路径重建（第五十二轮 并发 B 单）。

图以 dict 表示：键为节点名（str），值为邻接 dict（邻居名 -> 权重）。
边按给定方向为有向边；只作为邻居出现、未作键的节点视为无出边。
权重须为 int/float（bool 拒），非数值抛 TypeError；负权重抛 ValueError；
graph 非 dict、邻接非 dict、节点名非 str 均抛 TypeError。
"""

import math


def _validate_graph(graph):
    """校验并收集图的全部节点；返回 (nodes, adjacency)。"""
    if not isinstance(graph, dict):
        raise TypeError("graph must be a dict")
    nodes = set()
    for node, neighbors in graph.items():
        if not isinstance(node, str):
            raise TypeError("node name must be a str")
        if not isinstance(neighbors, dict):
            raise TypeError("adjacency must be a dict")
        nodes.add(node)
        for neighbor, weight in neighbors.items():
            if not isinstance(neighbor, str):
                raise TypeError("node name must be a str")
            if isinstance(weight, bool) or not isinstance(weight, (int, float)):
                raise TypeError("weight must be int or float")
            if weight < 0:
                raise ValueError("weight must be non-negative")
            nodes.add(neighbor)
    return nodes, graph


def dijkstra(graph, source):
    """返回 (dist, prev)：全部节点的最短距离与可达非源节点的前驱映射。"""
    nodes, adjacency = _validate_graph(graph)
    if source not in nodes:
        raise ValueError("source not in graph: %r" % (source,))

    dist = {node: math.inf for node in nodes}
    dist[source] = 0
    prev = {}
    visited = set()

    while True:
        current = None
        current_dist = math.inf
        for node in nodes:
            if node in visited:
                continue
            if dist[node] < current_dist:
                current_dist = dist[node]
                current = node
        if current is None:
            break
        visited.add(current)
        for neighbor, weight in adjacency.get(current, {}).items():
            candidate = dist[current] + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                prev[neighbor] = current

    return dist, prev


def shortest_path(graph, source, target):
    """返回源到目标的最短路径节点列表（含两端）；不可达返回 []。"""
    nodes, _ = _validate_graph(graph)
    if source not in nodes:
        raise ValueError("source not in graph: %r" % (source,))
    if target not in nodes:
        raise ValueError("target not in graph: %r" % (target,))
    if source == target:
        return [source]

    dist, prev = dijkstra(graph, source)
    if math.isinf(dist[target]):
        return []

    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()
    return path
