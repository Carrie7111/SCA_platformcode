import tkinter as tk
from tkinter import ttk, messagebox
import re
import math
from Des import Des


class DesSboxOut:
    SBOX_OUTPUT = 0
    XOR_OUTPUT = 1
    ABSOLUTE = 0
    SBOX_INPUT = 1
    ROUND_INPUT = 2
    ALL = 4
    HW = 5
    DES_ENCRYPT = 0
    DES_DECRYPT = 1
    BIT = "bit"
    ROUND = "round"
    TDES = "tdes"
    ENCRYPT = "encrypt"
    MODEL = "model"
    TARGET = "target"
    ROUND_KEY = "round.key"
    DES_1_KEY = "des.1.key"
    DES_2_KEY = "des.2.key"
    DES_3_KEY = "des.3.key"
    WHICH_DES = "which.des"
    KEY_SIZE = "key.size"
    MAX_TESTS = 1000000
    KEYS = 8
    KEY_BITS = 6

    k = [0x0, 0x41041041041, 0x82082082082, 0xc30c30c30c3, 0x104104104104, 0x145145145145, 0x186186186186,
         0x1c71c71c71c7, 0x208208208208, 0x249249249249, 0x28a28a28a28a, 0x2cb2cb2cb2cb, 0x30c30c30c30c, 0x34d34d34d34d,
         0x38e38e38e38e, 0x3cf3cf3cf3cf, 0x410410410410, 0x451451451451, 0x492492492492, 0x4d34d34d34d3, 0x514514514514,
         0x555555555555, 0x596596596596, 0x5d75d75d75d7, 0x618618618618, 0x659659659659, 0x69a69a69a69a, 0x6db6db6db6db,
         0x71c71c71c71c, 0x75d75d75d75d, 0x79e79e79e79e, 0x7df7df7df7df, 0x820820820820, 0x861861861861, 0x8a28a28a28a2,
         0x8e38e38e38e3, 0x924924924924, 0x965965965965, 0x9a69a69a69a6, 0x9e79e79e79e7, 0xa28a28a28a28, 0xa69a69a69a69,
         0xaaaaaaaaaaaa, 0xaebaebaebaeb, 0xb2cb2cb2cb2c, 0xb6db6db6db6d, 0xbaebaebaebae, 0xbefbefbefbef, 0xc30c30c30c30,
         0xc71c71c71c71, 0xcb2cb2cb2cb2, 0xcf3cf3cf3cf3, 0xd34d34d34d34, 0xd75d75d75d75, 0xdb6db6db6db6, 0xdf7df7df7df7,
         0xe38e38e38e38, 0xe79e79e79e79, 0xebaebaebaeba, 0xefbefbefbefb, 0xf3cf3cf3cf3c, 0xf7df7df7df7d, 0xfbefbefbefbe,
         0xffffffffffff]

    def __init__(self, parent=None):
        self.parent = parent
        self.window = None

        self.roundKeyString = ""
        self.datalen = 0
        self.tdes = False
        self.inputAndOutput = False
        self.encrypt = True
        self.targetDes = 0
        self.oldTargetDes = 0
        self.bit = self.HW
        self.selectedRound = 0
        self.round = 0
        self.model = self.ABSOLUTE
        self.target = self.SBOX_OUTPUT
        self.mismatches = 0
        self.encryptOption = self.DES_ENCRYPT
        self.keySize = 0
        self.keyBits = self.KEY_BITS
        self.roundKey = 0
        self.newRoundKey = 0
        self.desKey = 0
        self.des2Key = 0
        self.des3Key = 0
        self.testInput = 0
        self.testOutput = 0

        self.keys = self.KEYS
        self.keyOffset = 1
        self.dataLength = 512
        self.targets = 1
        self.candidates = 0
        self.weight = 4
        self.signalsPerKey = 0
        self.candidateStringLength = 0
        self.max = 64
        self.xorMask = 0
        self.numberOfSamples = 0
        self.fragmentLength = 0

        self.roundKeyTextField = None
        self.desKeyTextField = None
        self.des2KeyTextField = None
        self.des3KeyTextField = None
        self.bit1Button = None
        self.bit2Button = None
        self.bit3Button = None
        self.bit4Button = None
        self.hwButton = None
        self.allButton = None
        self.round1Button = None
        self.round2Button = None
        self.round15Button = None
        self.round16Button = None
        self.encryptButton = None
        self.decryptButton = None
        self.sboxButton = None
        self.xorButton = None
        self.firstDesButton = None
        self.secondDesButton = None
        self.thirdDesButton = None
        self.twoKeysButton = None
        self.threeKeysButton = None
        self.tdesCheckBox = None
        self.absButton = None
        self.sButton = None
        self.roundButton = None

        self.roundKeyVar = tk.StringVar()
        self.desKeyVar = tk.StringVar()
        self.des2KeyVar = tk.StringVar()
        self.des3KeyVar = tk.StringVar()
        self.bitVar = tk.IntVar(value=self.HW)
        self.roundVar = tk.IntVar(value=1)
        self.tdesVar = tk.BooleanVar(value=False)
        self.encryptVar = tk.IntVar(value=self.DES_ENCRYPT)
        self.targetVar = tk.IntVar(value=self.SBOX_OUTPUT)
        self.modelVar = tk.IntVar(value=self.ABSOLUTE)
        self.whichDesVar = tk.IntVar(value=0)
        self.keySizeVar = tk.IntVar(value=0)

    def initModule(self):
        self.moduleTitle = "DesAdvancedAnalysis"
        self.prefix = "Des Advanced analysis results"
        self.moduleDescription = "Perform advanced differential analysis on DES by computation of the correlation between data and samples"
        self.moduleVersion = "1.9"
        self.selectWindow = False
        self.keyTitle = "S盒"
        self.candidateTitle = "子密钥"
        self.titleSpace = 36
        self.keys = self.KEYS
        self.keyBits = self.KEY_BITS
        self.keyOffset = 1
        self.encryptOption = self.DES_ENCRYPT
        self.oldTargetDes = 0
        self.bit = self.HW
        self.round = 0
        self.model = self.ABSOLUTE
        self.target = self.SBOX_OUTPUT
        self.roundKey = self.desKey = self.des2Key = self.des3Key = 0
        self.set(self.WHICH_DES, self.targetDes)
        self.set(self.KEY_SIZE, self.keySize)
        self.set(self.BIT, self.bit)
        self.set(self.ROUND, self.round)
        self.set(self.TDES, self.tdes)
        self.set(self.ENCRYPT, self.encryptOption)
        self.set(self.MODEL, self.model)
        self.set(self.TARGET, self.target)
        self.set(self.ROUND_KEY, self.roundKey)
        self.set(self.DES_1_KEY, self.desKey)
        self.set(self.DES_2_KEY, self.des2Key)
        self.set(self.DES_3_KEY, self.des3Key)

    def initDialog(self):
        if self.window is None:
            self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
            self.window.title("DES分析设置")
            self.window.geometry("700x450")

        centerPanel = ttk.Frame(self.window)
        centerPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        centerPanel.configure(borderwidth=2, relief="groove")

        northPanel = ttk.Frame(centerPanel)
        northPanel.pack(fill=tk.X, pady=5)

        desPanel = ttk.LabelFrame(northPanel, text="Des设置")
        desPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        encryptPanel = ttk.Frame(desPanel)
        encryptPanel.pack(side=tk.RIGHT)
        self.encryptButton = ttk.Radiobutton(encryptPanel, text="加密", variable=self.encryptVar,
                                             value=self.DES_ENCRYPT, command=self.actionPerformed)
        self.encryptButton.pack(side=tk.LEFT)
        self.decryptButton = ttk.Radiobutton(encryptPanel, text="解密", variable=self.encryptVar,
                                             value=self.DES_DECRYPT, command=self.actionPerformed)
        self.decryptButton.pack(side=tk.LEFT)

        self.tdesCheckBox = ttk.Checkbutton(desPanel, text="3DES", variable=self.tdesVar, command=self.actionPerformed)
        self.tdesCheckBox.pack(side=tk.LEFT, padx=10)

        trackPanel = ttk.LabelFrame(northPanel, text="Track bit")
        trackPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.bit1Button = ttk.Radiobutton(trackPanel, text="1", variable=self.bitVar, value=1,
                                          command=self.actionPerformed)
        self.bit1Button.pack(side=tk.LEFT, padx=2)
        self.bit2Button = ttk.Radiobutton(trackPanel, text="2", variable=self.bitVar, value=2,
                                          command=self.actionPerformed)
        self.bit2Button.pack(side=tk.LEFT, padx=2)
        self.bit3Button = ttk.Radiobutton(trackPanel, text="3", variable=self.bitVar, value=3,
                                          command=self.actionPerformed)
        self.bit3Button.pack(side=tk.LEFT, padx=2)
        self.bit4Button = ttk.Radiobutton(trackPanel, text="4", variable=self.bitVar, value=4,
                                          command=self.actionPerformed)
        self.bit4Button.pack(side=tk.LEFT, padx=2)
        self.allButton = ttk.Radiobutton(trackPanel, text="All", variable=self.bitVar, value=self.ALL,
                                         command=self.actionPerformed)
        self.allButton.pack(side=tk.LEFT, padx=2)
        self.hwButton = ttk.Radiobutton(trackPanel, text="HW", variable=self.bitVar, value=self.HW,
                                        command=self.actionPerformed)
        self.hwButton.pack(side=tk.LEFT, padx=2)

        roundPanel = ttk.LabelFrame(northPanel, text="轮数")
        roundPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.round1Button = ttk.Radiobutton(roundPanel, text="1", variable=self.roundVar, value=1,
                                            command=self.actionPerformed)
        self.round1Button.pack(side=tk.LEFT, padx=5)
        self.round2Button = ttk.Radiobutton(roundPanel, text="2", variable=self.roundVar, value=2,
                                            command=self.actionPerformed)
        self.round2Button.pack(side=tk.LEFT, padx=5)

        keyLengthPanel = ttk.LabelFrame(northPanel, text="密钥长度")
        keyLengthPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        keySizePanel = ttk.Frame(keyLengthPanel)
        keySizePanel.pack(side=tk.RIGHT)
        self.twoKeysButton = ttk.Radiobutton(keySizePanel, text="112", variable=self.keySizeVar, value=0,
                                             command=self.actionPerformed)
        self.twoKeysButton.pack(side=tk.LEFT)
        self.threeKeysButton = ttk.Radiobutton(keySizePanel, text="168", variable=self.keySizeVar, value=1,
                                               command=self.actionPerformed)
        self.threeKeysButton.pack(side=tk.LEFT)

        southPanel = ttk.Frame(centerPanel)
        southPanel.pack(fill=tk.X, pady=5)

        roundKeyPanel = ttk.LabelFrame(southPanel, text="第一轮轮子密钥")
        roundKeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.roundKeyTextField = ttk.Entry(roundKeyPanel, textvariable=self.roundKeyVar, width=20)
        self.roundKeyTextField.pack(padx=5, pady=5)
        self.roundKeyTextField.bind('<KeyRelease>', self.keyReleased)

        targetPanel = ttk.LabelFrame(southPanel, text="Target")
        targetPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.sboxButton = ttk.Radiobutton(targetPanel, text="S盒", variable=self.targetVar, value=self.SBOX_OUTPUT,
                                          command=self.actionPerformed)
        self.sboxButton.pack(side=tk.LEFT, padx=5)
        self.xorButton = ttk.Radiobutton(targetPanel, text="异或", variable=self.targetVar, value=self.XOR_OUTPUT,
                                         command=self.actionPerformed)
        self.xorButton.pack(side=tk.LEFT, padx=5)

        modelPanel = ttk.LabelFrame(southPanel, text="Model")
        modelPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.absButton = ttk.Radiobutton(modelPanel, text="Abs", variable=self.modelVar, value=self.ABSOLUTE,
                                         command=self.actionPerformed)
        self.absButton.pack(side=tk.LEFT, padx=5)
        self.sButton = ttk.Radiobutton(modelPanel, text="S盒", variable=self.modelVar, value=self.SBOX_INPUT,
                                       command=self.actionPerformed)
        self.sButton.pack(side=tk.LEFT, padx=5)
        self.roundButton = ttk.Radiobutton(modelPanel, text="轮", variable=self.modelVar, value=self.ROUND_INPUT,
                                           command=self.actionPerformed)
        self.roundButton.pack(side=tk.LEFT, padx=5)

        desSelPanel = ttk.LabelFrame(southPanel, text="Target DES")
        desSelPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        whichDesPanel = ttk.Frame(desSelPanel)
        whichDesPanel.pack(side=tk.RIGHT)
        self.firstDesButton = ttk.Radiobutton(whichDesPanel, text="1", variable=self.whichDesVar, value=0,
                                              command=self.actionPerformed)
        self.firstDesButton.pack(side=tk.LEFT)
        self.secondDesButton = ttk.Radiobutton(whichDesPanel, text="2", variable=self.whichDesVar, value=1,
                                               command=self.actionPerformed)
        self.secondDesButton.pack(side=tk.LEFT)
        self.thirdDesButton = ttk.Radiobutton(whichDesPanel, text="3", variable=self.whichDesVar, value=2,
                                              command=self.actionPerformed)
        self.thirdDesButton.pack(side=tk.LEFT)

        keysPanel = ttk.Frame(centerPanel)
        keysPanel.pack(fill=tk.X, pady=5)

        des1KeyPanel = ttk.LabelFrame(keysPanel, text="First Des key")
        des1KeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.desKeyTextField = ttk.Entry(des1KeyPanel, textvariable=self.desKeyVar, width=20)
        self.desKeyTextField.pack(padx=5, pady=5)
        self.desKeyTextField.bind('<KeyRelease>', self.keyReleased)

        des2KeyPanel = ttk.LabelFrame(keysPanel, text="Second Des key")
        des2KeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.des2KeyTextField = ttk.Entry(des2KeyPanel, textvariable=self.des2KeyVar, width=20)
        self.des2KeyTextField.pack(padx=5, pady=5)
        self.des2KeyTextField.bind('<KeyRelease>', self.keyReleased)

        des3KeyPanel = ttk.LabelFrame(keysPanel, text="Third Des key")
        des3KeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.des3KeyTextField = ttk.Entry(des3KeyPanel, textvariable=self.des3KeyVar, width=20)
        self.des3KeyTextField.pack(padx=5, pady=5)
        self.des3KeyTextField.bind('<KeyRelease>', self.keyReleased)

        buttonFrame = ttk.Frame(centerPanel)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        self.updateEnabledPanels()

        return centerPanel

    def updateEnabledPanels(self):
        if self.roundVar.get() == 1:
            self.roundKeyTextField.config(state='disabled')
        else:
            self.roundKeyTextField.config(state='normal')

    def actionPerformed(self, evt=None):
        self.updateEnabledPanels()

    def keyReleased(self, event):
        tdes = self.tdesVar.get()
        if tdes:
            keySize = self.keySizeVar.get()
            if keySize == 0:
                if event.widget == self.des3KeyTextField:
                    self.desKeyVar.set(self.des3KeyVar.get())
                elif event.widget == self.desKeyTextField:
                    self.des3KeyVar.set(self.desKeyVar.get())
        self.actionPerformed()

    def setDialogValues(self, t=None, nt=0, sft=0, snt=0, sfs=0, sns=0):
        if t is None:
            self._setDialogValuesInternal()
            return
        if t.data is None:
            return
        self.datalen = len(t.data)
        self.inputAndOutput = len(t.data) >= 16
        self.testInput = self.toLong(t.data, 0, 8)
        self.testOutput = self.toLong(t.data, len(t.data) - 8, 8)
        self.testInput = Des.ip(self.testInput)
        self.testOutput = Des.ip(self.testOutput)

    def _setDialogValuesInternal(self):
        self.bitVar.set(self.bit)
        self.roundVar.set(self.selectedRound)
        self.tdesVar.set(self.tdes)
        self.encryptVar.set(self.encryptOption)
        self.targetVar.set(self.target)
        self.modelVar.set(self.model)
        self.whichDesVar.set(self.targetDes)
        self.keySizeVar.set(self.keySize)
        if self.roundKey != 0:
            self.roundKeyVar.set(self.formatNumberString(format(self.roundKey, 'x').upper(), 2))
        if self.desKey != 0:
            self.desKeyVar.set(self.formatNumberString(format(self.desKey, 'x').upper(), 2))
        if self.des2Key != 0:
            self.des2KeyVar.set(self.formatNumberString(format(self.des2Key, 'x').upper(), 2))
        if self.des3Key != 0:
            self.des3KeyVar.set(self.formatNumberString(format(self.des3Key, 'x').upper(), 2))
        self.updateEnabledPanels()

    def getDialogValues(self):
        self._getKeyValues()
        self.targetDes = self.whichDesVar.get()
        self.bit = self.bitVar.get()
        self.selectedRound = self.roundVar.get()
        self.tdes = self.tdesVar.get()
        self.encrypt = (self.encryptVar.get() == self.DES_ENCRYPT)
        self.encryptOption = self.encryptVar.get()
        if not self.tdes:
            self.targetDes = 0
        self.round = self.selectedRound
        self.target = self.targetVar.get()
        self.model = self.modelVar.get()
        self.target = 0
        self.model = 0
        self.keySize = self.keySizeVar.get()
        self.dataLength = 512
        self.targets = 1
        self.candidates = self.dataLength // self.keys
        if self.bit == self.ALL:
            self.targets *= 4
        if self.bit == self.HW:
            self.weight = 4
        else:
            self.weight = 1
        self.dataLength *= self.targets
        self.signalsPerKey = self.candidates * self.targets
        self.candidateStringLength = int(math.ceil(math.log(self.candidates - 1) / math.log(10)))
        if self.targetDes == 1:
            self.testInput = Des.des(self.desKey, self.testInput, self.encrypt)
            self.testOutput = Des.des(self.desKey, self.testOutput, not self.encrypt)

    def _getKeyValues(self):
        roundKeyString = self.roundKeyVar.get().strip()
        if len(roundKeyString) > 0:
            self.roundKeyString = roundKeyString
            try:
                self.roundKey = int(roundKeyString.replace(' ', ''), 16)
                self.set(self.ROUND_KEY, self.roundKey)
            except ValueError:
                pass
        desKeyString = self.desKeyVar.get().strip()
        if len(desKeyString) > 0:
            try:
                hex_str = desKeyString.replace(' ', '')
                ba = bytes.fromhex(hex_str)
                self.desKey = self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8)
                self.set(self.DES_1_KEY, self.desKey)
            except ValueError:
                pass
        desKeyString = self.des2KeyVar.get().strip()
        if len(desKeyString) > 0:
            try:
                hex_str = desKeyString.replace(' ', '')
                ba = bytes.fromhex(hex_str)
                self.des2Key = self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8)
                self.set(self.DES_2_KEY, self.des2Key)
            except ValueError:
                pass
        desKeyString = self.des3KeyVar.get().strip()
        if len(desKeyString) > 0:
            try:
                hex_str = desKeyString.replace(' ', '')
                ba = bytes.fromhex(hex_str)
                self.des3Key = self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8)
                self.set(self.DES_3_KEY, self.des3Key)
            except ValueError:
                pass

    def set(self, key, value):
        if key == self.WHICH_DES:
            self.targetDes = value
        elif key == self.KEY_SIZE:
            self.keySize = value
        elif key == self.BIT:
            self.bit = value
        elif key == self.ROUND:
            self.round = value
        elif key == self.TDES:
            self.tdes = value
        elif key == self.ENCRYPT:
            self.encryptOption = value
        elif key == self.MODEL:
            self.model = value
        elif key == self.TARGET:
            self.target = value
        elif key == self.ROUND_KEY:
            self.roundKey = value
        elif key == self.DES_1_KEY:
            self.desKey = value
        elif key == self.DES_2_KEY:
            self.des2Key = value
        elif key == self.DES_3_KEY:
            self.des3Key = value

    def get(self, key):
        if key == self.WHICH_DES:
            return self.targetDes
        elif key == self.KEY_SIZE:
            return self.keySize
        elif key == self.BIT:
            return self.bit
        elif key == self.ROUND:
            return self.round
        elif key == self.TDES:
            return self.tdes
        elif key == self.ENCRYPT:
            return self.encryptOption
        elif key == self.MODEL:
            return self.model
        elif key == self.TARGET:
            return self.target
        elif key == self.ROUND_KEY:
            return self.roundKey
        elif key == self.DES_1_KEY:
            return self.desKey
        elif key == self.DES_2_KEY:
            return self.des2Key
        elif key == self.DES_3_KEY:
            return self.des3Key
        return None

    def select(self, t):
        attackObj = DesSboxOutDefault()
        attackObj.module = self
        attackObj.round = self.round
        attackObj.roundKey = self.roundKey
        ret = attackObj.GetMidDataHW(t.data)
        self.round = attackObj.round
        self.roundKey = attackObj.roundKey
        return ret

    def ok_clicked(self):
        if self.checkDialogValues():
            self.getDialogValues()
            if self.window:
                self.window.destroy()

    def cancel_clicked(self):
        if self.window:
            self.window.destroy()

    @staticmethod
    def invPermuteText(in_val, mat, outsize, defaultValue):
        result = [defaultValue] * outsize
        i = 0
        temp = in_val
        while i < len(mat):
            result[mat[len(mat) - 1 - i] - 1] = '1' if (temp & 1) == 1 else '0'
            temp >>= 1
            i += 1
        return ''.join(result)

    @staticmethod
    def invPermuteTextFromString(in_str, mat, outsize, defaultValue):
        result = [defaultValue] * outsize
        i = 0
        while i < len(mat):
            result[mat[len(mat) - 1 - i] - 1] = in_str[len(in_str) - 1 - i]
            i += 1
        return ''.join(result)

    def deRotate(self, k, r):
        invert = (self.targetDes == 1) ^ (not self.encrypt)
        if r == 1:
            return Des.rotate(k, 0 if invert else 1)
        elif r == 2:
            return Des.rotate(k, -1 if invert else 2)
        elif r == 15:
            return Des.rotate(k, 2 if invert else -1)
        else:
            return Des.rotate(k, 1 if invert else 0)

    def makeCandidateRanking(self, bestVector):
        pass

    def report(self, key, best, fragmentOffset, fragmentEnd, noKeyRetrieval=False):
        if not noKeyRetrieval:
            self.reportKeyRetrieval(key, best)

    def reportKeyRetrieval(self, key, best):
        if key == 0:
            self.newRoundKey = 0
        self.newRoundKey = (self.newRoundKey << 6) + int(best[0][0])

        if key < self.keys - 1:
            return

        s = self.formatNumberString(format(self.newRoundKey, 'x').upper(), 2)
        if self.round == 0 or self.round == 3:
            self.set(self.ROUND_KEY, self.newRoundKey)
            print(f"轮密钥: {s}")
        else:
            r1 = self.deRotate(self.invPermuteText(self.roundKey, Des.PC2, 56, 'x'),
                               1 if self.selectedRound == 1 else 16)
            r1 = self.invPermuteTextFromString(r1, Des.PC1, 64, '0')
            r2 = self.deRotate(self.invPermuteText(self.newRoundKey, Des.PC2, 56, 'x'),
                               2 if self.selectedRound == 1 else 15)
            r2 = self.invPermuteTextFromString(r2, Des.PC1, 64, '0')
            print(f"DES 第 {1 if self.selectedRound == 1 else 16}轮子密钥: {r1}")
            print(f"DES 第 {2 if self.selectedRound == 1 else 15}轮子密钥: {r2}")

            sb = list(r2)
            self.mismatches = 0
            for i in range(len(r1)):
                if r1[i] != 'x' and r2[i] != 'x' and r1[i] != r2[i]:
                    print(f"第 {i} 比特不匹配")
                    self.mismatches += 1
                if r1[i] != 'x':
                    sb[i] = r1[i]

            s = ''.join(sb)
            bi = int(s, 2)
            s = format(bi, 'x').upper()
            while len(s) < 16:
                s = '0' + s
            s = self.formatNumberString(s, 2)
            ba = bi.to_bytes((bi.bit_length() + 7) // 8, 'big')
            if self.targetDes == 0:
                self.set(self.DES_1_KEY, self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8))
                if self.keySize == 0:
                    self.set(self.DES_3_KEY, self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8))
            elif self.targetDes == 1:
                self.set(self.DES_2_KEY, self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8))
            else:
                self.set(self.DES_3_KEY, self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8))
                if self.keySize == 0:
                    self.set(self.DES_1_KEY, self.toLong(ba) if len(ba) <= 8 else self.toLong(ba, len(ba) - 8, 8))

    def guessNextRoundKey(self, best):
        found = False
        k = -1
        rk = 0
        p = 0
        if self.round == 0 or self.round == 3:
            for p in range(256):
                if found:
                    break
                rk = self.makeKey(best, p, 0xFF, 2)
                if self.round == 0:
                    rk1 = Des.invRotate(Des.invPermute(rk, Des.PC2, 56), 0)
                    for i in range(256):
                        if found:
                            break
                        k = (rk1 | Des.counterToMissingBitsInFirstRoundKey(i))
                        if self.encrypt ^ (self.targetDes == 1):
                            found = Des.fastDesEncrypt(k, self.testInput) == self.testOutput
                        else:
                            found = Des.fastDesDecrypt(k, self.testInput) == self.testOutput
                else:
                    rk1 = Des.invRotate(Des.invPermute(rk, Des.PC2, 56), 15)
                    for i in range(256):
                        if found:
                            break
                        k = (rk1 | Des.counterToMissingBitsInLastRoundKey(i))
                        if self.encrypt ^ (self.targetDes == 1):
                            found = Des.fastDesEncrypt(k, self.testInput) == self.testOutput
                        else:
                            found = Des.fastDesDecrypt(k, self.testInput) == self.testOutput
        else:
            r0 = 0 if self.round == 1 else 15
            r1 = 1 if self.round == 1 else 14
            keyMask = (~(Des.invRotate(Des.invPermute(0xFFFFFFFFFFFF, Des.PC2, 56), r0) ^
                         Des.invRotate(Des.invPermute(0xFFFFFFFFFFFF, Des.PC2, 56), r1))) & 0xFFFFFFFFFFFFFF
            rk0 = Des.invRotate(Des.invPermute(self.roundKey, Des.PC2, 56), r0)
            keyErrors = (rk0 ^ Des.invRotate(Des.invPermute(self.newRoundKey, Des.PC2, 56), r1)) & keyMask
            mask = 0
            for j in range(8):
                mask <<= 1
                subKeyMask = Des.invRotate(Des.invPermute((0x3F << ((7 - j) * 6)), Des.PC2, 56), r1)
                if (keyErrors & subKeyMask) != 0:
                    mask += 1
                keyErrors &= (~subKeyMask) & 0xFFFFFFFFFFFFFF
            boxes = self.hw(mask)
            if boxes > 0:
                print(f"{self.mismatches} 第{boxes}个S盒对应的子密钥不匹配")
            step = 1
            tests = 0
            while True:
                tests = int(math.pow(step, boxes))
                if tests < self.MAX_TESTS and step < self.max and step < 64:
                    step += 1
                else:
                    break
            firstMatch = -1
            for p in range(tests):
                if found:
                    break
                rk = self.makeKey(best, p, mask, step)
                rk1 = Des.invRotate(Des.invPermute(rk, Des.PC2, 56), r1)
                if ((rk0 ^ rk1) & keyMask) == 0:
                    k = rk0 | rk1
                    if firstMatch < 0:
                        firstMatch = k
                    testResult = Des.fastDesEncrypt(k, self.testInput) if (
                                self.encrypt ^ (self.targetDes == 1)) else Des.fastDesDecrypt(k, self.testInput)
                    found = (testResult == self.testOutput) or (not self.inputAndOutput)
            if not found:
                k = firstMatch

        ba = bytearray(9)
        temp_ba = self.toByteArray(Des.invPermute(k, Des.PC1, 64))
        for i in range(8):
            ba[i + 1] = temp_ba[i]
        s = int.from_bytes(ba, 'big').to_bytes(9, 'big').hex().upper()
        s = s.lstrip('0')
        while len(s) < 16:
            s = '0' + s
        s = self.formatNumberString(s, 2)
        if found:
            if p != 1:
                roundKey = self.formatNumberString(format(rk, 'x').upper(), 2)
                if self.round == 0 or self.round == 3:
                    self.set(self.ROUND_KEY, rk)
                print(f"攻击成功的轮子密钥为: {roundKey}")
            if p != 0:
                print(f"找到匹配和验证的DES密钥: {s}")
        elif self.round == 0 or self.round == 3 or k < 0:
            print("没有匹配的DES密钥")
        else:
            print(f"找到匹配的 DES密钥: {s}")

    def makeKey(self, best, index, mask, step):
        key = 0
        for i in range(self.keys):
            k_idx = self.keys - 1 - i
            j = 0
            if ((mask >> k_idx) & 1) == 1:
                j = index % step
                index //= step
            key = (key << self.keyBits) + int(best[i][j][0])
        return key

    def generate(self, index):
        if self.targets > 1:
            title = f"Candidate {(index // self.targets) % self.candidates} of S-box {(index // (self.candidates * self.targets)) + 1} for target {index % self.targets}"
        else:
            title = f"Candidate {index % self.candidates} of S-box {(index // self.candidates) + 1}"
        trace = Trace()
        trace.setTitle(title)
        return trace

    def keyPressed(self, event):
        pass

    def keyTyped(self, event):
        pass

    @staticmethod
    def toLong(ba, offset=0, length=8):
        if ba is None:
            return 0
        result = 0
        for i in range(length):
            result = (result << 8)
            if offset + i < len(ba):
                result += ba[offset + i] & 0xFF
        return result

    @staticmethod
    def toByteArray(x):
        result = bytearray(8)
        for i in range(7, -1, -1):
            result[i] = x & 0xFF
            x >>= 8
        return bytes(result)

    @staticmethod
    def formatNumberString(s, groupSize):
        result = []
        for i in range(0, len(s), groupSize):
            result.append(s[i:i + groupSize])
        return ' '.join(result)

    @staticmethod
    def hw(x):
        return bin(x).count('1')

    @staticmethod
    def isInteger(s):
        pattern = re.compile(r'([A-F]|[a-f]|[0-9]|-|_){1,12}')
        return bool(pattern.match(s))

    def checkDialogValues(self):
        message = []
        if self.datalen != 16:
            message.append("明文&密文数据区不正确，请确认曲线为DES曲线！")
            if len(message) == 0:
                return True
            messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
            return False
        if self.max <= 0 or self.max > 64:
            message.append("候选密钥个数为[1,64]")
        if self.round == 1:
            if not self.isInteger(self.roundKeyString):
                message.append("第一轮的轮子密钥应为48比特！")
                if len(message) == 0:
                    return True
                messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
                return False
            if self.roundKeyTextField.get().strip() == "":
                message.append("请先输入第一轮的轮子密钥！")
        if len(message) == 0:
            return True
        messagebox.showerror("模块设置错误", "下面参数设置错误\n" + '\n'.join(message))
        return False


class DesSboxOutDefault:
    def __init__(self):
        self.module = None
        self.round = 0
        self.roundKey = 0

    def GetMidDataHW(self, data):
        return [0.0] * 512


class Trace:
    def __init__(self):
        self.data = None
        self.title = ""

    def setTitle(self, title):
        self.title = title


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = DesSboxOut(root)
    app.initModule()
    app.initDialog()
    root.mainloop()