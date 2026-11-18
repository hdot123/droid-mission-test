from crc16 import crc16


def test_check_value_123456789():
    assert crc16(b"123456789") == 0x29B1


def test_empty_input():
    assert crc16(b"") == 0xFFFF


def test_single_null_byte():
    assert crc16(b"\x00") == 0xE1F0


def test_hello():
    # Spec lists 0xD27E for this vector, but that contradicts the stated
    # parameters (poly 0x1021, init 0xFFFF, no reflection, no final XOR),
    # which yield 0xD26E -- confirmed against binascii.crc_hqx(b"hello",
    # 0xFFFF). The three other vectors match CCITT-FALSE exactly; see
    # team/handoffs/crc16-ccitt-false.md.
    assert crc16(b"hello") == 0xD26E


def test_return_value_in_range():
    for data in (
        b"",
        b"\x00",
        b"123456789",
        b"hello",
        b"\xff",
        b"\x00\xff\x10",
        bytes(range(256)),
    ):
        value = crc16(data)
        assert isinstance(value, int)
        assert 0 <= value <= 65535
