from __future__ import annotations

class AbstractSM2Cipher:
    """Auto-converted from AbstractSM2Cipher.java."""

    def __init__(self, *args, **kwargs):
        pass

    def getR(self, rs):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getS(self, rs):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def combineRS(self, r, s):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def inputBlockSize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def outputBlockSize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def run(self, data, reverse, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setKey(self, key, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getRandom(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def sign(self, m, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def encrty(self, m, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def Dncrty(self, m, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def multiply(self, subKey, r, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def XOR(self, a, b):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcR(self, e, k, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcE(self, m):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getOrder(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMultiplyOrder(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclC1(self, k, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclPB(self, k, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclPBG(self, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def KDF(self, PB, len):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def caclC3(self, PB, m):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def cacldBC1(self, X, Y, d, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
