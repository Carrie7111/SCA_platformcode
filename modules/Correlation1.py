import math
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from typing import Optional, List


class Correlation:
    BIT_GROUP = "bit.group"
    DATA_LENGTH = "data.length"
    TRACE_OFFSET = "trace.offset"

    def __init__(self):
        self.firstTextField = None
        self.numberTextField = None
        self.bitGroupTextField = None
        self.s = None
        self.s2 = None
        self.d = None
        self.d2 = None
        self.sd = None
        self.dataDeviation = None
        self.sampleDeviation = None
        self.sampleDataCorrelation = None
        self.bitGroup = 1
        self.traceDataLength = 0
        self.dataLength = 0
        self.memoryReady = False
        self.moduleTitle = "Correlation"
        self.prefix = "Correlation between data and samples"
        self.moduleDescription = "计算数据和样本的相关性"
        self.moduleVersion = "1.81"
        self.selectWindow = False
        self.helpFile = "doc/manual/modulesCorrelation.html"
        self.traceOffset = 0
        self.numberOfSamples = 0
        self.numberOfAnalyzedTraces = 0
        self.currentTraceIndex = -1
        self.lastTraceIndex = 0
        self.aborted = False
        self.globalTitle = ""
        self.yScale = 1.0
        self.yLabel = ""
        self.xOffset = 0
        self.firstSampleIndex = 0
        self.sampleCoding = 20
        self.numberOfResultTraces = 0
        self.window = None

    def initModule(self):
        self.moduleTitle = "Correlation"
        self.prefix = "Correlation between data and samples"
        self.moduleDescription = "计算数据和样本的相关性"
        self.moduleVersion = "1.81"
        self.selectWindow = False
        self.helpFile = "doc/manual/modulesCorrelation.html"
        self.bitGroup = 1
        self.dataLength = 0
        self.traceOffset = 0
        self.set(self.BIT_GROUP, self.bitGroup)
        self.set(self.DATA_LENGTH, self.dataLength)
        self.set(self.TRACE_OFFSET, self.traceOffset)

    def set(self, key, value):
        if key == self.BIT_GROUP:
            self.bitGroup = value
        elif key == self.DATA_LENGTH:
            self.dataLength = value
        elif key == self.TRACE_OFFSET:
            self.traceOffset = value

    def get(self, key):
        if key == self.BIT_GROUP:
            return self.bitGroup
        elif key == self.DATA_LENGTH:
            return self.dataLength
        elif key == self.TRACE_OFFSET:
            return self.traceOffset
        return None

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("相关性")

        var1 = ttk.Frame(self.window)
        var1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        var2 = ttk.LabelFrame(var1, text="比特位")
        var2.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.bitGroupTextField = ttk.Entry(var2, width=10)
        self.bitGroupTextField.insert(0, str(self.bitGroup))
        self.bitGroupTextField.pack(padx=5, pady=5)

        var3 = ttk.LabelFrame(var1, text="范围")
        var3.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Label(var3, text="起点: ").pack(side=tk.LEFT, padx=2)
        self.firstTextField = ttk.Entry(var3, width=8)
        self.firstTextField.pack(side=tk.LEFT, padx=2)

        ttk.Label(var3, text="数量: ").pack(side=tk.LEFT, padx=2)
        self.numberTextField = ttk.Entry(var3, width=8)
        self.numberTextField.pack(side=tk.LEFT, padx=2)

        var1.configure(width=300, height=120)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return var1

    def setDialogValues(self, var1=None, var2=0, var3=0, var4=0, var5=0, var6=0):
        if var1 is not None and var1.data is not None:
            self.traceDataLength = len(var1.data) * 8
        else:
            self.traceDataLength = 0

        self.traceOffset = self.getInt(self.TRACE_OFFSET)
        self.bitGroup = self.getInt(self.BIT_GROUP)
        if self.traceDataLength != 0 and (self.traceDataLength < self.bitGroup or self.bitGroup < 1):
            self.set(self.BIT_GROUP, 1)
            self.bitGroup = 1
        if self.traceDataLength != 0 and self.traceDataLength < self.traceOffset + self.bitGroup:
            self.set(self.TRACE_OFFSET, 0)
            self.traceOffset = 0
        self.dataLength = self.getInt(self.DATA_LENGTH)
        if self.traceDataLength != 0 and (
                self.dataLength <= 0 or (self.dataLength + self.traceOffset) * self.bitGroup > self.traceDataLength):
            self.set(self.DATA_LENGTH, self.traceDataLength // self.bitGroup - self.traceOffset)
            self.dataLength = self.traceDataLength // self.bitGroup - self.traceOffset
        self.setInt(self.firstTextField, self.TRACE_OFFSET)
        self.setInt(self.bitGroupTextField, self.BIT_GROUP)
        self.setInt(self.numberTextField, self.DATA_LENGTH)

    def getInt(self, key):
        if key == self.TRACE_OFFSET:
            return self.traceOffset
        elif key == self.BIT_GROUP:
            return self.bitGroup
        elif key == self.DATA_LENGTH:
            return self.dataLength
        return 0

    def setInt(self, textField, key):
        try:
            value = int(textField.get())
            self.set(key, value)
        except ValueError:
            pass

    def getDialogValues(self):
        try:
            self.bitGroup = int(self.bitGroupTextField.get())
        except ValueError:
            self.bitGroup = 1
        try:
            self.traceOffset = int(self.firstTextField.get())
        except ValueError:
            self.traceOffset = 0
        try:
            self.dataLength = int(self.numberTextField.get())
        except ValueError:
            self.dataLength = 0

    def getRequiredMemorySize(self):
        return 8 * (2 * self.numberOfSamples + 2 * self.dataLength + self.numberOfSamples * self.dataLength)

    def initProcess(self):
        if self.bitGroup == 1:
            self.globalTitle = "位"
        elif self.bitGroup == 8:
            self.globalTitle = "字节"
        else:
            self.globalTitle = f"{self.bitGroup}-bit data group"
        self.yScale = 1.0
        self.yLabel = ""
        self.memoryReady = False
        self.xOffset = self.firstSampleIndex
        return True

    def initProcessTrace(self, var1):
        if var1 is not None and var1.getSample() is not None and var1.getNumberOfSamples() != 0 and var1.data is not None and len(
                var1.data) != 0:
            self.numberOfSamples = var1.getNumberOfSamples()
            if self.traceDataLength != len(var1.data) * 8:
                self.traceDataLength = len(var1.data) * 8
                if self.bitGroup > self.traceDataLength and self.traceDataLength > 0:
                    self.bitGroup = self.traceDataLength
                    self.set(self.BIT_GROUP, self.bitGroup)
                if self.traceDataLength != 0 and self.traceDataLength < self.traceOffset + self.bitGroup:
                    self.set(self.TRACE_OFFSET, 0)
                    self.traceOffset = 0
            self.s = [0.0] * self.numberOfSamples
            self.s2 = [0.0] * self.numberOfSamples
            self.d = [0.0] * self.dataLength
            self.d2 = [0.0] * self.dataLength
            self.sd = [0.0] * (self.numberOfSamples * self.dataLength)
            self.dataDeviation = self.d2
            self.sampleDeviation = self.s2
            self.sampleDataCorrelation = self.sd
            self.memoryReady = True
            self.sampleCoding = 20
            return True
        else:
            return False

    def analyze(self, var1):
        if not self.memoryReady and not self.initProcessTrace(var1):
            self.err("错误:在此曲线设置上不能运行的相关性")
            return -1
        var2 = self.select(var1)
        if var2 is not None and var1.getSample() is not None:
            for var3 in range(len(var2)):
                self.d[var3] += var2[var3]
                self.d2[var3] += var2[var3] * var2[var3]
            for var8 in range(var1.getNumberOfSamples()):
                if self.aborted:
                    break
                var4 = var1.getSample(var8)
                self.s[var8] += var4
                self.s2[var8] += var4 * var4
                var6 = 0
                var7 = var8
                while var6 < len(var2):
                    self.sd[var7] += var4 * var2[var6]
                    var6 += 1
                    var7 += var1.getNumberOfSamples()
            self.numberOfAnalyzedTraces += 1
            if self.currentTraceIndex < self.lastTraceIndex and self.lastTraceIndex != 0:
                self.currentTraceIndex += 1
                return self.currentTraceIndex
            else:
                self.currentTraceIndex = -1
                return -1
        else:
            return -1

    def select(self, var1):
        return self.selectFromData(var1.getData())

    def selectFromData(self, var1):
        var2 = [0.0] * self.dataLength
        if var1 is None:
            return var2
        if self.bitGroup > 1:
            for var3 in range(self.dataLength):
                var4 = (var3 + self.traceOffset) * self.bitGroup
                for var5 in range(self.bitGroup):
                    var2[var3] += self.getBit(var1, var4 + var5)
        else:
            for var6 in range(self.dataLength):
                var2[var6] = self.getBit(var1, var6 + self.traceOffset)
        return var2

    def getBit(self, var1, var2):
        if var2 >= 0 and var2 < len(var1) * 8:
            return (var1[var2 // 8] >> (7 - var2 % 8)) & 1
        return 0

    def generate(self, var1):
        var2 = [0.0] * self.numberOfSamples
        var3 = 0
        var4 = var1 * self.numberOfSamples
        while var3 < self.numberOfSamples:
            var2[var3] = self.sampleDataCorrelation[var4]
            var3 += 1
            var4 += 1
        return Trace(None, None, var2)

    def finishProcess(self):
        if self.numberOfAnalyzedTraces != 0:
            for var1 in range(self.numberOfSamples):
                self.sampleDeviation[var1] = math.sqrt(
                    self.s2[var1] - self.s[var1] * self.s[var1] / self.numberOfAnalyzedTraces)
            for var4 in range(self.dataLength):
                self.dataDeviation[var4] = math.sqrt(
                    self.d2[var4] - self.d[var4] * self.d[var4] / self.numberOfAnalyzedTraces)
                var2 = 0
                var3 = var4 * self.numberOfSamples
                while var2 < self.numberOfSamples:
                    if self.dataDeviation[var4] != 0.0 and self.sampleDeviation[var2] != 0.0:
                        self.sampleDataCorrelation[var3] = (self.sd[var3] - self.s[var2] * self.d[
                            var4] / self.numberOfAnalyzedTraces) / (self.dataDeviation[var4] * self.sampleDeviation[
                            var2])
                    else:
                        self.sampleDataCorrelation[var3] = 0.0
                    var2 += 1
                    var3 += 1
            self.numberOfResultTraces = self.dataLength

    @staticmethod
    def computeCorrelation(var0, var1, var2, var3, var4, var5, var6):
        var7 = 0.0
        var9 = 0.0
        var11 = 0.0
        var13 = 0.0
        var15 = 0.0
        if var6 < 1:
            return 0.0
        var17 = 0
        var18 = var1
        var19 = var4
        while var17 < var6:
            var7 += var0[var18]
            var9 += var0[var18] * var0[var18]
            var11 += var3[var19]
            var13 += var3[var19] * var3[var19]
            var15 += var0[var18] * var3[var19]
            var17 += 1
            var18 += var2
            var19 += var5
        var21 = var9 - var7 * var7 / var6
        var22 = var13 - var11 * var11 / var6
        if var21 != 0.0 and var22 != 0.0:
            return (var15 - var7 * var11 / var6) / math.sqrt(var21 * var22)
        else:
            return 0.0

    @staticmethod
    def computeVariance(var0, var1, var2, var3):
        var4 = 0.0
        var6 = 0.0
        if var2 < 1:
            return 0.0
        var8 = 0
        var9 = var1
        while var8 < var2:
            var4 += var0[var9]
            var6 += var0[var9] * var0[var9]
            var8 += 1
            var9 += var3
        return (var6 - var4 * var4 / var2) / (var2 - 1)

    def ok_clicked(self):
        if self.checkDialogValues():
            self.getDialogValues()
            if self.window:
                self.window.destroy()

    def cancel_clicked(self):
        if self.window:
            self.window.destroy()

    def checkDialogValues(self):
        var1 = []
        if self.bitGroupTextField.get().strip() == "":
            var1.append("请输入比特位!")
        elif self.bitGroup < 1 or self.bitGroup > self.traceDataLength:
            var1.append(f"比特位的可选范围是:1--{self.traceDataLength}")
            messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(var1))
            return False
        if self.numberTextField.get().strip() == "":
            var1.append("请输入数量!")
        if self.firstTextField.get().strip() == "":
            var1.append("请输入起点!")
        elif self.traceOffset >= 0 and self.dataLength >= 1:
            if self.dataLength + self.traceOffset > self.traceDataLength // self.bitGroup:
                var1.append(f"起点+数量范围[1,{self.traceDataLength // self.bitGroup}]")
        else:
            var1.append("起点小于0或者数量范围小于1")
        if len(var1) == 0:
            return True
        else:
            messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(var1))
            return False

    def err(self, message):
        print(message)


class Trace:
    def __init__(self, title="", data=None, samples=None, sampleFrequency=1.0):
        self.title = title
        self.data = data
        self.samples = samples
        self.sampleFrequency = sampleFrequency

    def getNumberOfSamples(self):
        if self.samples is not None:
            return len(self.samples)
        return 0

    def getSample(self, index):
        if self.samples is not None and index < len(self.samples):
            return self.samples[index]
        return 0.0

    def getData(self):
        return self.data


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Correlation()
    app.initModule()
    app.initDialog()
    root.mainloop()