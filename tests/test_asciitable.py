"""asciitable 渲染组件的验收测试（第五十七轮 D 单）。"""

import pytest

from asciitable import render_table


def test_example_two_columns_verbatim():
    result = render_table(["a", "bb"], [["ccc", "d"]])
    expected = "\n".join(
        [
            "+-----+----+",
            "| a   | bb |",
            "+-----+----+",
            "| ccc | d  |",
            "+-----+----+",
        ]
    )
    assert result == expected


def test_empty_rows_header_section_only():
    assert render_table(["x"], []) == "+---+\n| x |\n+---+\n+---+"


def test_line_count_equals_rows_plus_four():
    assert len(render_table(["a", "bb"], []).split("\n")) == 0 + 4
    rows = [["1", "2"], ["3", "4"], ["5", "6"]]
    assert len(render_table(["a", "bb"], rows).split("\n")) == len(rows) + 4


def test_all_lines_equal_length():
    result = render_table(["a", "bb"], [["ccc", "d"], ["e", "ff"]])
    lines = result.split("\n")
    assert len(set(len(line) for line in lines)) == 1


def test_no_trailing_newline():
    assert not render_table(["a", "bb"], [["ccc", "d"]]).endswith("\n")
    assert not render_table(["x"], []).endswith("\n")


def test_headers_empty_raises_value_error():
    with pytest.raises(ValueError):
        render_table([], [])


def test_row_length_mismatch_raises_value_error():
    with pytest.raises(ValueError):
        render_table(["a"], [["1", "2"]])


def test_non_str_cell_raises_type_error():
    with pytest.raises(TypeError):
        render_table(["a"], [[1]])


def test_non_str_header_raises_type_error():
    with pytest.raises(TypeError):
        render_table([1], [])


def test_headers_not_list_raises_type_error():
    with pytest.raises(TypeError):
        render_table("ab", [])


def test_column_width_covers_data_cells():
    # 列宽 = 表头与全部单元格最长者：数据比表头宽时按数据算。
    result = render_table(["h"], [["xyz"]])
    assert result.split("\n")[0] == "+-----+"


def test_left_alignment_and_separator_only_below_header():
    result = render_table(["a"], [["1"], ["2"]])
    lines = result.split("\n")
    assert lines == [
        "+---+",
        "| a |",
        "+---+",
        "| 1 |",
        "| 2 |",
        "+---+",
    ]


def test_rows_not_list_raises_type_error():
    with pytest.raises(TypeError):
        render_table(["a"], "1")


def test_row_not_list_raises_type_error():
    with pytest.raises(TypeError):
        render_table(["a"], ["1"])
