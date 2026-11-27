"""code39: Code 39 校验字符（mod 43）。

字符集钉死为 43 个字符，字符值即其在字符集中的下标：
数字 0-9 为 0-9、大写字母 A-Z 为 10-35、``-`` ``.`` 空格 ``$`` ``/`` ``+`` ``%``
依次为 36-42。
"""

CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%"
_VALUE = {ch: i for i, ch in enumerate(CHARSET)}
_MOD = 43


def code39_checksum(text):
    """返回 text 的 Code 39 校验字符（各字符值之和 mod 43）。

    text 必须是 str（非 str 抛 TypeError），非空且全部字符都在字符集内
    （否则抛 ValueError）。
    """
    if not isinstance(text, str):
        raise TypeError("text must be str, got %r" % (type(text).__name__,))
    if text == "":
        raise ValueError("text must be non-empty")
    total = 0
    for ch in text:
        value = _VALUE.get(ch)
        if value is None:
            raise ValueError("character not in Code 39 charset: %r" % (ch,))
        total += value
    return CHARSET[total % _MOD]


def code39_encode(text):
    """返回带起止 ``*`` 与校验字符的完整 Code 39 符号：``*text<checksum>*``。

    校验与异常行为同 code39_checksum。
    """
    checksum = code39_checksum(text)
    return "*" + text + checksum + "*"


def code39_verify(symbol):
    """校验完整 Code 39 符号，返回 bool；除非 str 抛 TypeError 外不抛异常。

    当且仅当 symbol 以 ``*`` 起、以 ``*`` 止、总长 >= 4、内部字符全在
    字符集内、且内部末字符等于其余内部部分的校验字符时返回 True。
    """
    if not isinstance(symbol, str):
        raise TypeError("symbol must be str, got %r" % (type(symbol).__name__,))
    if len(symbol) < 4 or symbol[0] != "*" or symbol[-1] != "*":
        return False
    inner = symbol[1:-1]
    try:
        expected = code39_checksum(inner[:-1])
    except ValueError:
        return False
    return inner[-1] == expected
