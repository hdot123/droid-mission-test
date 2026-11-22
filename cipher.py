"""Caesar cipher text shifting.

Dependency-free beyond the Python standard library.

Note: another process creates a root-level ``string.py`` which can shadow the
stdlib ``string`` module when running from the repository root.  We therefore
import the alphabet constants defensively and fall back to loading the real
stdlib ``string`` module by path.
"""

try:
    from string import ascii_lowercase, ascii_uppercase
except ImportError:  # repo-root string.py shadowed the stdlib module
    import importlib.machinery
    import importlib.util
    import os
    import sys
    import sysconfig

    def _load_stdlib_string():
        """Load the real stdlib ``string`` module, bypassing any shadow."""
        # Already-imported stdlib copy (e.g. imported before the shadow).
        cached = sys.modules.get("string")
        if cached is not None and hasattr(cached, "ascii_lowercase"):
            return cached
        stdlib = sysconfig.get_paths().get("stdlib", "")
        for path in (
            os.path.join(stdlib, "string.py"),
            os.path.join(stdlib, "string", "__init__.py"),
        ):
            if os.path.isfile(path):
                spec = importlib.util.spec_from_file_location("_stdlib_string", path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
        # Last resort: ask the import system, skipping paths that shadow
        # ``string`` with a file named string.py.
        clean_path = [
            p
            for p in sys.path
            if not (p and os.path.isfile(os.path.join(p, "string.py")))
        ]
        spec = importlib.machinery.PathFinder.find_spec("string", clean_path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        raise ImportError("cannot locate the standard library string module")

    _mod = _load_stdlib_string()
    ascii_lowercase = _mod.ascii_lowercase
    ascii_uppercase = _mod.ascii_uppercase

__all__ = ["shift_text"]


def shift_text(text, n):
    """Shift every English letter in ``text`` by ``n`` Caesar positions.

    ``n`` may be negative or exceed 26 in magnitude; it is reduced with
    ``n % 26``.  Case is preserved and non-letter characters pass through
    unchanged.
    """
    k = n % 26
    shifted_lower = ascii_lowercase[k:] + ascii_lowercase[:k]
    shifted_upper = ascii_uppercase[k:] + ascii_uppercase[:k]
    table = str.maketrans(
        ascii_lowercase + ascii_uppercase,
        shifted_lower + shifted_upper,
    )
    return text.translate(table)
