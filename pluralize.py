"""pluralize: 英文名词复数规则小组件。"""

_UNCOUNTABLE = {"sheep", "fish", "deer", "species", "series", "aircraft"}

_IRREGULAR = {
    "child": "children",
    "person": "people",
    "man": "men",
    "woman": "women",
    "mouse": "mice",
    "goose": "geese",
    "tooth": "teeth",
    "foot": "feet",
    "ox": "oxen",
    "die": "dice",
    "quiz": "quizzes",
}

_F_FE = {"leaf", "life", "knife", "wife", "wolf", "loaf", "thief", "shelf", "half", "calf"}

_O_ES = {"hero", "potato", "tomato", "echo", "torpedo", "veto"}

_VOWELS = set("aeiou")


def pluralize(word):
    """按钉死顺序套用英文名词复数规则，返回复数形式。"""
    if not isinstance(word, str):
        raise TypeError("word must be str, got %r" % type(word).__name__)
    if not word:
        raise ValueError("word must be non-empty")
    if any(ch < "a" or ch > "z" for ch in word):
        raise ValueError("word must contain only lowercase a-z: %r" % (word,))

    if word in _UNCOUNTABLE:
        return word
    if word in _IRREGULAR:
        return _IRREGULAR[word]
    if word in _F_FE:
        if word.endswith("fe"):
            return word[:-2] + "ves"
        return word[:-1] + "ves"
    if word in _O_ES:
        return word + "es"
    if (
        len(word) >= 2
        and word.endswith("y")
        and word[-2] not in _VOWELS
    ):
        return word[:-1] + "ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    return word + "s"
