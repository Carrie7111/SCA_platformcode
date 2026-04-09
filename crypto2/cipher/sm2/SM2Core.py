from __future__ import annotations

class SM2Core:
    """Auto-converted from SM2Core.java."""

    def __init__(self, *args, **kwargs):
        pass

    def SM2init(self, pcurve, gx, gy, acurve, bcurve, ncurve, dprivate, krandom, Da, Db, flag):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def InitKeyChange(self, pcurve, gx, gy, acurve, bcurve, ncurve, Da, Db, krandom, flag):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def AddStringnum(self, str):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def AddZERO(self, str):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calculateMessage(self, ID, message, a, b, Gx, Gy, Qx, Qy):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def Signature(self, Message):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def RandomSignature(self, Message):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def verifySignature(self, byte_arrMessage, r, s):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def KDF(self, message, klen):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def Encrypt(self, message):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def Decrypt(self, message):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def calculateZ(self, ID, a, b, Gx, Gy, Qx, Qy):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def KeyChangeA(self, IDA):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def KeyChangeB(self, IDB):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def SM2INIT(self, C1X, C1Y, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def main(self, arg_arr):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
