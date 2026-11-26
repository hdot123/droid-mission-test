"""papersize: ISO 216 A 系列纸张尺寸（短边, 长边），单位 mm。

由 A0 = 841 x 1189 逐级按「长边对半取 floor、新短边 = 半分长边、
新长边 = 旧短边」生成，与 ISO 216 标准表一致；不逐档查表。
"""


def _check_n(n):
    """入参约定：非 int（含 bool）抛 TypeError；n 越界（< 0 或 > 10）抛 ValueError。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got %r" % (n,))
    if n < 0 or n > 10:
        raise ValueError("out of range: %r" % (n,))


def paper_size(n: int) -> tuple[int, int]:
    """返回 A<n> 的 (短边, 长边)（mm），n ∈ 0..10，由对半规则逐级生成。"""
    _check_n(n)
    short, long = 841, 1189
    for _ in range(n):
        short, long = long // 2, short
    return (short, long)


def paper_area(n: int) -> int:
    """返回 A<n> 的面积 mm²（同入参约定）。"""
    short, long = paper_size(n)
    return short * long
