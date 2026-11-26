import random

import pytest

from rectunion import union_area


def test_empty_returns_zero():
    assert union_area([]) == 0


def test_single_rectangle():
    assert union_area([(0, 0, 2, 2)]) == 4
    # 列表形态矩形同样接受
    assert union_area([[0, 0, 2, 2]]) == 4


def test_disjoint_rectangles():
    assert union_area([(0, 0, 1, 1), (2, 2, 3, 3)]) == 2


def test_partial_overlap():
    assert union_area([(0, 0, 2, 2), (1, 1, 3, 3)]) == 7


def test_containment():
    assert union_area([(0, 0, 4, 4), (1, 1, 2, 2)]) == 16


def test_edge_contact_no_overlap():
    assert union_area([(0, 0, 1, 1), (1, 0, 2, 1)]) == 2


def test_mixed_three_rectangles():
    # 3 + 2 + 9 = 14
    assert union_area([(0, 0, 3, 1), (0, 1, 1, 3), (2, 2, 5, 5)]) == 14


def test_float_coordinates_single():
    assert union_area([(0, 0, 1.5, 1.5)]) == 2.25


def test_float_coordinates_overlap():
    # 5 + 3 - 1 = 7.0
    assert union_area([(0.0, 0.0, 2.5, 2.0), (1.5, 1.0, 3.0, 3.0)]) == 7.0


def test_return_type_int_vs_float():
    assert isinstance(union_area([(0, 0, 1, 1)]), int)
    assert isinstance(union_area([(0.0, 0.0, 1.0, 1.0)]), float)


def _raster_count(rects):
    """单位格栅格化计数：被任一矩形覆盖的单位格数。"""
    covered = set()
    for x1, y1, x2, y2 in rects:
        for x in range(x1, x2):
            for y in range(y1, y2):
                covered.add((x, y))
    return len(covered)


def test_property_matches_grid_rasterization():
    # 任意整数坐标矩形组（坐标 0..7、边长 1..4、每组 1–5 个）与栅格化一致
    rng = random.Random(20261126)
    for _ in range(300):
        n = rng.randint(1, 5)
        rects = []
        for _ in range(n):
            x1 = rng.randint(0, 7)
            y1 = rng.randint(0, 7)
            side_x = rng.randint(1, 4)
            side_y = rng.randint(1, 4)
            rects.append((x1, y1, x1 + side_x, y1 + side_y))
        assert union_area(rects) == _raster_count(rects)
    # 变体：全部坐标都落在 0..7 内
    for _ in range(300):
        n = rng.randint(1, 5)
        rects = []
        for _ in range(n):
            side_x = rng.randint(1, 4)
            side_y = rng.randint(1, 4)
            x1 = rng.randint(0, 7 - side_x)
            y1 = rng.randint(0, 7 - side_y)
            rects.append((x1, y1, x1 + side_x, y1 + side_y))
        assert union_area(rects) == _raster_count(rects)


def test_degenerate_rectangles_raise_value_error():
    # x1 == x2
    with pytest.raises(ValueError):
        union_area([(0, 0, 0, 1)])
    # x1 > x2
    with pytest.raises(ValueError):
        union_area([(2, 2, 1, 3)])
    # y1 == y2
    with pytest.raises(ValueError):
        union_area([(0, 3, 1, 3)])


def test_bad_types_raise_type_error():
    # 非数值坐标
    with pytest.raises(TypeError):
        union_area([("a", 0, 1, 1)])
    # bool 不算数值坐标
    with pytest.raises(TypeError):
        union_area([(True, 0, 1, 1)])
    # 矩形不是长度 4 的序列
    with pytest.raises(TypeError):
        union_area([(0, 0, 1)])
    # 容器不是列表形态
    with pytest.raises(TypeError):
        union_area("nope")
    # 元素不是序列
    with pytest.raises(TypeError):
        union_area([5])


def test_non_list_container_raises_type_error():
    with pytest.raises(TypeError):
        union_area(((0, 0, 1, 1),))
    with pytest.raises(TypeError):
        union_area({"a": 1})
