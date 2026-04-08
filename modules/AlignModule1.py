import os
import tkinter as tk
from tkinter import ttk, filedialog
from abc import ABC, abstractmethod


class AlignModule(ABC):
    REF = "ref"
    SAVE_FILE_NAME = "save.file.name"
    REF_FILE_PATH = "ref.file.path"
    ACTION = "action"

    def __init__(self):
        self.initialized = False
        self.externalRefTrace = False
        self.refTrace = None
        self.actionPanel = None
        self.optionsPanel = None
        self.saveFileNameTextField = None
        self.refTextField = None
        self.refNameTextField = None
        self.refSelectButton = None
        self.useCurrentCheckBox = None
        self.ref = 0
        self.chained = False
        self.action = 0
        self.refFilePath = ""
        self.saveFileName = "shifts.txt"
        self.lastTraceIndex = -1
        self.traceSetPath = ""
        self.window = None

    def initModule(self):
        self.ref = 0
        self.externalRefTrace = False
        self.refTrace = None
        self.refFilePath = ""
        self.saveFileName = "shifts.txt"
        self.action = 0
        self.lastTraceIndex = -1
        self.set("ref", self.ref)
        self.set("save.file.name", self.saveFileName)
        self.set("ref.file.path", self.refFilePath)
        self.set("action", self.action)

    def set(self, key, value):
        if key == "ref":
            self.ref = value
        elif key == "save.file.name":
            self.saveFileName = value
        elif key == "ref.file.path":
            self.refFilePath = value
        elif key == "action":
            self.action = value

    def get(self, key):
        if key == "ref":
            return self.ref
        elif key == "save.file.name":
            return self.saveFileName
        elif key == "ref.file.path":
            return self.refFilePath
        elif key == "action":
            return self.action
        return None

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("对齐模块")

        var1 = ttk.Frame(self.window)
        var1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.actionPanel = ttk.LabelFrame(var1, text="Action")
        self.actionPanel.pack(fill=tk.X, pady=5)

        self.actionVar = tk.IntVar(value=0)
        var2 = ttk.Radiobutton(self.actionPanel, text="Align", variable=self.actionVar, value=0,
                               command=self.actionPerformed)
        var2.pack(side=tk.LEFT, padx=5)
        var4 = ttk.Radiobutton(self.actionPanel, text="Store", variable=self.actionVar, value=1,
                               command=self.actionPerformed)
        var4.pack(side=tk.LEFT, padx=5)
        var5 = ttk.Radiobutton(self.actionPanel, text="Apply", variable=self.actionVar, value=2,
                               command=self.actionPerformed)
        var5.pack(side=tk.LEFT, padx=5)

        var6 = ttk.LabelFrame(var1, text="Alignment storage file")
        var6.pack(fill=tk.X, pady=5)

        self.saveFileNameTextField = ttk.Entry(var6, width=30)
        self.saveFileNameTextField.insert(0, self.saveFileName)
        self.saveFileNameTextField.pack(side=tk.LEFT, padx=5, pady=5)

        var7 = ttk.LabelFrame(var1, text="参考曲线")
        var7.pack(fill=tk.X, pady=5)

        var8 = ttk.Label(var7, text="请根据曲线集的曲线数设置：")
        var8.pack(side=tk.LEFT, padx=5)

        self.refTextField = ttk.Entry(var7, width=10)
        self.refTextField.insert(0, str(self.ref))
        self.refTextField.pack(side=tk.LEFT, padx=5)

        var9 = ttk.LabelFrame(var1, text="Trace set")
        var9.pack(fill=tk.X, pady=5)

        self.refSelectButton = ttk.Button(var9, text="Select", command=self.refSelectButtonClicked)
        self.refSelectButton.pack(side=tk.LEFT, padx=5)

        self.useCurrentCheckBox = ttk.Checkbutton(var9, text="Use current", command=self.useCurrentCheckBoxClicked)
        self.useCurrentCheckBox.pack(side=tk.LEFT, padx=5)

        var10 = ttk.LabelFrame(var1, text="External Reference")
        var10.pack(fill=tk.X, pady=5)

        self.refNameTextField = ttk.Entry(var10, width=40)
        self.refNameTextField.pack(side=tk.LEFT, padx=5, pady=5)

        self.optionsPanel = ttk.LabelFrame(var1, text="参数设置")
        self.optionsPanel.pack(fill=tk.BOTH, expand=True, pady=5)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        self.updateEnabledPanels()

        return var1

    def refSelectButtonClicked(self):
        try:
            var4 = filedialog.askopenfilename(
                title="选择曲线集",
                initialdir=self.traceSetPath,
                filetypes=[("TRS files", "*.trs"), ("All files", "*.*")]
            )
            if var4:
                self.set("ref.file.path", self.refFilePath)
                self.refNameTextField.delete(0, tk.END)
                self.refNameTextField.insert(0, os.path.basename(var4))
                self.useCurrentCheckBox.state(['!selected'])
                self.externalRefTrace = True
        except Exception as var5:
            print("错误:无法加载参考曲线！")
            print(var5)

    def useCurrentCheckBoxClicked(self):
        self.set("ref.file.path", "")
        self.refNameTextField.delete(0, tk.END)
        self.refNameTextField.insert(0, "")
        self.externalRefTrace = False

    def actionPerformed(self, event=None):
        self.updateEnabledPanels()

    def updateEnabledPanels(self):
        self.getDialogValues()
        if self.action != 0:
            self.saveFileNameTextField.config(state='normal')
        else:
            self.saveFileNameTextField.config(state='disabled')

        if self.externalRefTrace and self.action != 2:
            self.useCurrentCheckBox.config(state='normal')
        else:
            self.useCurrentCheckBox.config(state='disabled')

        if self.action != 2:
            self.refTextField.config(state='normal')
            self.refSelectButton.config(state='normal')
        else:
            self.refTextField.config(state='disabled')
            self.refSelectButton.config(state='disabled')

    def setDialogValues(self):
        self.setInt(self.actionVar, "action")
        self.setInt(self.refTextField, "ref")
        self.setString(self.saveFileNameTextField, "save.file.name")
        self.refFilePath = self.getString("ref.file.path")
        self.externalRefTrace = self.refFilePath is not None and len(self.refFilePath) > 0
        if not self.externalRefTrace:
            self.useCurrentCheckBox.state(['selected'])
        else:
            self.useCurrentCheckBox.state(['!selected'])
        if self.externalRefTrace:
            self.useCurrentCheckBox.config(state='normal')
        else:
            self.useCurrentCheckBox.config(state='disabled')
        if self.externalRefTrace:
            self.refNameTextField.delete(0, tk.END)
            self.refNameTextField.insert(0, os.path.basename(self.refFilePath))
        self.refTrace = None
        self.updateEnabledPanels()

    def setInt(self, source, key):
        if key == "action":
            self.action = source.get()
        elif key == "ref":
            try:
                self.ref = int(source.get())
            except ValueError:
                pass

    def setString(self, source, key):
        if key == "save.file.name":
            self.saveFileName = source.get()

    def getString(self, key):
        if key == "ref.file.path":
            return self.refFilePath
        return ""

    def getDialogValues(self):
        self.saveFileName = self.getStringFromEntry(self.saveFileNameTextField, "save.file.name")
        self.ref = self.parseInt(self.refTextField, "ref")
        self.action = self.getIntFromVar(self.actionVar, "action")

    def getStringFromEntry(self, entry, key):
        return entry.get()

    def parseInt(self, entry, key):
        try:
            return int(entry.get())
        except ValueError:
            return 0

    def getIntFromVar(self, var, key):
        return var.get()

    def ok_clicked(self):
        if self.checkDialogValues():
            self.getDialogValues()
            if self.window:
                self.window.destroy()

    def cancel_clicked(self):
        if self.window:
            self.window.destroy()

    def checkDialogValues(self):
        return True

    def err(self, message):
        print(message)

    def accept(self, var1, var2):
        return var2.endswith(".trs")

    @abstractmethod
    def process(self, t):
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


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # 这是一个抽象类，不能直接实例化
    # app = AlignModule()
    # app.initModule()
    # app.initDialog()
    # root.mainloop()
    pass