class Des:
    IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    S = [
        [0xe, 0x0, 0x4, 0xf, 0xd, 0x7, 0x1, 0x4, 0x2, 0xe, 0xf, 0x2, 0xb, 0xd, 0x8, 0x1, 0x3, 0xa, 0xa, 0x6, 0x6, 0xc, 0xc, 0xb, 0x5, 0x9, 0x9, 0x5, 0x0, 0x3, 0x7, 0x8, 0x4, 0xf, 0x1, 0xc, 0xe, 0x8, 0x8, 0x2, 0xd, 0x4, 0x6, 0x9, 0x2, 0x1, 0xb, 0x7, 0xf, 0x5, 0xc, 0xb, 0x9, 0x3, 0x7, 0xe, 0x3, 0xa, 0xa, 0x0, 0x5, 0x6, 0x0, 0xd],
        [0xf, 0x3, 0x1, 0xd, 0x8, 0x4, 0xe, 0x7, 0x6, 0xf, 0xb, 0x2, 0x3, 0x8, 0x4, 0xe, 0x9, 0xc, 0x7, 0x0, 0x2, 0x1, 0xd, 0xa, 0xc, 0x6, 0x0, 0x9, 0x5, 0xb, 0xa, 0x5, 0x0, 0xd, 0xe, 0x8, 0x7, 0xa, 0xb, 0x1, 0xa, 0x3, 0x4, 0xf, 0xd, 0x4, 0x1, 0x2, 0x5, 0xb, 0x8, 0x6, 0xc, 0x7, 0x6, 0xc, 0x9, 0x0, 0x3, 0x5, 0x2, 0xe, 0xf, 0x9],
        [0xa, 0xd, 0x0, 0x7, 0x9, 0x0, 0xe, 0x9, 0x6, 0x3, 0x3, 0x4, 0xf, 0x6, 0x5, 0xa, 0x1, 0x2, 0xd, 0x8, 0xc, 0x5, 0x7, 0xe, 0xb, 0xc, 0x4, 0xb, 0x2, 0xf, 0x8, 0x1, 0xd, 0x1, 0x6, 0xa, 0x4, 0xd, 0x9, 0x0, 0x8, 0x6, 0xf, 0x9, 0x3, 0x8, 0x0, 0x7, 0xb, 0x4, 0x1, 0xf, 0x2, 0xe, 0xc, 0x3, 0x5, 0xb, 0xa, 0x5, 0xe, 0x2, 0x7, 0xc],
        [0x7, 0xd, 0xd, 0x8, 0xe, 0xb, 0x3, 0x5, 0x0, 0x6, 0x6, 0xf, 0x9, 0x0, 0xa, 0x3, 0x1, 0x4, 0x2, 0x7, 0x8, 0x2, 0x5, 0xc, 0xb, 0x1, 0xc, 0xa, 0x4, 0xe, 0xf, 0x9, 0xa, 0x3, 0x6, 0xf, 0x9, 0x0, 0x0, 0x6, 0xc, 0xa, 0xb, 0x1, 0x7, 0xd, 0xd, 0x8, 0xf, 0x9, 0x1, 0x4, 0x3, 0x5, 0xe, 0xb, 0x5, 0xc, 0x2, 0x7, 0x8, 0x2, 0x4, 0xe],
        [0x2, 0xe, 0xc, 0xb, 0x4, 0x2, 0x1, 0xc, 0x7, 0x4, 0xa, 0x7, 0xb, 0xd, 0x6, 0x1, 0x8, 0x5, 0x5, 0x0, 0x3, 0xf, 0xf, 0xa, 0xd, 0x3, 0x0, 0x9, 0xe, 0x8, 0x9, 0x6, 0x4, 0xb, 0x2, 0x8, 0x1, 0xc, 0xb, 0x7, 0xa, 0x1, 0xd, 0xe, 0x7, 0x2, 0x8, 0xd, 0xf, 0x6, 0x9, 0xf, 0xc, 0x0, 0x5, 0x9, 0x6, 0xa, 0x3, 0x4, 0x0, 0x5, 0xe, 0x3],
        [0xc, 0xa, 0x1, 0xf, 0xa, 0x4, 0xf, 0x2, 0x9, 0x7, 0x2, 0xc, 0x6, 0x9, 0x8, 0x5, 0x0, 0x6, 0xd, 0x1, 0x3, 0xd, 0x4, 0xe, 0xe, 0x0, 0x7, 0xb, 0x5, 0x3, 0xb, 0x8, 0x9, 0x4, 0xe, 0x3, 0xf, 0x2, 0x5, 0xc, 0x2, 0x9, 0x8, 0x5, 0xc, 0xf, 0x3, 0xa, 0x7, 0xb, 0x0, 0xe, 0x4, 0x1, 0xa, 0x7, 0x1, 0x6, 0xd, 0x0, 0xb, 0x8, 0x6, 0xd],
        [0x4, 0xd, 0xb, 0x0, 0x2, 0xb, 0xe, 0x7, 0xf, 0x4, 0x0, 0x9, 0x8, 0x1, 0xd, 0xa, 0x3, 0xe, 0xc, 0x3, 0x9, 0x5, 0x7, 0xc, 0x5, 0x2, 0xa, 0xf, 0x6, 0x8, 0x1, 0x6, 0x1, 0x6, 0x4, 0xb, 0xb, 0xd, 0xd, 0x8, 0xc, 0x1, 0x3, 0x4, 0x7, 0xa, 0xe, 0x7, 0xa, 0x9, 0xf, 0x5, 0x6, 0x0, 0x8, 0xf, 0x0, 0xe, 0x5, 0x2, 0x9, 0x3, 0x2, 0xc],
        [0xd, 0x1, 0x2, 0xf, 0x8, 0xd, 0x4, 0x8, 0x6, 0xa, 0xf, 0x3, 0xb, 0x7, 0x1, 0x4, 0xa, 0xc, 0x9, 0x5, 0x3, 0x6, 0xe, 0xb, 0x5, 0x0, 0x0, 0xe, 0xc, 0x9, 0x7, 0x2, 0x7, 0x2, 0xb, 0x1, 0x4, 0xe, 0x1, 0x7, 0x9, 0x4, 0xc, 0xa, 0xe, 0x8, 0x2, 0xd, 0x0, 0xf, 0x6, 0xc, 0xa, 0x9, 0xd, 0x0, 0xf, 0x3, 0x3, 0x5, 0x5, 0x6, 0x8, 0xb]
    ]
    SP = None
    LSinc = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 0]
    maskTable = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 0x200000, 0x400000, 0x800000, 0x1000000, 0x2000000, 0x4000000, 0x8000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x100000000, 0x200000000, 0x400000000, 0x800000000, 0x1000000000, 0x2000000000, 0x4000000000, 0x8000000000, 0x10000000000, 0x20000000000, 0x40000000000, 0x80000000000, 0x100000000000, 0x200000000000, 0x400000000000, 0x800000000000, 0x1000000000000, 0x2000000000000, 0x4000000000000, 0x8000000000000, 0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000, 0x100000000000000, 0x200000000000000, 0x400000000000000, 0x800000000000000, 0x1000000000000000, 0x2000000000000000, 0x4000000000000000, 0x8000000000000000]

    @classmethod
    def permute(cls, in_val, mat, insize=None):
        if insize is None:
            insize = len(mat)
        result = 0
        i = 0
        while True:
            result = ((result << 1) | ((in_val >> (insize - mat[i])) & 1))
            i += 1
            if not (i < len(mat)):
                break
        return result

    @classmethod
    def intPermute(cls, in_val, mat, insize):
        result = 0
        i = 0
        while True:
            result = ((result << 1) | ((in_val >> (insize - mat[i])) & 1))
            i += 1
            if not (i < len(mat)):
                break
        return result

    @classmethod
    def invPermute(cls, in_val, mat, outsize=None):
        if outsize is None:
            outsize = len(mat)
        result = 0
        i = 0
        temp = in_val
        while True:
            result |= ((temp & 1) << (outsize - mat[len(mat) - 1 - i]))
            temp >>= 1
            i += 1
            if not (i < len(mat)):
                break
        return result

    @classmethod
    def sbox(cls, in_val):
        result = 0
        for i in range(8):
            result = ((result << 4) + cls.S[i][(in_val >> (6 * (7 - i))) & 0x3F])
        return result

    @classmethod
    def rotate(cls, key, round):
        left = key >> 28
        right = key & 0xFFFFFFF
        left = (((left << cls.LSinc[round]) + (left >> (28 - cls.LSinc[round]))) & 0xFFFFFFF)
        right = (((right << cls.LSinc[round]) + (right >> (28 - cls.LSinc[round]))) & 0xFFFFFFF)
        return ((left << 28) + right)

    @classmethod
    def invRotate(cls, key, round):
        left = key >> 28
        right = key & 0xFFFFFFF
        left = (((left >> cls.LSinc[round]) + (left << (28 - cls.LSinc[round]))) & 0xFFFFFFF)
        right = (((right >> cls.LSinc[round]) + (right << (28 - cls.LSinc[round]))) & 0xFFFFFFF)
        return ((left << 28) + right)

    @classmethod
    def rotate_string(cls, key, shifts):
        sb = list(key)
        for i in range(28):
            sb[i] = key[(i - shifts + 28) % 28]
            sb[i + 28] = key[((i - shifts + 28) % 28) + 28]
        return ''.join(sb)

    @classmethod
    def f(cls, r, k, round):
        return cls.permute(cls.sbox(cls.permute(r, cls.E, 32) ^ cls.permute(cls.rotate(k, round), cls.PC2, 56)), cls.P)

    @classmethod
    def des(cls, key, data, enc):
        data = cls.permute(data, cls.IP)
        key = cls.permute(key, cls.PC1, 64)
        L = data >> 32
        R = data & 0xFFFFFFFF
        if enc:
            i = 0
            while i < 16:
                L = cls.f(R & 0xFFFFFFFF, key, i) ^ L
                i += 1
                R = cls.f(L & 0xFFFFFFFF, key, i) ^ R
                i += 1
        else:
            i = 15
            while i >= 0:
                L = cls.f(R & 0xFFFFFFFF, key, i) ^ L
                i -= 1
                R = cls.f(L & 0xFFFFFFFF, key, i) ^ R
                i -= 1
        data = (((R & 0xFFFFFFFF) << 32) + (L & 0xFFFFFFFF))
        data = cls.invPermute(data, cls.IP)
        return data

    @classmethod
    def fastF(cls, r, k, round):
        left = k >> 28
        right = k & 0xFFFFFFF
        left = (((left << cls.LSinc[round]) + (left >> (28 - cls.LSinc[round]))) & 0xFFFFFFF)
        right = (((right << cls.LSinc[round]) + (right >> (28 - cls.LSinc[round]))) & 0xFFFFFFF)
        ki = ((left << 28) + right)
        return (cls.SP[0][(((r << 11) | ((r >> 21) & 0x7C0) | ((r >> 23) & 0x3F)) & 0xFFF) ^ int(((ki & 0x40000000000) >> 31) + ((ki & 0x8000000000) >> 29) + ((ki & 0x200000000000) >> 36) + ((ki & 0x110000000) >> 24) + ((ki & 0xa4000000000000) >> 48) + ((ki & 0x8000000000000) >> 45) + ((ki & 0x20000000000) >> 38) + ((ki & 0x800000000) >> 34) + ((ki & 0x400000000000) >> 46))] |
                cls.SP[1][(((r >> 13) & 0xFC0) | ((r >> 15) & 0x3F)) ^ int(((ki & 0x200000000) >> 22) + ((ki & 0x2000000000) >> 27) + ((ki & 0x110000000000) >> 35) + ((ki & 0x10000000000000) >> 44) + ((ki & 0x40000000) >> 23) + ((ki & 0x1080000000000) >> 42) + ((ki & 0x2000000000000) >> 45) + ((ki & 0x20000000) >> 26) + ((ki & 0x1000000000) >> 34) + ((ki & 0x40000000000000) >> 54))] |
                cls.SP[2][(((r >> 5) & 0xFC0) | ((r >> 7) & 0x3F)) ^ int(((ki & 0x8000) >> 4) + ((ki & 0x10) << 6) + ((ki & 0x2000000) >> 16) + ((ki & 0x80000) >> 11) + ((ki & 0x220) >> 2) + ((ki & 0x2) << 5) + ((ki & 0x4000000) >> 21) + ((ki & 0x10000) >> 12) + ((ki & 0x800) >> 9) + ((ki & 0x800000) >> 22) + ((ki & 0x100) >> 8))] |
                cls.SP[3][(((r << 3) & 0xFC0) | (((r << 1) | (r >> 31)) & 0x3F)) ^ int(((ki & 0x1000) >> 1) + ((ki & 0x88) << 3) + ((ki & 0x20000) >> 8) + ((ki & 0x1) << 8) + ((ki & 0x400000) >> 15) + ((ki & 0x400) >> 5) + ((ki & 0x4000) >> 10) + ((ki & 0x40) >> 3) + ((ki & 0x100000) >> 18) + ((ki & 0x8000000) >> 26) + ((ki & 0x1000000) >> 24))])

    @classmethod
    def fastDes(cls, key, data, enc):
        key = cls.pc1(key)
        data = cls.ip(data)
        if enc:
            data = cls.fastDesEncrypt(key, data)
        else:
            data = cls.fastDesDecrypt(key, data)
        return cls.fp(data)

    @classmethod
    def fastDesEncrypt(cls, key, data):
        l = data >> 32
        r = data & 0xFFFFFFFF
        i = 0
        while i < 16:
            l = (l ^ cls.fastF(r, key, i)) & 0xFFFFFFFF
            i += 1
            r = (r ^ cls.fastF(l, key, i)) & 0xFFFFFFFF
            i += 1
        return (((r & 0xFFFFFFFF) << 32) + (l & 0xFFFFFFFF))

    @classmethod
    def fastDesDecrypt(cls, key, data):
        l = data >> 32
        r = data & 0xFFFFFFFF
        i = 15
        while i >= 0:
            l = (l ^ cls.fastF(r, key, i)) & 0xFFFFFFFF
            i -= 1
            r = (r ^ cls.fastF(l, key, i)) & 0xFFFFFFFF
            i -= 1
        return (((r & 0xFFFFFFFF) << 32) + (l & 0xFFFFFFFF))

    @classmethod
    def ip(cls, d):
        return ((d & 0x40) << 57) + ((d & 0x4000) << 48) + ((d & 0x400001) << 39) + ((d & 0x40000100) << 30) + ((d & 0x4000010000) << 21) + ((d & 0x400001000008) << 12) + ((d & 0x40000100000800) << 3) + ((d & 0x4000010000080000) >> 6) + ((d & 0x10) << 51) + ((d & 0x1000) << 42) + ((d & 0x100000) << 33) + ((d & 0x10000080) << 24) + ((d & 0x1000008000) << 15) + ((d & 0x100000800002) << 6) + ((d & 0x10000080000200) >> 3) + ((d & 0x1000008000020000) >> 12) + ((d & 0x4) << 45) + ((d & 0x400) << 36) + ((d & 0x40000) << 27) + ((d & 0x4000020) << 18) + ((d & 0x400002000) << 9) + (d & 0x40000200000) + ((d & 0x4000020000000) >> 9) + ((d & 0x400002000000000) >> 18) + ((d & 0x1000008000000) >> 15) + ((d & 0x100000800000000) >> 24) + ((d & 0x800002000000) >> 21) + ((d & 0x80000200000000) >> 30) + ((d & 0x8000020000000000) >> 39) + ((d & 0x200000000000) >> 27) + ((d & 0x20000000000000) >> 36) + ((d & 0x2000000000000000) >> 45) + ((d & 0x80000000000) >> 33) + ((d & 0x8000000000000) >> 42) + ((d & 0x800000000000000) >> 51) + ((d & 0x2000000000000) >> 48) + ((d & 0x200000000000000) >> 57)

    @classmethod
    def fp(cls, d):
        return ((d & 0x1000004) << 39) + ((d & 0x100000400002000) << 6) + ((d & 0x10000) << 45) + ((d & 0x1000008000020) << 12) + ((d & 0x100) << 51) + ((d & 0x10000080000) << 18) + ((d & 0x1) << 57) + ((d & 0x100000800) << 24) + ((d & 0x2000008) << 30) + ((d & 0x200000800004000) >> 3) + ((d & 0x20000) << 36) + ((d & 0x2000010000040) << 3) + ((d & 0x200) << 42) + ((d & 0x20000100000) << 9) + ((d & 0x2) << 48) + ((d & 0x200001000) << 15) + ((d & 0x4000010) << 21) + ((d & 0x400001000008000) >> 12) + ((d & 0x40000) << 27) + ((d & 0x4000020000080) >> 6) + ((d & 0x400) << 33) + (d & 0x40000200000) + ((d & 0x800002000000000) >> 21) + ((d & 0x8000040000000) >> 15) + ((d & 0x80000400000) >> 9) + ((d & 0x1000004000000000) >> 30) + ((d & 0x10000080000000) >> 24) + ((d & 0x100000800000) >> 18) + ((d & 0x2000008000000000) >> 39) + ((d & 0x20000000000000) >> 33) + ((d & 0x200000000000) >> 27) + ((d & 0x4000000000000000) >> 48) + ((d & 0x40000000000000) >> 42) + ((d & 0x400000000000) >> 36) + ((d & 0x8000000000000000) >> 57) + ((d & 0x80000000000000) >> 51) + ((d & 0x800000000000) >> 45)

    @classmethod
    def pc1(cls, d):
        return ((d & 0x80) << 48) + ((d & 0x8000) << 39) + ((d & 0x800000) << 30) + ((d & 0x80000000) << 21) + ((d & 0x8000000000) << 12) + ((d & 0x800000000000) << 3) + ((d & 0x80000000000000) >> 6) + ((d & 0x8000000000000000) >> 15) + ((d & 0x40) << 41) + ((d & 0x4000) << 32) + ((d & 0x400000) << 23) + ((d & 0x40000000) << 14) + ((d & 0x4000000000) << 5) + ((d & 0x400000000000) >> 4) + ((d & 0x40000000000000) >> 13) + ((d & 0x4000000000000000) >> 22) + ((d & 0x20) << 34) + ((d & 0x2000) << 25) + ((d & 0x200000) << 16) + ((d & 0x20000000) << 7) + ((d & 0x2000000000) >> 2) + ((d & 0x200000000000) >> 11) + ((d & 0x20000000000000) >> 20) + ((d & 0x2000000000000000) >> 29) + ((d & 0x10) << 27) + ((d & 0x1000) << 18) + ((d & 0x100000) << 9) + (d & 0x10000000) + ((d & 0x2) << 26) + ((d & 0x204) << 17) + ((d & 0x20408) << 8) + ((d & 0x2040800) >> 1) + ((d & 0x204080000) >> 10) + ((d & 0x20408000000) >> 19) + ((d & 0x2040800000000) >> 28) + ((d & 0x204080000000000) >> 37) + ((d & 0x408000000000000) >> 46) + ((d & 0x800000000000000) >> 55) + ((d & 0x1000000000) >> 33) + ((d & 0x100000000000) >> 42) + ((d & 0x10000000000000) >> 51) + ((d & 0x1000000000000000) >> 60)

    @classmethod
    def counterToMissingBitsInFirstRoundKey(cls, k):
        return ((k & 0x1) << 1) + ((k & 0x2) << 11) + ((k & 0x4) << 15) + ((k & 0x8) << 17) + ((k & 0x10) << 26) + ((k & 0x20) << 28) + ((k & 0x40) << 31) + ((k & 0x80) << 39)

    @classmethod
    def counterToMissingBitsInLastRoundKey(cls, k):
        return ((k & 0x1) << 2) + ((k & 0x2) << 12) + ((k & 0x4) << 16) + ((k & 0x8) << 18) + ((k & 0x10) << 27) + ((k & 0x20) << 29) + ((k & 0x40) << 32) + ((k & 0x80) << 40)

    @classmethod
    def makeTables(cls):
        cls.SP = [[0] * 4096 for _ in range(4)]
        for i in range(4):
            p = 0
            for j in range(64):
                for q in range(64):
                    cls.SP[i][p] = cls.permute((((cls.S[2 * i][j] << 4) | cls.S[2 * i + 1][q]) & 0xFF) << (24 - (8 * i)), cls.P)
                    p += 1

    @classmethod
    def tdes_mac(cls, key, data, icv):
        result = [0] * 8
        for j in range(8):
            if icv is not None and j < len(icv):
                result[j] = icv[j]
            else:
                result[j] = 0
        k = 0
        for i in range(0, len(data), 8):
            for j in range(8):
                if k < len(data):
                    result[j] ^= data[k]
                k += 1
            result = list(cls.tdes_ecb(key, bytes(result), True))
        return bytes(result)

    @classmethod
    def tdes_ecb(cls, key, data, enc):
        k1 = cls.toLong(key)
        k2 = cls.toLong(key, 8)
        result_length = len(data) + (7 - ((len(data) - 1) % 8))
        result = bytearray(result_length)
        for i in range(0, len(data), 8):
            tmp = cls.fastDes(k1, cls.toLong(data, i), enc)
            tmp = cls.fastDes(k2, tmp, not enc)
            tmp_bytes = cls.toByteArray(cls.des(k1, tmp, enc))
            for j in range(8):
                if i + j < result_length:
                    result[i + j] = tmp_bytes[j]
        return bytes(result)

    @classmethod
    def tdes24_ecb(cls, key, data, enc):
        k1 = cls.toLong(key)
        k2 = cls.toLong(key, 8)
        k3 = cls.toLong(key, 16)
        result_length = len(data) + (7 - ((len(data) - 1) % 8))
        result = bytearray(result_length)
        for i in range(0, len(data), 8):
            tmp = cls.fastDes(k1, cls.toLong(data, i), enc)
            tmp = cls.fastDes(k2, tmp, not enc)
            tmp_bytes = cls.toByteArray(cls.des(k3, tmp, enc))
            for j in range(8):
                if i + j < result_length:
                    result[i + j] = tmp_bytes[j]
        return bytes(result)

    @classmethod
    def toLong(cls, ba, offset=0):
        if ba is None:
            return 0
        result = 0
        for i in range(8):
            result = (result << 8)
            if offset + i < len(ba):
                result += (ba[offset + i] & 0xFF)
        return result

    @classmethod
    def toByteArray(cls, x):
        result = bytearray(8)
        for i in range(7, -1, -1):
            result[i] = (x & 0xFF)
            x >>= 8
        return bytes(result)

    @classmethod
    def tdes_cbc(cls, key, data, icv, enc):
        k1 = cls.toLong(key)
        k2 = cls.toLong(key, 8)
        tmp = cls.toLong(icv)
        result_length = len(data) + (7 - ((len(data) - 1) % 8))
        result = bytearray(result_length)
        if enc:
            for i in range(0, len(data), 8):
                tmp = cls.des(k1, tmp ^ cls.toLong(data, i), True)
                tmp = cls.des(k2, tmp, False)
                tmp = cls.des(k1, tmp, True)
                tmp_bytes = cls.toByteArray(tmp)
                for j in range(8):
                    if i + j < result_length:
                        result[i + j] = tmp_bytes[j]
        else:
            for i in range(0, len(data), 8):
                d = cls.des(k1, cls.toLong(data, i), False)
                d = cls.des(k2, d, True)
                tmp = cls.des(k1, d, False) ^ tmp
                tmp_bytes = cls.toByteArray(tmp)
                for j in range(8):
                    if i + j < result_length:
                        result[i + j] = tmp_bytes[j]
                tmp = cls.toLong(data, i)
        return bytes(result)


Des.makeTables()