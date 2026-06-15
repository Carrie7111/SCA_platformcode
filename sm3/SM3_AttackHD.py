"""SM3 Hamming-distance differential analysis module (converted from SM3_AttackHD.java)."""

from __future__ import annotations

import math
import re
from typing import Any

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    tk = None
    ttk = None

from sm3.SM3 import SM3
from sm3.sm3_attack_hd_default import SM3AttackHDDefault

LOG10 = math.log(10)


class DifferentialAnalysis:
    """Minimal base class converted from crypto.DifferentialAnalysis."""

    max = 4
    keys = 1
    precisionDigits = 4
    bestCorrelationHeader = "最相关"
    keyTitle = "密钥"
    candidateTitle = "可能的密钥"
    keyOffset = 0
    candidates = 0
    precision = math.exp(math.log(10) * precisionDigits)
    candidateStringLength = 0
    mustReport = True
    mustGenerate = True
    prefix = ""
    moduleDescription = ""
    moduleVersion = ""
    helpFile = ""
    selectWindow = False
    titleSpace = 30
    bitGroup = 1
    dataLength = 0
    firstTraceIndex = 0
    lastTraceIndex = 0
    numberOfTraces = 0
    numberOfAnalyzedTraces = 0
    numberOfSamples = 0
    firstSampleIndex = 0
    currentTraceIndex = 0
    memoryReady = False
    xOffset = 0
    sampleDataCorrelation: list[float] = []

    def initModule(self) -> None:
        pass

    def init(self, t: Any, pi: Any, nt: int, sft: int, snt: int, sfs: int, sns: int) -> int:
        return 0

    def initProcess(self) -> bool:
        return True

    def finishProcess(self) -> None:
        pass

    def analyze(self, t: Any) -> None:
        pass

    def out(self, message: str) -> None:
        print(message)

    def set(self, key: str, value: Any) -> None:
        setattr(self, f"_param_{key}", value)

    def getLong(self, key: str) -> int:
        return int(getattr(self, f"_param_{key}", 0))

    def setDialogValues(self, t: Any = None, nt: int = 0, sft: int = 0, snt: int = 0, sfs: int = 0, sns: int = 0) -> None:
        pass

    def report(self, key: int, best: list[list[float]], fragmentOffset: int, fragmentEnd: int) -> None:
        if self.keys == 1:
            self.out(f"{self.bestCorrelationHeader}:")
        else:
            self.out(f"{self.bestCorrelationHeader} {self.keyTitle} {self.keyOffset + key}:")
        for i in range(min(self.max, len(best))):
            value = str(round(self.precision * best[i][2]) / self.precision)
            if not value.startswith("-"):
                value = " " + value
            while len(value) < self.precisionDigits + 3:
                value += "0"
            candidate = str(int(best[i][0]))
            while len(candidate) < self.candidateStringLength:
                candidate = " " + candidate
            candidate_hex = format(int(best[i][0]), "X")
            if len(candidate_hex) & 1:
                candidate_hex = "0" + candidate_hex
            candidate += f" (0x{candidate_hex})"
            self.out(
                f"{i}, {self.candidateTitle}: {candidate},值: {value},位置: {int(best[i][1]) + self.xOffset}"
            )

    def generate(self, index: int) -> Any:
        return None

    @staticmethod
    def hw(value: int) -> int:
        result = 0
        while value > 0:
            if value & 1:
                result += 1
            value >>= 1
        return result

    @staticmethod
    def formatNumberString(text: str, width: int) -> str:
        while len(text) < width:
            text = "0" + text
        return text

    @staticmethod
    def trim(text: str) -> str:
        return text.strip()

    def parseInt(self, widget: Any, key: str) -> int:
        if widget is None:
            return int(getattr(self, f"_param_{key}", 0))
        return int(widget.get())

    def getInt(self, panel: Any, key: str) -> int:
        return int(getattr(self, f"_param_{key}", 0))

    def setInt(self, widget: Any, key: str) -> None:
        if widget is not None and hasattr(widget, "delete"):
            widget.delete(0, tk.END)
            widget.insert(0, str(getattr(self, f"_param_{key}", 0)))

    def parseLong(self, widget: Any, key: str, min_len: int, max_len: int) -> int:
        if widget is None:
            return int(getattr(self, f"_param_{key}", 0))
        text = widget.get().strip()
        if not text:
            return 0
        return int(text, 16)


