from __future__ import annotations

class FirstOrder:
    """Auto-converted from FirstOrder.java."""

    def __init__(self, *args, **kwargs):
        pass

    def init(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateState(self, t, input, output):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getDerivedSamples(self, t):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateSD(self, hypPower, sample):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateS(self, sample):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateS1(self, data, sample):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateS2(self, data, sample):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateDD(self, data):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateD(self, data):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def updateCorrelationSum(self, t, correlationSum, peakCorrelation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def computeResults(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def computeCorrelation(self, x, xOffset, xStep, y, yOffset, yStep, length):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcInterDataCorrelation(self, dataDeviation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcCrossCorrelation(self, sampleDataCorrelation, interDataCorrelation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcEuclideanSimilarity(self, sampleDataCorrelation, interDataCorrelation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def computeEuclidDist(self, x, xOffset, xStep, y, yOffset, yStep, length):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcDifferential(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcAmplifiedCorrelation(self, dataDeviation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcCorrelation(self, dataDeviation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calcDataDeviation(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def makeCandidateRanking(self, sampleDataCorrelation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def resultTraces(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def get(self, index):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def size(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def attackKeyIndex(self, key):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getNumberOfSamples(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setNumberOfSamples(self, numberOfSamples):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getCrossCorrelationType(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setCrossCorrelationType(self, crossCorrelationType):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def isAmplifiedCorrelation(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setAmplifiedCorrelation(self, amplifiedCorrelation):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getCriterion(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setCriterion(self, criterion):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMethod(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setMethod(self, method):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getxOffset(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def setxOffset(self, xOffset):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getNumberOfAnalyzedTraces(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getSignalsPerKey(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getMaxPower(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def getTargets(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
