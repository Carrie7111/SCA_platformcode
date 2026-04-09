from __future__ import annotations

from modules.python.rsa_sm2.sm3_hash import sm3_digest, sm3_hexdigest


class SM3_HASH:
    """Python version of modules/sm2/SM3_HASH.java."""

    @staticmethod
    def getDigestOfBytes(data: bytes) -> bytes:
        return sm3_digest(data)

    @staticmethod
    def getDigestOfString(data: bytes) -> str:
        return sm3_hexdigest(data)

    @staticmethod
    def byteArrayToHexString(data: bytes) -> str:
        return data.hex().upper()

    @staticmethod
    def StringToByte(hex_str: str) -> bytes:
        return bytes.fromhex(hex_str)

