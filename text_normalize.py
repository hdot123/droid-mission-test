"""Text normalization utilities.

Turns messy text into one uniform clean form by tidying case, punctuation,
and whitespace. Standard library only; no CLI, no package directory.
"""

import string

__all__ = [
    "lowercase",
    "strip_punctuation",
    "collapse_whitespace",
    "normalize",
]


def lowercase(text):
    """Return ``text`` converted to lower case.

    Only case is changed; punctuation and whitespace are left untouched.

    >>> lowercase("Hello WORLD")
    'hello world'
    """
    return text.lower()


def strip_punctuation(text):
    """Return ``text`` with every ASCII punctuation character removed.

    ASCII punctuation is every character in ``string.punctuation``
    (``!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~``). Removing a punctuation
    character does not insert a space, so adjacent characters become
    adjacent in the result. Whitespace and case are left untouched.

    >>> strip_punctuation("hi, there!")
    'hi there'
    >>> strip_punctuation("hi,there")
    'hithere'
    """
    return "".join(ch for ch in text if ch not in string.punctuation)


def collapse_whitespace(text):
    """Return ``text`` with runs of whitespace collapsed and edges stripped.

    Any contiguous run of whitespace (spaces, tabs, newlines, etc.) is
    replaced by a single space, and leading/trailing whitespace is
    removed. Case and punctuation are left untouched.

    >>> collapse_whitespace("  a\\t\\n b  ")
    'a b'
    """
    return " ".join(text.split())


def normalize(text):
    """Return ``text`` in one uniform clean form.

    Applies, in order:

    1. lower case (``lowercase``);
    2. every ASCII punctuation character replaced by a single space, so
       words separated only by punctuation stay separated;
    3. whitespace collapsing and edge stripping (``collapse_whitespace``).

    The result is a lower-case, punctuation-free, single-spaced string
    with no leading or trailing whitespace.

    >>> normalize("  Hello,   WORLD!\\n")
    'hello world'
    >>> normalize("one...two")
    'one two'
    """
    step1 = lowercase(text)
    step2 = "".join(ch if ch not in string.punctuation else " " for ch in step1)
    return collapse_whitespace(step2)
