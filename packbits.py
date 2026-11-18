"""PackBits-style run-length encoding for bytes.

Packet format:
  0 <= h <= 127  : copy the following h + 1 bytes literally
  h == 128       : no-op (skipped on decode, never emitted by encode)
  129 <= h <= 255: repeat the following 1 byte (257 - h) times
"""

MAX_LITERAL = 128
MAX_RUN = 128


def encode(data: bytes) -> bytes:
    """Encode bytes greedily into PackBits-style packets."""
    out = bytearray()
    i = 0
    n = len(data)
    literal = bytearray()

    def flush_literal() -> None:
        if literal:
            out.append(len(literal) - 1)
            out.extend(literal)
            literal.clear()

    while i < n:
        # Length of the run of identical bytes starting at i.
        j = i
        while j < n and data[j] == data[i]:
            j += 1
        run_len = j - i

        if run_len >= 3:
            flush_literal()
            remaining = run_len
            while remaining > 0:
                chunk = min(remaining, MAX_RUN)
                if remaining - chunk == 1:
                    # Never leave a single repeat: split 129 as 127 + 2.
                    chunk -= 1
                out.append(257 - chunk)
                out.append(data[i])
                remaining -= chunk
            i = j
        else:
            literal.extend(data[i : i + run_len])
            if len(literal) >= MAX_LITERAL:
                flush_literal()
            i = j

    flush_literal()
    return bytes(out)


def decode(data: bytes) -> bytes:
    """Decode PackBits-style packets back into the original bytes."""
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        h = data[i]
        i += 1
        if h <= 127:
            count = h + 1
            if i + count > n:
                raise ValueError(
                    "packet header promises more bytes than remain in input"
                )
            out.extend(data[i : i + count])
            i += count
        elif h == 128:
            continue
        else:
            if i >= n:
                raise ValueError(
                    "packet header promises more bytes than remain in input"
                )
            out.extend(bytes([data[i]]) * (257 - h))
            i += 1
    return bytes(out)
