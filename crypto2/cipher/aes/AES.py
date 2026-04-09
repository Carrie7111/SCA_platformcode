from __future__ import annotations

class AES:
    """Auto-converted from AES.java."""

    def __init__(self, *args, **kwargs):
        pass

    def toInt(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toString(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def rounds(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createIntermediates(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createLeakages(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getShortName(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def inputBlockSize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def keySize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setKey(self, key, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def shift(self, r, shift):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def FFmulX(self, x):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def mcol(self, x):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def inv_mcol(self, x):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def subWord(self, x):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def generateWorkingKey(self, key):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def invKeySched(self, ints):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def flip(self, i):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def encrypt(self, block, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def decrypt(self, block, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def subByte(self, x, round, col, row, ints):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def invSubByte(self, x, round, col, row, ints):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
