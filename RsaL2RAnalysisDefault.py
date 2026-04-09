from __future__ import annotations


class RsaL2RAnalysisDefault:
    """Python version of template/RsaL2RAnalysisDefault.java."""

    def __init__(self) -> None:
        self.dataLength = 0
        self.dataBytes = 0
        self.keys = 0
        self.ExpGuess0 = 0
        self.ExpGuess1 = 0
        self.modN = 0
        self.Exp0Result = 0
        self.Exp1Result = 0

    @staticmethod
    def BytetoUnsignedBigInteger(data: bytes, offset: int, length: int) -> int:
        return int.from_bytes(data[offset : offset + length], "big", signed=False)

    @staticmethod
    def GetHW(buf: bytes, idx: int) -> float:
        if idx < 0 or idx >= len(buf):
            return 0.0
        return float(int(buf[idx]).bit_count())

    def GetMidDataHW(self, data: bytes) -> list[float]:
        mid_data_hw = [0.0] * self.dataLength
        m = self.BytetoUnsignedBigInteger(data, 0, self.dataBytes)
        self.Exp0Result = pow(m, self.ExpGuess0, self.modN)
        self.Exp1Result = pow(m, self.ExpGuess1, self.modN)
        exp0_res_b = self.Exp0Result.to_bytes((self.Exp0Result.bit_length() + 7) // 8 or 1, "big")
        exp1_res_b = self.Exp1Result.to_bytes((self.Exp1Result.bit_length() + 7) // 8 or 1, "big")
        exp0_idx = len(exp0_res_b) - self.dataBytes
        exp1_idx = len(exp1_res_b) - self.dataBytes
        for i in range(self.keys):
            mid_data_hw[2 * i] = self.GetHW(exp0_res_b, exp0_idx)
            mid_data_hw[2 * i + 1] = self.GetHW(exp1_res_b, exp1_idx)
            exp0_idx += 1
            exp1_idx += 1
        return mid_data_hw

