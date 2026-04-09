from __future__ import annotations

class AbstractBlockCipher:
    """Auto-converted from AbstractBlockCipher.java."""

    def __init__(self, *args, **kwargs):
        pass

    def run(self, data, reverse, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def rounds(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def encrypt(self, plain, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def decrypt(self, cipher, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setMode(self, mode):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMode(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def isEncrypt(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def outputBlockSize(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
