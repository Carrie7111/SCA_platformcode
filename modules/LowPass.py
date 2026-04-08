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

        valuePanel = ttk.Frame(self.window)
        valuePanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        valuePanel.configure(borderwidth=2, relief="groove")

        self.weightTextField = ttk.Entry(valuePanel, width=20)
        self.weightTextField.insert(0, str(self.weight))
        self.weightTextField.pack(padx=5, pady=5)

        valuePanel.configure(width=80, height=100)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return valuePanel

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

    def process(self, t):
        result = [0.0] * t.getNumberOfSamples()
        samples = t.getSample()
        for i in range(len(result)):
            result[i] = samples[i]
        for i in range(1, t.getNumberOfSamples()):
            result[i] = (result[i] + self.weight * result[i - 1]) / self.weight_1
        for i in range(t.getNumberOfSamples() - 2, -1, -1):
            result[i] = (result[i] + self.weight * result[i + 1]) / self.weight_1
        return Trace(t.title, t.data, result, t.sampleFrequency)

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
        s1 = self.weightTextField.get().strip()
        pattern = re.compile(r"^\d+$")
        if not pattern.match(s1):
            message.append("权重应为非负整数！")
        if len(message) == 0:
            return True
        messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
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