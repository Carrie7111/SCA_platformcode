# 1. 去掉Java包导入，直接定义父类（如果需要）
class AesSinAnalysisBase:
    def GetHW(self, x):
        # 补全汉明重量计算方法（原Java的GetHW逻辑）
        return bin(x).count("1")


# 2. 去掉Java注解（Python没有对应注解，用注释保留）
# @ModuleDesc(pkgName="AES", name="AES S盒输入攻击分析", desc="", isVisible=True)
class AesSinAnalysisDefault(AesSinAnalysisBase):
    # 3. 函数名改成Python蛇形命名（符合PEP8，消除规范提示）
    def get_mid_data_hw(self, data):
        if data is None:
            return None

        mid_data_hw = [0.0] * 4096
        tem = [0] * 16

        for i in range(256):
            for j in range(16):
                tem[j] = data[j] ^ i

            for j in range(16):
                s_in = tem[j]
                mid_data_hw[i + 256 * j] = self.get_hw(s_in & 0xFF)

        return mid_data_hw

    # 4. 补全GetHW方法（对应原Java的GetHW）
    def get_hw(self, x):
        return bin(x).count("1")