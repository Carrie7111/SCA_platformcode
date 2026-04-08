import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from abc import ABC, abstractmethod
import threading
import time
import xml.etree.ElementTree as ET
from typing import Optional, List, Any


class Chain:
    CHAIN_STORE = "recentChain.parameters"
    CHAIN = "Chain.parameters"

    def __init__(self):
        self.chainPanel = None
        self.addButton = None
        self.removeButton = None
        self.setupButton = None
        self.reloadButton = None
        self.loadButton = None
        self.saveButton = None
        self.firstTrace = None
        self.top = None
        self.selectedNode = None
        self.draggedNode = None
        self.treeModel = None
        self.tree = None
        self.treeView = None
        self.dragging = False
        self.embedded = False
        self.originalCursor = None
        self.linked = None
        self.time = 0
        self.suggestedNumberOfSamples = 0
        self.nt = 0
        self.finished = False
        self.started = False
        self.parameterFile = None
        self.isAcquisition = False
        self.processCalled = False
        self.moduleTitle = "Chain"
        self.moduleDescription = "Perform multiple filter steps at once"
        self.moduleVersion = "1.2"
        self.helpFile = "doc/manual/modulesChain.html"
        self.enableParameterButtons = True
        self.inputRequired = False
        self.forceSampleTracePanels = True
        self.path = ""
        self.modulePath = ""
        self.workPath = ""
        self.xScale = 1.0
        self.yScale = 1.0
        self.xLabel = ""
        self.yLabel = ""
        self.logScale = False
        self.sampleFrequency = 0.0
        self.numberOfResultTraces = 0
        self.forceFilenameChain = True
        self.firstTraceIndex = 0
        self.numberOfTraces = 0
        self.autoReload = True
        self.window = None
        self.pi = None
        self.nt = 0

    def initModule(self):
        self.moduleTitle = "Chain"
        self.moduleDescription = "Perform multiple filter steps at once"
        self.moduleVersion = "1.2"
        self.helpFile = "doc/manual/modulesChain.html"
        self.enableParameterButtons = True
        self.inputRequired = False
        self.forceSampleTracePanels = True

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel()
            self.window.title("Chain")

        self.chainPanel = ttk.Frame(self.window)
        self.chainPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        var1 = ttk.Frame(self.chainPanel)
        var1.pack(fill=tk.X, pady=5)

        self.addButton = ttk.Button(var1, text="添加", command=self.addButtonClicked)
        self.addButton.pack(side=tk.LEFT, padx=2)

        self.removeButton = ttk.Button(var1, text="移除", command=self.removeButtonClicked, state='disabled')
        self.removeButton.pack(side=tk.LEFT, padx=2)

        self.setupButton = ttk.Button(var1, text="设置", command=self.setupButtonClicked, state='disabled')
        self.setupButton.pack(side=tk.LEFT, padx=2)

        self.reloadButton = ttk.Button(var1, text="重载", command=self.reloadButtonClicked)
        self.reloadButton.pack(side=tk.LEFT, padx=2)

        if self.embedded:
            self.loadButton = ttk.Button(var1, text="加载", command=self.loadButtonClicked)
            self.loadButton.pack(side=tk.LEFT, padx=2)
            self.saveButton = ttk.Button(var1, text="保存", command=self.saveButtonClicked, state='disabled')
            self.saveButton.pack(side=tk.LEFT, padx=2)

        self.top = ChainNode(self.moduleTitle)
        self.selectedNode = self.top
        self.treeModel = self.top
        self.tree = ttk.Treeview(self.chainPanel)
        self.treeView = ttk.Frame(self.chainPanel)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        return self.chainPanel

    def addButtonClicked(self):
        self.insertNode()

    def removeButtonClicked(self):
        if self.selectedNode and self.selectedNode != self.top:
            self.removeNode(self.selectedNode)
            if self.saveButton:
                self.saveButton.config(state='normal')

    def setupButtonClicked(self):
        try:
            if self.selectedNode == self.top:
                return
            var8 = self.selectedNode.getModule()
            var4 = self.selectedNode.getPreviousNode()
            if var4 != self.top and isinstance(var8, Linkable):
                var8.setLinked(var4.getModule())
            var5 = var8.getInt(26)
            var6 = var8.getInt(27)
            var8.init(self.firstTrace, self.pi, self.nt, 0, 0, var5,
                      var6 if var6 != 0 else self.suggestedNumberOfSamples)
        except Exception as var7:
            print(var7)

    def reloadButtonClicked(self):
        self.reload()

    def loadButtonClicked(self):
        self.load()

    def saveButtonClicked(self):
        self.save()

    def setPreferredSize(self, var1, var2):
        pass

    def setEmbedded(self, var1):
        self.embedded = var1
        self.autoReload = not var1

    def getPanel(self):
        return self.chainPanel

    def actionPerformed(self, var1):
        pass

    def valueChanged(self, var1):
        self.selectedNode = var1
        self.setupButton.config(state='normal' if self.selectedNode != self.top else 'disabled')
        self.removeButton.config(state='normal' if self.selectedNode != self.top else 'disabled')

    def mouseClicked(self, var1):
        self.expandAll()

    def mouseEntered(self, var1):
        pass

    def mouseMoved(self, var1):
        pass

    def mouseDragged(self, var1):
        if not self.dragging:
            if self.selectedNode.isRoot():
                return
            self.originalCursor = self.tree.cget("cursor")
            self.draggedNode = self.selectedNode
            self.dragging = True
        else:
            self.dragging = True

    def mouseExited(self, var1):
        pass

    def mousePressed(self, var1):
        pass

    def mouseReleased(self, var1):
        if self.dragging:
            self.dragging = False
            self.tree.config(cursor=self.originalCursor)
            self.tree.update()
            self.expandAll()

    def keyPressed(self, var1):
        if var1.keysym == 'Delete':
            self.removeNode(self.selectedNode)
        elif var1.keysym == 'Insert':
            self.insertNode()

    def keyReleased(self, var1):
        pass

    def keyTyped(self, var1):
        pass

    def insertNode(self, var1=None, var2=None, var3=-1, var4=None):
        pass

    def removeNode(self, var1):
        if var1 != self.top:
            var2 = var1
            var3 = var2.getModule()
            var4 = var3.__class__.__name__
            if "XYAcquisition" in var4 or "ScopeAcquisition" in var4:
                self.isAcquisition = False
            var5 = var1.getParent()
            var6 = var5.getIndex(var1)
            for var7 in range(var1.getChildCount()):
                var5.insert(var1.getChildAt(var7), var6 + var7)
            var1.removeAllChildren()
            var1.removeFromParent()
            self.tree.update()

    def getParameterFile(self):
        if self.parameterFile is None:
            if self.embedded:
                self.parameterFile = os.path.join(self.modulePath, self.path + self.CHAIN)
            else:
                self.parameterFile = os.path.join(self.workPath, self.CHAIN_STORE)
        return self.parameterFile

    def reload(self):
        self.load(self.getParameterFile(), True)

    def load(self, var1=None, var2=False):
        pass

    def save(self):
        pass

    def getParametersAsString(self):
        var1 = []
        var2 = 0
        var3 = 0
        self.linked = None
        for var4 in range(self.top.getChildCount()):
            var3 = self.storeChain(self.top.getChildAt(var4), var2, var3 + 1, var1)
        return ''.join(var1)

    def expandAll(self):
        pass

    def init(self, var1, var2, var3, var4, var5, var6, var7):
        if self.isAcquisition:
            self.firstTrace = None
            self.suggestedNumberOfSamples = 0
            self.nt = 0
        else:
            self.firstTrace = var1
            self.suggestedNumberOfSamples = var7
            self.nt = var3
        return 0

    def initProcess(self):
        self.isAcquisition = False
        self.processCalled = False
        var1 = self.top.getChildCount()
        if var1 > 0:
            self.save(self.getParameterFile())
        self.finished = False
        self.started = False
        for var2 in range(var1):
            self.resetStarted(self.top.getChildAt(var2))
        self.time = time.time()
        self.forceFilenameChain = True
        if self.numberOfResultTraces == 0 and var1 > 0:
            var8 = self.top.getChildAt(0)
            var3 = var8.getModule()
            if "GenericAcquisition" in var3.__class__.__name__:
                var4 = var3.getInt(26)
                var5 = var3.getInt(27)
                var6 = var3.getBoolean(32)
                var3.setBoolean(32, False)
                var3.init(self.firstTrace, self.pi, self.nt, self.firstTraceIndex, self.numberOfTraces, var4,
                          var5 if var5 != 0 else self.suggestedNumberOfSamples)
                var3.setBoolean(32, var6)
                var7 = var3
                self.numberOfResultTraces = var7.getNumberOfTraces()
                self.forceFilenameChain = False
        return True

    def resetStarted(self, var1):
        var1.started = False
        for var2 in range(var1.getChildCount()):
            self.resetStarted(var1.getChildAt(var2))

    def storeChain(self, var1, var2, var3, var4):
        var5 = var1
        var6 = var5.getModule()
        if isinstance(var6, Linkable):
            var6.setLinked(self.linked)
        self.linked = var6
        var4.append(var5.getDirectory() + ":" + var5.getModulePath() + ":" + str(var2))
        var7 = var6.getParameters()
        var4.append(str(var7))
        var4.append("\n")
        self.linked.finishModule()
        for var8 in range(var1.getChildCount()):
            var3 = self.storeChain(var1.getChildAt(var8), var3, var3 + 1, var4)
        return var3

    def process(self, var1):
        self.processCalled = True
        self.firstTrace = None
        var2 = None
        var3 = self.top.getChildCount()
        if var3 == 0:
            return var1
        for var4 in range(var3):
            var2 = self.processNode(self.top.getChildAt(var4), var1, var4 == 0)
        self.started = True
        return var2

    def generate(self, var1):
        if var1 == 0:
            if self.processCalled:
                self.isAcquisition = False
            else:
                self.isAcquisition = True
        if self.isAcquisition:
            return self.process(None)
        else:
            return None

    def processNode(self, var1, var2, var3):
        var4 = var1
        var5 = var2 is None
        try:
            var6 = var4.getModule()
            var7 = None
            if var3 and not self.started and not var5:
                var8 = var2.getTraceSet()
                if var2.sampleFrequency != 0.0 and var2.sampleFrequency != 1.0:
                    self.xScale = 1.0 / var2.sampleFrequency
                elif var8 is not None:
                    self.xScale = var8.getXScale()
                if var8 is not None:
                    self.yScale = var8.getYScale()
                    self.xLabel = var8.getXLabel()
                    self.yLabel = var8.getYLabel()
            if not self.started or not var4.started:
                var6.setFloat(6, self.xScale)
                var6.setFloat(7, self.yScale)
                var6.setString(12, self.xLabel)
                var6.setString(13, self.yLabel)
                var13 = var6.getInt(26)
                var9 = var6.getInt(27)
                var10 = var6.getBoolean(32)
                var6.setBoolean(32, False)
                var6.init(var2, self.pi, self.nt, self.firstTraceIndex, self.numberOfTraces, var13,
                          var9 if var9 != 0 else self.suggestedNumberOfSamples)
                var6.setBoolean(32, var10)
                var6.getBoolean(30)
                var4.started = True
            if not var5:
                if not hasattr(var6, 'Inspector400'):
                    var2.forceSample()
                var6.analyze(var2)
            var2 = var6.get()
            if var2 is None:
                return None
            var14 = var1.getChildCount()
            if var14 == 0 or var5:
                if not self.started:
                    self.sampleFrequency = var2.sampleFrequency
                    self.xScale = 1.0 / self.sampleFrequency if self.sampleFrequency > 0.0 and self.sampleFrequency != 1.0 else var6.getFloat(
                        6)
                    self.yScale = var6.getFloat(7)
                    self.xLabel = var6.getString(12)
                    self.yLabel = var6.getString(13)
                    self.logScale = var6.getInt(20) != 0
                if var14 == 0:
                    return var2
            for var15 in range(var14):
                var7 = self.processNode(var1.getChildAt(var15), var2, False)
            return var7
        except Exception as var11:
            raise RuntimeError(var11)

    def get(self):
        if not self.finished:
            return None
        var1 = self.top
        if var1 is None:
            return None
        var2 = 0
        while True:
            var2 = var1.getChildCount()
            if var2 > 0:
                var1 = var1.getChildAt(var2 - 1)
            else:
                break
        if isinstance(var1, ChainNode):
            var3 = var1.getModule()
            if var3 is not None:
                return var3.get()
        return None

    def finishModule(self):
        var1 = self.top.getChildCount()
        for var2 in range(var1):
            self.finishProcess(self.top.getChildAt(var2))
        self.finished = True
        self.save(self.getParameterFile())
        self.out(f"Finished after {(time.time() - self.time):.1f} s")

    def finishProcess(self):
        var1 = self.top.getChildCount()
        for var2 in range(var1):
            self.finishProcess(self.top.getChildAt(var2))
        self.finished = True
        self.save(self.getParameterFile())
        self.out(f"Finished after {(time.time() - self.time):.1f} s")

    def finishProcessNode(self, var1):
        var2 = var1
        try:
            var3 = var2.getModule()
            if var3 is not None:
                var3.finishProcess()
                var3.finishModule()
            var4 = var1.getChildCount()
            for var5 in range(var4):
                self.finishProcessNode(var1.getChildAt(var5))
        except Exception as var6:
            self.err(f"Error in module {var2}: {var6}")
            print(var6)

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

    def getDialogValues(self):
        pass

    def setDialogValues(self):
        pass

    def out(self, message):
        print(message)

    def err(self, message):
        print(message)


