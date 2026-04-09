from __future__ import annotations

class AbstractLeakages:
    """Auto-converted from AbstractLeakages.java."""

    def __init__(self, *args, **kwargs):
        pass

    def getInputGenerators(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def addLeakageModel(self, name, MapIntermediateValue, keyPower, generator, inout, dependencies):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def clearLeakages(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getAttacks(self, input, output, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def compare(self, o1, o2):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def createLeakageModel(self, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def canAttack(self, lm, input, output):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getSimulation(self, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getKnownKeyPower(self, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getTemplate(self, intermediates):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
