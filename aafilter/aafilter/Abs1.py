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
        self.set("offset", self.offset)
        self.set("auto", self.autoOffset)

    def set(self, key, value):
        if key == "offset":
            self.offset = value
        elif key == "auto":
            self.autoOffset = value

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("绝对值")

        var1 = ttk.Frame(self.window)
        var1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        var1.configure(borderwidth=2, relief="groove")

        self.offsetTextField = ttk.Entry(var1, width=20)
        self.offsetTextField.insert(0, str(self.offset))
        self.offsetTextField.pack(side=tk.LEFT, padx=5, pady=5)

        self.autoOffsetCheckBox = ttk.Checkbutton(var1, text="自动")
        self.autoOffsetCheckBox.pack(side=tk.RIGHT, padx=5, pady=5)

        var1.configure(width=80, height=120)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return var1

    def setDialogValues(self):
        self.setFloat(self.offsetTextField, "offset", 3)
        self.setBoolean(self.autoOffsetCheckBox, "auto")

    def setFloat(self, textField, key, decimals):
        try:
            value = float(textField.get())
            self.set(key, value)
        except ValueError:
            pass

    def setBoolean(self, checkBox, key):
        self.set(key, checkBox.instate(['selected']))

    def getDialogValues(self):
        self.offset = self.parseFloat(self.offsetTextField, "offset") / self.yScale
        self.autoOffset = self.getBoolean(self.autoOffsetCheckBox, "auto")

    def parseFloat(self, textField, key):
        try:
            return float(textField.get())
        except ValueError:
            return 0.0

    def getBoolean(self, checkBox, key):
        return checkBox.instate(['selected'])

    def process(self, var1):
        var2 = [0.0] * var1.getNumberOfSamples()
        if self.autoOffset:
            self.offset = 0.0
            for var3 in range(var1.getNumberOfSamples()):
                self.offset += var1.getSample(var3)
            self.offset /= float(var1.getNumberOfSamples())
            self.offsetTextField.delete(0, tk.END)
            self.offsetTextField.insert(0, str(self.offset * self.yScale))
        for var4 in range(len(var2)):
            var2[var4] = abs(var1.getSample(var4) - self.offset)
        return Trace(var1.title, var1.data, var2, var1.sampleFrequency)

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
        var2 = self.offsetTextField.get().strip()
        var3 = re.compile(r"^(-?\d+)(\.\d+)?$")
        if not var3.match(var2):
            var1.append("偏移应为浮点数！")
        if len(var1) == 0:
            return True
        else:
            print("模块设置错误:", "下面参数设置错误", '\n'.join(var1))
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