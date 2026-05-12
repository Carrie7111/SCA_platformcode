class AesSinAnalysisDefault(AesSinAnalysisBase):
    """
    AES S盒输入攻击分析
    功能：计算猜测密钥下S盒输入的汉明重量，与原Java代码完全一致
    """

    def GetMidDataHW(self, data):
        """
        与Java方法功能、逻辑、返回值完全相同
        :param data: 字节数组 (bytes/bytearray)
        :return: 长度为4096的float数组，存储汉明重量
        """
        # 与Java一致：输入为空直接返回None
        if data is None:
            return None

        # 初始化长度4096的浮点数组（Java: float[] MidDataHW = new float[4096]）
        MidDataHW = [0.0] * 4096
        # 初始化长度16的临时字节数组（Java: byte[] tem = new byte[16]）
        tem = bytearray(16)

        # 外层循环：猜测密钥 i 0~255（与Java完全一致）
        for i in range(256):
            # 第一步：data[j] ^ i 赋值到tem[j]
            for j in range(16):
                tem[j] = data[j] ^ i

            # 第二步：计算每个S盒输入的汉明重量
            for j in range(16):
                s_in = tem[j]
                # 索引计算：i + 256 * j （与Java完全一致）
                index = i + 256 * j
                # (s_in & 0xFF) 保证无符号计算 → 调用汉明重量方法
                MidDataHW[index] = float(self.GetHW(s_in & 0xFF))

        return MidDataHW

    # 汉明重量计算方法（原Java父类AesSinAnalysisBase中的方法，补充实现保证代码可独立运行）
    def GetHW(self, value):
        """
        计算一个字节的汉明重量（二进制中1的个数）
        :param value: 无符号字节 0~255
        :return: 汉明重量 int
        """
        return bin(value).count('1')


# ==================== 基类模拟（原Java: AesSinAnalysisBase）====================
class AesSinAnalysisBase:
    pass