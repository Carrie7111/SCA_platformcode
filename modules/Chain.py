import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from abc import ABC, abstractmethod
import time
import threading
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
        self.autoReload = True
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
        self.window = None
        self.pi = None

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

        chainButtonPanel = ttk.Frame(self.chainPanel)
        chainButtonPanel.pack(fill=tk.X, pady=5)

        self.addButton = ttk.Button(chainButtonPanel, text="添加", command=self.addButtonClicked)
        self.addButton.pack(side=tk.LEFT, padx=2)

        self.removeButton = ttk.Button(chainButtonPanel, text="移除", command=self.removeButtonClicked,
                                       state='disabled')
        self.removeButton.pack(side=tk.LEFT, padx=2)

        self.setupButton = ttk.Button(chainButtonPanel, text="设置", command=self.setupButtonClicked, state='disabled')
        self.setupButton.pack(side=tk.LEFT, padx=2)

        self.reloadButton = ttk.Button(chainButtonPanel, text="重载", command=self.reloadButtonClicked)
        self.reloadButton.pack(side=tk.LEFT, padx=2)

        if self.embedded:
            self.loadButton = ttk.Button(chainButtonPanel, text="加载", command=self.loadButtonClicked)
            self.loadButton.pack(side=tk.LEFT, padx=2)
            self.saveButton = ttk.Button(chainButtonPanel, text="保存", command=self.saveButtonClicked,
                                         state='disabled')
            self.saveButton.pack(side=tk.LEFT, padx=2)

        self.top = ChainNode(self.moduleTitle)
        self.selectedNode = self.top
        self.tree = ttk.Treeview(self.chainPanel)
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
        module = self.selectedNode.getModule()
        module.finishModule()
        self.removeNode(self.selectedNode)
        if self.saveButton is not None:
            self.saveButton.config(state='normal')

    def setupButtonClicked(self):
        try:
            if self.selectedNode == self.top:
                return
            module = self.selectedNode.getModule()
            prevNode = self.selectedNode.getPreviousNode()
            if prevNode != self.top and isinstance(module, Linkable):
                module.setLinked(prevNode.getModule())
            fs = module.getInt(26)
            sns = module.getInt(27)
            module.init(self.firstTrace, self.pi, self.nt, 0, 0, fs, sns if sns != 0 else self.suggestedNumberOfSamples)
        except Exception as exc:
            print(exc)

    def reloadButtonClicked(self):
        self.reload()

    def loadButtonClicked(self):
        self.load()

    def saveButtonClicked(self):
        self.save()

    def setPreferredSize(self, width, height):
        pass

    def setEmbedded(self, embedded):
        self.embedded = embedded
        self.autoReload = not embedded

    def getPanel(self):
        return self.chainPanel

    def actionPerformed(self, e):
        src = e
        if src == self.addButton:
            self.insertNode()
        elif src == self.removeButton:
            module = self.selectedNode.getModule()
            module.finishModule()
            self.removeNode(self.selectedNode)
            if self.saveButton is not None:
                self.saveButton.config(state='normal')
        elif src == self.reloadButton:
            self.reload()
        elif src == self.loadButton:
            self.load()
        elif src == self.saveButton:
            self.save()
        elif src == self.setupButton:
            try:
                if self.selectedNode == self.top:
                    return
                module = self.selectedNode.getModule()
                prevNode = self.selectedNode.getPreviousNode()
                if prevNode != self.top and isinstance(module, Linkable):
                    module.setLinked(prevNode.getModule())
                fs = module.getInt(26)
                sns = module.getInt(27)
                module.init(self.firstTrace, self.pi, self.nt, 0, 0, fs,
                            sns if sns != 0 else self.suggestedNumberOfSamples)
            except Exception as exc:
                print(exc)

    def valueChanged(self, e):
        self.selectedNode = e
        self.setupButton.config(state='normal' if self.selectedNode != self.top else 'disabled')
        self.removeButton.config(state='normal' if self.selectedNode != self.top else 'disabled')

    def mouseClicked(self, mouseEvent):
        self.expandAll()

    def mouseEntered(self, mouseEvent):
        pass

    def mouseMoved(self, mouseEvent):
        pass

    def mouseDragged(self, mouseEvent):
        if not self.dragging:
            if self.selectedNode.isRoot():
                return
            self.originalCursor = self.tree.cget("cursor")
            self.draggedNode = self.selectedNode
            self.dragging = True
        else:
            self.dragging = True

    def mouseExited(self, mouseEvent):
        pass

    def mousePressed(self, mouseEvent):
        pass

    def mouseReleased(self, mouseEvent):
        if self.dragging:
            self.dragging = False
            self.tree.config(cursor=self.originalCursor)
            self.tree.update()
            self.expandAll()

    def keyPressed(self, keyEvent):
        if keyEvent.keysym == 'Delete':
            self.removeNode(self.selectedNode)
        elif keyEvent.keysym == 'Insert':
            self.insertNode()

    def keyReleased(self, keyEvent):
        pass

    def keyTyped(self, keyEvent):
        pass

    def insertNode(self, className=None, classFile=None, index=-1, settings=None):
        pass

    def removeNode(self, node):
        if node == self.top:
            return
        cn = node
        module = cn.getModule()
        name = module.__class__.__name__
        if "XYAcquisition" in name or "ScopeAcquisition" in name:
            self.isAcquisition = False
        parent = node.getParent()
        idx = parent.getIndex(node)
        for i in range(node.getChildCount()):
            parent.insert(node.getChildAt(i), idx + i)
        node.removeAllChildren()
        node.removeFromParent()
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

    def load(self, chainFile=None, reload=False):
        pass

    def save(self):
        pass

    def getParametersAsString(self):
        sb = []
        parentIndex = 0
        index = 0
        self.linked = None
        for i in range(self.top.getChildCount()):
            index = self.storeChain(self.top.getChildAt(i), parentIndex, index + 1, sb)
        return ''.join(sb)

    def expandAll(self):
        pass

    def init(self, t, pi, nt, sft, snt, sfs, sns):
        if self.isAcquisition:
            self.firstTrace = None
            self.suggestedNumberOfSamples = 0
            self.nt = 0
        else:
            self.firstTrace = t
            self.suggestedNumberOfSamples = sns
            self.nt = nt
        return 0

    def initProcess(self):
        self.isAcquisition = False
        self.processCalled = False
        children = self.top.getChildCount()
        if children > 0:
            self.save(self.getParameterFile())
        self.finished = False
        self.started = False
        for i in range(children):
            self.resetStarted(self.top.getChildAt(i))
        self.time = time.time()
        self.forceFilenameChain = True
        if self.numberOfResultTraces == 0:
            if children > 0:
                node = self.top.getChildAt(0)
                module = node.getModule()
                if "GenericAcquisition" in module.__class__.__name__:
                    fs = module.getInt(26)
                    sns = module.getInt(27)
                    sd = module.getBoolean(32)
                    module.setBoolean(32, False)
                    module.init(self.firstTrace, self.pi, self.nt, self.firstTraceIndex, self.numberOfTraces, fs,
                                sns if sns != 0 else self.suggestedNumberOfSamples)
                    module.setBoolean(32, sd)
                    ga = module
                    self.numberOfResultTraces = ga.getNumberOfTraces()
                    self.forceFilenameChain = False
        return True

    def resetStarted(self, node):
        node.started = False
        for i in range(node.getChildCount()):
            self.resetStarted(node.getChildAt(i))

    def storeChain(self, node, parentIndex, index, sb):
        nv = node
        module = nv.getModule()
        if isinstance(module, Linkable):
            module.setLinked(self.linked)
        self.linked = module
        sb.append(nv.getDirectory() + ":" + nv.getModulePath() + ":" + str(parentIndex))
        parameters = module.getParameters()
        sb.append(str(parameters))
        sb.append("\n")
        self.linked.finishModule()
        for i in range(node.getChildCount()):
            index = self.storeChain(node.getChildAt(i), index, index + 1, sb)
        return index

    def process(self, t):
        self.processCalled = True
        self.firstTrace = None
        resultTrace = None
        children = self.top.getChildCount()
        if children == 0:
            return t
        for i in range(children):
            resultTrace = self.processNode(self.top.getChildAt(i), t, i == 0)
        self.started = True
        return resultTrace

    def generate(self, trace):
        if trace == 0:
            if self.processCalled:
                self.isAcquisition = False
            else:
                self.isAcquisition = True
        if self.isAcquisition:
            return self.process(None)
        else:
            return None

    def processNode(self, node, t, firstNode):
        nv = node
        noInputTrace = t is None
        try:
            module = nv.getModule()
            resultTrace = None
            if firstNode and not self.started and not noInputTrace:
                ts = t.getTraceSet()
                if t.sampleFrequency != 0 and t.sampleFrequency != 1:
                    self.xScale = 1 / t.sampleFrequency
                elif ts is not None:
                    self.xScale = ts.getXScale()
                if ts is not None:
                    self.yScale = ts.getYScale()
                    self.xLabel = ts.getXLabel()
                    self.yLabel = ts.getYLabel()
            if not self.started or not nv.started:
                module.setFloat(6, self.xScale)
                module.setFloat(7, self.yScale)
                module.setString(12, self.xLabel)
                module.setString(13, self.yLabel)
                fs = module.getInt(26)
                sns = module.getInt(27)
                sd = module.getBoolean(32)
                module.setBoolean(32, False)
                module.init(t, self.pi, self.nt, self.firstTraceIndex, self.numberOfTraces, fs,
                            sns if sns != 0 else self.suggestedNumberOfSamples)
                module.setBoolean(32, sd)
                module.getBoolean(30)
                nv.started = True
            if not noInputTrace:
                if not hasattr(module, 'Inspector400'):
                    t.forceSample()
                module.analyze(t)
            t = module.get()
            if t is None:
                return None
            children = node.getChildCount()
            if children == 0 or noInputTrace:
                if not self.started:
                    self.sampleFrequency = t.sampleFrequency
                    self.xScale = 1 / self.sampleFrequency if self.sampleFrequency > 0 and self.sampleFrequency != 1 else module.getFloat(
                        6)
                    self.yScale = module.getFloat(7)
                    self.xLabel = module.getString(12)
                    self.yLabel = module.getString(13)
                    self.logScale = module.getInt(20) != 0
                if children == 0:
                    return t
            for i in range(children):
                resultTrace = self.processNode(node.getChildAt(i), t, False)
            return resultTrace
        except Exception as e:
            raise RuntimeError(e)

    def get(self):
        if not self.finished:
            return None
        dmtn = self.top
        if dmtn is None:
            return None
        children = 0
        while True:
            children = dmtn.getChildCount()
            if children > 0:
                dmtn = dmtn.getChildAt(children - 1)
            else:
                break
        if isinstance(dmtn, ChainNode):
            module = dmtn.getModule()
            if module is not None:
                return module.get()
        return None

    def finishModule(self):
        children = self.top.getChildCount()
        for i in range(children):
            self.finishProcessNode(self.top.getChildAt(i))
        self.finished = True
        self.save(self.getParameterFile())
        self.out(f"Finished after {(time.time() - self.time):.1f} s")

    def finishProcess(self):
        children = self.top.getChildCount()
        for i in range(children):
            self.finishProcessNode(self.top.getChildAt(i))
        self.finished = True
        self.save(self.getParameterFile())
        self.out(f"Finished after {(time.time() - self.time):.1f} s")

    def finishProcessNode(self, node):
        nv = node
        try:
            module = nv.getModule()
            if module is not None:
                module.finishProcess()
                module.finishModule()
            children = node.getChildCount()
            for i in range(children):
                self.finishProcessNode(node.getChildAt(i))
        except Exception as e:
            self.err(f"Error in module {nv}: {e}")
            print(e)

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

    def getPreviousNode(self):
        if self.parent:
            idx = self.parent.getIndex(self)
            if idx > 0:
                return self.parent.getChildAt(idx - 1)
        return None

    def getIndex(self, child):
        return self.children.index(child)

    def getLastChild(self):
        if self.children:
            return self.children[-1]
        return None

    def isRoot(self):
        return self.parent is None

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