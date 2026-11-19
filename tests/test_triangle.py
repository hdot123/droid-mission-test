"""triangle.py 验收测试：分类、海伦面积、内切/外接半径与全部校验分支。"""

import pytest

from triangle import area, circumradius, classify, inradius


# ---- classify: 分类结果 -------------------------------------------------


def test_classify_scalene():
    assert classify(3, 4, 5) == "scalene"


def test_classify_equilateral():
    assert classify(5, 5, 5) == "equilateral"


def test_classify_isosceles_two_orders():
    assert classify(5, 5, 8) == "isosceles"
    assert classify(5, 8, 5) == "isosceles"


# ---- area: 海伦公式 -----------------------------------------------------


def test_area_right_triangle():
    assert area(3, 4, 5) == 6.0


def test_area_equilateral():
    assert abs(area(5, 5, 5) - 10.825317547305483) <= 1e-9


def test_area_isosceles():
    assert area(5, 5, 8) == 12.0


# ---- inradius / circumradius --------------------------------------------


def test_inradius_right_triangle():
    assert inradius(3, 4, 5) == 1.0


def test_circumradius_right_triangle():
    assert circumradius(3, 4, 5) == 2.5


def test_inradius_equilateral():
    assert abs(inradius(5, 5, 5) - 1.4433756729740645) <= 1e-9


def test_circumradius_equilateral():
    assert abs(circumradius(5, 5, 5) - 2.886751345948129) <= 1e-9


def test_inradius_isosceles():
    assert abs(inradius(5, 5, 8) - 1.3333333333333333) <= 1e-9


def test_circumradius_isosceles():
    assert abs(circumradius(5, 5, 8) - 4.166666666666667) <= 1e-9


# ---- ValueError: 退化 / 非正 / 违反三角不等式 ----------------------------


def test_classify_degenerate_raises():
    with pytest.raises(ValueError):
        classify(1, 2, 3)


def test_classify_zero_and_negative_raise():
    with pytest.raises(ValueError):
        classify(0, 4, 5)
    with pytest.raises(ValueError):
        classify(-3, 4, 5)


def test_classify_inequality_raises():
    with pytest.raises(ValueError):
        classify(1, 1, 5)


def test_area_degenerate_raises():
    with pytest.raises(ValueError):
        area(1, 2, 3)


def test_metrics_invalid_sides_raise_valueerror():
    for fn in (area, inradius, circumradius):
        with pytest.raises(ValueError):
            fn(0, 4, 5)
        with pytest.raises(ValueError):
            fn(-3, 4, 5)
        with pytest.raises(ValueError):
            fn(1, 2, 3)


# ---- TypeError: 非数值边 -------------------------------------------------


def test_classify_non_numeric_raises():
    with pytest.raises(TypeError):
        classify("3", 4, 5)
    with pytest.raises(TypeError):
        classify(3, 4, None)


def test_classify_bool_rejected():
    with pytest.raises(TypeError):
        classify(True, 4, 5)


def test_metrics_non_numeric_raises_typeerror():
    for fn in (classify, area, inradius, circumradius):
        with pytest.raises(TypeError):
            fn("3", 4, 5)
        with pytest.raises(TypeError):
            fn(3, 4, None)
