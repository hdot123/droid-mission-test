"""bacon: Bacon 双字母密码（26 字母版）。

字母按 0..25 编成 5 位二进制，a=0、b=1，编码表逐字为：
A=aaaaa B=aaaab C=aaaba D=aaabb E=aabaa F=aabab G=aabba H=aabbb
I=abaaa J=abaab K=ababa L=ababb M=abbaa N=abbab O=abbba P=abbbb
Q=baaaa R=baaab S=baaba T=baabb U=babaa V=babab W=babba X=babbb
Y=bbaaa Z=bbaab

bacon_encode: 每个字母编为一组 5 位 a/b，组间以单个空格分隔；
              大小写不敏感；空串返回空串；含非字母字符抛 ValueError；
              非 str 输入抛 TypeError。
bacon_decode: 空格分隔的 5 位 a/b 组解回大写字母；
              空串返回空串；每组须恰为 5 个 a/b 字符，否则抛 ValueError；
              非 str 输入抛 TypeError。
"""

_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_tables():
    encode = {}
    for index, letter in enumerate(_ALPHA):
        bits = format(index, "05b").translate(str.maketrans("01", "ab"))
        encode[letter] = bits
    decode = {bits: letter for letter, bits in encode.items()}
    return encode, decode


_ENCODE, _DECODE = _build_tables()


def bacon_encode(text):
    """把纯字母文本编成空格分隔的 5 位 a/b 组；见模块文档字符串。"""
    if not isinstance(text, str):
        raise TypeError("text must be str, got %r" % (type(text).__name__,))
    parts = []
    for ch in text:
        upper = ch.upper()
        if upper not in _ENCODE:
            raise ValueError("non-letter character: %r" % (ch,))
        parts.append(_ENCODE[upper])
    return " ".join(parts)


def bacon_decode(code):
    """把空格分隔的 5 位 a/b 组解回大写字母；见模块文档字符串。"""
    if not isinstance(code, str):
        raise TypeError("code must be str, got %r" % (type(code).__name__,))
    if code == "":
        return ""
    letters = []
    for group in code.split(" "):
        if len(group) != 5 or group not in _DECODE:
            raise ValueError("invalid group: %r" % (group,))
        letters.append(_DECODE[group])
    return "".join(letters)
