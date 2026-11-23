"""flesch: Flesch 易读度小组件（音节计数与阅读易读度）。

标准库实现，不依赖仓库内其他模块。所有行为以验收规格为准：
音节计数启发式与 Flesch 公式均逐条钉死，返回原始浮点数、不四舍五入。
"""

_VOWELS = frozenset("aeiouy")
_ASCII_LETTERS = frozenset("abcdefghijklmnopqrstuvwxyz")
_SENTENCE_ENDINGS = (".", "!", "?")


def _strip_to_letters(word):
    """取 word 小写后仅保留 a-z 字母（其余字符剔除），返回 w。"""
    return "".join(ch for ch in word.lower() if ch in _ASCII_LETTERS)


def count_syllables(word):
    """按钉死的启发式统计 word 的音节数；word 非 str 抛 TypeError。

    规则：
    1. 小写后仅保留 a-z 字母得 w；w 为空返回 0；
    2. len(w) <= 3 返回 1；
    3. 元音集 = {a, e, i, o, u, y}，groups = 连续元音段的段数；
    4. 若 w 以 'e' 结尾：当以 'le' 结尾且 len(w) > 2 且 w[-3] 非元音时不扣减，
       其余情形 groups -= 1；
    5. 返回 max(groups, 1)。
    """
    if not isinstance(word, str):
        raise TypeError("word must be str, got %r" % (type(word).__name__,))
    w = _strip_to_letters(word)
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    groups = 0
    in_vowel_run = False
    for ch in w:
        if ch in _VOWELS:
            if not in_vowel_run:
                groups += 1
                in_vowel_run = True
        else:
            in_vowel_run = False
    if w.endswith("e"):
        if not (w.endswith("le") and len(w) > 2 and w[-3] not in _VOWELS):
            groups -= 1
    return max(groups, 1)


def flesch_reading_ease(text):
    """计算 text 的 Flesch 阅读易读度；text 非 str 抛 TypeError，无词抛 ValueError。

    词 = 按空白切分后、含至少一个 ASCII 字母的 token；
    句数 = max(1, text 中 '.', '!', '?' 出现总次数)；
    音节总数 = 每个词先剔除非 a-z 字符后按 count_syllables 计得之和；
    公式 = 206.835 - 1.015 * (词数 / 句数) - 84.6 * (音节总数 / 词数)，
    返回原始 float、不四舍五入。
    """
    if not isinstance(text, str):
        raise TypeError("text must be str, got %r" % (type(text).__name__,))
    words = [
        token
        for token in text.split()
        if any(ch.isascii() and ch.isalpha() for ch in token)
    ]
    if not words:
        raise ValueError("no words found in text")
    word_count = len(words)
    sentence_count = max(1, sum(text.count(mark) for mark in _SENTENCE_ENDINGS))
    syllable_total = sum(count_syllables(w) for w in words)
    return (
        206.835
        - 1.015 * (word_count / sentence_count)
        - 84.6 * (syllable_total / word_count)
    )
