import random

import pytest

from uuencode import uudecode, uuencode


def _ref_uuencode(data: bytes) -> str:
    """独立参照实现：按 24 位整数提取（int.from_bytes）逐行编码。"""
    lines = []
    for start in range(0, len(data), 45):
        chunk = data[start:start + 45]
        chars = [chr(len(chunk) + 32)]
        for i in range(0, len(chunk), 3):
            group = int.from_bytes(chunk[i:i + 3].ljust(3, b"\x00"), "big")
            for shift in (18, 12, 6, 0):
                value = (group >> shift) & 0x3F
                chars.append("`" if value == 0 else chr(value + 32))
        lines.append("".join(chars))
    lines.append("`")
    return "\n".join(lines)


def test_uuencode_cat():
    assert uuencode(b"Cat") == "#0V%T\n`"


def test_uuencode_empty():
    assert uuencode(b"") == "`"


def test_uuencode_all_zeros_are_backticks():
    assert uuencode(b"\x00\x00\x00") == "#````\n`"
    # 编码侧零值必须写反引号，绝不能写空格
    assert " " not in uuencode(b"\x00" * 45)


def test_uudecode_known_vectors():
    assert uudecode(uuencode(b"Cat")) == b"Cat"
    assert uudecode("`") == b""
    assert uudecode("#0V%T\n`") == b"Cat"


def test_uuencode_46_bytes_three_lines_first_is_m():
    text = uuencode(b"A" * 46)
    lines = text.split("\n")
    assert len(lines) == 3  # 45 字节行 + 1 字节行 + 收尾行
    assert lines[0][0] == "M"  # 45 + 32 == 77 == "M"
    assert lines[2] == "`"


def test_uudecode_tolerates_space_as_zero():
    assert uudecode("#    \n`") == b"\x00\x00\x00"


def test_property_roundtrip_and_reference():
    rng = random.Random(580058)
    for n in range(0, 101):
        for _ in range(3):
            data = bytes(rng.getrandbits(8) for _ in range(n))
            encoded = uuencode(data)
            assert encoded == _ref_uuencode(data)
            assert uudecode(encoded) == data


def test_uuencode_type_errors():
    with pytest.raises(TypeError):
        uuencode("Cat")
    with pytest.raises(TypeError):
        uuencode(bytearray(b"Cat"))


def test_uudecode_type_error_on_bytes():
    with pytest.raises(TypeError):
        uudecode(uuencode(b"Cat").encode("ascii"))


def test_uudecode_value_errors():
    for bad in (
        "",                                  # 空文本
        "#0V%T",                             # 缺收尾行
        "#0V%\n`",                           # 正文长度与长度字符不合
        "#0V%T\n`\n",                        # 尾随换行（含空行）
        "#0V%T\n\n`",                        # 正文含空行
        "`\n#0V%T\n`",                       # 收尾行不在末行
        "#0V%T\n`\n#0V%T",                   # 收尾行不在末行
    ):
        with pytest.raises(ValueError):
            uudecode(bad)
