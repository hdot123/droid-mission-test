"""第五十七轮 motzkin.py 验收测试：锚列逐 n 比对＋入参约定。"""

import pytest

from motzkin import motzkin


# 锚列（验收逐 n 比对，不以 Catalan 求和捷径代替）。
ANCHORS = [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 4),
    (4, 9),
    (5, 21),
    (6, 51),
    (7, 127),
    (8, 323),
    (9, 835),
    (10, 2188),
    (15, 310572),
]


@pytest.mark.parametrize("n,expected", ANCHORS)
def test_motzkin_anchor_values(n, expected):
    result = motzkin(n)
    assert result == expected
    assert type(result) is int


def test_motzkin_15_is_exact_int():
    result = motzkin(15)
    assert result == 310572
    assert type(result) is int


def test_motzkin_zero_is_one():
    assert motzkin(0) == 1


def test_motzkin_negative_raises_value_error():
    with pytest.raises(ValueError):
        motzkin(-1)


def test_motzkin_float_raises_type_error():
    with pytest.raises(TypeError):
        motzkin(2.0)


def test_motzkin_bool_raises_type_error():
    with pytest.raises(TypeError):
        motzkin(True)
