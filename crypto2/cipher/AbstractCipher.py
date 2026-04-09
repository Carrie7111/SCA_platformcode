from __future__ import annotations

class AbstractCipher:
    """Auto-converted from AbstractCipher.java."""

    def __init__(self, *args, **kwargs):
        pass

    def runAttack(self, data, reverse, target, powerIntermediates, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def verify(self, input, output, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toString(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getFullName(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def keyBytes(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
