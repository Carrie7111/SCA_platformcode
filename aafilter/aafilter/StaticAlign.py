import os
import re
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List


class AlignModule:
    REF = "ref"
    SAVE_FILE_NAME = "save.file.name"
    REF_FILE_PATH = "ref.file.path"
    ACTION = "action"

    def __init__(self):
        self.ref = 0
        self.action = 0
        self.refFilePath = ""
        self.saveFileName = "shifts.txt"
        self.externalRefTrace = False
        self.refTrace = None
        self.traceSetPath = ""
        self.workPath = ""
        self.modulePath = ""
        self.path = ""
        self.autoReload = True
        self.firstTraceIndex = 0
        self.numberOfTraces = 0
        self.numberOfSamples = 0
        self.firstSampleIndex = 0
        self.xScale = 1.0
        self.yScale = 1.0
        self.xLabel = ""
        self.yLabel = ""
        self.logScale = False
        self.sampleFrequency = 0.0
        self.numberOfResultTraces = 0
        self.resultTrace = None
        self.currentTraceIndex = -1
        self.lastTraceIndex = -1
        self.aborted = False
        self.operation = None
        self.refSelectButton = None
        self.refNameTextField = None
        self.useCurrentCheckBox = None
        self.refTextField = None
        self.optionsPanel = None
        self.tracesPanel = None
        self.samplesPanel = None
        self.scopePanel = None
        self.window = None
        self.NO_TRACE = -1

    def initModule(self):
        pass

    def initDialog(self):
        pass

    def setDialogValues(self, t=None, nt=0, sft=0, snt=0, sfs=0, sns=0):
        pass

    def updateEnabledPanels(self):
        pass

    def err(self, message):
        print(message)

    def out(self, message):
        print(message)

    def getInt(self, key):
        return 0

    def setInt(self, textField, key):
        pass

    def setFloat(self, textField, key, decimals):
        pass

    def setString(self, textField, key):
        pass

    def parseFloat(self, textField, key):
        try:
            return float(textField.get())
        except ValueError:
            return 0.0

    def parseInt(self, textField, key):
        try:
            return int(textField.get())
        except ValueError:
            return 0

    def closePw(self):
        pass

    def closeBr(self):
        pass

    def finalize(self):
        pass


class Data:
    def __init__(self, data):
        self.data = data

    def getDoubleData(self):
        return self.data


class Operation:
    def createData(self, data):
        return Data(data)

    def r2hc(self, data):
        n = len(data.data)
        result = [0.0] * n
        for i in range(n):
            result[i] = data.data[i]
        return Data(result)

    def hc2r(self, data):
        n = len(data.data)
        result = [0.0] * n
        for i in range(n):
            result[i] = data.data[i]
        return Data(result)

    def normalize(self, data, size):
        n = len(data.data)
        result = [0.0] * n
        for i in range(n):
            result[i] = data.data[i] / size
        return Data(result)


