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
        self.set(self.REF, self.ref)
        self.set(self.SAVE_FILE_NAME, self.saveFileName)
        self.set(self.REF_FILE_PATH, self.refFilePath)
        self.set(self.ACTION, self.action)

    def set(self, key, value):
        if key == self.REF:
            self.ref = value
        elif key == self.SAVE_FILE_NAME:
            self.saveFileName = value
        elif key == self.REF_FILE_PATH:
            self.refFilePath = value
        elif key == self.ACTION:
            self.action = value

    def get(self, key):
        if key == self.REF:
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
            self.window.title("对齐模块")

        centerPanel = ttk.Frame(self.window)
        centerPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Action panel
        self.actionPanel = ttk.LabelFrame(centerPanel, text="Action")
        self.actionPanel.pack(fill=tk.X, pady=5)

        actionAlignButton = ttk.Radiobutton(self.actionPanel, text="Align", value=0, command=self.actionPerformed)
        actionAlignButton.pack(side=tk.LEFT, padx=5)
        actionSaveButton = ttk.Radiobutton(self.actionPanel, text="Store", value=1, command=self.actionPerformed)
        actionSaveButton.pack(side=tk.LEFT, padx=5)
        actionLoadButton = ttk.Radiobutton(self.actionPanel, text="Apply", value=2, command=self.actionPerformed)
        actionLoadButton.pack(side=tk.LEFT, padx=5)

        # Storage file
        filePanel = ttk.LabelFrame(centerPanel, text="Alignment storage file")
        filePanel.pack(fill=tk.X, pady=5)

        self.saveFileNameTextField = ttk.Entry(filePanel, width=30)
        self.saveFileNameTextField.insert(0, self.saveFileName)
        self.saveFileNameTextField.pack(side=tk.LEFT, padx=5, pady=5)

        # Reference panel
        refTracePanel = ttk.LabelFrame(centerPanel, text="参考曲线")
        refTracePanel.pack(fill=tk.X, pady=5)

        refLabel = ttk.Label(refTracePanel, text="请根据曲线集的曲线数设置：")
        refLabel.pack(side=tk.LEFT, padx=5)

        self.refTextField = ttk.Entry(refTracePanel, width=10)
        self.refTextField.insert(0, str(self.ref))
        self.refTextField.pack(side=tk.LEFT, padx=5)

        # Trace set selection panel
        traceSetSelectionPanel = ttk.LabelFrame(centerPanel, text="Trace set")
        traceSetSelectionPanel.pack(fill=tk.X, pady=5)

        self.refSelectButton = ttk.Button(traceSetSelectionPanel, text="Select", command=self.refSelectButtonClicked)
        self.refSelectButton.pack(side=tk.LEFT, padx=5)

        self.useCurrentCheckBox = ttk.Checkbutton(traceSetSelectionPanel, text="Use current",
                                                  command=self.useCurrentCheckBoxClicked)
        self.useCurrentCheckBox.pack(side=tk.LEFT, padx=5)

        # External Reference panel
        referenceTraceSetPanel = ttk.LabelFrame(centerPanel, text="External Reference")
        referenceTraceSetPanel.pack(fill=tk.X, pady=5)

        self.refNameTextField = ttk.Entry(referenceTraceSetPanel, width=40)
        self.refNameTextField.pack(side=tk.LEFT, padx=5, pady=5)

        # Options panel
        self.optionsPanel = ttk.LabelFrame(centerPanel, text="参数设置")
        self.optionsPanel.pack(fill=tk.BOTH, expand=True, pady=5)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        self.updateEnabledPanels()

        return centerPanel

    def refSelectButtonClicked(self):
        try:
            fd = filedialog.askopenfilename(
                title="选择曲线集",
                initialdir=self.traceSetPath,
                filetypes=[("TRS files", "*.trs"), ("All files", "*.*")]
            )
            if fd:
                self.set(self.REF_FILE_PATH, fd)
                self.refNameTextField.delete(0, tk.END)
                self.refNameTextField.insert(0, os.path.basename(fd))
                self.useCurrentCheckBox.state(['!selected'])
                self.useCurrentCheckBox.config(state='normal')
                self.externalRefTrace = True
        except Exception as exc:
            self.err("错误:无法加载参考曲线！")
            print(exc)

    def useCurrentCheckBoxClicked(self):
        self.set(self.REF_FILE_PATH, "")
        self.refNameTextField.delete(0, tk.END)
        self.refNameTextField.insert(0, "")
        self.useCurrentCheckBox.config(state='disabled')
        self.externalRefTrace = False

    def actionPerformed(self, event=None):
        pass

    def setDialogValues(self):
        self.setInt(self.actionPanel, self.ACTION)
        self.setInt(self.refTextField, self.REF)
        self.setString(self.saveFileNameTextField, self.SAVE_FILE_NAME)
        self.refFilePath = self.getString(self.REF_FILE_PATH)
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
        pass

    def setString(self, source, key):
        if key == self.SAVE_FILE_NAME:
            self.saveFileName = source.get()

    def getString(self, key):
        if key == self.REF_FILE_PATH:
            return self.refFilePath
        return ""

    def getDialogValues(self):
        self.saveFileName = self.getStringFromEntry(self.saveFileNameTextField, self.SAVE_FILE_NAME)
        self.ref = self.parseInt(self.refTextField, self.REF)
        self.action = self.getIntFromPanel(self.actionPanel, self.ACTION)

    def getStringFromEntry(self, entry, key):
        return entry.get()

    def parseInt(self, entry, key):
        try:
            return int(entry.get())
        except ValueError:
            return 0

    def getIntFromPanel(self, panel, key):
        return 0

    def updateEnabledPanels(self):
        self.getDialogValues()
        if self.action != 0:
            self.saveFileNameTextField.config(state='normal')
        else:
            self.saveFileNameTextField.config(state='disabled')
        if not self.externalRefTrace:
            self.useCurrentCheckBox.state(['selected'])
        else:
            self.useCurrentCheckBox.state(['!selected'])
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

    def accept(self, dir, name):
        return name.endswith(".trs")

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
    pass