"""Tests for packbits."""

import packbits


# --- encode examples -------------------------------------------------------

def test_encode_empty():
    assert packbits.encode(b"") == b""


def test_encode_literal():
    assert packbits.encode(b"abc") == bytes([2, 97, 98, 99])


def test_encode_run():
    assert packbits.encode(b"aaaa") == bytes([253, 97])


def test_encode_literal_then_run():
    assert packbits.encode(b"abaaaa") == bytes([1, 97, 98, 253, 97])


def test_encode_run_of_two_is_literal():
    assert packbits.encode(b"aab") == bytes([2, 97, 97, 98])


# --- decode examples -------------------------------------------------------

def test_decode_repeat_packet():
    assert packbits.decode(bytes([254, 65])) == b"AAA"


def test_decode_noop_then_literal():
    assert packbits.decode(bytes([128, 0, 65])) == b"A"


def test_decode_literal_packet():
    assert packbits.decode(bytes([2, 97, 98, 99])) == b"abc"


# --- h == 128 no-op --------------------------------------------------------

def test_decode_noop_is_skipped_anywhere():
    assert packbits.decode(bytes([128, 128, 0, 65])) == b"A"
    assert packbits.decode(bytes([0, 65, 128])) == b"A"
    assert packbits.decode(bytes([128])) == b""


def _packet_headers(encoded: bytes):
    """Return the list of header bytes in an encoded stream."""
    headers = []
    i = 0
    n = len(encoded)
    while i < n:
        h = encoded[i]
        headers.append(h)
        i += 1
        if h <= 127:
            i += h + 1
        elif h >= 129:
            i += 1
        # h == 128 consumes no following bytes
    return headers


def test_encode_never_emits_noop_header():
    for data in (
        b"",
        b"abc",
        b"aaaa",
        b"abaaaa",
        b"aab",
        b"\x00" * 300,
        bytes(range(256)) * 3,
        b"aaabbbcccddd",
    ):
        encoded = packbits.encode(data)
        assert 128 not in _packet_headers(encoded)


# --- packet caps -----------------------------------------------------------

def test_literal_packet_capped_at_128_bytes():
    # A long run of identical bytes is split, but runs of length < 3
    # accumulate into literal packets of at most 128 bytes.
    data = bytes(range(256))  # all distinct, no runs of >= 3
    encoded = packbits.encode(data)
    # First packet: literal of 128 bytes -> header 127.
    assert encoded[0] == 127
    assert encoded[1:129] == data[:128]
    # Second packet: literal of the remaining 128 bytes.
    assert encoded[129] == 127
    assert encoded[130:258] == data[128:]
    assert len(encoded) == 258
    assert packbits.decode(encoded) == data

    # 129 distinct bytes must split into 128 + 1.
    data129 = bytes(range(129))
    encoded129 = packbits.encode(data129)
    assert encoded129[0] == 127
    assert encoded129[129] == 0  # single literal byte
    assert packbits.decode(encoded129) == data129


def test_repeat_packet_capped_at_128_repeats():
    # 200 identical bytes: 128 repeats in the first packet, 72 in the second.
    data = b"z" * 200
    encoded = packbits.encode(data)
    # 257 - 128 = 129 header for 128 repeats; 257 - 72 = 185 header for 72.
    assert encoded == bytes([129, ord("z"), 185, ord("z")])
    assert packbits.decode(encoded) == data

    # Exactly 128 repeats fits in one packet (header 129).
    data128 = b"z" * 128
    encoded128 = packbits.encode(data128)
    assert encoded128 == bytes([129, ord("z")])
    assert packbits.decode(encoded128) == data128


# --- decode errors ---------------------------------------------------------

def test_decode_raises_when_literal_promises_too_many_bytes():
    # Header 2 promises 3 literal bytes but only 1 remains.
    try:
        packbits.decode(bytes([2, 97]))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for truncated literal packet")


def test_decode_raises_when_repeat_packet_is_truncated():
    # Repeat packet with no byte following the header.
    try:
        packbits.decode(bytes([253]))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for truncated repeat packet")


# --- round-trips -----------------------------------------------------------

def test_roundtrip_various_inputs():
    samples = [
        b"",
        b"a",
        b"ab",
        b"abc",
        b"aaaa",
        b"abaaaa",
        b"aab",
        b"aaabbbcccddd",
        b"a" * 128,
        b"a" * 129,
        b"a" * 200,
        b"a" * 256,
        bytes(range(256)),
        bytes(range(256)) * 3,
        b"hello, world! hello, world!",
        b"\x00" * 3 + b"\x01" * 3 + b"\x02" * 400,
        bytes([i % 7 for i in range(500)]),
    ]
    for data in samples:
        assert packbits.decode(packbits.encode(data)) == data


def test_roundtrip_randomish_data():
    # Deterministic pseudo-random data with runs and literals mixed.
    data = bytearray()
    seed = 12345
    for _ in range(60):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        if seed % 3 == 0:
            run_len = (seed % 150) + 1
            data.extend(bytes([seed % 256]) * run_len)
        else:
            lit_len = (seed % 200) + 1
            for k in range(lit_len):
                data.append((seed + k) % 256)
    data = bytes(data)
    assert packbits.decode(packbits.encode(data)) == data
