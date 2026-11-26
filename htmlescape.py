"""htmlescape: HTML 转义与反转义工具（第五十六轮 B 单新增件）。

escape_html 做五种字符的逐字替换（& 最先替换，输入里已有的实体文本会被再转义）；
unescape_html 解五命名实体（amp、lt、gt、quot、apos）与十进制／十六进制数字实体，
未知实体、无分号结尾、代理区（U+D800–U+DFFF）与超范围码点一律原样保留。

注意 escape 与 unescape 不完全对称：escape 把单引号写成十六进制数字实体 27，
unescape 须同时认三种单引号写法：命名 apos、十进制 39、十六进制 27。

实现只用标准库，不 import 仓库内其他模块。
"""

import re

# 实体字面量分段拼接，避免源码里出现连续的 amp 类实体文本被误读。
_AMP = "&" + "amp;"
_LT = "&" + "lt;"
_GT = "&" + "gt;"
_QUOT = "&" + "quot;"
_HASH_X27 = "&" + "#x27;"

_NAMED_ENTITIES = {
    "amp": "&",
    "lt": "<",
    "gt": ">",
    "quot": '"',
    "apos": "'",
}

# & 后接数字实体（十进制或 x/X 前缀十六进制）或字母命名实体，且以分号结尾。
_ENTITY_RE = re.compile("&(" + "#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z]+" + ");")

_MAX_CODEPOINT = 0x10FFFF
_SURROGATE_START = 0xD800
_SURROGATE_END = 0xDFFF


def _require_str(text):
    if not isinstance(text, str):
        raise TypeError("expected str, got %s" % type(text).__name__)


def _decode_match(match):
    """把正则命中的一个实体还原成字符；不合法则原样返回该实体文本。"""
    token = match.group(0)
    body = match.group(1)
    if body.startswith("#"):
        digits = body[1:]
        if digits[:1] in ("x", "X"):
            base = 16
            digits = digits[1:]
        else:
            base = 10
        try:
            value = int(digits, base)
        except ValueError:  # 位数过多等异常输入，原样保留
            return token
        if value > _MAX_CODEPOINT or _SURROGATE_START <= value <= _SURROGATE_END:
            return token
        return chr(value)
    return _NAMED_ENTITIES.get(body, token)


def escape_html(text: str) -> str:
    """把 &、<、>、双引号、单引号逐字转义；& 先替换，已有实体文本会被再转义。

    非 str 入参抛 TypeError。
    """
    _require_str(text)
    return (
        text.replace("&", _AMP)
        .replace("<", _LT)
        .replace(">", _GT)
        .replace('"', _QUOT)
        .replace("'", _HASH_X27)
    )


def unescape_html(text: str) -> str:
    """还原五命名实体与十进制／十六进制数字实体；其余输入原样保留。

    未知实体、无分号结尾、代理区（U+D800–U+DFFF）与超范围码点一律不改写。
    非 str 入参抛 TypeError。
    """
    _require_str(text)
    return _ENTITY_RE.sub(_decode_match, text)
