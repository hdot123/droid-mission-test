"""fletcher16: Fletcher-16 校验和（本轮新增组件）。

标准 Fletcher-16：对字节序列做模 255 的双累加和，返回
``(sum2 << 8) | sum1`` 形式的 16 位整数。空输入返回 0。
"""

__all__ = ["checksum", "verify"]


def checksum(data: bytes) -> int:
    """计算 ``data`` 的 Fletcher-16 校验和（16 位整数）。

    模 255 双和；空输入返回 0。
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like, got %r" % (type(data),))
    sum1 = 0
    sum2 = 0
    for byte in data:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1


def verify(data: bytes, check: int) -> bool:
    """校验 ``data`` 的 Fletcher-16 是否等于 ``check``。"""
    return checksum(data) == check
