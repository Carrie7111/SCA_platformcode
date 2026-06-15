# -*- coding: utf-8 -*-
def byte_to_unsigned_bigint(data: bytes, offset: int, length: int) -> int:
    slice_data = data[offset:offset + length]
    return int.from_bytes(slice_data, byteorder='big', signed=False)

def get_hw_bytes(arr: bytes, index: int) -> float:
    if index < 0 or index >= len(arr):
        return 0.0
    byte_val = arr[index] & 0xFF
    return bin(byte_val).count('1')

class RsaR2LAnalysisDefault:
    def __init__(self):
        self.dataLength = 256
        self.dataBytes = 16
        self.keys = 128
        self.ExpGuess0 = 0
        self.ExpGuess1 = 0
        self.modN = 0
        self.Exp0Result = 0
        self.Exp1Result = 0

    def GetMidDataHW(self, data: bytes) -> list[float]:
        MidDataHW = [0.0] * self.dataLength
        M = byte_to_unsigned_bigint(data, 0, self.dataBytes)

        self.Exp0Result = pow(M, self.ExpGuess0, self.modN)
        self.Exp1Result = pow(M, self.ExpGuess1, self.modN)

        Exp0ResB = self.Exp0Result.to_bytes((self.Exp0Result.bit_length() + 7) // 8 or 1, byteorder='big')
        Exp1ResB = self.Exp1Result.to_bytes((self.Exp1Result.bit_length() + 7) // 8 or 1, byteorder='big')

        idx0 = len(Exp0ResB) - self.dataBytes
        idx1 = len(Exp1ResB) - self.dataBytes

        for i in range(self.keys):
            MidDataHW[2 * i] = get_hw_bytes(Exp0ResB, idx0)
            MidDataHW[2 * i + 1] = get_hw_bytes(Exp1ResB, idx1)
            idx0 += 1
            idx1 += 1

        return MidDataHW