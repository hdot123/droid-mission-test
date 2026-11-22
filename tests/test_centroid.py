"""centroid 验收要点测试（第五十二轮并发 A 单，逐条对应规格）。"""

import pytest

from centroid import polygon_area, polygon_centroid


# --- 正方形（逆时针） -------------------------------------------------------


def test_centroid_ccw_square():
    assert polygon_centroid([(0, 0), (2, 0), (2, 2), (0, 2)]) == (1.0, 1.0)


def test_area_ccw_square():
    assert polygon_area([(0, 0), (2, 0), (2, 2), (0, 2)]) == 4.0


# --- 正方形（顺时针）：面积取负、重心一致 -----------------------------------


def test_area_cw_square():
    assert polygon_area([(0, 0), (0, 2), (2, 2), (2, 0)]) == -4.0


def test_centroid_cw_square():
    assert polygon_centroid([(0, 0), (0, 2), (2, 2), (2, 0)]) == (1.0, 1.0)


# --- 三角形 -----------------------------------------------------------------


def test_centroid_triangle():
    assert polygon_centroid([(0, 0), (3, 0), (0, 3)]) == (1.0, 1.0)


def test_area_triangle():
    assert polygon_area([(0, 0), (3, 0), (0, 3)]) == 4.5


# --- 长方形 -----------------------------------------------------------------


def test_centroid_rectangle():
    assert polygon_centroid([(0, 0), (4, 0), (4, 2), (0, 2)]) == (2.0, 1.0)


def test_area_rectangle():
    assert polygon_area([(0, 0), (4, 0), (4, 2), (0, 2)]) == 8.0


# --- L 形 -------------------------------------------------------------------


def test_area_l_shape():
    assert polygon_area([(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)]) == 5.0


def test_centroid_l_shape_within_1e9():
    cx, cy = polygon_centroid([(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)])
    assert abs(cx - 1.1) < 1e-9
    assert abs(cy - 1.1) < 1e-9


# --- 房屋形 -----------------------------------------------------------------


def test_area_house():
    assert polygon_area([(0, 0), (4, 0), (4, 3), (2, 5), (0, 3)]) == 16.0


def test_centroid_house_within_1e9():
    cx, cy = polygon_centroid([(0, 0), (4, 0), (4, 3), (2, 5), (0, 3)])
    assert abs(cx - 2.0) < 1e-9
    assert abs(cy - 2.0416666666666665) < 1e-9


# --- 退化（共线） -----------------------------------------------------------


def test_area_collinear_returns_zero():
    assert polygon_area([(0, 0), (1, 1), (2, 2)]) == 0.0


# --- ValueError 验收要点 ---------------------------------------------------


def test_centroid_collinear_raises_value_error():
    with pytest.raises(ValueError):
        polygon_centroid([(0, 0), (1, 1), (2, 2)])


def test_centroid_two_vertices_raises_value_error():
    with pytest.raises(ValueError):
        polygon_centroid([(0, 0), (1, 1)])


def test_area_one_vertex_raises_value_error():
    with pytest.raises(ValueError):
        polygon_area([(0, 0)])


# --- TypeError 验收要点 -----------------------------------------------------


def test_centroid_non_container_raises_type_error():
    with pytest.raises(TypeError):
        polygon_centroid("abc")


def test_centroid_non_numeric_coord_raises_type_error():
    with pytest.raises(TypeError):
        polygon_centroid([(0, 0), (1, "x"), (2, 2)])


def test_centroid_non_pair_vertex_raises_type_error():
    with pytest.raises(TypeError):
        polygon_centroid([(0, 0), (1, 1), (2,)])


def test_centroid_bool_coord_raises_type_error():
    with pytest.raises(TypeError):
        polygon_centroid([(0, 0), (True, 1), (2, 2)])


# --- 补充：容器形态与 polygon_area 的类型校验 ------------------------------


def test_tuple_container_accepted():
    assert polygon_area(((0, 0), (2, 0), (2, 2), (0, 2))) == 4.0
    assert polygon_centroid(((0, 0), (2, 0), (2, 2), (0, 2))) == (1.0, 1.0)


def test_area_non_container_raises_type_error():
    with pytest.raises(TypeError):
        polygon_area("abc")
    with pytest.raises(TypeError):
        polygon_area(123)


def test_area_bad_vertex_raises_type_error():
    with pytest.raises(TypeError):
        polygon_area([(0, 0), (1, "x"), (2, 2)])
    with pytest.raises(TypeError):
        polygon_area([(0, 0), (1, 1), (2,)])
    with pytest.raises(TypeError):
        polygon_area([(0, 0), (False, 1), (2, 2)])
