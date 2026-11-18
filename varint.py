"""varint: 无符号 LEB128 变长整数编解码。

每个字节低 7 位载荷（小端序），最高位为续位标志：置位表示后随字节。
decode 必须恰好消费全部输入，任何多余或缺失的字节都视为错误。
"""


def encode(n: int) -> bytes:
    """把非负整数 n 编码为无符号 LEB128 字节串；n 为负数抛 ValueError。"""
    if n < 0:
        raise ValueError("cannot encode negative number: %r" % (n,))
    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def decode(data: bytes) -> int:
    """解码无符号 LEB128 字节串；空输入、未终止或有尾随字节抛 ValueError。"""
    if not data:
        raise ValueError("empty input")
    total = 0
    shift = 0
    for index, byte in enumerate(data):
        total |= (byte & 0x7F) << shift
        shift += 7
        if not byte & 0x80:
            if index != len(data) - 1:
                raise ValueError("trailing bytes after terminator")
            return total
    raise ValueError("unterminated varint")
