from __future__ import annotations

class DES:
    """Auto-converted from DES.java."""

    def __init__(self, *args, **kwargs):
        pass

    def permute(self, in_arg, mat_arr, insize):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def intPermute(self, in_arg, mat_arr, insize):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def invPermute(self, in_arg, mat_arr, outsize):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def sbox(self, in_arg):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def rotate(self, key, round):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def invRotate(self, key, round):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def f(self, r, k, round):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def des(self, key, data, enc):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def fastF(self, r, k, round):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def fastDes(self, key, data, enc):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def fastDesEncrypt(self, key, data):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def fastDesDecrypt(self, key, data):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def ip(self, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def fp(self, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def pc1(self, d):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def counterToMissingBitsInFirstRoundKey(self, k):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def counterToMissingBitsInLastRoundKey(self, k):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def makeTables(self):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def tdes_mac(self, key, data, icv):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def tdes_ecb(self, key, data, enc):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def tdes24_ecb(self, key, data, enc):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toLong(self, ba):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def toByteArray(self, x):
        raise NotImplementedError("Converted stub: implement Java logic in Python")

    def tdes_cbc(self, key, data, icv, enc):
        raise NotImplementedError("Converted stub: implement Java logic in Python")
