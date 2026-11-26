"""asciitable: ASCII 表格渲染（第五十七轮新增组件）。

本模块只做输出方向的渲染（与 csv 家族的输入解析方向相反），
只用标准库，不依赖仓库内其他轮次的模块。

渲染口径（钉死）：
- 边框行 "+---+" 式：每列贡献 "+" + "-" * (列宽 + 2)，列间以 "+" 相连；
- 单元格左右各填充一个空格（"| a |"）；
- 列宽 = 该列表头与全部该列单元格的最长者（表头与单元格参与同一宽度计算）；
- 全部左对齐；
- 表头下有一条分隔边框行，数据行之间**没有**分隔行，末尾以边框行收尾；
- 行以 "\\n" 连接，结果**无尾随换行**；
- rows 可为空（只渲染表头段）；
- 总行数恒为 len(rows) + 4（上边框、表头、分隔边框、数据行、收尾边框）。

入参校验：
- headers 为空抛 ValueError；
- 行长度与表头列数不符抛 ValueError；
- 表头/单元格非 str 抛 TypeError；
- headers/rows 非列表形态（含 headers 为 str）抛 TypeError。
"""

__all__ = ["render_table"]


def _check_str(value, what):
    if not isinstance(value, str):
        raise TypeError("%s must be str, got %r" % (what, type(value).__name__))


def _check_str_sequence(value, what):
    if not isinstance(value, list):
        raise TypeError("%s must be a list, got %r" % (what, type(value).__name__))
    for item in value:
        _check_str(item, what)


def render_table(headers, rows) -> str:
    """按钉死口径渲染 ASCII 表格，行以 "\\n" 连接、无尾随换行。

    headers 必须是非空 list[str]；rows 必须是 list，其每个元素是
    与表头等长的 list[str]。空 rows 只渲染表头段（总行数 4）。
    """
    if not isinstance(headers, list):
        raise TypeError("headers must be a list, got %r" % type(headers).__name__)
    if not headers:
        raise ValueError("headers must not be empty")
    _check_str_sequence(headers, "header")
    if not isinstance(rows, list):
        raise TypeError("rows must be a list, got %r" % type(rows).__name__)

    ncols = len(headers)
    for index, row in enumerate(rows):
        if not isinstance(row, list):
            raise TypeError(
                "row %d must be a list, got %r" % (index, type(row).__name__)
            )
        if len(row) != ncols:
            raise ValueError(
                "row %d has %d cells, expected %d"
                % (index, len(row), ncols)
            )
        _check_str_sequence(row, "cell")

    # 列宽：表头与全部单元格一起取最长。
    widths = [len(h) for h in headers]
    for row in rows:
        for col, cell in enumerate(row):
            if len(cell) > widths[col]:
                widths[col] = len(cell)

    def border():
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(values):
        return (
            "| "
            + " | ".join(v.ljust(w) for v, w in zip(values, widths))
            + " |"
        )

    out = [border(), line(headers), border()]
    for row in rows:
        out.append(line(row))
    out.append(border())
    return "\n".join(out)
