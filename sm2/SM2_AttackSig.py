from __future__ import annotations

import math
from typing import Optional

from modules.python.rsa_sm2.sm2 import SM2_STD
from modules.python.rsa_sm2.sm2_attack import recover_private_key_from_sig_k


class SM2_AttackSig:
    """Python version of modules/sm2/SM2_AttackSig.java (core helpers)."""

    @staticmethod
    def computeCorrelationf(x: list[float], y: list[float], n: float) -> float:
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
    def caldA(randomk_bin: str, message_hex: str, r_hex: str, s_hex: str) -> Optional[str]:
        return recover_private_key_from_sig_k(SM2_STD, message_hex, r_hex, s_hex, randomk_bin)

