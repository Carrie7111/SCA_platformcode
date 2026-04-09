from __future__ import annotations

import math


class SM2AttackSigDefault:
    """Python version of template/SM2AttackSigDefault.java."""

    @staticmethod
    def computeCorrelation(x: list[float], y: list[float], n: float) -> float:
        m = int(n)
        sumx = 0.0
        sumxx = 0.0
        sumy = 0.0
        sumyy = 0.0
        sumxy = 0.0
        for i in range(m):
            sumx += x[i]
            sumxx += x[i] * x[i]
            sumy += y[i]
            sumyy += y[i] * y[i]
            sumxy += x[i] * y[i]
        varx = sumxx - sumx * sumx / n
        vary = sumyy - sumy * sumy / n
        if varx == 0 or vary == 0:
            return 0.0
        return (sumxy - sumx * sumy / n) / math.sqrt(varx * vary)

