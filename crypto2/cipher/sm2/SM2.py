from __future__ import annotations

class SM2:
    """Auto-converted from SM2.java."""

    def __init__(self, *args, **kwargs):
        pass

    def init(self, ecCurve, generator, order, multOrder):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createLeakages(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createIntermediates(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMultiplyOrder(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def keySize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setKey(self, key, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getShortName(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toString(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getOrder(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toLong(self, ba, offset, length):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcR(self, e, k, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcE(self, m):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calculateMessage(self, ID, message, a, b, Gx, Gy, Qx, Qy):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def AddStringnum(self, str):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclC1(self, k, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclPB(self, k, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def KDF(self, PB, len):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclC3(self, PB, m):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def KDFcalc(self, message, klen):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclPBG(self, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def cacldBC1(self, X, Y, d, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
