"""tests/test_papersize.py: ISO 216 A 系列纸张尺寸验收测试。"""

import pytest

import papersize

# ISO 216 标准表：n -> (短边, 长边)，mm
_ISO_TABLE = {
    0: (841, 1189),
    1: (594, 841),
    2: (420, 594),
    3: (297, 420),
    4: (210, 297),
    5: (148, 210),
    6: (105, 148),
    7: (74, 105),
    8: (52, 74),
    9: (37, 52),
    10: (26, 37),
}


def test_paper_size_matches_iso_table_each_n():
    for n, dims in _ISO_TABLE.items():
        assert papersize.paper_size(n) == dims, n


def test_paper_size_halving_rule_generates_series():
    # 尺寸必须由对半规则生成（长边 // 2 为新短边、旧短边为新长边），不查表。
    short, long = 841, 1189
    for n in range(11):
        assert papersize.paper_size(n) == (short, long)
        short, long = long // 2, short


def test_paper_area_zero():
    assert papersize.paper_area(0) == 999949


def test_paper_area_equals_product_of_sides_every_n():
    for n in range(11):
        size = papersize.paper_size(n)
        assert papersize.paper_area(n) == size[0] * size[1], n


@pytest.mark.parametrize("n", [-1, 11])
def test_paper_size_out_of_range_raises_value_error(n):
    with pytest.raises(ValueError):
        papersize.paper_size(n)


@pytest.mark.parametrize("n", [4.0, "4", True])
def test_paper_size_non_int_raises_type_error(n):
    with pytest.raises(TypeError):
        papersize.paper_size(n)


@pytest.mark.parametrize("n", [-1, 11])
def test_paper_area_out_of_range_raises_value_error(n):
    with pytest.raises(ValueError):
        papersize.paper_area(n)


@pytest.mark.parametrize("n", [4.0, "4", True])
def test_paper_area_non_int_raises_type_error(n):
    with pytest.raises(TypeError):
        papersize.paper_area(n)
