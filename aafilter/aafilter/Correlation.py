import math
import tkinter as tk
from tkinter import ttk, messagebox
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
        self.NO_TRACE = -1
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

        centerPanel = ttk.Frame(self.window)
        centerPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        trackPanel = ttk.LabelFrame(centerPanel, text="比特位")
        trackPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.bitGroupTextField = ttk.Entry(trackPanel, width=10)
        self.bitGroupTextField.insert(0, str(self.bitGroup))
        self.bitGroupTextField.pack(padx=5, pady=5)

        rangePanel = ttk.LabelFrame(centerPanel, text="范围")
        rangePanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Label(rangePanel, text="起点: ").pack(side=tk.LEFT, padx=2)
        self.firstTextField = ttk.Entry(rangePanel, width=8)
        self.firstTextField.pack(side=tk.LEFT, padx=2)

        ttk.Label(rangePanel, text="数量: ").pack(side=tk.LEFT, padx=2)
        self.numberTextField = ttk.Entry(rangePanel, width=8)
        self.numberTextField.pack(side=tk.LEFT, padx=2)

        centerPanel.configure(width=300, height=120)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return centerPanel

    def setDialogValues(self, t=None, nt=0, sft=0, snt=0, sfs=0, sns=0):
        if t is not None and t.data is not None:
            self.traceDataLength = len(t.data) * 8
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
        self.bitGroup = self.parseInt(self.bitGroupTextField, self.BIT_GROUP)
        self.traceOffset = self.parseInt(self.firstTextField, self.TRACE_OFFSET)
        self.dataLength = self.parseInt(self.numberTextField, self.DATA_LENGTH)

    def parseInt(self, textField, key):
        try:
            return int(textField.get())
        except ValueError:
            return 0

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

    def initProcessTrace(self, t):
        if t is None or t.getSample() is None or t.getNumberOfSamples() == 0 or t.data is None or len(t.data) == 0:
            return False
        self.numberOfSamples = t.getNumberOfSamples()
        if self.traceDataLength != len(t.data) * 8:
            self.traceDataLength = len(t.data) * 8
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

    def analyze(self, t):
        if not self.memoryReady and not self.initProcessTrace(t):
            self.err("错误:在此曲线设置上不能运行的相关性")
            return self.NO_TRACE
        data = self.select(t)
        if data is None or t.getSample() is None:
            return self.NO_TRACE
        for i in range(len(data)):
            self.d[i] += data[i]
            self.d2[i] += data[i] * data[i]
        for i in range(t.getNumberOfSamples()):
            if self.aborted:
                break
            f = t.getSample(i)
            self.s[i] += f
            self.s2[i] += f * f
            k = i
            for j in range(len(data)):
                self.sd[k] += f * data[j]
                k += t.getNumberOfSamples()
        self.numberOfAnalyzedTraces += 1
        if self.currentTraceIndex < self.lastTraceIndex and self.lastTraceIndex != 0:
            self.currentTraceIndex += 1
            return self.currentTraceIndex
        self.currentTraceIndex = self.NO_TRACE
        return self.NO_TRACE

    def select(self, t):
        return self.selectFromData(t.getData())

    def selectFromData(self, data):
        selected = [0.0] * self.dataLength
        if data is None:
            return selected
        if self.bitGroup > 1:
            for i in range(self.dataLength):
                bitOffset = (i + self.traceOffset) * self.bitGroup
                for j in range(self.bitGroup):
                    selected[i] += self.getBit(data, bitOffset + j)
        else:
            for i in range(self.dataLength):
                selected[i] = self.getBit(data, i + self.traceOffset)
        return selected

    def getBit(self, in_data, offset):
        if offset < 0 or offset >= len(in_data) * 8:
            return 0
        return (in_data[offset // 8] >> (7 - (offset % 8))) & 1

    def generate(self, index):
        f = [0.0] * self.numberOfSamples
        j = index * self.numberOfSamples
        for i in range(self.numberOfSamples):
            f[i] = self.sampleDataCorrelation[j]
            j += 1
        return Trace(None, None, f)

    def finishProcess(self):
        if self.numberOfAnalyzedTraces == 0:
            return
        for i in range(self.numberOfSamples):
            self.sampleDeviation[i] = math.sqrt(self.s2[i] - self.s[i] * self.s[i] / self.numberOfAnalyzedTraces)
        for i in range(self.dataLength):
            self.dataDeviation[i] = math.sqrt(self.d2[i] - self.d[i] * self.d[i] / self.numberOfAnalyzedTraces)
            k = i * self.numberOfSamples
            for j in range(self.numberOfSamples):
                if self.dataDeviation[i] == 0 or self.sampleDeviation[j] == 0:
                    self.sampleDataCorrelation[k] = 0.0
                else:
                    self.sampleDataCorrelation[k] = (self.sd[k] - self.s[j] * self.d[
                        i] / self.numberOfAnalyzedTraces) / (self.dataDeviation[i] * self.sampleDeviation[j])
                k += 1
        self.numberOfResultTraces = self.dataLength

    @staticmethod
    def computeCorrelation(x, xOffset, xStep, y, yOffset, yStep, length):
        sx = 0.0
        sx2 = 0.0
        sy = 0.0
        sy2 = 0.0
        sxy = 0.0
        if length < 1:
            return 0.0
        p = xOffset
        q = yOffset
        for i in range(length):
            sx += x[p]
            sx2 += x[p] * x[p]
            sy += y[q]
            sy2 += y[q] * y[q]
            sxy += x[p] * y[q]
            p += xStep
            q += yStep
        xVar = sx2 - sx * sx / length
        yVar = sy2 - sy * sy / length
        if xVar == 0 or yVar == 0:
            return 0.0
        return (sxy - sx * sy / length) / math.sqrt(xVar * yVar)

    @staticmethod
    def computeVariance(x, offset, length, step):
        sx = 0.0
        sx2 = 0.0
        if length < 1:
            return 0.0
        j = offset
        for i in range(length):
            sx += x[j]
            sx2 += x[j] * x[j]
            j += step
        return (sx2 - sx * sx / length) / (length - 1)

    def ok_clicked(self):
        if self.checkDialogValues():
            self.getDialogValues()
            if self.window:
                self.window.destroy()

    def cancel_clicked(self):
        if self.window:
            self.window.destroy()

    def checkDialogValues(self):
        message = []
        if self.bitGroupTextField.get().strip() == "":
            message.append("请输入比特位!")
        elif self.bitGroup < 1 or self.bitGroup > self.traceDataLength:
            message.append(f"比特位的可选范围是:1--{self.traceDataLength}")
            messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
            return False
        if self.numberTextField.get().strip() == "":
            message.append("请输入数量!")
        if self.firstTextField.get().strip() == "":
            message.append("请输入起点!")
        elif self.traceOffset < 0 or self.dataLength < 1:
            message.append("起点小于0或者数量范围小于1")
        elif (self.dataLength + self.traceOffset) > self.traceDataLength // self.bitGroup:
            message.append(f"起点+数量范围[1,{self.traceDataLength // self.bitGroup}]")
        if len(message) == 0:
            return True
        messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
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