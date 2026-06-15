"""SM3 cryptographic hash algorithm (converted from SM3.java)."""

from __future__ import annotations

_MASK32 = 0xFFFFFFFF


class SM3:
    abcdefgh = [
        0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
        0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
    ]

    H1 = H2 = H3 = H4 = H5 = H6 = H7 = H8 = 0
    digestlong = [0] * 8
    X = [0] * 68
    Y = [0] * 64
    T1 = 0x79CC4519
    T2 = 0x7A879D8A

    @staticmethod
    def _u32(x: int) -> int:
        return x & _MASK32

    @staticmethod
    def process_input_bytes(bytedata: bytes | bytearray) -> int:
        SM3.digestlong = list(SM3.abcdefgh)
        newbyte = SM3.byteArrayFormatData(bytedata)
        m_count = len(newbyte) // 64

        SM3.X = [0] * 68
        SM3.H1 = 0x7380166F
        SM3.H2 = 0x4914B2B9
        SM3.H3 = 0x172442D7
        SM3.H4 = 0xDA8A0600
        SM3.H5 = 0xA96F30BC
        SM3.H6 = 0x163138AA
        SM3.H7 = 0xE38DEE4D
        SM3.H8 = 0xB0FB0E4E
        SM3.Y = [0] * 64

        for pos in range(m_count):
            for j in range(16):
                SM3.X[j] = SM3.byteArrayTolong(newbyte, pos * 64 + j * 4)
            SM3.processBlock()

        return 20

    @staticmethod
    def byteArrayFormatData(bytedata: bytes | bytearray) -> bytearray:
        n = len(bytedata)
        m = n % 64

        if m < 56:
            zeros = 55 - m
            size = n - m + 64
        elif m == 56:
            zeros = 63
            size = n + 8 + 64
        else:
            zeros = 63 - m + 56
            size = (n + 64) - m + 64

        newbyte = bytearray(size)
        newbyte[:n] = bytedata
        l = n
        newbyte[l] = 0x80
        l += 1
        for _ in range(zeros):
            newbyte[l] = 0x00
            l += 1

        bit_len = n * 8
        newbyte[l:l + 8] = bit_len.to_bytes(8, byteorder="big")
        return newbyte

    @staticmethod
    def FF1(x: int, y: int, z: int) -> int:
        return SM3._u32(x ^ y ^ z)

    @staticmethod
    def FF2(x: int, y: int, z: int) -> int:
        return SM3._u32((x & y) | (x & z) | (y & z))

    @staticmethod
    def GG1(x: int, y: int, z: int) -> int:
        return SM3._u32(x ^ y ^ z)

    @staticmethod
    def GG2(x: int, y: int, z: int) -> int:
        return SM3._u32((x & y) | ((~x) & z))

    @staticmethod
    def P0(x: int) -> int:
        return SM3._u32(SM3.ROL(x, 9) ^ SM3.ROL(x, 17) ^ x)

    @staticmethod
    def P1(x: int) -> int:
        return SM3._u32(SM3.ROL(x, 15) ^ SM3.ROL(x, 23) ^ x)

    @staticmethod
    def ROL(x: int, y: int) -> int:
        x = SM3._u32(x)
        y = y % 32
        a = (x << y) & _MASK32
        b = (x >> (32 - y)) & _MASK32
        return a | b

    @staticmethod
    def ROR(x: int, y: int) -> int:
        x = SM3._u32(x)
        y = y % 32
        a = (x >> y) & _MASK32
        b = (x << (32 - y)) & _MASK32
        return a | b

    @staticmethod
    def processBlock() -> None:
        for t in range(16, 68):
            SM3.X[t] = SM3._u32(
                SM3.P1(SM3.X[t - 16] ^ SM3.X[t - 9] ^ SM3.ROL(SM3.X[t - 3], 15))
                ^ SM3.ROL(SM3.X[t - 13], 7)
                ^ SM3.X[t - 6]
            )

        for t in range(64):
            SM3.Y[t] = SM3._u32(SM3.X[t] ^ SM3.X[t + 4])

        a, b, c, d = SM3.H1, SM3.H2, SM3.H3, SM3.H4
        e, f, g, h = SM3.H5, SM3.H6, SM3.H7, SM3.H8

        for i in range(16):
            ss1 = SM3._u32(SM3.ROL(a, 12) + e + SM3.ROL(SM3.T1, i))
            ss1 = SM3.ROL(ss1, 7)
            ss2 = SM3._u32(ss1 ^ SM3.ROL(a, 12))
            tt1 = SM3._u32(SM3.FF1(a, b, c) + d + ss2 + SM3.Y[i])
            tt2 = SM3._u32(SM3.GG1(e, f, g) + h + ss1 + SM3.X[i])
            d, c, b, a = c, SM3.ROL(b, 9), a, tt1
            h, g, f, e = g, SM3.ROL(f, 19), e, SM3.P0(tt2)

        for i in range(16, 64):
            if i == 33:
                _ = SM3.ROL(SM3.T2, i)

            ss1 = SM3._u32(SM3.ROL(a, 12) + e + SM3.ROL(SM3.T2, i))
            ss1 = SM3.ROL(ss1, 7)
            ss2 = SM3._u32(ss1 ^ SM3.ROL(a, 12))
            tt1 = SM3._u32(SM3.FF2(a, b, c) + d + ss2 + SM3.Y[i])
            tt2 = SM3._u32(SM3.GG2(e, f, g) + h + ss1 + SM3.X[i])
            d, c, b, a = c, SM3.ROL(b, 9), a, tt1
            h, g, f, e = g, SM3.ROL(f, 19), e, SM3.P0(tt2)

            print(i)
            print(f"{a:x}")
            print(f"{b:x}")
            print(f"{c:x}")
            print(f"{d:x}")
            print(f"{e:x}")
            print(f"{f:x}")
            print(f"{g:x}")
            print()

        SM3.H1 = SM3._u32(SM3.H1 ^ a)
        SM3.digestlong[0] = SM3.H1
        SM3.H2 = SM3._u32(SM3.H2 ^ b)
        SM3.digestlong[1] = SM3.H2
        SM3.H3 = SM3._u32(SM3.H3 ^ c)
        SM3.digestlong[2] = SM3.H3
        SM3.H4 = SM3._u32(SM3.H4 ^ d)
        SM3.digestlong[3] = SM3.H4
        SM3.H5 = SM3._u32(SM3.H5 ^ e)
        SM3.digestlong[4] = SM3.H5
        SM3.H6 = SM3._u32(SM3.H6 ^ f)
        SM3.digestlong[5] = SM3.H6
        SM3.H7 = SM3._u32(SM3.H7 ^ g)
        SM3.digestlong[6] = SM3.H7
        SM3.H8 = SM3._u32(SM3.H8 ^ h)
        SM3.digestlong[7] = SM3.H8

        for i in range(16):
            SM3.X[i] = 0

    @staticmethod
    def byteArrayTolong(bytedata: bytes | bytearray, i: int) -> int:
        num = 0
        num |= (bytedata[i + 3] & 0xFF) << 0
        num |= (bytedata[i + 2] & 0xFF) << 8
        num |= (bytedata[i + 1] & 0xFF) << 16
        num |= (bytedata[i] & 0xFF) << 24
        return num

    @staticmethod
    def longToByteArray(long_value: int, byte_data: bytearray | list, i: int) -> None:
        v = long_value & _MASK32
        byte_data[i] = (v >> 24) & 0xFF
        byte_data[i + 1] = (v >> 16) & 0xFF
        byte_data[i + 2] = (v >> 8) & 0xFF
        byte_data[i + 3] = v & 0xFF

    @staticmethod
    def byteToHexString(ib: int) -> str:
        digit = "0123456789ABCDEF"
        return digit[(ib >> 4) & 0x0F] + digit[ib & 0x0F]

    @staticmethod
    def byteArrayToHexString(bytearray_data: bytes | bytearray) -> str:
        return "".join(SM3.byteToHexString(b) for b in bytearray_data)

    @staticmethod
    def getDigestOfBytes(byte_data: bytes | bytearray) -> bytes:
        SM3.process_input_bytes(byte_data)
        digest = bytearray(32)
        for i in range(len(SM3.digestlong)):
            SM3.longToByteArray(SM3.digestlong[i], digest, i * 4)
        return bytes(digest)

    @staticmethod
    def byteToString(data: bytes | bytearray) -> str:
        chars = []
        for n in range(len(data)):
            unsigned = (data[n] + 256) % 256
            tmp1 = unsigned >> 4
            tmp2 = unsigned & 0x0F
            chars.append(chr(tmp1 - 0xA + ord("A")) if tmp1 >= 0xA else chr(tmp1 + ord("0")))
            chars.append(chr(tmp2 - 0xA + ord("A")) if tmp2 >= 0xA else chr(tmp2 + ord("0")))
        return "".join(chars)

    @staticmethod
    def StringToByte(text: str) -> bytes:
        result = bytearray(len(text) // 2)
        for n in range(len(text) // 2):
            a = text[2 * n]
            b = text[2 * n + 1]
            a_val = ord(a) - ord("A") + 10 if a >= "A" else ord(a) - ord("0")
            b_val = ord(b) - ord("A") + 10 if b >= "A" else ord(b) - ord("0")
            result[n] = (a_val << 4) + b_val
        return bytes(result)

    @staticmethod
    def getDigestOfString(byte_data: bytes | bytearray) -> str:
        return SM3.byteArrayToHexString(SM3.getDigestOfBytes(byte_data))


if __name__ == "__main__":
    data = bytes([
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
        0x61, 0x62, 0x63, 0x64, 0x61, 0x62, 0x63, 0x64,
    ])
    print(SM3.getDigestOfString(data))
