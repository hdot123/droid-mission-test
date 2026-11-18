"""kelvin: 温标换算（摄氏、开尔文、华氏）小组件（第四十三轮 D）。"""


def c_to_k(c: float) -> float:
    """摄氏度转开尔文：c + 273.15。"""
    return c + 273.15


def k_to_c(k: float) -> float:
    """开尔文转摄氏度：k - 273.15；k 小于 0 抛 ValueError。"""
    if k < 0:
        raise ValueError("kelvin cannot be negative: %r" % (k,))
    return k - 273.15


def c_to_f(c: float) -> float:
    """摄氏度转华氏度：c * 9/5 + 32。"""
    return c * 9 / 5 + 32


def f_to_c(f: float) -> float:
    """华氏度转摄氏度：(f - 32) * 5/9。"""
    return (f - 32) * 5 / 9
