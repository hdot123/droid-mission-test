import pytest

from braille import from_braille, to_braille

# 点位表逐条钉死自工单（点位 1–6，码点 = 0x2800 + Σ 2^(点位 − 1)）。
DOTS = {
    "a": (1,),
    "b": (1, 2),
    "c": (1, 4),
    "d": (1, 4, 5),
    "e": (1, 5),
    "f": (1, 2, 4),
    "g": (1, 2, 4, 5),
    "h": (1, 2, 5),
    "i": (2, 4),
    "j": (2, 4, 5),
    "k": (1, 3),
    "l": (1, 2, 3),
    "m": (1, 3, 4),
    "n": (1, 3, 4, 5),
    "o": (1, 3, 5),
    "p": (1, 2, 3, 4),
    "q": (1, 2, 3, 4, 5),
    "r": (1, 2, 3, 5),
    "s": (2, 3, 4),
    "t": (2, 3, 4, 5),
    "u": (1, 3, 6),
    "v": (1, 2, 3, 6),
    "w": (2, 4, 5, 6),
    "x": (1, 3, 4, 6),
    "y": (1, 3, 4, 5, 6),
    "z": (1, 3, 5, 6),
}


def test_to_braille_single_a():
    assert to_braille("a") == "⠁"  # U+2801


def test_to_braille_hello():
    assert to_braille("hello") == "⠓⠑⠇⠇⠕"


def test_to_braille_braille():
    assert to_braille("braille") == "⠃⠗⠁⠊⠇⠇⠑"


def test_to_braille_abc_xyz():
    assert to_braille("abc xyz") == "⠁⠃⠉⠀⠭⠽⠵"


def test_to_braille_empty():
    assert to_braille("") == ""


def test_from_braille_hello():
    assert from_braille("⠓⠑⠇⠇⠕") == "hello"


def test_from_braille_roundtrip_phrase():
    phrase = "the quick brown fox"
    assert from_braille(to_braille(phrase)) == phrase


def test_each_letter_roundtrip_and_dot_formula():
    assert len(DOTS) == 26
    for letter in sorted(DOTS):
        braille = to_braille(letter)
        assert from_braille(braille) == letter
        assert ord(braille) == 0x2800 + sum(1 << (dot - 1) for dot in DOTS[letter])


def test_to_braille_rejects_non_lowercase():
    with pytest.raises(ValueError):
        to_braille("Hello")
    with pytest.raises(ValueError):
        to_braille("abc1")


def test_from_braille_rejects_uncovered_patterns():
    with pytest.raises(ValueError):
        from_braille("⠿")  # U+283F，表外盲文图案
    with pytest.raises(ValueError):
        from_braille("ab")  # 普通拉丁字母


def test_type_errors():
    with pytest.raises(TypeError):
        to_braille(None)
    with pytest.raises(TypeError):
        from_braille(5)


def test_from_braille_empty():
    assert from_braille("") == ""


def test_space_roundtrip_via_blank_cell():
    assert to_braille(" ") == "⠀"  # U+2800
    assert from_braille("⠀") == " "
