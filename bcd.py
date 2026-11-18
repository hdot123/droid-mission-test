"""bcd: 压缩 BCD 编解码工具。

把非负整数的每一位十进制数字压进一个十六进制 nibble，
例如 123 -> 0x123。encode 与 decode 互逆；
负数或非法 nibble（大于 9）一律抛 ValueError。
"""


def encode(n: int) -> int:
    """把非负整数编码为压缩 BCD；n 为负数抛 ValueError。"""
    if n < 0:
        raise ValueError("negative number: %r" % (n,))
    result = 0
    place = 1
    while True:
        digit = n % 10
        result += digit * place
        n //= 10
        if n == 0:
            return result
        place <<= 4


def decode(b: int) -> int:
    """把压缩 BCD 解码为整数；b 为负数或任一 nibble 大于 9 抛 ValueError。"""
    if b < 0:
        raise ValueError("negative BCD value: %r" % (b,))
    result = 0
    multiplier = 1
    while True:
        nibble = b & 0xF
        if nibble > 9:
            raise ValueError("invalid BCD nibble: %r" % (nibble,))
        result += nibble * multiplier
        b >>= 4
        if b == 0:
            return result
        multiplier *= 10
