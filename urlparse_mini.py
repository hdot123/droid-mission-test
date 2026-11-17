"""Minimal parser for simple http/https URLs.

Splits a URL into scheme, host, port, path and query.  Userinfo and
fragments are not supported.
"""

_DEFAULT_PORTS = {"http": 80, "https": 443}
_SUPPORTED_SCHEMES = frozenset(_DEFAULT_PORTS)


def parse(url):
    """Parse a simple http/https URL into a dict.

    Returns a dict with keys ``scheme``, ``host``, ``port``, ``path`` and
    ``query``.  The port defaults to 80 for http and 443 for https unless an
    explicit port is given.  The path defaults to ``"/"`` and the query is the
    raw query string without the leading ``"?"`` (empty string when absent).

    Raises ``ValueError`` for userinfo ("@"), fragments ("#"), unsupported
    schemes, an empty host, or a malformed port.
    """
    if "@" in url or "#" in url:
        raise ValueError("userinfo and fragments are not supported: %r" % (url,))
    if "://" not in url:
        raise ValueError("invalid URL (missing scheme): %r" % (url,))

    scheme, rest = url.split("://", 1)
    scheme = scheme.lower()
    if scheme not in _SUPPORTED_SCHEMES:
        raise ValueError("unsupported scheme: %r" % (scheme,))

    if "?" in rest:
        authority_and_path, query = rest.split("?", 1)
    else:
        authority_and_path, query = rest, ""

    if "/" in authority_and_path:
        authority, path_part = authority_and_path.split("/", 1)
        path = "/" + path_part
    else:
        authority, path = authority_and_path, ""

    if not authority:
        raise ValueError("empty host: %r" % (url,))

    if ":" in authority:
        host, _, port_str = authority.rpartition(":")
        if not host or not port_str.isdigit():
            raise ValueError("invalid port in URL: %r" % (url,))
        port = int(port_str)
    else:
        host, port = authority, _DEFAULT_PORTS[scheme]

    if not path:
        path = "/"

    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query": query,
    }
