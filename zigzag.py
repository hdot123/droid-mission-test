"""zigzag: ZigZag varint 编解码（Protocol Buffers 式）。

先把任意整数做 ZigZag 映射（非负 → 2n，负 → -2n-1，等价于
`(n << 1) ^ (n >> 63)`），再以小端 7 位组 varint 编码：低组在前，
除末字节外各字节高位置 1。
"""


def encode(n: int) -> bytes:
    """把整数 n 按 ZigZag + 小端 varint 编码为字节串。"""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be int: %r" % (n,))
    z = 2 * n if n >= 0 else -2 * n - 1
    if z < 0:
        raise ValueError("cannot zigzag-encode negative value: %r" % (n,))
    out = bytearray()
    while True:
        b = z & 0x7F
        z >>= 7
        if z:
            out.append(b | 0x80)
        else:
            out.append(b)
            break
    return bytes(out)


def decode(data: bytes) -> int:
    """把 ZigZag varint 字节串解码回整数；空串或未终止的 varint 抛 ValueError。"""
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like: %r" % (data,))
    data = bytes(data)
    if not data:
        raise ValueError("empty varint input")
    z = 0
    shift = 0
    for i, b in enumerate(data):
        z |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            if i != len(data) - 1:
                raise ValueError("trailing bytes after varint: %r" % (data,))
            return (z >> 1) ^ -(z & 1)
    raise ValueError("unterminated varint: %r" % (data,))
