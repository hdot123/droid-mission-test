"""Case-conversion helpers: snake_case and lowerCamelCase.

Standard library only; this module is intentionally standalone and does not
import any sibling project module.
"""

import re

# Boundaries inside camelCase / PascalCase text: between a lowercase-or-digit
# run and an uppercase letter, or between an acronym run and a capitalized
# word ("XMLHttpRequest" -> "XML_Http_Request").
_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_SEPARATOR_RUN = re.compile(r"[\s\-]+")
_UNDERSCORE_RUN = re.compile(r"_+")


def to_snake_case(text):
    """Convert space-, hyphen-, or camelCase-separated text to snake_case.

    Example: to_snake_case("HelloWorld") == "hello_world".
    An empty string returns an empty string.
    """
    if not text:
        return ""
    spaced = _CAMEL_BOUNDARY.sub("_", text)
    separated = _SEPARATOR_RUN.sub("_", spaced)
    return _UNDERSCORE_RUN.sub("_", separated).strip("_").lower()


def to_camel_case(text):
    """Convert space-, hyphen-, or underscore-separated text to lowerCamelCase.

    Example: to_camel_case("hello_world") == "helloWorld".
    An empty string returns an empty string.
    """
    if not text:
        return ""
    parts = [part for part in re.split(r"[\s\-_]+", text) if part]
    if not parts:
        return ""
    head = parts[0].lower()
    tail = "".join(part.capitalize() for part in parts[1:])
    return head + tail