class SM3_AttackHD(DifferentialAnalysis):
    """Perform first-order differential analysis on SM3."""

    TRACK = "trackbit"
    ROUND = "round"
    KEY = "key"
    HWORHD = "hwd"
    ROUND_KEY_ONE = "roundone.key"
    ROUND_KEY_TWO = "roundtwo.key"
    ROUND_KEY_THREE = "roundthree.key"
    ROUND_KEY_FOUR = "roundfour.key"
    DEFAULT_ROUND_KEY = ""
    MAX = "max"
    KEY_ONE = "one.key"
    KEY_TWO = "two.key"
    KEY_THREE = "three.key"
    KEY_FOUR = "four.key"
    KEY_FIVE = "five.key"
    KEY_SIX = "six.key"
    KEY_SEVEN = "seven.key"
    KEY_EIGHT = "eight.key"
    KEY_NINE = "nine.key"
    KEY_TEN = "ten.key"

    fragmentLength = 0
    X = [0] * 68
    Y = [0] * 64
    T1 = SM3.T1
    T2 = SM3.T2
    digestInt = [0] * 8
    sr_check = False
    resultKey = 0

    def __init__(self) -> None:
        super().__init__()
        self.moduleBaseObj: SM3AttackHDDefault = SM3AttackHDDefault()
        self.tlink = None
        self.track = 8
        self.round = 0
        self.keynum = 0
        self.HWD = 0
        self.roundKeyone = 0
        self.roundKeytwo = 0
        self.roundKeythree = 0
        self.roundKeyfour = 0
        self.newRoundKey = 0
        self.Key = [0] * 10
        self.HW = 0
        self.Maxkey = 16
        self.keyButton: list[Any] = []
        self.KeyTextField: list[Any] = []
        self.maxTextField = None
        self.roundKeyTextFieldone = None
        self.roundKeyTextFieldtwo = None
        self.roundKeyTextFieldthree = None
        self.roundKeyTextFieldfour = None
        self.srCheckBox = None
        self.trackPanel = None
        self.roundPanel = None
        self.keyPanel = None
        self.hwPanel = None
        self.centerPanelsub = None
        self.southPanel = None
        self.midPanel = None
        self.initModule()

    def initModule(self) -> None:
        super().initModule()
        self.moduleBaseObj = SM3AttackHDDefault()
        self.prefix = "SM3 analysis results"
        self.moduleDescription = "Perform first order differential analysis on SM3"
        self.moduleVersion = "1.0"
        self.helpFile = "doc/modulesSM3Analysis.html"
        self.selectWindow = False
        self.keys = 1
        self.candidates = 256
        self.dataLength = self.keys * self.candidates
        self.max = 10
        self.keyOffset = 1
        self.candidateStringLength = math.ceil(math.log(self.candidates - 1) / LOG10)
        self.keyTitle = "S-Box"
        self.candidateTitle = "子密钥"
        self.titleSpace = 30

        self.set(self.MAX, self.max)
        self.set(self.TRACK, self.track)
        self.set(self.ROUND, self.round)
        self.set(self.KEY, self.keynum)
        self.set(self.ROUND_KEY_ONE, self.roundKeyone)
        self.set(self.ROUND_KEY_TWO, self.roundKeytwo)
        self.set(self.ROUND_KEY_THREE, self.roundKeythree)
        self.set(self.ROUND_KEY_FOUR, self.roundKeyfour)
        self.set(self.HWORHD, self.HWD)
        for idx, name in enumerate([
            self.KEY_ONE, self.KEY_TWO, self.KEY_THREE, self.KEY_FOUR,
            self.KEY_FIVE, self.KEY_SIX, self.KEY_SEVEN, self.KEY_EIGHT,
            self.KEY_NINE, self.KEY_TEN,
        ]):
            self.set(name, self.Key[idx])

    def initDialog(self) -> Any:
        if tk is None:
            return None

        center_panel = ttk.Frame(None)

        self.trackPanel = ttk.LabelFrame(center_panel, text="攻击比特位")
        track_group: dict[str, tk.Variable] = {}
        for i in range(9):
            last = i == 8
            track_string = str(i + 1) if not last else "所有"
            var = tk.StringVar(value=track_string)
            track_group[track_string] = var
            ttk.Radiobutton(self.trackPanel, text=track_string, variable=var, value=track_string).pack(side=tk.LEFT)

        self.midPanel = ttk.Frame(center_panel)
        self.roundPanel = ttk.LabelFrame(self.midPanel, text="轮数")
        for i, label in enumerate(["1", "2", "3", "4"]):
            ttk.Radiobutton(self.roundPanel, text=label, value=i).pack(side=tk.LEFT)

        self.srCheckBox = ttk.Checkbutton(self.midPanel, text="选择单次攻击")
        self.hwPanel = ttk.Frame(self.midPanel)
        self.hwPanel.pack()
        self.srCheckBox.pack(in_=self.hwPanel)

        self.keyPanel = ttk.LabelFrame(self.midPanel, text="攻击顺序")
        self.keyButton = []
        for i in range(10):
            btn = ttk.Radiobutton(self.keyPanel, text=str(i + 1), value=i, command=self.actionPerformed)
            btn.pack(side=tk.LEFT)
            self.keyButton.append(btn)

        self.centerPanelsub = ttk.Frame(center_panel)
        round_key_fields = [
            ("第1轮结果", "roundKeyTextFieldone"),
            ("第2轮结果", "roundKeyTextFieldtwo"),
            ("第3轮结果", "roundKeyTextFieldthree"),
            ("第4轮结果", "roundKeyTextFieldfour"),
        ]
        for title, attr in round_key_fields:
            frame = ttk.LabelFrame(self.centerPanelsub, text=title)
            field = ttk.Entry(frame)
            field.pack(fill=tk.BOTH, expand=True)
            setattr(self, attr, field)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.southPanel = ttk.Frame(center_panel)
        candidate_panel = ttk.LabelFrame(self.southPanel, text="候选密钥的个数")
        self.maxTextField = ttk.Entry(candidate_panel)
        self.maxTextField.insert(0, str(self.max))
        self.maxTextField.pack(fill=tk.BOTH, expand=True)
        candidate_panel.grid(row=0, column=0, sticky="nsew")

        key_labels = ["X：", "Y", "A0：", "E0", "B0", "C0", "D0", "F0", "G0", "H0"]
        self.KeyTextField = []
        for idx, label in enumerate(key_labels):
            frame = ttk.LabelFrame(self.southPanel, text=label)
            field = ttk.Entry(frame, state="disabled")
            field.pack(fill=tk.BOTH, expand=True)
            self.KeyTextField.append(field)
            frame.grid(row=(idx + 1) // 2, column=(idx + 1) % 2, sticky="nsew")

        self.southPanel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.midPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.centerPanelsub.pack(side=tk.CENTER, fill=tk.BOTH, expand=True)
        return center_panel

    def getDialogValues(self) -> None:
        self.max = self.parseInt(self.maxTextField, self.MAX)
        self.track = self.getInt(self.trackPanel, self.TRACK)
        self.round = self.getInt(self.roundPanel, self.ROUND)
        self.keynum = self.getInt(self.keyPanel, self.KEY)
        self.bitGroup = 1 if self.track < 8 else 8

        self.roundKeyone = self.parseLong(self.roundKeyTextFieldone, self.ROUND_KEY_ONE, 0, 16)
        self.roundKeytwo = self.parseLong(self.roundKeyTextFieldtwo, self.ROUND_KEY_TWO, 0, 16)
        self.roundKeythree = self.parseLong(self.roundKeyTextFieldthree, self.ROUND_KEY_THREE, 0, 16)

        key_names = [
            self.KEY_ONE, self.KEY_TWO, self.KEY_THREE, self.KEY_FOUR,
            self.KEY_FIVE, self.KEY_SIX, self.KEY_SEVEN, self.KEY_EIGHT,
            self.KEY_NINE, self.KEY_TEN,
        ]
        for idx, name in enumerate(key_names):
            self.Key[idx] = self.parseLong(self.KeyTextField[idx], name, 0, 16)

    def setDialogValues(self, t: Any = None, nt: int = 0, sft: int = 0, snt: int = 0, sfs: int = 0, sns: int = 0) -> None:
        if t is not None:
            super().setDialogValues(t, nt, sft, snt, sfs, sns)
            if getattr(t, "data", None) is not None:
                self.tlink = getattr(t, "ts", None)
            return

        self.setInt(self.maxTextField, self.MAX)
        self.setInt(self.trackPanel, self.TRACK)
        self.setInt(self.roundPanel, self.ROUND)
        self.setInt(self.keyPanel, self.KEY)
        self.setInt(self.hwPanel, self.HWORHD)

        for field, key in [
            (self.roundKeyTextFieldone, self.ROUND_KEY_ONE),
            (self.roundKeyTextFieldtwo, self.ROUND_KEY_TWO),
            (self.roundKeyTextFieldthree, self.ROUND_KEY_THREE),
        ]:
            value = self.getLong(key)
            if value != 0 and field is not None:
                field.configure(state="normal")
                field.delete(0, tk.END)
                field.insert(0, self.formatNumberString(format(value, "X"), 2))

        key_names = [
            self.KEY_ONE, self.KEY_TWO, self.KEY_THREE, self.KEY_FOUR,
            self.KEY_FIVE, self.KEY_SIX, self.KEY_SEVEN, self.KEY_EIGHT,
            self.KEY_NINE, self.KEY_TEN,
        ]
        for idx, name in enumerate(key_names):
            self.Key[idx] = self.getLong(name)
            if self.Key[idx] != 0 and self.KeyTextField[idx] is not None:
                self.KeyTextField[idx].configure(state="normal")
                self.KeyTextField[idx].delete(0, tk.END)
                self.KeyTextField[idx].insert(0, self.formatNumberString(format(self.Key[idx], "X"), 2))

    def updateEnabledPanels(self) -> None:
        if self.srCheckBox is not None:
            self.sr_check = bool(self.srCheckBox.instate(["selected"]))
        for temp in range(10):
            if self.keyButton and hasattr(self.keyButton[temp], "instate") and self.keyButton[temp].instate(["selected"]):
                self.renewTextField(temp)

    def renewTextField(self, i: int) -> None:
        for j1 in range(10):
            if self.KeyTextField[j1] is None:
                continue
            state = "normal" if j1 < i else "disabled"
            self.KeyTextField[j1].configure(state=state)

    def actionPerformed(self, evt: Any = None) -> None:
        self.updateEnabledPanels()

    def select(self, t: Any) -> list[float]:
        attack_obj = self.moduleBaseObj
        attack_obj.module = self
        attack_obj.dataLength = self.dataLength
        attack_obj.round = self.round
        attack_obj.keynum = self.keynum
        attack_obj.track = self.track
        attack_obj.T1 = self.T1
        attack_obj.roundKeyone = self.roundKeyone
        attack_obj.roundKeytwo = self.roundKeytwo
        attack_obj.roundKeythree = self.roundKeythree
        attack_obj.Key = self.Key
        attack_obj.X = self.X
        attack_obj.Y = self.Y

        ret = attack_obj.GetMidDataHW(t.data)

        self.dataLength = attack_obj.dataLength
        self.round = attack_obj.round
        self.keynum = attack_obj.keynum
        self.track = attack_obj.track
        self.roundKeyone = attack_obj.roundKeyone
        self.roundKeytwo = attack_obj.roundKeytwo
        self.roundKeythree = attack_obj.roundKeythree
        self.Key = attack_obj.Key
        self.X = attack_obj.X
        self.Y = attack_obj.Y
        return ret

    def init(self, t: Any, pi: Any, nt: int, sft: int, snt: int, sfs: int, sns: int) -> int:
        r = super().init(t, pi, nt, sft, snt, sfs, sns)
        trace_first = self.firstTraceIndex
        trace_number = self.numberOfTraces
        self.roundKeyone = self.getLong(self.ROUND_KEY_ONE)
        self.roundKeytwo = self.getLong(self.ROUND_KEY_TWO)
        self.roundKeythree = self.getLong(self.ROUND_KEY_THREE)

        if self.sr_check:
            for i in range(4):
                self.roundKeyone = self.getLong(self.ROUND_KEY_ONE)
                self.roundKeytwo = self.getLong(self.ROUND_KEY_TWO)
                self.roundKeythree = self.getLong(self.ROUND_KEY_THREE)
                if hasattr(pi, "initProgress"):
                    pi.initProgress(f"TN{i}T{i}C0")
                self.round = i

                for k in range(self.firstTraceIndex, self.lastTraceIndex + 1):
                    if hasattr(pi, "updateProgressPanel"):
                        pi.updateProgressPanel(f"RD {i + 1}", f"CN {k}", True)
                    try:
                        self.analyze(self.tlink.getTrace(k, self.firstSampleIndex, self.numberOfSamples))
                    except Exception:
                        self.out("错误！")
                self.finishProcess()
                self.numberOfAnalyzedTraces = 0
                self.memoryReady = False
                if hasattr(pi, "finishProgress"):
                    pi.finishProgress(True, True)
                self.firstTraceIndex = trace_first
                self.numberOfTraces = trace_number
                self.lastTraceIndex = self.firstTraceIndex + self.numberOfTraces - 1
                self.currentTraceIndex = self.firstTraceIndex

            if self.round == 3:
                self.round += 1
            self.initProcess()
        return r

    def report(self, key: int, best: list[list[float]], fragmentOffset: int, fragmentEnd: int) -> None:
        if self.round > 3:
            return
        super().report(key, best, fragmentOffset, fragmentEnd)

        if key == 0:
            self.newRoundKey = 0

        value = str(round(self.precision * best[0][2]) / self.precision)
        if not value.startswith("-"):
            self.newRoundKey = (self.newRoundKey << 8) + int(best[0][0])
        else:
            self.newRoundKey = (self.newRoundKey << 8) + int(best[1][0])

        if key < self.keys - 1:
            return

        s = self.formatNumberString(format(self.newRoundKey, "X").upper(), 2)

        if self.round < 4:
            if self.round == 0:
                self.set(self.ROUND_KEY_ONE, self.newRoundKey)
                self.out(f"中间值_1: {s}")
            elif self.round == 1:
                self.set(self.ROUND_KEY_TWO, self.newRoundKey)
                self.out(f"中间值_2: {s}")
            elif self.round == 2:
                self.set(self.ROUND_KEY_THREE, self.newRoundKey)
                self.out(f"中间值_3: {s}")
            elif self.round == 3:
                self.set(self.ROUND_KEY_FOUR, self.newRoundKey)
                self.out(f"中间值_4: {s}")

                self.resultKey = (
                    self.roundKeyone
                    + (self.roundKeytwo << 8)
                    + (self.roundKeythree << 16)
                    + (self.newRoundKey << 24)
                )
                result = self.formatNumberString(format(self.resultKey, "X").upper(), 2)

                if self.keynum == 0:
                    self.out(f"当前X的值: {result}")
                    self.set(self.KEY_ONE, self.resultKey)
                elif self.keynum == 1:
                    self.out(f"当前Y的值: {result}")
                    self.set(self.KEY_TWO, self.resultKey)
                elif self.keynum == 2:
                    self.out(f"当前A0的值: {result}")
                    self.set(self.KEY_THREE, self.resultKey)
                elif self.keynum == 3:
                    self.out(f"当前E0的值: {result}")
                    self.set(self.KEY_FOUR, self.resultKey)
                elif self.keynum == 4:
                    self.resultKey = SM3.ROR(self.resultKey, 9)
                    result = self.formatNumberString(format(self.resultKey, "X").upper(), 2)
                    self.out(f"当前B0的值: {result}")
                    self.set(self.KEY_FIVE, self.resultKey)
                elif self.keynum == 5:
                    self.out(f"当前C0的值: {result}")
                    self.set(self.KEY_SIX, self.resultKey)
                elif self.keynum == 6:
                    self.out(f"当前D0的值: {result}")
                    self.set(self.KEY_SEVEN, self.resultKey)
                elif self.keynum == 7:
                    self.resultKey = SM3.ROR(self.resultKey, 19)
                    result = self.formatNumberString(format(self.resultKey, "X").upper(), 2)
                    self.out(f"当前F0的值: {result}")
                    self.set(self.KEY_EIGHT, self.resultKey)
                elif self.keynum == 8:
                    self.out(f"当前G0的值: {result}")
                    self.set(self.KEY_NINE, self.resultKey)
                elif self.keynum == 9:
                    self.out(f"当前H0的值: {result}")
                    self.set(self.KEY_TEN, self.resultKey)

    def generate(self, index: int) -> Any:
        t = super().generate(index)
        if t is not None and hasattr(t, "setTitle"):
            t.setTitle(
                f"Candidate {index % self.candidates} of Candidate{(index // self.candidates) + 1}"
            )
        return t

    def checkDialogValues(self) -> bool:
        message: list[str] = []
        fields = [f.get() if f is not None else "" for f in self.KeyTextField[:10]]
        pattern = re.compile(r"([A-F]|[a-f]|[0-9]|-|_){1,8}")

        if self.max > 256 or self.max < 2:
            message.append("候选密钥数为[2,256]")

        checks = {
            2: [(fields[0], "X应为8位16进制数！")],
            3: [(fields[1], "Y应为8位16进制数！")],
            4: [(fields[0], "X和A0应都为8位16进制数！"), (fields[2], "X和A0应都为8位16进制数！")],
            5: [
                (fields[0], "X、Y、A0、B0应都为8位16进制数！"),
                (fields[1], "X、Y、A0、B0应都为8位16进制数！"),
                (fields[2], "X、Y、A0、B0应都为8位16进制数！"),
                (fields[4], "X、Y、A0、B0应都为8位16进制数！"),
            ],
            6: [
                (fields[2], "A0、E0、B0、C0应都为8位16进制数！"),
                (fields[3], "A0、E0、B0、C0应都为8位16进制数！"),
                (fields[4], "A0、E0、B0、C0应都为8位16进制数！"),
                (fields[5], "A0、E0、B0、C0应都为8位16进制数！"),
            ],
            7: [(fields[1], "Y、E0应都为8位16进制数！"), (fields[3], "Y、E0应都为8位16进制数！")],
            8: [
                (fields[0], "X、Y、E0、F0应都为8位16进制数！"),
                (fields[1], "X、Y、E0、F0应都为8位16进制数！"),
                (fields[3], "X、Y、E0、F0应都为8位16进制数！"),
                (fields[7], "X、Y、E0、F0应都为8位16进制数！"),
            ],
            9: [
                (fields[2], "A0、E0、F0、G0应都为8位16进制数！"),
                (fields[3], "A0、E0、F0、G0应都为8位16进制数！"),
                (fields[7], "A0、E0、F0、G0应都为8位16进制数！"),
                (fields[8], "A0、E0、F0、G0应都为8位16进制数！"),
            ],
        }

        if self.keynum in checks:
            for text, err in checks[self.keynum]:
                if not pattern.match(self.trim(text)):
                    message.append(err)
                    break

        if not message:
            return True

        self.out("模块设置错误: " + "".join(message))
        return False
