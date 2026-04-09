from __future__ import annotations

class AbstractRSACipher:
    """Auto-converted from AbstractRSACipher.java."""

    def __init__(self, *args, **kwargs):
        pass

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

    def RL(self, m, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toLong(self, ba, offset, length):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def LR(self, m, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMultiplyOrder(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMod(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
