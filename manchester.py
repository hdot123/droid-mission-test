"""manchester: IEEE 802.3 曼彻斯特编解码工具。

比特 '1' 编码为 "10"，比特 '0' 编码为 "01"。只接受仅含 '0'/'1'
的比特字符串；解码要求信号长度为偶数且每一对都是 "10" 或 "01"，
否则抛 ValueError。
"""

_ENCODE_MAP = {"0": "01", "1": "10"}
_DECODE_MAP = {"10": "1", "01": "0"}


def encode(bits):
    """把只含 '0'/'1' 的比特字符串编码为曼彻斯特信号；含其他字符抛 ValueError。"""
    if not isinstance(bits, str):
        raise ValueError("bits must be a str: %r" % (bits,))
    out = []
    for ch in bits:
        if ch not in _ENCODE_MAP:
            raise ValueError("invalid bit: %r" % (ch,))
        out.append(_ENCODE_MAP[ch])
    return "".join(out)


def decode(signal):
    """把偶数长度的曼彻斯特信号还原为比特串；长度为奇数或非法对时抛 ValueError。"""
    if not isinstance(signal, str):
        raise ValueError("signal must be a str: %r" % (signal,))
    if len(signal) % 2 != 0:
        raise ValueError("odd-length signal: %r" % (signal,))
    out = []
    for i in range(0, len(signal), 2):
        pair = signal[i:i + 2]
        if pair not in _DECODE_MAP:
            raise ValueError("illegal pair at index %d: %r" % (i, pair))
        out.append(_DECODE_MAP[pair])
    return "".join(out)
