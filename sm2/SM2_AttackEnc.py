from __future__ import annotations

import math
from typing import Optional

from modules.python.rsa_sm2.sm2 import SM2_STD
from modules.python.rsa_sm2.sm2_attack import recover_plaintext_from_guess


class SM2_AttackEnc:
    """Python version of modules/sm2/SM2_AttackEnc.java (core helpers)."""

    @staticmethod
    def computeCorrelation(x: list[float], y: list[float], n: float) -> float:
        m = int(n)
        sx = sum(x[:m])
        sy = sum(y[:m])
        sx2 = sum(v * v for v in x[:m])
        sy2 = sum(v * v for v in y[:m])
        sxy = sum(a * b for a, b in zip(x[:m], y[:m]))
        varx = sx2 - sx * sx / n
        vary = sy2 - sy * sy / n
        if varx == 0 or vary == 0:
            return 0.0
        return abs((sxy - sx * sy / n) / math.sqrt(varx * vary))

    @staticmethod
    def GetM(cipher_hex: str, guessed_k_hex: str) -> Optional[str]:
        # Java attack module validates guessed ephemeral key against ciphertext.
        return recover_plaintext_from_guess(SM2_STD, cipher_hex, guessed_k_hex)

