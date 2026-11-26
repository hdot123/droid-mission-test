"""ngrams: n-gram 切分小组件（纯切分，不计数）。

- ``char_ngrams``：字符滑动窗口切分，每个元素是长度为 n 的子串。
- ``word_ngrams``：按 ``str.split()`` 切词后的词组窗口，每个元素是 tuple。

文本长度（词数）不足 n 返回 ``[]``；n < 1 抛 ``ValueError``；
text 非 str 或 n 非 int（含 bool）抛 ``TypeError``。
"""

__all__ = ["char_ngrams", "word_ngrams"]


def _validate(text, n):
    """校验入参：text 必须是 str、n 必须是非 bool 的 int；n < 1 抛 ValueError。"""
    if not isinstance(text, str):
        raise TypeError("text must be str, got %s" % type(text).__name__)
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %s" % type(n).__name__)
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))


def char_ngrams(text: str, n: int) -> list[str]:
    """返回 text 的字符 n-gram 列表（滑动窗口）。

    长度不足 n 时返回 ``[]``；n < 1 抛 ValueError；
    text 非 str 或 n 非 int（含 bool）抛 TypeError。
    """
    _validate(text, n)
    return [text[i : i + n] for i in range(len(text) - n + 1)]


def word_ngrams(text: str, n: int) -> list[tuple[str, ...]]:
    """返回 text 按 ``str.split()`` 切词后的词 n-gram 列表（元素为 tuple）。

    split 口径吸收连续空白（含制表符）；词数不足 n 时返回 ``[]``；
    n < 1 抛 ValueError；text 非 str 或 n 非 int（含 bool）抛 TypeError。
    """
    _validate(text, n)
    words = text.split()
    return [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]
