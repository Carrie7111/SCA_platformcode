"""Average trace computation module (converted from Average.java)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    tk = None
    ttk = None

NO_TRACE = -1


@dataclass
class Trace:
    """Minimal Trace class converted from com.module.core.Trace."""

    title: str
    data: bytes | bytearray | None
    sample: list[float]

    def getSample(self) -> list[float]:
        return self.sample

    def getData(self) -> bytes | bytearray | None:
        return self.data

    def getTraceSet(self) -> Any:
        return getattr(self, "trace_set", None)

    def setTitle(self, title: str) -> None:
        self.title = title


class Module:
    """Minimal base class converted from com.module.core.Module."""

    titleSpace = 0
    moduleTitle = ""
    moduleDescription = ""
    helpFile = ""
    moduleVersion = ""
    selectWindow = False
    numberOfTraces = 0
    numberOfAnalyzedTraces = 0
    numberOfSamples = 0
    numberOfResultTraces = 0
    firstTraceIndex = 0
    lastTraceIndex = 0
    currentTraceIndex = 0
    firstSampleIndex = 0
    sampleCoding = 0
    logScale = False
    aborted = False

    def set(self, key: str, value: Any) -> None:
        setattr(self, f"_param_{key}", value)

    def getInt(self, panel: Any, key: str) -> int:
        return int(getattr(self, f"_param_{key}", 0))

    def setInt(self, panel: Any, key: str) -> None:
        pass

    def out(self, message: str) -> None:
        print(message)


class Average(Module):
    """Computes average trace of input trace set."""

    METHOD = "method"
    LABEL = "Average"
    PER_SAMPLE = 0
    PER_TRACE = 1

    def __init__(self) -> None:
        super().__init__()
        self.average: list[float] = []
        self.traceButton: Any = None
        self.sampleButton: Any = None
        self.applicationPanel: Any = None
        self.perTrace = False
        self.length = 0
        self.method = 0
        self.tracedata: bytes | bytearray | None = None
        self._method_var: Any = None
        self.initModule()

    def initModule(self) -> None:
        self.titleSpace = len(self.LABEL)
        self.moduleTitle = "Average"
        self.moduleDescription = "Computes average trace of input trace set"
        self.helpFile = "doc/manual/modulesAverage.html"
        self.moduleVersion = "1.4"
        self.selectWindow = True
        self.method = 0
        self.set(self.METHOD, self.method)

    def initDialog(self) -> Any:
        if tk is None:
            return None

        self.applicationPanel = ttk.LabelFrame(None, text="Application")
        self._method_var = tk.IntVar(value=self.PER_SAMPLE)

        self.sampleButton = ttk.Radiobutton(
            self.applicationPanel,
            text="Per sample",
            variable=self._method_var,
            value=self.PER_SAMPLE,
        )
        self.sampleButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.traceButton = ttk.Radiobutton(
            self.applicationPanel,
            text="Per trace",
            variable=self._method_var,
            value=self.PER_TRACE,
        )
        self.traceButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        return self.applicationPanel

    def getRequiredMemorySize(self) -> int:
        self.length = self.numberOfTraces if self.perTrace else self.numberOfSamples
        return self.length * (self.sampleCoding & 0xF)

    def getDialogValues(self) -> None:
        if self._method_var is not None:
            self.method = int(self._method_var.get())
        else:
            self.method = self.getInt(self.applicationPanel, self.METHOD)
        self.perTrace = self.method == self.PER_TRACE
        self.set(self.METHOD, self.method)

    def setDialogValues(self) -> None:
        if self._method_var is not None:
            self._method_var.set(self.getInt(self.applicationPanel, self.METHOD))
        else:
            self.setInt(self.applicationPanel, self.METHOD)

    def initProcess(self) -> bool:
        self.average = [0.0] * self.length
        self.tracedata = None
        return True

    def analyze(self, t: Trace) -> int:
        sample = t.getSample()

        if self.perTrace:
            for i in range(self.numberOfSamples):
                self.average[self.numberOfAnalyzedTraces] += sample[i]
        else:
            for i in range(self.numberOfSamples):
                self.average[i] += sample[i]

        if self.tracedata is None:
            self.tracedata = t.getData()
        else:
            current_data = t.getData()
            if current_data is None:
                equal = self.tracedata is None
            elif self.tracedata is None:
                equal = False
            else:
                equal = bytes(self.tracedata) == bytes(current_data)
            if not equal:
                self.tracedata = b""

        self.numberOfAnalyzedTraces += 1
        trace_set = t.getTraceSet()
        if trace_set is not None:
            is_log_scale = getattr(trace_set, "isLogScale", False)
            self.logScale = is_log_scale() if callable(is_log_scale) else bool(is_log_scale)

        if self.currentTraceIndex < self.lastTraceIndex and not self.aborted:
            self.currentTraceIndex += 1
            return self.currentTraceIndex

        self.numberOfResultTraces = 1
        self.currentTraceIndex = NO_TRACE
        return NO_TRACE

    def finishProcess(self) -> None:
        self.numberOfResultTraces = 1

    def generate(self, index: int) -> Trace | None:
        if index == 0:
            if self.numberOfAnalyzedTraces > 0:
                divisor = self.numberOfSamples if self.perTrace else self.numberOfAnalyzedTraces
                for i in range(self.length):
                    self.average[i] /= divisor
            if self.length > 1:
                return Trace(self.LABEL, self.tracedata, self.average)
            self.out(f"Average: {self.average[0]}")
        return None
