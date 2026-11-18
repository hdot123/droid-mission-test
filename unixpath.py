"""POSIX path lexical normalization, implemented from scratch.

No filesystem access and no posixpath/os.path usage: everything below is
pure string processing, so the module is safe to use anywhere.
"""


def normalize(path: str) -> str:
    """Normalize *path* lexically, aligned with posixpath.normpath.

    Rules:
    - collapse consecutive ``/`` separators;
    - drop ``.`` segments;
    - ``..`` cancels the previous segment; for absolute paths this stops at
      the root, for relative paths un-cancellable leading ``..`` are kept;
    - drop the trailing ``/`` (except for the root ``/`` itself);
    - the empty string normalizes to ``"."``.
    """
    if path == "":
        return "."

    is_absolute = path.startswith("/")

    segments = []
    for segment in path.split("/"):
        if segment == "" or segment == ".":
            # Empty string comes from collapsed separators; "." is dropped.
            continue
        if segment == "..":
            if segments and segments[-1] != "..":
                # Cancel the previous (normal or "..") segment.
                segments.pop()
            elif is_absolute:
                # Absolute paths cannot climb above the root.
                continue
            else:
                # Relative paths keep leading ".." that cannot be cancelled.
                segments.append("..")
        else:
            segments.append(segment)

    if is_absolute:
        return "/" + "/".join(segments)
    if not segments:
        return "."
    return "/".join(segments)
