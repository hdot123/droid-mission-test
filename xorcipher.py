"""重复密钥 XOR 加解密（十六进制进出）。

明文与密钥均按 UTF-8 编码为字节，密钥字节循环使用，逐字节异或；
加密输出小写十六进制字符串，解密把十六进制串还原为字节后按 UTF-8 解码。
仅用标准库。
"""

__all__ = ["xor_encrypt_hex", "xor_decrypt_hex"]


def _check_key(key):
    if not isinstance(key, str):
        raise TypeError("key must be str, got %s" % type(key).__name__)
    if key == "":
        raise ValueError("key must not be empty")


def xor_encrypt_hex(plaintext, key):
    """把明文按重复密钥 XOR 加密，返回小写十六进制字符串。

    空密钥抛 ValueError；plaintext 或 key 非 str 抛 TypeError。
    """
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be str, got %s" % type(plaintext).__name__)
    _check_key(key)
    key_bytes = key.encode("utf-8")
    data = plaintext.encode("utf-8")
    out = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))
    return out.hex()


def xor_decrypt_hex(hexstr, key):
    """把十六进制字符串按重复密钥 XOR 解密，返回 UTF-8 解码后的明文。

    空密钥抛 ValueError；hexstr 非 str 抛 TypeError；
    长度为奇数或含非法十六进制字符抛 ValueError。
    """
    if not isinstance(hexstr, str):
        raise TypeError("hexstr must be str, got %s" % type(hexstr).__name__)
    _check_key(key)
    if len(hexstr) % 2 != 0:
        raise ValueError("hex string must have even length: %r" % (hexstr,))
    try:
        data = bytes.fromhex(hexstr)
    except ValueError:
        raise ValueError("invalid hex string: %r" % (hexstr,))
    key_bytes = key.encode("utf-8")
    out = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))
    return out.decode("utf-8")
