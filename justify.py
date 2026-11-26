"""justify: 文本两端对齐（贪心分行后的空格分配）。

按空白切词、贪心（first-fit）分行；非末行的多词行两端对齐至恰 width：
空格先均分词间间隙，余数自左逐隙 +1；末行单空格连接、不补齐。
本题只做贪心分行后的空格分配，不做最优断行（与 wordwrap 家族不同）。
仅用标准库，不 import 本仓库任何其他模块。
"""


def _check_args(text, width):
    """入参校验：width < 1 抛 ValueError；非 str 文本／非 int（含 bool）宽度抛 TypeError。"""
    if not isinstance(text, str):
        raise TypeError("text must be str, got %r" % (type(text).__name__,))
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be int, got %r" % (type(width).__name__,))
    if width < 1:
        raise ValueError("width must be >= 1, got %r" % (width,))


def _distribute(total_spaces, gaps):
    """把 total_spaces 个空格分到 gaps 个间隙：先均分，余数自左逐隙 +1。"""
    if gaps <= 0:
        return []
    base, rem = divmod(total_spaces, gaps)
    return [base + (1 if i < rem else 0) for i in range(gaps)]


def _join_justified(words, width):
    """把多词行两端对齐到恰 width，返回对齐后的行。"""
    chars = sum(len(w) for w in words)
    gaps = len(words) - 1
    counts = _distribute(width - chars, gaps)
    parts = []
    for i, word in enumerate(words):
        parts.append(word)
        if i < gaps:
            parts.append(" " * counts[i])
    return "".join(parts)


def justify_text(text: str, width: int) -> list[str]:
    """按空白切词、贪心分行并两端对齐。

    - 非末行的多词行：两端对齐至恰 width（空格先均分词间间隙、余数自左逐隙 +1）。
    - 末行：单空格连接、不补齐。
    - 仅一词的行不对齐；超长单词独占一行原样保留。
    - 空/纯空白文本返回 []。
    - width < 1 抛 ValueError；非 str 文本／非 int（含 bool）宽度抛 TypeError。
    """
    _check_args(text, width)

    words = text.split()
    if not words:
        return []

    lines = []          # 已定型的行（词列表）
    current = []
    for word in words:
        if not current:
            current = [word]
            continue
        # 贪心 first-fit：还能塞下就继续放当前行
        if len(" ".join(current)) + 1 + len(word) <= width:
            current.append(word)
        else:
            lines.append(current)
            current = [word]
    if current:
        lines.append(current)

    # 定型行做两端对齐；末行单空格连接
    result = []
    last_index = len(lines) - 1
    for i, line_words in enumerate(lines):
        if i == last_index:
            result.append(" ".join(line_words))
        elif len(line_words) == 1:
            result.append(line_words[0])  # 仅一词的行不对齐
        else:
            result.append(_join_justified(line_words, width))
    return result
