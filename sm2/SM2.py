from __future__ import annotations

from typing import Optional, Tuple

from modules.python.rsa_sm2.sm2 import SM2_STD, calc_z, decrypt, encrypt, kdf, sign, verify


class SM2:
    """Python version of modules/sm2/SM2.java (algorithm core)."""

    curve = SM2_STD

    @staticmethod
    def KDF(message_hex: str, klen: int) -> str:
        return kdf(message_hex, klen)

    @staticmethod
    def calculateZ(ID: str, a: str, b: str, Gx: str, Gy: str, Qx: str, Qy: str) -> str:
        # Keep signature compatibility; uses standard curve in current migration.
        return calc_z(ID, SM2_STD, int(Qx, 16), int(Qy, 16))

    @staticmethod
    def Signature(message_after_za_hex: str, d_hex: str, k_hex: str) -> Tuple[int, int]:
        return sign(SM2_STD, int(d_hex, 16), message_after_za_hex, int(k_hex, 16))

    @staticmethod
    def verifySignature(message_after_za_hex: str, qx_hex: str, qy_hex: str, r: int, s: int) -> bool:
        return verify(SM2_STD, (int(qx_hex, 16), int(qy_hex, 16)), message_after_za_hex, r, s)

    @staticmethod
    def Encrypt(message_hex: str, qx_hex: str, qy_hex: str, k_hex: str) -> str:
        return encrypt(SM2_STD, (int(qx_hex, 16), int(qy_hex, 16)), message_hex, int(k_hex, 16))

    @staticmethod
    def Decrypt(cipher_hex: str, d_hex: str) -> Optional[str]:
        return decrypt(SM2_STD, int(d_hex, 16), cipher_hex)

