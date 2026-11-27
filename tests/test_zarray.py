"""tests/test_zarray.py —— zarray.z_array 验收测试。

覆盖工作单 #953 / 子单 #965 的全部验收要点：
定值样例、随机小字母表串与朴素逐位比较实现逐个一致、非 str 入参抛 TypeError。
只用标准库（pytest 断言、random 固定种子）。
"""

import random

import pytest

from zarray import z_array


def _naive_z(s):
    """朴素逐位比较参考实现（独立于 zarray 模块）。"""
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    for i in range(1, n):
        k = 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        z[i] = k
    return z


def test_empty_string():
    assert z_array("") == []


def test_aaaaa():
    assert z_array("aaaaa") == [0, 4, 3, 2, 1]


def test_abcab():
    assert z_array("abcab") == [0, 0, 0, 2, 0]


def test_aabcaabxaaaz():
    assert z_array("aabcaabxaaaz") == [0, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0]


def test_property_random_small_alphabet_matches_naive():
    rng = random.Random(20261127)
    alphabet = "abc"
    for _ in range(300):
        length = rng.randint(0, 30)
        s = "".join(rng.choice(alphabet) for _ in range(length))
        assert z_array(s) == _naive_z(s), s


def test_bytes_raises_typeerror():
    with pytest.raises(TypeError):
        z_array(b"ab")


def test_none_raises_typeerror():
    with pytest.raises(TypeError):
        z_array(None)
