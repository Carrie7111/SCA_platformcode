import re
import tkinter as tk
from tkinter import ttk


class Abs:
    OFFSET = "offset"
    AUTO = "auto"

    def __init__(self):
        self.offsetTextField = None
        self.autoOffsetCheckBox = None
        self.offset = 0.0
        self.autoOffset = False
        self.yScale = 1.0
        self.moduleDescription = "Produce absolute values of input data"
        self.prefix = "Absolute value"
        self.moduleVersion = "1.3"
        self.helpFile = "doc/manual/modulesAbs.html"
        self.window = None

    def initModule(self):
        self.set(self.OFFSET, self.offset)
        self.set(self.AUTO, self.autoOffset)

    def set(self, key, value):
        if key == self.OFFSET:
            self.offset = value
        elif key == self.AUTO:
            self.autoOffset = value

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("绝对值")

        offsetPanel = ttk.Frame(self.window)
        offsetPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        offsetPanel.configure(borderwidth=2, relief="groove")

        self.offsetTextField = ttk.Entry(offsetPanel, width=20)
        self.offsetTextField.insert(0, str(self.offset))
        self.offsetTextField.pack(side=tk.LEFT, padx=5, pady=5)

        self.autoOffsetCheckBox = ttk.Checkbutton(offsetPanel, text="自动")
        self.autoOffsetCheckBox.pack(side=tk.RIGHT, padx=5, pady=5)

        offsetPanel.configure(width=80, height=120)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return offsetPanel

    def setDialogValues(self):
        self.setFloat(self.offsetTextField, self.OFFSET, 3)
        self.setBoolean(self.autoOffsetCheckBox, self.AUTO)

    def setFloat(self, textField, key, decimals):
        try:
            value = float(textField.get())
            self.set(key, value)
        except ValueError:
            pass

    def setBoolean(self, checkBox, key):
        self.set(key, checkBox.instate(['selected']))

    def getDialogValues(self):
        self.offset = self.parseFloat(self.offsetTextField, self.OFFSET) / self.yScale
        self.autoOffset = self.getBoolean(self.autoOffsetCheckBox, self.AUTO)

    def parseFloat(self, textField, key):
        try:
            return float(textField.get())
        except ValueError:
            return 0.0

    def getBoolean(self, checkBox, key):
        return checkBox.instate(['selected'])

    def process(self, t):
        f = [0.0] * t.getNumberOfSamples()
        if self.autoOffset:
            self.offset = 0.0
            for i in range(t.getNumberOfSamples()):
                self.offset += t.getSample(i)
            self.offset /= t.getNumberOfSamples()
            self.offsetTextField.delete(0, tk.END)
            self.offsetTextField.insert(0, str(self.offset * self.yScale))
        for i in range(len(f)):
            f[i] = abs(t.getSample(i) - self.offset)
        return Trace(t.title, t.data, f, t.sampleFrequency)

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
        s1 = self.offsetTextField.get().strip()
        pattern = re.compile(r"^(-?\d+)(\.\d+)?$")
        if not pattern.match(s1):
            message.append("偏移应为浮点数！")
        if len(message) == 0:
            return True
        print("模块设置错误:", "下面参数设置错误", '\n'.join(message))
        return False


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


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Abs()
    app.initModule()
    app.initDialog()
    root.mainloop()