class Linkable(ABC):
    @abstractmethod
    def setLinked(self, linked):
        pass


class ChainNode:
    def __init__(self, text, dir="", modulePath="", module=None):
        self.text = text
        self.dir = dir
        self.modulePath = modulePath
        self.module = module
        self.started = False
        self.children = []
        self.parent = None

    def getText(self):
        return self.text

    def getDirectory(self):
        return self.dir

    def getModulePath(self):
        return self.modulePath

    def getModule(self):
        return self.module

    def getParent(self):
        return self.parent

    def getChildCount(self):
        return len(self.children)

    def getChildAt(self, index):
        return self.children[index]

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def insert(self, child, index):
        child.parent = self
        self.children.insert(index, child)

    def removeFromParent(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def removeAllChildren(self):
        for child in self.children:
            child.parent = None
        self.children = []

    def getIndex(self, child):
        return self.children.index(child)

    def getPreviousNode(self):
        if self.parent:
            idx = self.parent.getIndex(self)
            if idx > 0:
                return self.parent.getChildAt(idx - 1)
        return None

    def getLastChild(self):
        if self.children:
            return self.children[-1]
        return None

    def isRoot(self):
        return self.parent is None

    def getPath(self):
        path = []
        node = self
        while node:
            path.insert(0, node)
            node = node.parent
        return path

    def toString(self):
        return self.getText()


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

    def getTraceSet(self):
        return None

    def forceSample(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Chain()
    app.initModule()
    app.initDialog()
    root.mainloop()