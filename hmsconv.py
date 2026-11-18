"""秒与时分秒互转。

split_seconds 把非负整数秒拆成 (时, 分, 秒)，分与秒均小于 60，时数不封顶；
join_seconds 是其逆运算，任一输入为负或分、秒不小于 60 均抛 ValueError。
"""


def split_seconds(total: int) -> tuple[int, int, int]:
    """把非负整数秒拆为 (时, 分, 秒)；负数抛 ValueError。"""
    if not isinstance(total, int) or isinstance(total, bool):
        raise ValueError("total must be a non-negative int: %r" % (total,))
    if total < 0:
        raise ValueError("total must be non-negative: %r" % (total,))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return h, m, s


def join_seconds(h: int, m: int, s: int) -> int:
    """把 (时, 分, 秒) 合并为总秒数；任一为负或 m、s >= 60 抛 ValueError。"""
    for name, value in (("h", h), ("m", m), ("s", s)):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("%s must be an int: %r" % (name, value))
        if value < 0:
            raise ValueError("%s must be non-negative: %r" % (name, value))
    if m >= 60 or s >= 60:
        raise ValueError("minutes and seconds must be < 60: %r" % ((h, m, s),))
    return h * 3600 + m * 60 + s
