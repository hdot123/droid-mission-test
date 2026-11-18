"""tempconv: 温度单位换算工具（第四十轮 · 并发 D 单）。

六个函数负责摄氏（Celsius）、华氏（Fahrenheit）、开尔文（Kelvin）
两两互换，返回值一律 round(x, 2) 保留两位小数。
"""


def c_to_f(c):
    """摄氏转华氏：F = C * 9/5 + 32。"""
    return round(c * 9 / 5 + 32, 2)


def f_to_c(f):
    """华氏转摄氏：C = (F - 32) * 5/9。"""
    return round((f - 32) * 5 / 9, 2)


def c_to_k(c):
    """摄氏转开尔文：K = C + 273.15。"""
    return round(c + 273.15, 2)


def k_to_c(k):
    """开尔文转摄氏：C = K - 273.15。"""
    return round(k - 273.15, 2)


def f_to_k(f):
    """华氏转开尔文：K = (F - 32) * 5/9 + 273.15。"""
    return round((f - 32) * 5 / 9 + 273.15, 2)


def k_to_f(k):
    """开尔文转华氏：F = (K - 273.15) * 9/5 + 32。"""
    return round((k - 273.15) * 9 / 5 + 32, 2)
