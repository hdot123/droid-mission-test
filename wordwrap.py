"""wordwrap: 贪心按空白折行工具。

规格（第三十八轮 · 并发 D 单）：
按空白切词（连续空白视为一个分隔），贪心逐行填充：每行词间单个空格、
行长不超过 width；单个词长超过 width 时独占一行、原样不截断；
空串或全空白返回空列表；width 小于 1 抛 ValueError。
"""

__all__ = ["wrap"]


def wrap(text: str, width: int) -> list[str]:
    """把 text 按空白切词后贪心折行，返回行列表。"""
    if width < 1:
        raise ValueError("width must be at least 1: %r" % (width,))
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
