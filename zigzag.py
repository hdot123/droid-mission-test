"""zigzag: ZigZag 有符号整数与无符号整数互映射。

把有符号整数交错映射为非负整数：非负数取偶数、负数取奇数，
使得数值小的数（无论正负）映射到较小的无符号值，
常见于 varint 编码前的有符号整数预处理。
"""


def encode(n: int) -> int:
    """把有符号整数 n 映射为无符号整数。

    规则：n >= 0 时结果为 2n；n < 0 时结果为 -2n - 1。
    即 0→0、-1→1、1→2、-2→3、2→4（负数在前交错）。
    """
    if n >= 0:
        return n * 2
    return -n * 2 - 1


def decode(u: int) -> int:
    """encode 的逆运算：把无符号整数映射回有符号整数。

    u 为偶数时结果为 u // 2；u 为奇数时结果为 -(u + 1) // 2。
    u 为负数抛 ValueError。
    """
    if u < 0:
        raise ValueError("u must be non-negative: %r" % (u,))
    if u % 2 == 0:
        return u // 2
    return -(u + 1) // 2
