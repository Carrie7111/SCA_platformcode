class Des:
    IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    S = [
        [14, 0, 4, 15, 13, 7, 1, 4, 2, 14, 15, 2, 11, 13, 8, 1, 3, 10, 10, 6, 6, 12, 12, 11, 5, 9, 9, 5, 0, 3, 7, 8, 4, 15, 1, 12, 14, 8, 8, 2, 13, 4, 6, 9, 2, 1, 11, 7, 15, 5, 12, 11, 9, 3, 7, 14, 3, 10, 10, 0, 5, 6, 0, 13],
        [15, 3, 1, 13, 8, 4, 14, 7, 6, 15, 11, 2, 3, 8, 4, 14, 9, 12, 7, 0, 2, 1, 13, 10, 12, 6, 0, 9, 5, 11, 10, 5, 0, 13, 14, 8, 7, 10, 11, 1, 10, 3, 4, 15, 13, 4, 1, 2, 5, 11, 8, 6, 12, 7, 6, 12, 9, 0, 3, 5, 2, 14, 15, 9],
        [10, 13, 0, 7, 9, 0, 14, 9, 6, 3, 3, 4, 15, 6, 5, 10, 1, 2, 13, 8, 12, 5, 7, 14, 11, 12, 4, 11, 2, 15, 8, 1, 13, 1, 6, 10, 4, 13, 9, 0, 8, 6, 15, 9, 3, 8, 0, 7, 11, 4, 1, 15, 2, 14, 12, 3, 5, 11, 10, 5, 14, 2, 7, 12],
        [7, 13, 13, 8, 14, 11, 3, 5, 0, 6, 6, 15, 9, 0, 10, 3, 1, 4, 2, 7, 8, 2, 5, 12, 11, 1, 12, 10, 4, 14, 15, 9, 10, 3, 6, 15, 9, 0, 0, 6, 12, 10, 11, 1, 7, 13, 13, 8, 15, 9, 1, 4, 3, 5, 14, 11, 5, 12, 2, 7, 8, 2, 4, 14],
        [2, 14, 12, 11, 4, 2, 1, 12, 7, 4, 10, 7, 11, 13, 6, 1, 8, 5, 5, 0, 3, 15, 15, 10, 13, 3, 0, 9, 14, 8, 9, 6, 4, 11, 2, 8, 1, 12, 11, 7, 10, 1, 13, 14, 7, 2, 8, 13, 15, 6, 9, 15, 12, 0, 5, 9, 6, 10, 3, 4, 0, 5, 14, 3],
        [12, 10, 1, 15, 10, 4, 15, 2, 9, 7, 2, 12, 6, 9, 8, 5, 0, 6, 13, 1, 3, 13, 4, 14, 14, 0, 7, 11, 5, 3, 11, 8, 9, 4, 14, 3, 15, 2, 5, 12, 2, 9, 8, 5, 12, 15, 3, 10, 7, 11, 0, 14, 4, 1, 10, 7, 1, 6, 13, 0, 11, 8, 6, 13],
        [4, 13, 11, 0, 2, 11, 14, 7, 15, 4, 0, 9, 8, 1, 13, 10, 3, 14, 12, 3, 9, 5, 7, 12, 5, 2, 10, 15, 6, 8, 1, 6, 1, 6, 4, 11, 11, 13, 13, 8, 12, 1, 3, 4, 7, 10, 14, 7, 10, 9, 15, 5, 6, 0, 8, 15, 0, 14, 5, 2, 9, 3, 2, 12],
        [13, 1, 2, 15, 8, 13, 4, 8, 6, 10, 15, 3, 11, 7, 1, 4, 10, 12, 9, 5, 3, 6, 14, 11, 5, 0, 0, 14, 12, 9, 7, 2, 7, 2, 11, 1, 4, 14, 1, 7, 9, 4, 12, 10, 14, 8, 2, 13, 0, 15, 6, 12, 10, 9, 13, 0, 15, 3, 3, 5, 5, 6, 8, 11]
    ]
    SP = None
    LSinc = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 0]
    maskTable = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296, 8589934592, 17179869184, 34359738368, 68719476736, 137438953472, 274877906944, 549755813888, 1099511627776, 2199023255552, 4398046511104, 8796093022208, 17592186044416, 35184372088832, 70368744177664, 140737488355328, 281474976710656, 562949953421312, 1125899906842624, 2251799813685248, 4503599627370496, 9007199254740992, 18014398509481984, 36028797018963968, 72057594037927936, 144115188075855872, 288230376151711744, 576460752303423488, 1152921504606846976, 2305843009213693952, 4611686018427387904, 9223372036854775808]

    @classmethod
    def permute(cls, var0, var2, var3=None):
        if var3 is None:
            var3 = len(var2)
        var4 = 0
        var6 = 0
        while var6 < len(var2):
            var4 = ((var4 << 1) | ((var0 >> (var3 - var2[var6])) & 1))
            var6 += 1
        return var4

    @classmethod
    def intPermute(cls, var0, var2, var3):
        var4 = 0
        var5 = 0
        while var5 < len(var2):
            var4 = ((var4 << 1) | ((var0 >> (var3 - var2[var5])) & 1))
            var5 += 1
        return var4

    @classmethod
    def invPermute(cls, var0, var2, var3=None):
        if var3 is None:
            var3 = len(var2)
        var4 = 0
        var6 = 0
        temp = var0
        while var6 < len(var2):
            var4 |= ((temp & 1) << (var3 - var2[len(var2) - 1 - var6]))
            temp >>= 1
            var6 += 1
        return var4

    @classmethod
    def sbox(cls, var0):
        var2 = 0
        for var3 in range(8):
            var2 = ((var2 << 4) + cls.S[var3][(var0 >> (6 * (7 - var3))) & 0x3F])
        return var2

    @classmethod
    def rotate(cls, var0, var2):
        var3 = var0 >> 28
        var4 = var0 & 0xFFFFFFF
        var3 = (((var3 << cls.LSinc[var2]) + (var3 >> (28 - cls.LSinc[var2]))) & 0xFFFFFFF)
        var4 = (((var4 << cls.LSinc[var2]) + (var4 >> (28 - cls.LSinc[var2]))) & 0xFFFFFFF)
        return ((var3 << 28) + var4)

    @classmethod
    def invRotate(cls, var0, var2):
        var3 = var0 >> 28
        var4 = var0 & 0xFFFFFFF
        var3 = (((var3 >> cls.LSinc[var2]) + (var3 << (28 - cls.LSinc[var2]))) & 0xFFFFFFF)
        var4 = (((var4 >> cls.LSinc[var2]) + (var4 << (28 - cls.LSinc[var2]))) & 0xFFFFFFF)
        return ((var3 << 28) + var4)

    @classmethod
    def rotate_string(cls, var0, var1):
        var2 = list(var0)
        for var3 in range(28):
            var2[var3] = var0[(var3 - var1 + 28) % 28]
            var2[var3 + 28] = var0[((var3 - var1 + 28) % 28) + 28]
        return ''.join(var2)

    @classmethod
    def f(cls, var0, var1, var3):
        return cls.permute(cls.sbox(cls.permute(var0, cls.E, 32) ^ cls.permute(cls.rotate(var1, var3), cls.PC2, 56)), cls.P)

    @classmethod
    def des(cls, var0, var2, var4):
        var2 = cls.permute(var2, cls.IP)
        var0 = cls.permute(var0, cls.PC1, 64)
        var5 = var2 >> 32
        var6 = var2 & 0xFFFFFFFF
        if var4:
            var7 = 0
            while var7 < 16:
                var5 = (cls.f(var6 & 0xFFFFFFFF, var0, var7) ^ var5) & 0xFFFFFFFF
                var7 += 1
                var6 = (cls.f(var5 & 0xFFFFFFFF, var0, var7) ^ var6) & 0xFFFFFFFF
                var7 += 1
        else:
            var13 = 15
            while var13 >= 0:
                var5 = (cls.f(var6 & 0xFFFFFFFF, var0, var13) ^ var5) & 0xFFFFFFFF
                var13 -= 1
                var6 = (cls.f(var5 & 0xFFFFFFFF, var0, var13) ^ var6) & 0xFFFFFFFF
                var13 -= 1
        var2 = (((var6 & 0xFFFFFFFF) << 32) + (var5 & 0xFFFFFFFF))
        var2 = cls.invPermute(var2, cls.IP)
        return var2

    @classmethod
    def fastF(cls, var0, var1, var3):
        var4 = var1 >> 28
        var5 = var1 & 0xFFFFFFF
        var4 = (((var4 << cls.LSinc[var3]) + (var4 >> (28 - cls.LSinc[var3]))) & 0xFFFFFFF)
        var5 = (((var5 << cls.LSinc[var3]) + (var5 >> (28 - cls.LSinc[var3]))) & 0xFFFFFFF)
        var6 = ((var4 << 28) + var5)
        return (cls.SP[0][(((var0 << 11) | ((var0 >> 21) & 0x7C0) | ((var0 >> 23) & 0x3F)) & 0xFFF) ^ int(((var6 & 0x40000000000) >> 31) + ((var6 & 0x8000000000) >> 29) + ((var6 & 0x200000000000) >> 36) + ((var6 & 0x110000000) >> 24) + ((var6 & 0xa4000000000000) >> 48) + ((var6 & 0x8000000000000) >> 45) + ((var6 & 0x20000000000) >> 38) + ((var6 & 0x800000000) >> 34) + ((var6 & 0x400000000000) >> 46))] |
                cls.SP[1][(((var0 >> 13) & 0xFC0) | ((var0 >> 15) & 0x3F)) ^ int(((var6 & 0x200000000) >> 22) + ((var6 & 0x2000000000) >> 27) + ((var6 & 0x110000000000) >> 35) + ((var6 & 0x10000000000000) >> 44) + ((var6 & 0x40000000) >> 23) + ((var6 & 0x1080000000000) >> 42) + ((var6 & 0x2000000000000) >> 45) + ((var6 & 0x20000000) >> 26) + ((var6 & 0x1000000000) >> 34) + ((var6 & 0x40000000000000) >> 54))] |
                cls.SP[2][(((var0 >> 5) & 0xFC0) | ((var0 >> 7) & 0x3F)) ^ int(((var6 & 0x8000) >> 4) + ((var6 & 0x10) << 6) + ((var6 & 0x2000000) >> 16) + ((var6 & 0x80000) >> 11) + ((var6 & 0x220) >> 2) + ((var6 & 0x2) << 5) + ((var6 & 0x4000000) >> 21) + ((var6 & 0x10000) >> 12) + ((var6 & 0x800) >> 9) + ((var6 & 0x800000) >> 22) + ((var6 & 0x100) >> 8))] |
                cls.SP[3][(((var0 << 3) & 0xFC0) | (((var0 << 1) | (var0 >> 31)) & 0x3F)) ^ int(((var6 & 0x1000) >> 1) + ((var6 & 0x88) << 3) + ((var6 & 0x20000) >> 8) + ((var6 & 0x1) << 8) + ((var6 & 0x400000) >> 15) + ((var6 & 0x400) >> 5) + ((var6 & 0x4000) >> 10) + ((var6 & 0x40) >> 3) + ((var6 & 0x100000) >> 18) + ((var6 & 0x8000000) >> 26) + ((var6 & 0x1000000) >> 24))])

    @classmethod
    def fastDes(cls, var0, var2, var4):
        var0 = cls.pc1(var0)
        var2 = cls.ip(var2)
        if var4:
            var2 = cls.fastDesEncrypt(var0, var2)
        else:
            var2 = cls.fastDesDecrypt(var0, var2)
        return cls.fp(var2)

    @classmethod
    def fastDesEncrypt(cls, var0, var2):
        var4 = var2 >> 32
        var5 = var2 & 0xFFFFFFFF
        var6 = 0
        while var6 < 16:
            var4 = (var4 ^ cls.fastF(var5, var0, var6)) & 0xFFFFFFFF
            var6 += 1
            var5 = (var5 ^ cls.fastF(var4, var0, var6)) & 0xFFFFFFFF
            var6 += 1
        return (((var5 & 0xFFFFFFFF) << 32) + (var4 & 0xFFFFFFFF))

    @classmethod
    def fastDesDecrypt(cls, var0, var2):
        var4 = var2 >> 32
        var5 = var2 & 0xFFFFFFFF
        var6 = 15
        while var6 >= 0:
            var4 = (var4 ^ cls.fastF(var5, var0, var6)) & 0xFFFFFFFF
            var6 -= 1
            var5 = (var5 ^ cls.fastF(var4, var0, var6)) & 0xFFFFFFFF
            var6 -= 1
        return (((var5 & 0xFFFFFFFF) << 32) + (var4 & 0xFFFFFFFF))

    @classmethod
    def ip(cls, var0):
        return ((var0 & 64) << 57) + ((var0 & 16384) << 48) + ((var0 & 4194305) << 39) + ((var0 & 1073742080) << 30) + ((var0 & 274877972480) << 21) + ((var0 & 70368760954888) << 12) + ((var0 & 18014402804451328) << 3) + ((var0 & 4611687117939539968) >> 6) + ((var0 & 16) << 51) + ((var0 & 4096) << 42) + ((var0 & 1048576) << 33) + ((var0 & 268435584) << 24) + ((var0 & 68719509504) << 15) + ((var0 & 17592194433026) << 6) + ((var0 & 4503601774854656) >> 3) + ((var0 & 1152922054362791936) >> 12) + ((var0 & 4) << 45) + ((var0 & 1024) << 36) + ((var0 & 262144) << 27) + ((var0 & 67108896) << 18) + ((var0 & 17179877376) << 9) + (var0 & 4398048608256) + ((var0 & 1125900443713536) >> 9) + ((var0 & 288230513590665216) >> 18) + ((var0 & 281475110928384) >> 15) + ((var0 & 72057628397666304) >> 24) + ((var0 & 140737521909760) >> 21) + ((var0 & 36028805608898560) >> 30) + ((var0 & 9223369837831520256) >> 39) + ((var0 & 35184372088832) >> 27) + ((var0 & 9007199254740992) >> 36) + ((var0 & 2305843009213693952) >> 45) + ((var0 & 8796093022208) >> 33) + ((var0 & 2251799813685248) >> 42) + ((var0 & 576460752303423488) >> 51) + ((var0 & 562949953421312) >> 48) + ((var0 & 144115188075855872) >> 57)

    @classmethod
    def fp(cls, var0):
        return ((var0 & 16777220) << 39) + ((var0 & 72057611217805312) << 6) + ((var0 & 65536) << 45) + ((var0 & 281475110928416) << 12) + ((var0 & 256) << 51) + ((var0 & 1099512152064) << 18) + ((var0 & 1) << 57) + ((var0 & 4294969344) << 24) + ((var0 & 33554440) << 30) + ((var0 & 144115222435610624) >> 3) + ((var0 & 131072) << 36) + ((var0 & 562950221856832) << 3) + ((var0 & 512) << 42) + ((var0 & 2199024304128) << 9) + ((var0 & 2) << 48) + ((var0 & 8589938688) << 15) + ((var0 & 67108880) << 21) + ((var0 & 288230444871221248) >> 12) + ((var0 & 262144) << 27) + ((var0 & 1125900443713664) >> 6) + ((var0 & 1024) << 33) + (var0 & 4398048608256) + ((var0 & 576460889742376960) >> 21) + ((var0 & 2251800887427072) >> 15) + ((var0 & 8796097216512) >> 9) + ((var0 & 1152921779484753920) >> 30) + ((var0 & 4503601774854144) >> 24) + ((var0 & 17592194433024) >> 18) + ((var0 & 2305843558969507840) >> 39) + ((var0 & 9007199254740992) >> 33) + ((var0 & 35184372088832) >> 27) + ((var0 & 4611686018427387904) >> 48) + ((var0 & 18014398509481984) >> 42) + ((var0 & 70368744177664) >> 36) + ((var0 & 9223372036854775808) >> 57) + ((var0 & 36028797018963968) >> 51) + ((var0 & 140737488355328) >> 45)

    @classmethod
    def pc1(cls, var0):
        return ((var0 & 128) << 48) + ((var0 & 32768) << 39) + ((var0 & 8388608) << 30) + ((var0 & 2147483648) << 21) + ((var0 & 549755813888) << 12) + ((var0 & 140737488355328) << 3) + ((var0 & 36028797018963968) >> 6) + ((var0 & 9223372036854775808) >> 15) + ((var0 & 64) << 41) + ((var0 & 16384) << 32) + ((var0 & 4194304) << 23) + ((var0 & 1073741824) << 14) + ((var0 & 274877906944) << 5) + ((var0 & 70368744177664) >> 4) + ((var0 & 18014398509481984) >> 13) + ((var0 & 4611686018427387904) >> 22) + ((var0 & 32) << 34) + ((var0 & 8192) << 25) + ((var0 & 2097152) << 16) + ((var0 & 536870912) << 7) + ((var0 & 137438953472) >> 2) + ((var0 & 35184372088832) >> 11) + ((var0 & 9007199254740992) >> 20) + ((var0 & 2305843009213693952) >> 29) + ((var0 & 16) << 27) + ((var0 & 4096) << 18) + ((var0 & 1048576) << 9) + (var0 & 268435456) + ((var0 & 2) << 26) + ((var0 & 516) << 17) + ((var0 & 132104) << 8) + ((var0 & 33818624) >> 1) + ((var0 & 8657567744) >> 10) + ((var0 & 2216337342464) >> 19) + ((var0 & 567382359670784) >> 28) + ((var0 & 145249884075720704) >> 37) + ((var0 & 290482175965396992) >> 46) + ((var0 & 576460752303423488) >> 55) + ((var0 & 68719476736) >> 33) + ((var0 & 17592186044416) >> 42) + ((var0 & 4503599627370496) >> 51) + ((var0 & 1152921504606846976) >> 60)

    @classmethod
    def counterToMissingBitsInFirstRoundKey(cls, var0):
        return ((var0 & 1) << 1) + ((var0 & 2) << 11) + ((var0 & 4) << 15) + ((var0 & 8) << 17) + ((var0 & 16) << 26) + ((var0 & 32) << 28) + ((var0 & 64) << 31) + ((var0 & 128) << 39)

    @classmethod
    def counterToMissingBitsInLastRoundKey(cls, var0):
        return ((var0 & 1) << 2) + ((var0 & 2) << 12) + ((var0 & 4) << 16) + ((var0 & 8) << 18) + ((var0 & 16) << 27) + ((var0 & 32) << 29) + ((var0 & 64) << 32) + ((var0 & 128) << 40)

    @classmethod
    def makeTables(cls):
        cls.SP = [[0] * 4096 for _ in range(4)]
        for var0 in range(4):
            var1 = 0
            for var2 in range(64):
                for var3 in range(64):
                    cls.SP[var0][var1] = cls.permute((((cls.S[2 * var0][var2] << 4) | cls.S[2 * var0 + 1][var3]) & 0xFF) << (24 - (8 * var0)), cls.P)
                    var1 += 1

    @classmethod
    def tdes_mac(cls, var0, var1, var2):
        var3 = [0] * 8
        for var4 in range(8):
            if var2 is not None and var4 < len(var2):
                var3[var4] = var2[var4]
            else:
                var3[var4] = 0
        var7 = 0
        var5 = 0
        while var7 < len(var1):
            for var6 in range(8):
                if var5 < len(var1):
                    var3[var6] ^= var1[var5]
                var5 += 1
            var3 = cls.tdes_ecb(var0, bytes(var3), True)
            var7 += 8
        return bytes(var3)

    @classmethod
    def tdes_ecb(cls, var0, var1, var2):
        var3 = cls.toLong(var0)
        var5 = cls.toLong(var0, 8)
        var7 = len(var1) + (7 - ((len(var1) - 1) % 8))
        var8 = bytearray(var7)
        for var9 in range(0, len(var1), 8):
            var10 = cls.fastDes(var3, cls.toLong(var1, var9), var2)
            var10 = cls.fastDes(var5, var10, not var2)
            var10_bytes = cls.toByteArray(cls.des(var3, var10, var2))
            for var12 in range(8):
                if var9 + var12 < var7:
                    var8[var9 + var12] = var10_bytes[var12]
        return bytes(var8)

    @classmethod
    def tdes24_ecb(cls, var0, var1, var2):
        var3 = cls.toLong(var0)
        var5 = cls.toLong(var0, 8)
        var7 = cls.toLong(var0, 16)
        var9 = len(var1) + (7 - ((len(var1) - 1) % 8))
        var10 = bytearray(var9)
        for var11 in range(0, len(var1), 8):
            var12 = cls.fastDes(var3, cls.toLong(var1, var11), var2)
            var12 = cls.fastDes(var5, var12, not var2)
            var12_bytes = cls.toByteArray(cls.des(var7, var12, var2))
            for var14 in range(8):
                if var11 + var14 < var9:
                    var10[var11 + var14] = var12_bytes[var14]
        return bytes(var10)

    @classmethod
    def toLong(cls, var0, var1=None):
        if var0 is None:
            return 0
        if var1 is None:
            return cls.toLong(var0, 0)
        var2 = 0
        var4 = 0
        var5 = var1
        while var4 < 8:
            var2 <<= 8
            if var5 < len(var0):
                var2 += (var0[var5] & 0xFF)
            var4 += 1
            var5 += 1
        return var2

    @classmethod
    def toByteArray(cls, var0):
        var2 = bytearray(8)
        for var3 in range(7, -1, -1):
            var2[var3] = (var0 & 0xFF)
            var0 >>= 8
        return bytes(var2)

    @classmethod
    def tdes_cbc(cls, var0, var1, var2, var3):
        var4 = cls.toLong(var0)
        var6 = cls.toLong(var0, 8)
        var8 = cls.toLong(var2)
        var10 = len(var1) + (7 - ((len(var1) - 1) % 8))
        var11 = bytearray(var10)
        if var3:
            for var12 in range(0, len(var1), 8):
                var15 = cls.des(var4, var8 ^ cls.toLong(var1, var12), True)
                var16 = cls.des(var6, var15, False)
                var8 = cls.des(var4, var16, True)
                var8_bytes = cls.toByteArray(var8)
                for var18 in range(8):
                    if var12 + var18 < var10:
                        var11[var12 + var18] = var8_bytes[var18]
        else:
            for var18 in range(0, len(var1), 8):
                var13 = cls.des(var4, cls.toLong(var1, var18), False)
                var13 = cls.des(var6, var13, True)
                var8 = cls.des(var4, var13, False) ^ var8
                var8_bytes = cls.toByteArray(var8)
                for var20 in range(8):
                    if var18 + var20 < var10:
                        var11[var18 + var20] = var8_bytes[var20]
                var8 = cls.toLong(var1, var18)
        return bytes(var11)


# Initialize tables
Des.makeTables()