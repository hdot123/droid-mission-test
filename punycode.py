"""punycode: RFC 3492 Bootstring 单标签 Punycode 编解码（第五十五轮并发 D 单组件）。

本模块实现 RFC 3492 的 Bootstring 编解码，作用域为单个标签（label），
**不包含** ``xn--`` 前缀——前缀属于 IDNA 层，不在本组件职责内。

算法参数按 RFC 3492 钉死：底数 base=36、tmin=1、tmax=26、skew=38、
damp=700、初始 bias=72、初始 n=128；bias 适配按 RFC 3492 §3.4
（首次出现时 delta 除以 damp，之后除以 2）。

入参约定：
- 编码与解码函数对非 str 入参抛 TypeError；
- 解码输入含非 ASCII 字符、非法数字字符或输入截断抛 ValueError。
"""

_BASE = 36
_TMIN = 1
_TMAX = 26
_SKEW = 38
_DAMP = 700
_INITIAL_BIAS = 72
_INITIAL_N = 128
_DELIMITER = "-"

_BASE_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


def _adapt(delta, numpoints, firsttime):
    """RFC 3492 §3.4 bias 适配。"""
    if firsttime:
        delta = delta // _DAMP
    else:
        delta = delta // 2
    delta += delta // numpoints
    k = 0
    while delta > ((_BASE - _TMIN) * _TMAX) // 2:
        delta //= _BASE - _TMIN
        k += _BASE
    return k + (((_BASE - _TMIN + 1) * delta) // (delta + _SKEW))


def _encode_digit(digit):
    """把 0..35 的数字编码为 ASCII 字符。"""
    if digit < 26:
        return chr(ord("a") + digit)
    return chr(ord("0") + digit - 26)


def _decode_digit(cp):
    """把 ASCII 字符解码为 0..35 的数字，非法字符返回 -1。"""
    if ord("0") <= cp <= ord("9"):
        return cp - ord("0") + 26
    if ord("a") <= cp <= ord("z"):
        return cp - ord("a")
    if ord("A") <= cp <= ord("Z"):
        return cp - ord("A")
    return -1


def puny_encode(text: str) -> str:
    """把单个标签编码为不含 ``xn--`` 前缀的 Punycode 字符串。

    纯 ASCII 输入的编码结果带尾部 ``-``（与 RFC 一致，如 ``"abc"`` → ``"abc-"``）；
    空串编码为 ``""``。非 str 入参抛 TypeError。
    """
    if not isinstance(text, str):
        raise TypeError("expected str, got %r" % type(text).__name__)
    if text == "":
        return ""

    output = []
    input_length = len(text)
    n = _INITIAL_N
    delta = 0
    bias = _INITIAL_BIAS

    # 基本码点（ASCII）原样输出，末尾补分隔符。
    basic_length = 0
    for i, ch in enumerate(text):
        if ord(ch) < 0x80:
            output.append(ch)
            basic_length += 1
    if basic_length:
        output.append(_DELIMITER)
    h = basic_length

    while h < input_length:
        m = 0x7FFFFFFF
        for ch in text:
            cp = ord(ch)
            if m > cp >= n:
                m = cp
        delta += (m - n) * (h + 1)
        n = m
        for ch in text:
            cp = ord(ch)
            if cp < n:
                delta += 1
            if cp == n:
                q = delta
                k = _BASE
                while True:
                    t = _TMIN if k <= bias else _TMAX if k >= bias + _TMAX else k - bias
                    if q < t:
                        break
                    output.append(_encode_digit(t + ((q - t) % (_BASE - t))))
                    q = (q - t) // (_BASE - t)
                    k += _BASE
                output.append(_encode_digit(q))
                bias = _adapt(delta, h + 1, h == basic_length)
                delta = 0
                h += 1
        delta += 1
        n += 1
    return "".join(output)


def puny_decode(code: str) -> str:
    """把不含 ``xn--`` 前缀的 Punycode 字符串解码回原标签。

    非 str 入参抛 TypeError；输入含非 ASCII 字符、非法数字字符
    或输入截断抛 ValueError；空串解码为 ``""``。
    """
    if not isinstance(code, str):
        raise TypeError("expected str, got %r" % type(code).__name__)
    if code == "":
        return ""

    output = []
    # 分隔符出现在最后一个（编码约定里基本部分与扩展部分之间）。
    delimiter_index = code.rfind(_DELIMITER)
    if delimiter_index >= 0:
        basic = code[:delimiter_index]
        extended = code[delimiter_index + 1 :]
        for ch in basic:
            cp = ord(ch)
            if cp >= 0x80:
                raise ValueError("non-ASCII character in basic part: %r" % ch)
            output.append(cp)
    else:
        extended = code

    n = _INITIAL_N
    i = 0
    bias = _INITIAL_BIAS
    index = 0
    extended_length = len(extended)

    while index < extended_length:
        oldi = i
        w = 1
        k = _BASE
        while True:
            if index >= extended_length:
                raise ValueError("truncated punycode input: %r" % code)
            digit = _decode_digit(ord(extended[index]))
            if digit < 0:
                raise ValueError("invalid punycode digit: %r" % extended[index])
            index += 1
            i += digit * w
            t = _TMIN if k <= bias else _TMAX if k >= bias + _TMAX else k - bias
            if digit < t:
                break
            w *= _BASE - t
            k += _BASE
        out_len = len(output) + 1
        bias = _adapt(i - oldi, out_len, oldi == 0)
        n += i // out_len
        i %= out_len
        if n < 0 or n > 0x10FFFF:
            raise ValueError("invalid code point: %r" % n)
        output.insert(i, n)
        i += 1

    return "".join(chr(cp) for cp in output)
