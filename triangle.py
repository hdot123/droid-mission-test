"""triangle: 三角形分类与度量（第四十六轮 · B 单）。

只依赖标准库，不 import 本仓库其他模块。所有公开入口共用同一套
校验规则：边必须是 int/float（拒 bool）、必须为正、且满足严格三角
不等式，否则分别抛 TypeError / ValueError。
"""

import math

__all__ = ["classify", "area", "inradius", "circumradius"]


def _validate(a, b, c):
    """校验三边并返回 (a, b, c) 的 float 元组。"""
    for value in (a, b, c):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("sides must be int or float: %r" % (value,))
    a, b, c = float(a), float(b), float(c)
    if not (a > 0 and b > 0 and c > 0):
        raise ValueError("sides must be positive: %r" % ((a, b, c),))
    if not (a + b > c and a + c > b and b + c > a):
        raise ValueError("sides violate strict triangle inequality: %r" % ((a, b, c),))
    return a, b, c


def classify(a, b, c):
    """三边分类：全等边 equilateral、恰两边等 isosceles、互不等 scalene。"""
    a, b, c = _validate(a, b, c)
    if a == b == c:
        return "equilateral"
    if a == b or a == c or b == c:
        return "isosceles"
    return "scalene"


def area(a, b, c):
    """海伦公式面积。"""
    a, b, c = _validate(a, b, c)
    s = (a + b + c) / 2.0
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def inradius(a, b, c):
    """内切圆半径 = 面积 ÷ 半周长。"""
    a, b, c = _validate(a, b, c)
    s = (a + b + c) / 2.0
    return area(a, b, c) / s


def circumradius(a, b, c):
    """外接圆半径 = a×b×c ÷ (4×面积)。"""
    a, b, c = _validate(a, b, c)
    return a * b * c / (4.0 * area(a, b, c))
