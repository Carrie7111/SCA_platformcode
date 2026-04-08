import re
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class LowPass:
    WEIGHT = "weight"

    def __init__(self):
        self.weightTextField = None
        self.weight = 1
        self.weight_1 = self.weight + 1
        self.moduleTitle = "LowPass"
        self.moduleDescription = "Low pass module"
        self.moduleVersion = "1.3"
        self.helpFile = "doc/manual/modulesLowPass.html"
        self.window = None

    def initModule(self):
        self.moduleTitle = "LowPass"
        self.moduleDescription = "Low pass module"
        self.moduleVersion = "1.3"
        self.helpFile = "doc/manual/modulesLowPass.html"
        self.weight = 1
        self.weight_1 = self.weight + 1
        self.set(self.WEIGHT, self.weight)

    def set(self, key, value):
        if key == self.WEIGHT:
            self.weight = value
            self.weight_1 = self.weight + 1

    def get(self, key):
        if key == self.WEIGHT:
            return self.weight
        return None

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("低通滤波")

        var1 = ttk.Frame(self.window)
        var1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        var1.configure(borderwidth=2, relief="groove")

        self.weightTextField = ttk.Entry(var1, width=20)
        self.weightTextField.insert(0, str(self.weight))
        self.weightTextField.pack(padx=5, pady=5)

        var1.configure(width=80, height=100)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return var1

    def setDialogValues(self):
        self.setInt(self.weightTextField, self.WEIGHT)

    def setInt(self, textField, key):
        try:
            value = int(textField.get())
            self.set(key, value)
        except ValueError:
            pass

    def getDialogValues(self):
        self.weight = self.parseInt(self.weightTextField, self.WEIGHT)
        self.weight_1 = self.weight + 1

    def parseInt(self, textField, key):
        try:
            return int(textField.get())
        except ValueError:
            return 0

    def process(self, var1):
        var2 = [0.0] * var1.getNumberOfSamples()
        samples = var1.getSample()
        for i in range(len(var2)):
            var2[i] = samples[i]

        for var3 in range(1, var1.getNumberOfSamples()):
            var2[var3] = (var2[var3] + self.weight * var2[var3 - 1]) / self.weight_1

        for var4 in range(var1.getNumberOfSamples() - 2, -1, -1):
            var2[var4] = (var2[var4] + self.weight * var2[var4 + 1]) / self.weight_1

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
        var2 = self.weightTextField.get().strip()
        var3 = re.compile(r"^\d+$")
        if not var3.match(var2):
            var1.append("权重应为非负整数！")
        if len(var1) == 0:
            return True
        else:
            messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(var1))
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

    def getSample(self):
        return self.samples


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = LowPass()
    app.initModule()
    app.initDialog()
    root.mainloop()