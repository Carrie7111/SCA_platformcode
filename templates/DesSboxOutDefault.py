class DesSboxOutDefault:

    def __init__(self):
        self.round = 0
        self.roundKey = 0

    # DES常量定义
    IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40,
          32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63,
          55, 47, 39, 31, 23, 15, 7]
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20,
         21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11,
         4, 25]
    S = [
        [14, 0, 4, 15, 13, 7, 1, 4, 2, 14, 15, 2, 11, 13, 8, 1, 3, 10, 10, 6, 6, 12, 12, 11, 5, 9, 9, 5, 0, 3, 7, 8, 4,
         15, 1, 12, 14, 8, 8, 2, 13, 4, 6, 9, 2, 1, 11, 7, 15, 5, 12, 11, 9, 3, 7, 14, 3, 10, 10, 0, 5, 6, 0, 13],
        [15, 3, 1, 13, 8, 4, 14, 7, 6, 15, 11, 2, 3, 8, 4, 14, 9, 12, 7, 0, 2, 1, 13, 10, 12, 6, 0, 9, 5, 11, 10, 5, 0,
         13, 14, 8, 7, 10, 11, 1, 10, 3, 4, 15, 13, 4, 1, 2, 5, 11, 8, 6, 12, 7, 6, 12, 9, 0, 3, 5, 2, 14, 15, 9],
        [10, 13, 0, 7, 9, 0, 14, 9, 6, 3, 3, 4, 15, 6, 5, 10, 1, 2, 13, 8, 12, 5, 7, 14, 11, 12, 4, 11, 2, 15, 8, 1, 13,
         1, 6, 10, 4, 13, 9, 0, 8, 6, 15, 9, 3, 8, 0, 7, 11, 4, 1, 15, 2, 14, 12, 3, 5, 11, 10, 5, 14, 2, 7, 12],
        [7, 13, 13, 8, 14, 11, 3, 5, 0, 6, 6, 15, 9, 0, 10, 3, 1, 4, 2, 7, 8, 2, 5, 12, 11, 1, 12, 10, 4, 14, 15, 9, 10,
         3, 6, 15, 9, 0, 0, 6, 12, 10, 11, 1, 7, 13, 13, 8, 15, 9, 1, 4, 3, 5, 14, 11, 5, 12, 2, 7, 8, 2, 4, 14],
        [2, 14, 12, 11, 4, 2, 1, 12, 7, 4, 10, 7, 11, 13, 6, 1, 8, 5, 5, 0, 3, 15, 15, 10, 13, 3, 0, 9, 14, 8, 9, 6, 4,
         11, 2, 8, 1, 12, 11, 7, 10, 1, 13, 14, 7, 2, 8, 13, 15, 6, 9, 15, 12, 0, 5, 9, 6, 10, 3, 4, 0, 5, 14, 3],
        [12, 10, 1, 15, 10, 4, 15, 2, 9, 7, 2, 12, 6, 9, 8, 5, 0, 6, 13, 1, 3, 13, 4, 14, 14, 0, 7, 11, 5, 3, 11, 8, 9,
         4, 14, 3, 15, 2, 5, 12, 2, 9, 8, 5, 12, 15, 3, 10, 7, 11, 0, 14, 4, 1, 10, 7, 1, 6, 13, 0, 11, 8, 6, 13],
        [4, 13, 11, 0, 2, 11, 14, 7, 15, 4, 0, 9, 8, 1, 13, 10, 3, 14, 12, 3, 9, 5, 7, 12, 5, 2, 10, 15, 6, 8, 1, 6, 1,
         6, 4, 11, 11, 13, 13, 8, 12, 1, 3, 4, 7, 10, 14, 7, 10, 9, 15, 5, 6, 0, 8, 15, 0, 14, 5, 2, 9, 3, 2, 12],
        [13, 1, 2, 15, 8, 13, 4, 8, 6, 10, 15, 3, 11, 7, 1, 4, 10, 12, 9, 5, 3, 6, 14, 11, 5, 0, 0, 14, 12, 9, 7, 2, 7,
         2, 11, 1, 4, 14, 1, 7, 9, 4, 12, 10, 14, 8, 2, 13, 0, 15, 6, 12, 10, 9, 13, 0, 15, 3, 3, 5, 5, 6, 8, 11]
    ]

    @classmethod
    def permute(cls, in_val, mat, insize=None):
        if insize is None:
            insize = len(mat)
        result = 0
        i = 0
        while i < len(mat):
            result = ((result << 1) | ((in_val >> (insize - mat[i])) & 1))
            i += 1
        return result

    @classmethod
    def invPermute(cls, in_val, mat, outsize=None):
        if outsize is None:
            outsize = len(mat)
        result = 0
        i = 0
        temp = in_val
        while i < len(mat):
            result |= ((temp & 1) << (outsize - mat[len(mat) - 1 - i]))
            temp >>= 1
            i += 1
        return result

    @classmethod
    def sbox(cls, in_val):
        result = 0
        for i in range(8):
            result = ((result << 4) + cls.S[i][(in_val >> (6 * (7 - i))) & 0x3F])
        return result

    @staticmethod
    def BytetoLong(ba, offset, length):
        result = 0
        for i in range(length):
            result = (result << 8)
            if offset + i < len(ba):
                result += ba[offset + i] & 0xFF
        return result

    @staticmethod
    def GetHW(x):
        return float(bin(x).count('1'))

    def GetMidDataHW(self, data):
        s_out = 0
        s_in = 0
        Des_R = 0
        Des_L = 0
        e_out = 0

        guess_key = [
            0x0, 0x41041041041, 0x82082082082, 0xc30c30c30c3, 0x104104104104, 0x145145145145,
            0x186186186186, 0x1c71c71c71c7, 0x208208208208, 0x249249249249, 0x28a28a28a28a,
            0x2cb2cb2cb2cb, 0x30c30c30c30c, 0x34d34d34d34d, 0x38e38e38e38e, 0x3cf3cf3cf3cf,
            0x410410410410, 0x451451451451, 0x492492492492, 0x4d34d34d34d3, 0x514514514514,
            0x555555555555, 0x596596596596, 0x5d75d75d75d7, 0x618618618618, 0x659659659659,
            0x69a69a69a69a, 0x6db6db6db6db, 0x71c71c71c71c, 0x75d75d75d75d, 0x79e79e79e79e,
            0x7df7df7df7df, 0x820820820820, 0x861861861861, 0x8a28a28a28a2, 0x8e38e38e38e3,
            0x924924924924, 0x965965965965, 0x9a69a69a69a6, 0x9e79e79e79e7, 0xa28a28a28a28,
            0xa69a69a69a69, 0xaaaaaaaaaaaa, 0xaebaebaebaeb, 0xb2cb2cb2cb2c, 0xb6db6db6db6d,
            0xbaebaebaebae, 0xbefbefbefbef, 0xc30c30c30c30, 0xc71c71c71c71, 0xcb2cb2cb2cb2,
            0xcf3cf3cf3cf3, 0xd34d34d34d34, 0xd75d75d75d75, 0xdb6db6db6db6, 0xdf7df7df7df7,
            0xe38e38e38e38, 0xe79e79e79e79, 0xebaebaebaeba, 0xefbefbefbefb, 0xf3cf3cf3cf3c,
            0xf7df7df7df7d, 0xfbefbefbefbe, 0xffffffffffff
        ]

        MidDataHW = [0.0] * 512

        if data is None:
            return None

        Des_Input = self.BytetoLong(data, 0, 8)
        Des_IP_out = self.permute(Des_Input, self.IP)
        Des_R = Des_IP_out & 0xFFFFFFFF
        Des_L = (Des_IP_out >> 32) & 0xFFFFFFFF

        if 1 == self.round:
            s_in = self.permute(Des_R, self.E, 32)
            s_out = self.sbox(s_in ^ self.roundKey)
            tem = Des_R
            Des_R = Des_L ^ self.permute(s_out, self.P)
            Des_L = tem

        e_out = self.permute(Des_R, self.E, 32)

        for i in range(64):
            s_in = guess_key[i] ^ e_out
            s_out = self.sbox(s_in)
            index_skey = i
            index_sbit = 28
            for j in range(7, -1, -1):
                MidDataHW[index_skey] = self.GetHW((s_out >> index_sbit) & 0xF)
                index_skey += 64
                index_sbit -= 4

        return MidDataHW


class DesSboxOutBase:
    pass