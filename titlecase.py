"""titlecase: 标题式大小写转换（第五十五轮并发 C 单 · R51 题池）。

规则钉死（与验收规格逐字对应）：
- 空白归一化：任意空白串折叠为单空格并去首尾（按空白切词）；空串返回 ""。
- 每词首字母大写、其余字母小写；「首字母」指词内首个字母字符，前导符号保留原样。
- 小词表中的词，非首词非尾词时全小写；位于首位或末位时仍按普通词大写。
- 连字符复合词逐段处理：首段恒大写、后续段若为小词仍小写。
- 缩略词不保留全大写（NASA -> Nasa）。
- 非 str 入参抛 TypeError。
"""

_SMALL_WORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "nor",
        "for",
        "so",
        "yet",
        "at",
        "by",
        "in",
        "into",
        "of",
        "off",
        "on",
        "onto",
        "per",
        "to",
        "up",
        "via",
        "as",
    }
)


def _alpha_core(token):
    """词的字母核：去掉非字母字符后的小写形式，用于小词判定。"""
    return "".join(ch for ch in token if ch.isalpha()).lower()


def _capitalize(token):
    """词内首个字母字符大写，其余字母小写；非字母字符原样保留。"""
    out = []
    first_seen = False
    for ch in token:
        if ch.isalpha():
            if first_seen:
                out.append(ch.lower())
            else:
                out.append(ch.upper())
                first_seen = True
        else:
            out.append(ch)
    return "".join(out)


def _lowercase(token):
    """词内所有字母小写，非字母字符原样保留。"""
    return "".join(ch.lower() if ch.isalpha() else ch for ch in token)


def _title_word(word, position, count):
    """对单个空白切出的词做标题化（含连字符分段规则）。"""
    segments = word.split("-")
    out = []
    for index, segment in enumerate(segments):
        if index == 0:
            # 首段恒大写。
            out.append(_capitalize(segment))
        elif _alpha_core(segment) in _SMALL_WORDS:
            # 后续段若为小词仍小写。
            out.append(_lowercase(segment))
        else:
            out.append(_capitalize(segment))
    # 整词级小词规则：非首词非尾词时全小写（按词内全部字母）。
    if position != 0 and position != count - 1 and _alpha_core(word) in _SMALL_WORDS:
        return _lowercase(word)
    return "-".join(out)


def title_case(text):
    """标题式大小写转换；非 str 抛 TypeError。"""
    if not isinstance(text, str):
        raise TypeError("title_case() expected str, got %r" % type(text).__name__)
    words = text.split()
    if not words:
        return ""
    count = len(words)
    return " ".join(
        _title_word(word, index, count) for index, word in enumerate(words)
    )
