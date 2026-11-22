"""String utilities: reverse_words, count_vowels, title_case.

Stdlib-only; independent of the other root modules.

Because this file is intentionally named ``string.py`` at the repository
root, it shadows the standard library module of the same name whenever the
repo root is on ``sys.path`` (e.g. ``python -m pytest``). To stay compatible
with anything doing ``import string`` / ``from string import Template``
(including pytest's own dependencies), the real stdlib ``string`` module is
loaded under an alias and its public names are re-exported here.
"""

import importlib.util
import os
import sysconfig

# The real stdlib ``string`` may be a package (string/__init__.py) or a plain
# module (string.py), depending on the Python build; support both.
_stdlib_pkg = os.path.join(sysconfig.get_paths()["stdlib"], "string")
if os.path.isdir(_stdlib_pkg):
    _stdlib_path = os.path.join(_stdlib_pkg, "__init__.py")
    _search_locations = [_stdlib_pkg]
else:
    _stdlib_path = _stdlib_pkg + ".py"
    _search_locations = None
_spec = importlib.util.spec_from_file_location(
    "_stdlib_string", _stdlib_path, submodule_search_locations=_search_locations
)
_stdlib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_stdlib)

# Re-export every public name of the standard library ``string`` module.
for _name in dir(_stdlib):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_stdlib, _name)
del _name, _stdlib, _spec, _stdlib_path, _stdlib_pkg, _search_locations

VOWELS = "aeiou"


def reverse_words(s):
    """Split on whitespace, reverse word order, join with single spaces.

    Leading/trailing whitespace is ignored.
    """
    return " ".join(s.split()[::-1])


def count_vowels(s):
    """Count occurrences of a, e, i, o, u (case-insensitive)."""
    return sum(1 for ch in s if ch.lower() in VOWELS)


def title_case(s):
    """Capitalize each word's first letter, lowercase the rest, join with spaces."""
    return " ".join(word[:1].upper() + word[1:].lower() for word in s.split())
