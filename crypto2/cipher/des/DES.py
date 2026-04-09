from __future__ import annotations

class DES:
    """Auto-converted from DES.java."""

    def __init__(self, *args, **kwargs):
        pass

    def inputBlockSize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def keySize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def rounds(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getType(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createLeakages(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createIntermediates(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setKey(self, key, intermediate):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def splitKeys(self, key):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getShortName(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def encrypt(self, plain, intermediate):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def doDES(self, input, roundSchedule, decrypt, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def decrypt(self, cipher, intermediate):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def f(self, halfData, round, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcRoundKey(self, key, round):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcInverseRoundKey(self, roundKey, round):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def invPermute(self, in_arg, mat_arr):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