class StaticAlign(AlignModule):
    SHIFT = "shift"
    THRESHOLD = "threshold"

    def __init__(self):
        super().__init__()
        self.shiftTextField = None
        self.thresholdTextField = None
        self.shiftResult = None
        self.shiftMax = 100
        self.first = 0
        self.selStart = 0
        self.selLength = 0
        self.selEnd = 0
        self.refStart = 0
        self.refEnd = 0
        self.refLength = 0
        self.selSize = 0
        self.shifts = 0
        self.ns = 0
        self.depth = 0
        self.threshold = 0.95
        self.refTraceFrequency = None
        self.testSample = None
        self.sy = None
        self.s2y = None
        self.sr = 0.0
        self.s2r = 0.0
        self.initialized = False
        self.bestShift = 0
        self.seq = None
        self.pw = None
        self.init = False
        self.line = None
        self.br = None
        self.bestCorr = 0.0
        self.align = None
        self.chained = False
        self.moduleTitle = "Align"
        self.moduleDescription = "Align multiple traces"
        self.moduleVersion = "1.7"
        self.helpFile = "doc/manual/modulesStaticAlign.html"
        self.operation = Operation()

    def initModule(self):
        self.moduleTitle = "Align"
        self.moduleDescription = "Align multiple traces"
        self.helpFile = "doc/manual/modulesStaticAlign.html"
        self.moduleVersion = "1.7"
        self.shiftMax = 100
        self.threshold = 0.95
        self.pw = None
        self.lastTraceIndex = -1
        self.shiftResult = None
        self.set(self.SHIFT, self.shiftMax)
        self.set(self.THRESHOLD, self.threshold)

    def set(self, key, value):
        if key == self.SHIFT:
            self.shiftMax = value
        elif key == self.THRESHOLD:
            self.threshold = value
        elif key == self.REF:
            self.ref = value
        elif key == self.SAVE_FILE_NAME:
            self.saveFileName = value
        elif key == self.REF_FILE_PATH:
            self.refFilePath = value
        elif key == self.ACTION:
            self.action = value

    def get(self, key):
        if key == self.SHIFT:
            return self.shiftMax
        elif key == self.THRESHOLD:
            return self.threshold
        elif key == self.REF:
            return self.ref
        elif key == self.SAVE_FILE_NAME:
            return self.saveFileName
        elif key == self.REF_FILE_PATH:
            return self.refFilePath
        elif key == self.ACTION:
            return self.action
        return None

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("静态对齐")

        centerPanel = ttk.Frame(self.window)
        centerPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        staticPanel = ttk.Frame(centerPanel)
        staticPanel.pack(fill=tk.X, pady=5)

        shiftPanel = ttk.LabelFrame(staticPanel, text="位移最大量")
        shiftPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.shiftTextField = ttk.Entry(shiftPanel, width=10)
        self.shiftTextField.insert(0, str(self.shiftMax))
        self.shiftTextField.pack(padx=5, pady=5)

        thresholdPanel = ttk.LabelFrame(staticPanel, text="阈值")
        thresholdPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.thresholdTextField = ttk.Entry(thresholdPanel, width=10)
        self.thresholdTextField.insert(0, str(self.threshold))
        self.thresholdTextField.pack(padx=5, pady=5)

        self.optionsPanel = centerPanel
        centerPanel.configure(width=300, height=200)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return centerPanel

    def actionPerformed(self, e=None):
        src = e
        if src == self.refSelectButton:
            try:
                selectedFile = filedialog.askopenfilename(
                    title="选择曲线集",
                    initialdir=self.traceSetPath,
                    filetypes=[("TRS files", "*.trs"), ("All files", "*.*")]
                )
                if selectedFile:
                    self.refFilePath = selectedFile
                    self.set(self.REF_FILE_PATH, self.refFilePath)
                    if self.refNameTextField:
                        self.refNameTextField.delete(0, tk.END)
                        self.refNameTextField.insert(0, os.path.basename(selectedFile))
                    if self.useCurrentCheckBox:
                        self.useCurrentCheckBox.state(['!selected'])
                        self.useCurrentCheckBox.config(state='normal')
                    self.externalRefTrace = True
            except Exception as exc:
                self.err("错误:无法加载参考曲线！")
                print(exc)
        if src == self.useCurrentCheckBox:
            self.refFilePath = ""
            self.set(self.REF_FILE_PATH, self.refFilePath)
            if self.refNameTextField:
                self.refNameTextField.delete(0, tk.END)
                self.refNameTextField.insert(0, "")
            if self.useCurrentCheckBox:
                self.useCurrentCheckBox.config(state='disabled')
            self.externalRefTrace = False
        self.updateEnabledPanels()

    def updateEnabledPanels(self):
        if self.action != 2:
            if self.thresholdTextField:
                self.thresholdTextField.config(state='normal')
            if self.shiftTextField:
                self.shiftTextField.config(state='normal')
        else:
            if self.thresholdTextField:
                self.thresholdTextField.config(state='disabled')
            if self.shiftTextField:
                self.shiftTextField.config(state='disabled')

    def loadRefFile(self, fileName):
        if fileName is None or len(fileName) == 0:
            return None
        ts = TraceSet(fileName)
        if self.ref > ts.getNumberOfTraces():
            raise ValueError("参考曲线序号大于参考曲线集中可用的曲线数量！")
        t = ts.getTrace(self.ref)
        ts.close()
        return t

    def accept(self, dir, name):
        return name.endswith(".trs")

    def getRequiredMemorySize(self):
        return self.selLength * 20

    def setDialogValuesTrace(self, t, nt, sft, snt, sfs, sns):
        self.chained = nt == 0
        if not self.chained and not self.init:
            self.set(self.REF, sft)
            self.ref = sft
            self.init = True
        self.setDialogValues()
        if nt == 0:
            if self.tracesPanel:
                self.tracesPanel.pack_forget()
            if self.samplesPanel:
                self.samplesPanel.pack()
            if self.scopePanel:
                self.scopePanel.pack()
        self.refTrace = t
        if t is None:
            return
        self.ns = t.getNumberOfSamples() if t.getSample() is not None else 0

    def setDialogValues(self):
        if self.thresholdTextField:
            self.setFloat(self.thresholdTextField, self.THRESHOLD, 3)
        if self.shiftTextField:
            self.setInt(self.shiftTextField, self.SHIFT)
        self.firstTraceIndex = self.getIntValue("firstTraceIndex")
        self.numberOfTraces = self.getIntValue("traces")

    def setFloat(self, textField, key, decimals):
        try:
            value = float(textField.get())
            self.set(key, value)
        except ValueError:
            pass

    def setInt(self, textField, key):
        try:
            value = int(textField.get())
            self.set(key, value)
        except ValueError:
            pass

    def getIntValue(self, key):
        return 0

    def getDialogValues(self):
        if self.thresholdTextField:
            self.threshold = self.parseFloat(self.thresholdTextField, self.THRESHOLD)
        if self.shiftTextField:
            self.shiftMax = self.parseInt(self.shiftTextField, self.SHIFT)

    def initProcess(self):
        if self.action == 2:
            if self.align is not None:
                return True
            try:
                self.closeBr()
                if len(self.saveFileName) == 0:
                    return False
                self.br = open(os.path.join(self.workPath, self.saveFileName), 'r')
                self.line = self.readNextTrace()
                self.currentTraceIndex = self.getIndex(self.line)
                return True
            except FileNotFoundError:
                print(f"错误:不能打开在{self.workPath}{self.saveFileName} 文件 ")
                return False

        self.refTrace = None
        try:
            if self.externalRefTrace:
                self.refTrace = self.loadRefFile(self.refFilePath)
                if self.refTrace is None:
                    return False
        except Exception as e:
            raise RuntimeError(e)
        self.closePw()
        if self.action == 1 and len(self.saveFileName) > 0:
            try:
                self.pw = open(os.path.join(self.workPath, self.saveFileName), 'w')
            except Exception as fnfe:
                print(fnfe)
        if not self.externalRefTrace and self.ref != 0:
            if not self.chained:
                self.currentTraceIndex = self.ref
            else:
                self.err(f"无效的参考曲线序号{self.ref}")

        self.refStart = self.firstSampleIndex
        self.refLength = self.numberOfSamples
        if self.refStart < 0 or (self.ns > 0 and self.refStart >= self.ns):
            self.refStart = 0
        if self.refStart + self.refLength > self.ns and self.ns > 0:
            self.refLength = self.ns - self.refStart
        if self.refStart < self.shiftMax:
            print(f"警告: 选择的部分只能左移{self.firstSampleIndex}个采样点")
        if self.refStart + self.refLength >= self.ns - self.shiftMax and self.ns > 0:
            print(f"警告: 选择的部分只能右移{self.ns - self.numberOfSamples - self.firstSampleIndex}个样本点")
        self.refEnd = self.refStart + self.refLength
        self.firstSampleIndex = 0
        self.numberOfSamples = self.ns
        self.selStart = self.refStart - self.shiftMax if self.shiftMax < self.refStart else 0
        self.selEnd = self.ns if self.refEnd + self.shiftMax >= self.ns and self.ns != 0 else self.refEnd + self.shiftMax
        self.selLength = self.selEnd - self.selStart
        self.selSize = 1
        while self.selSize < self.selLength:
            self.selSize <<= 1
        self.shifts = self.selLength - self.refLength + 1
        if self.refStart == 0 and self.refLength == self.ns:
            self.err("错误: 无法运行， 没有选择静态对齐的区域！")
            return False
        self.testSample = [0.0] * self.selSize
        self.sy = [0.0] * self.selSize
        self.s2y = [0.0] * self.selSize
        self.refTraceFrequency = None
        return True

    def analyze(self, t):
        oret = 0
        if self.action == 2:
            self.line = self.readNextTrace()
            self.currentTraceIndex = self.getIndex(self.line)
            if self.currentTraceIndex > self.lastTraceIndex or self.aborted:
                return self.NO_TRACE
            return self.currentTraceIndex
        return oret

    def process(self, t):
        if self.action == 2:
            return self.processShift(t)
        else:
            return self.processAlign(t)

    def finishAlign(self, t, shifted):
        pass

    def doAlign(self, t):
        self.bestShift -= self.refStart - self.selStart
        if self.currentTraceIndex < 1000:
            self.out(
                f"包含曲线{self.currentTraceIndex}, 偏移: {self.bestShift}, 相关性: {self.toStringCorr(self.bestCorr, 6)}")
        elif self.currentTraceIndex < 10000:
            self.out(f"{self.currentTraceIndex}: +")
        alignMid = self.refStart + self.refLength // 2
        self.shiftResult = f"{self.currentTraceIndex}\t{alignMid}:{self.bestShift}"
        f = [0.0] * self.numberOfSamples
        for i in range(self.numberOfSamples):
            f[i] = t.getSample((self.numberOfSamples + i + self.bestShift) % self.numberOfSamples)
        self.finishAlign(t, f)
        if self.action == 1:
            if self.pw is not None:
                self.pw.write(self.shiftResult + "\n")
                self.pw.flush()
            self.numberOfResultTraces = 0
        else:
            self.resultTrace = Trace(t.getTitle(), t.getData(), f, t.sampleFrequency)
            self.numberOfResultTraces = 1

    def processAlign(self, t):
        self.ns = t.getNumberOfSamples()
        if self.refTraceFrequency is None:
            self.refTrace = self.createReference(self.refTrace if self.refTrace is not None else t)
            if not self.externalRefTrace and self.ref != self.firstTraceIndex:
                if not self.chained:
                    self.currentTraceIndex = self.firstTraceIndex - 1
                    return None
        self.resultTraceIndex = 0
        self.numberOfResultTraces = 1
        for i in range(len(self.testSample)):
            self.testSample[i] = 0.0
        j = 0
        for i in range(self.selStart, self.selStart + self.selLength):
            self.testSample[j] = t.getSample(i)
            j += 1
        c = self.correlation(self.refTraceFrequency, self.sr, self.s2r, self.testSample, self.refLength)
        self.bestShift = 0
        self.bestCorr = -1.0
        for i in range(self.shifts):
            if i < len(c) and c[i] > self.bestCorr:
                self.bestShift = i
                self.bestCorr = c[i]
        if self.bestCorr >= self.threshold:
            self.doAlign(t)
        else:
            if self.currentTraceIndex < 1000:
                self.out(f"剔除曲线{self.currentTraceIndex}, 相关性: {self.toStringCorr(self.bestCorr, 3)}")
            elif self.currentTraceIndex < 10000:
                self.out(f"{self.currentTraceIndex}: -")
            self.numberOfResultTraces = 0
            self.shiftResult = None
        if self.numberOfResultTraces > 0:
            return self.resultTrace
        return None

    def processShift(self, t):
        original = t.getSample()
        self.numberOfSamples = t.getNumberOfSamples()
        sample = [0.0] * self.numberOfSamples
        if self.align is not None:
            self.line = self.align.getShiftResult()
        if self.line is None or len(self.line) == 0:
            return None
        parts = self.line.replace('\t', ' ').replace(',', ' ').replace(':', ' ').split()
        state = 0
        offset = 0
        index = 0
        shift = 0
        for token in parts:
            value = int(token)
            if state == 1:
                index = value
            if state == 2:
                shift = value
            state += 1
            if state == 3:
                for i in range(offset, index):
                    if i < len(sample):
                        sample[i] = original[self.normalize(i + shift)]
                offset = index
                state = 1
        for i in range(offset, self.numberOfSamples):
            if i < len(sample):
                sample[i] = original[self.normalize(i + shift)]
        return Trace(t.getTitle(), t.getData(), sample, t.sampleFrequency)

    def readNextTrace(self):
        if self.br is None:
            return None
        try:
            return self.br.readline()
        except Exception as e:
            self.err("无法读取文件")
            print(e)
        return None

    def normalize(self, i):
        while i < 0:
            i += self.numberOfSamples
        return i % self.numberOfSamples

    def closeBr(self):
        try:
            if self.br is not None:
                self.br.close()
                self.br = None
        except Exception:
            pass

    def getIndex(self, s):
        if s is None:
            return self.NO_TRACE
        parts = s.strip().split('\t')
        try:
            return int(parts[0])
        except Exception:
            return self.NO_TRACE

    def finalize(self):
        self.closePw()
        self.closeBr()

    def closePw(self):
        if self.pw is not None:
            self.pw.flush()
            self.pw.close()
            self.pw = None

    def createReference(self, t):
        self.numberOfResultTraces = 0
        refSample = [0.0] * self.selSize
        j = 0
        for i in range(self.refStart, self.refStart + self.refLength):
            if j < len(refSample):
                refSample[j] = t.getSample(i)
                j += 1
        self.sr = self.getSum(refSample, self.refLength)
        self.s2r = self.getVar(refSample, self.sr, self.refLength)

        data = self.operation.createData(refSample)
        data = self.operation.r2hc(data)
        data = self.operation.normalize(data, self.selSize)
        self.refTraceFrequency = data.getDoubleData()

        return t

    def getStats(self, in_arr, s, s2, len1, len2):
        for i in range(len(s)):
            if i < len(in_arr):
                s[i] = in_arr[i]
                s2[i] = s[i] * s[i]
        s0 = s[0]
        s20 = s2[0]
        for i in range(1, len1):
            if i < len(s):
                s[0] += s[i]
                s2[0] += s2[i]
        k = 0
        for i in range(1, len2):
            j = i + len1 - 1
            if i < len(s) and j < len(s):
                sn = s[i]
                s2n = s2[i]
                s[i] = s[k] - s0 + s[j]
                s2[i] = s2[k] - s20 + s2[j]
                s0 = sn
                s20 = s2n
                k += 1
        for i in range(len2):
            if i < len(s2):
                s2[i] -= s[i] * s[i] / len1

    def getSum(self, in_arr, length):
        sum_val = 0.0
        for i in range(length):
            if i < len(in_arr):
                sum_val += in_arr[i]
        return sum_val

    def getVar(self, in_arr, sum_val, length):
        sumOfSquares = 0.0
        for i in range(length):
            if i < len(in_arr):
                sumOfSquares += in_arr[i] * in_arr[i]
        return sumOfSquares - sum_val * sum_val / length

    def correlation(self, xf, sx, s2x, y, length):
        self.getStats(y, self.sy, self.s2y, self.refLength, self.shifts)

        yf = self.operation.r2hc(self.operation.createData(y)).getDoubleData()
        yf[0] *= xf[0]
        i = 1
        j = len(xf) - 1
        while i < j:
            s1 = yf[i]
            s2 = xf[i]
            s3 = yf[j]
            s4 = xf[j]
            yf[j] = s3 * s2 - s1 * s4
            yf[i] = s1 * s2 + s3 * s4
            i += 1
            j -= 1
        if len(xf) % 2 == 0:
            yf[len(xf) // 2] = xf[len(xf) // 2] * yf[len(xf) // 2]

        c = self.operation.hc2r(self.operation.createData(yf)).getDoubleData()
        if s2x > 0:
            for i in range(len(xf)):
                if i < len(self.s2y) and self.s2y[i] > 0:
                    c[i] = (c[i] - sx * self.sy[i] / length) / math.sqrt(s2x * self.s2y[i])
                else:
                    c[i] = 0.0
        return c

    def correlationWithStats(self, xf, sx, s2x, y, length):
        sy = self.getSum(y, length)
        s2y = self.getVar(y, sy, length)

        yf = self.operation.r2hc(self.operation.createData(y)).getDoubleData()
        yf[0] *= xf[0]
        i = 1
        j = len(xf) - 1
        while i < j:
            s1 = xf[i]
            s2 = yf[i]
            s3 = xf[j]
            s4 = yf[j]
            yf[j] = s3 * s2 - s1 * s4
            yf[i] = s1 * s2 + s3 * s4
            i += 1
            j -= 1
        if len(xf) % 2 == 0:
            yf[len(xf) // 2] = xf[len(xf) // 2] * yf[len(xf) // 2]
        c = self.operation.hc2r(self.operation.createData(yf)).getDoubleData()
        if s2y > 0:
            for i in range(len(xf)):
                if i < len(s2x) and s2x[i] > 0:
                    c[i] = (c[i] - sx[i] * sy / length) / math.sqrt(s2x[i] * s2y)
                else:
                    c[i] = 0.0
        return c

    def finishProcess(self):
        self.init = False

    def getShiftResult(self):
        return self.shiftResult

    def setLinked(self, m):
        if isinstance(m, StaticAlign):
            self.align = m

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
        s1 = self.refTextField.get().strip() if self.refTextField else ""
        s2 = self.thresholdTextField.get().strip() if self.thresholdTextField else ""
        s3 = self.shiftTextField.get().strip() if self.shiftTextField else ""
        pattern1 = re.compile(r"^\d+$")
        pattern2 = re.compile(r"^(-?\d+)(\.\d+)?$")
        if not pattern1.match(s1) or self.ref >= self.getIntValue("traces"):
            message.append(f"参考曲线的可选范围是:0--{self.getIntValue('traces') - 1}")
        if not pattern2.match(s2):
            message.append("阈值应为浮点数！")
        elif self.threshold < -1 or self.threshold > 1:
            message.append("阈值的可选范围是:[-1,1]")
        if not pattern1.match(s3):
            message.append("请输入位移最大量(非负整数)!")
        if len(message) == 0:
            return True
        messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
        return False

    def out(self, message):
        print(message)

    def err(self, message):
        print(message)

    def toStringCorr(self, value, decimals):
        return f"{value:.{decimals}f}"


class TraceSet:
    def __init__(self, path):
        self.path = path

    def getNumberOfTraces(self):
        return 0

    def getTrace(self, index):
        return None

    def close(self):
        pass


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

    def getTitle(self):
        return self.title


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = StaticAlign()
    app.initModule()
    app.initDialog()
    root.mainloop()