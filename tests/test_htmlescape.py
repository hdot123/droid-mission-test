"""tests/test_htmlescape: htmlescape.py 的验收测试（第五十六轮 B 单）。

实体字面量全部用 chr(38) 拼接构造，避免测试源码里出现连续实体文本。
"""

import pytest

from htmlescape import escape_html, unescape_html

A = chr(38)  # & 符号
S = chr(39)  # 单引号
D = chr(34)  # 双引号

# 五命名实体
AMP = A + "amp;"
LT = A + "lt;"
GT = A + "gt;"
QUOT = A + "quot;"
APOS = A + "apos;"

# 数字实体
HASH39 = A + "#39;"
HASHX27 = A + "#x27;"
HASH65 = A + "#65;"
HASHX42 = A + "#x42;"
HASHX43 = A + "#X43;"

# escape 的输出形态
ESC_LT = A + "lt;"  # escape 后的 <
ESC_GT = A + "gt;"
ESC_AMP = A + "amp;"
ESC_QUOT = A + "quot;"
ESC_X27 = A + "#x27;"


def test_escape_empty_and_plain():
    assert escape_html("") == ""
    assert escape_html("plain") == "plain"


def test_escape_full_tag_sample():
    got = escape_html('<a href="x">&' + S)
    expected = (
        A
        + "lt;a href="
        + A
        + "quot;x"
        + A
        + "quot;"
        + A
        + "gt;"
        + A
        + "amp;"
        + A
        + "#x27;"
    )
    assert got == expected


def test_escape_reescapes_existing_entity_text():
    # 输入里已有的实体文本会被再转义（& 先于其余替换生效）
    assert escape_html(LT) == ESC_AMP + "lt;"


def test_unescape_named_entities():
    assert unescape_html(LT + "a" + GT) == "<a>"
    # 已被转义的实体再解一次得到 < 文本
    assert unescape_html(ESC_AMP + "lt;") == LT
    assert unescape_html(APOS) == S
    # escape 写出的十六进制写法也须认
    assert unescape_html(HASHX27) == S
    # 十进制 39 写法也须认
    assert unescape_html(HASH39) == S


def test_unescape_numeric_entities():
    assert unescape_html(HASH65 + HASHX42 + HASHX43) == "ABC"


def test_unescape_unknown_and_unterminated_kept_verbatim():
    assert unescape_html(A + "unknown;") == A + "unknown;"
    assert unescape_html(A + "amp") == A + "amp"


def test_unescape_invalid_codepoints_kept_verbatim():
    # 代理区
    assert unescape_html(A + "#xD800;") == A + "#xD800;"
    # 超范围码点
    assert unescape_html(A + "#999999999;") == A + "#999999999;"


def test_unescape_no_entities():
    assert unescape_html("no entities") == "no entities"


def test_round_trip_sample_set():
    samples = [
        "<p class='a'>Tom & Jerry</p>",
        "5 > 3 & 2 < 4",
        "café <b>naïve</b>",
    ]
    for s in samples:
        assert unescape_html(escape_html(s)) == s


def test_type_errors():
    with pytest.raises(TypeError):
        escape_html(1)
    with pytest.raises(TypeError):
        unescape_html(None)
