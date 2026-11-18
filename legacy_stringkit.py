"""legacy_stringkit: 早期遗留的字符串工具集（存量代码）。

本模块是多年前留下的存量代码，各函数的行为以其文档字符串为准。
仓库基线中附带的测试全部通过，但不代表实现与文档处处一致。
"""


def shout(text):
    """把文本转成全大写，并在末尾加上一个感叹号。"""
    return text.upper() + "!"


def count_vowels(text):
    """统计文本中元音字母（a、e、i、o、u）的数量，大小写都算。"""
    total = 0
    for ch in text:
        if ch in "aeiouAEIOU":
            total += 1
    return total


def _words(text):
    """按空白切分文本并去除首尾空白，返回单词列表（没有单词时为空列表）。"""
    return text.strip().split()


def first_word(text):
    """返回文本的第一个单词（按空白切分）；没有单词时返回空字符串。"""
    parts = _words(text)
    if not parts:
        return ""
    return parts[0]


def last_word(text):
    """返回文本的最后一个单词（按空白切分）；没有单词时返回空字符串。"""
    parts = _words(text)
    if not parts:
        return ""
    return parts[-1]


def initials(text):
    """返回文本中每个单词首字母的大写拼接；没有单词时返回空字符串。"""
    return "".join(word[0].upper() for word in _words(text))
