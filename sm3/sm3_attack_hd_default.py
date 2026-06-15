"""SM3 Hamming-distance attack helper (converted from SM3AttackHDDefault)."""

from __future__ import annotations

from sm3.SM3 import SM3

_MASK32 = 0xFFFFFFFF


def _hw(value: int) -> int:
    result = 0
    while value > 0:
        if value & 1:
            result += 1
        value >>= 1
    return result


class SM3AttackHDDefault:
    """Computes hypothetical intermediate values for SM3 HD/CPA attack."""

    module = None
    dataLength = 0
    round = 0
    keynum = 0
    track = 0
    T1 = SM3.T1
    roundKeyone = 0
    roundKeytwo = 0
    roundKeythree = 0
    Key: list[int] = []
    X: list[int] = []
    Y: list[int] = []

    def GetMidDataHW(self, data: bytes | bytearray | None) -> list[float]:
        selected = [0.0] * self.dataLength

        if self.round > 3 or data is None:
            return selected

        mdata = bytearray(32)
        mdata[:32] = data[:32]

        newbyte = SM3.byteArrayFormatData(mdata)
        m_count = len(newbyte) // 64

        for i in range(64):
            self.Y[i] = 0

        for pos in range(m_count):
            for j in range(16):
                self.X[j] = SM3.byteArrayTolong(newbyte, pos * 64 + j * 4)

        for t1 in range(16, 68):
            self.X[t1] = SM3._u32(
                SM3.P1(self.X[t1 - 16] ^ self.X[t1 - 9] ^ SM3.ROL(self.X[t1 - 3], 15))
                ^ SM3.ROL(self.X[t1 - 13], 7)
                ^ self.X[t1 - 6]
            )

        for t0 in range(64):
            self.Y[t0] = SM3._u32(self.X[t0] ^ self.X[t0 + 4])

        s_in = 0
        keynum = self.keynum

        if keynum == 0:
            s_in = self.Y[0]
        elif keynum == 1:
            s_in = self.X[0]
        elif keynum == 2:
            s_in = (self.Key[0] + self.Y[0]) & _MASK32
        elif keynum == 3:
            s_in = SM3.P0(self.Key[1] + self.X[0]) & _MASK32
        elif keynum == 4:
            b1 = self.Key[2]
            a1 = self.Key[0] + self.Y[0]
            s_in = b1 ^ a1
        elif keynum == 5:
            b1_temp = self.Key[2]
            a1_temp = self.Key[0] + self.Y[0]
            c1_temp = SM3.ROL(self.Key[4], 9)
            ss1_5 = (SM3.ROL(a1_temp, 12) + SM3.P0(self.Key[1] + self.X[0]) + SM3.ROL(self.T1, 1)) & _MASK32
            ss1_5 = SM3.ROL(ss1_5, 7) & _MASK32
            ss2_5 = (ss1_5 ^ SM3.ROL(a1_temp, 12)) & _MASK32
            s_in = SM3.FF1(a1_temp, b1_temp, c1_temp) + ss2_5 + self.Y[1]
        elif keynum == 6:
            ss1_6 = (SM3.ROL(self.Key[2], 12) + self.Key[3] + SM3.ROL(self.T1, 0)) & _MASK32
            ss1_6 = SM3.ROL(ss1_6, 7) & _MASK32
            ss2_6 = (ss1_6 ^ SM3.ROL(self.Key[2], 12)) & _MASK32
            s_in = SM3.FF1(self.Key[2], self.Key[4], self.Key[5]) + ss2_6 + self.Y[0]
        elif keynum == 7:
            e1 = SM3.P0(self.Key[1] + self.X[0])
            f1 = self.Key[3]
            s_in = e1 ^ f1 & _MASK32
        elif keynum == 8:
            a1temp0 = self.Key[0] + self.Y[0]
            ss1_9 = (SM3.ROL(a1temp0, 12) + SM3.P0(self.Key[1] + self.X[0]) + SM3.ROL(self.T1, 1)) & _MASK32
            ss1_9 = SM3.ROL(ss1_9, 7) & _MASK32
            e1_9 = SM3.P0(self.Key[1] + self.X[0])
            f1_9 = self.Key[3]
            g1_9 = SM3.ROL(self.Key[7], 19)
            s_in = SM3.GG1(e1_9, f1_9, g1_9) + ss1_9 + self.X[1]
        elif keynum == 9:
            a0 = self.Key[2]
            e0 = self.Key[3]
            f0 = self.Key[7]
            g0 = self.Key[8]
            ss1 = (SM3.ROL(a0, 12) + e0 + SM3.ROL(self.T1, 0)) & _MASK32
            ss1 = SM3.ROL(ss1, 7) & _MASK32
            s_in = SM3.GG1(e0, f0, g0) + ss1 + self.X[0]

        s_in &= _MASK32
        round_shift = self.round * 8

        for i in range(256):
            if keynum in (0, 1, 5, 6, 8, 9):
                s_out = (
                    (i << round_shift)
                    + self.roundKeyone
                    + (self.roundKeytwo << 8)
                    + (self.roundKeythree << 16)
                    + s_in
                ) & _MASK32
            else:
                s_out = (
                    (i << round_shift)
                    ^ self.roundKeyone
                    ^ (self.roundKeytwo << 8)
                    ^ (self.roundKeythree << 16)
                    ^ s_in
                ) & _MASK32

            s_out = (s_out >> round_shift) & _MASK32

            if self.track < 8:
                selected[i] = float(2 * ((s_out >> self.track) & 1) - 1)
            elif self.track == 8:
                selected[i] = float(_hw(s_out & 0xFF))

        return selected
