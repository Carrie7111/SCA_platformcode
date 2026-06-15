# -*- coding: utf-8 -*-
def rol(val: int, shift: int, bits: int = 32) -> int:
    shift %= bits
    return ((val << shift) | (val >> (bits - shift))) & ((1 << bits) - 1)

def sm3_p1(x: int) -> int:
    return x ^ rol(x, 15) ^ rol(x, 23)

def sm3_p0(x: int) -> int:
    return x ^ rol(x, 9) ^ rol(x, 17)

def sm3_ff1(a: int, b: int, c: int) -> int:
    return a ^ b ^ c

def sm3_gg1(e: int, f: int, g: int) -> int:
    return e ^ f ^ g

def sm3_byte_array_to_long(data: bytes, offset: int) -> int:
    slice_data = data[offset:offset + 4]
    return int.from_bytes(slice_data, byteorder='big', signed=False) & 0xFFFFFFFF

def sm3_long_to_byte_array(val: int, arr: bytearray, offset: int):
    bytes_val = val.to_bytes(4, byteorder='big', signed=False)
    arr[offset:offset + 4] = bytes_val

def sm3_byte_array_format_data(mdata: bytes) -> bytes:
    length = len(mdata) * 8
    padding = bytearray()
    padding.append(0x80)
    while (len(mdata) + len(padding) + 8) % 64 != 0:
        padding.append(0x00)
    length_bytes = length.to_bytes(8, byteorder='big', signed=False)
    return mdata + padding + length_bytes

def get_hw_long(val: int) -> float:
    return bin(val & 0xFF).count('1')

class SM3AttackHDDefault:
    def __init__(self):
        self.dataLength = 256
        self.round = 0
        self.keynum = 0
        self.track = 0
        self.T1 = 0
        self.Key = [0] * 10
        self.roundKeyone = 0
        self.roundKeytwo = 0
        self.roundKeythree = 0
        self.X = [0] * 68
        self.Y = [0] * 64

    def GetMidDataHW(self, data: bytes) -> list[float] | None:
        if self.round > 3 or data is None:
            return None

        MidDataHW = [0.0] * self.dataLength
        s_out = 0
        s_in = 0

        mdata = bytearray(32)
        mdata[:len(data)] = data[:32]
        newbyte = sm3_byte_array_format_data(mdata)
        MCount = len(newbyte) // 64

        self.Y = [0] * 64

        for pos in range(MCount):
            for j in range(16):
                offset = (pos * 64) + (j * 4)
                self.X[j] = sm3_byte_array_to_long(newbyte, offset)

        for t1 in range(16, 68):
            part1 = self.X[t1-16] ^ self.X[t1-9] ^ rol(self.X[t1-3], 15)
            part2 = rol(self.X[t1-13], 7)
            self.X[t1] = sm3_p1(part1) ^ part2 ^ self.X[t1-6]
            self.X[t1] &= 0xFFFFFFFF

        for t0 in range(64):
            self.Y[t0] = self.X[t0] ^ self.X[t0 + 4]
            self.Y[t0] &= 0xFFFFFFFF

        if self.keynum == 0:
            s_in = self.Y[0]
        elif self.keynum == 1:
            s_in = self.X[0]
        elif self.keynum == 2:
            s_in = (self.Key[0] + self.Y[0]) & 0xFFFFFFFF
        elif self.keynum == 3:
            s_in = sm3_p0(self.Key[1] + self.X[0]) & 0xFFFFFFFF
        elif self.keynum == 4:
            B1 = self.Key[2]
            A1 = self.Key[0] + self.Y[0]
            s_in = B1 ^ A1
        elif self.keynum == 5:
            B1_temp = self.Key[2]
            A1_temp = self.Key[0] + self.Y[0]
            C1_temp = rol(self.Key[4], 9)
            ss1_5 = (rol(A1_temp, 12) + sm3_p0(self.Key[1] + self.X[0]) + rol(self.T1, 1)) & 0xFFFFFFFF
            ss1_5 = rol(ss1_5, 7)
            ss2_5 = ss1_5 ^ rol(A1_temp, 12)
            s_in = (sm3_ff1(A1_temp, B1_temp, C1_temp) + ss2_5 + self.Y[1]) & 0xFFFFFFFF
        elif self.keynum == 6:
            ss1_6 = (rol(self.Key[2], 12) + self.Key[3] + rol(self.T1, 0)) & 0xFFFFFFFF
            ss1_6 = rol(ss1_6, 7)
            ss2_6 = ss1_6 ^ rol(self.Key[2], 12)
            s_in = (sm3_ff1(self.Key[2], self.Key[4], self.Key[5]) + ss2_6 + self.Y[0]) & 0xFFFFFFFF
        elif self.keynum == 7:
            E1 = sm3_p0(self.Key[1] + self.X[0])
            F1 = self.Key[3]
            s_in = (E1 ^ F1) & 0xFFFFFFFF
        elif self.keynum == 8:
            A1temp0 = self.Key[0] + self.Y[0]
            ss1_9 = (rol(A1temp0, 12) + sm3_p0(self.Key[1] + self.X[0]) + rol(self.T1, 1)) & 0xFFFFFFFF
            ss1_9 = rol(ss1_9, 7)
            E1_9 = sm3_p0(self.Key[1] + self.X[0])
            F1_9 = self.Key[3]
            G1_9 = rol(self.Key[7], 19)
            s_in = (sm3_gg1(E1_9, F1_9, G1_9) + ss1_9 + self.X[1]) & 0xFFFFFFFF
        elif self.keynum == 9:
            A0 = self.Key[2]
            E0 = self.Key[3]
            F0 = self.Key[7]
            G0 = self.Key[8]
            ss1 = (rol(A0, 12) + E0 + rol(self.T1, 0)) & 0xFFFFFFFF
            ss1 = rol(ss1, 7)
            s_in = (sm3_gg1(E0, F0, G0) + ss1 + self.X[0]) & 0xFFFFFFFF

        for i in range(256):
            shift = self.round * 8
            base = (i << shift)
            key_part = (self.roundKeyone | (self.roundKeytwo << 8) | (self.roundKeythree << 16))

            if self.keynum in [0, 1, 5, 6, 8, 9]:
                temp_val = (base + key_part + s_in) & 0xFFFFFFFF
            else:
                temp_val = (base ^ key_part ^ s_in) & 0xFFFFFFFF

            s_out = (temp_val >> shift) & 0xFFFFFFFF

            if self.track < 8:
                bit = (s_out >> self.track) & 1
                MidDataHW[i] = 2 * bit - 1
            elif self.track == 8:
                MidDataHW[i] = get_hw_long(s_out)

        return MidDataHW