import re
import math
from Des import Des


class DesSboxIn:
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

    k = [0, 4467856773185, 8935713546370, 13403570319555, 17871427092740, 22339283865925, 26807140639110,
         31274997412295, 35742854185480, 40210710958665, 44678567731850, 49146424505035, 53614281278220, 58082138051405,
         62549994824590, 67017851597775, 71485708370960, 75953565144145, 80421421917330, 84889278690515, 89357135463700,
         93824992236885, 98292849010070, 102760705783255, 107228562556440, 111696419329625, 116164276102810,
         120632132875995, 125099989649180, 129567846422365, 134035703195550, 138503559968735, 142971416741920,
         147439273515105, 151907130288290, 156374987061475, 160842843834660, 165310700607845, 169778557381030,
         174246414154215, 178714270927400, 183182127700585, 187649984473770, 192117841246955, 196585698020140,
         201053554793325, 205521411566510, 209989268339695, 214457125112880, 218924981886065, 223392838659250,
         227860695432435, 232328552205620, 236796408978805, 241264265751990, 245732122525175, 250199979298360,
         254667836071545, 259135692844730, 263603549617915, 268071406391100, 272539263164285, 277007119937470,
         281474976710655]

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
        self.precision = 1.0

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
        self.helpFile = "doc/manual/modulesDesAdvancedAnalysis.html"
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
        import tkinter as tk
        from tkinter import ttk

        if self.window is None:
            self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
            self.window.title("DES分析设置")
            self.window.geometry("700x450")

        self.centerPanel = ttk.Frame(self.window)
        self.centerPanel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.centerPanel.configure(borderwidth=2, relief="groove")

        self.northPanel = ttk.Frame(self.centerPanel)
        self.northPanel.pack(fill=tk.X, pady=5)

        self.desPanel = ttk.LabelFrame(self.northPanel, text="DES设置")
        self.desPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.encryptPanel = ttk.Frame(self.desPanel)
        self.encryptPanel.pack(side=tk.RIGHT)
        self.encryptButton = ttk.Radiobutton(self.encryptPanel, text="加密", variable=self.encryptVar,
                                             value=self.DES_ENCRYPT, command=self.actionPerformed)
        self.encryptButton.pack(side=tk.LEFT)
        self.decryptButton = ttk.Radiobutton(self.encryptPanel, text="解密", variable=self.encryptVar,
                                             value=self.DES_DECRYPT, command=self.actionPerformed)
        self.decryptButton.pack(side=tk.LEFT)

        self.tdesCheckBox = ttk.Checkbutton(self.desPanel, text="3DES", variable=self.tdesVar,
                                            command=self.actionPerformed)
        self.tdesCheckBox.pack(side=tk.LEFT, padx=10)

        self.trackPanel = ttk.LabelFrame(self.northPanel, text="Track bit")
        self.trackPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.bit1Button = ttk.Radiobutton(self.trackPanel, text="1", variable=self.bitVar, value=1,
                                          command=self.actionPerformed)
        self.bit1Button.pack(side=tk.LEFT, padx=2)
        self.bit2Button = ttk.Radiobutton(self.trackPanel, text="2", variable=self.bitVar, value=2,
                                          command=self.actionPerformed)
        self.bit2Button.pack(side=tk.LEFT, padx=2)
        self.bit3Button = ttk.Radiobutton(self.trackPanel, text="3", variable=self.bitVar, value=3,
                                          command=self.actionPerformed)
        self.bit3Button.pack(side=tk.LEFT, padx=2)
        self.bit4Button = ttk.Radiobutton(self.trackPanel, text="4", variable=self.bitVar, value=4,
                                          command=self.actionPerformed)
        self.bit4Button.pack(side=tk.LEFT, padx=2)
        self.allButton = ttk.Radiobutton(self.trackPanel, text="All", variable=self.bitVar, value=self.ALL,
                                         command=self.actionPerformed)
        self.allButton.pack(side=tk.LEFT, padx=2)
        self.hwButton = ttk.Radiobutton(self.trackPanel, text="HW", variable=self.bitVar, value=self.HW,
                                        command=self.actionPerformed)
        self.hwButton.pack(side=tk.LEFT, padx=2)

        self.roundPanel = ttk.LabelFrame(self.northPanel, text="轮数")
        self.roundPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.round1Button = ttk.Radiobutton(self.roundPanel, text="1", variable=self.roundVar, value=1,
                                            command=self.actionPerformed)
        self.round1Button.pack(side=tk.LEFT, padx=5)
        self.round2Button = ttk.Radiobutton(self.roundPanel, text="2", variable=self.roundVar, value=2,
                                            command=self.actionPerformed)
        self.round2Button.pack(side=tk.LEFT, padx=5)

        self.keyLengthPanel = ttk.LabelFrame(self.northPanel, text="密钥长度")
        self.keyLengthPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.keySizePanel = ttk.Frame(self.keyLengthPanel)
        self.keySizePanel.pack(side=tk.RIGHT)
        self.twoKeysButton = ttk.Radiobutton(self.keySizePanel, text="112", variable=self.keySizeVar, value=0,
                                             command=self.actionPerformed)
        self.twoKeysButton.pack(side=tk.LEFT)
        self.threeKeysButton = ttk.Radiobutton(self.keySizePanel, text="168", variable=self.keySizeVar, value=1,
                                               command=self.actionPerformed)
        self.threeKeysButton.pack(side=tk.LEFT)

        self.southPanel = ttk.Frame(self.centerPanel)
        self.southPanel.pack(fill=tk.X, pady=5)

        self.roundKeyPanel = ttk.LabelFrame(self.southPanel, text="第一轮轮子密钥")
        self.roundKeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.roundKeyTextField = ttk.Entry(self.roundKeyPanel, textvariable=self.roundKeyVar, width=20)
        self.roundKeyTextField.pack(padx=5, pady=5)
        self.roundKeyTextField.bind('<KeyRelease>', self.keyReleased)

        self.targetPanel = ttk.LabelFrame(self.southPanel, text="Target")
        self.targetPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.sboxButton = ttk.Radiobutton(self.targetPanel, text="S盒", variable=self.targetVar, value=self.SBOX_OUTPUT,
                                          command=self.actionPerformed)
        self.sboxButton.pack(side=tk.LEFT, padx=5)
        self.xorButton = ttk.Radiobutton(self.targetPanel, text="异或", variable=self.targetVar, value=self.XOR_OUTPUT,
                                         command=self.actionPerformed)
        self.xorButton.pack(side=tk.LEFT, padx=5)

        self.modelPanel = ttk.LabelFrame(self.southPanel, text="Model")
        self.modelPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.absButton = ttk.Radiobutton(self.modelPanel, text="Abs", variable=self.modelVar, value=self.ABSOLUTE,
                                         command=self.actionPerformed)
        self.absButton.pack(side=tk.LEFT, padx=5)
        self.sButton = ttk.Radiobutton(self.modelPanel, text="S盒", variable=self.modelVar, value=self.SBOX_INPUT,
                                       command=self.actionPerformed)
        self.sButton.pack(side=tk.LEFT, padx=5)
        self.roundButton = ttk.Radiobutton(self.modelPanel, text="轮", variable=self.modelVar, value=self.ROUND_INPUT,
                                           command=self.actionPerformed)
        self.roundButton.pack(side=tk.LEFT, padx=5)

        self.desSelPanel = ttk.LabelFrame(self.southPanel, text="Target DES")
        self.desSelPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.whichDesPanel = ttk.Frame(self.desSelPanel)
        self.whichDesPanel.pack(side=tk.RIGHT)
        self.firstDesButton = ttk.Radiobutton(self.whichDesPanel, text="1", variable=self.whichDesVar, value=0,
                                              command=self.actionPerformed)
        self.firstDesButton.pack(side=tk.LEFT)
        self.secondDesButton = ttk.Radiobutton(self.whichDesPanel, text="2", variable=self.whichDesVar, value=1,
                                               command=self.actionPerformed)
        self.secondDesButton.pack(side=tk.LEFT)
        self.thirdDesButton = ttk.Radiobutton(self.whichDesPanel, text="3", variable=self.whichDesVar, value=2,
                                              command=self.actionPerformed)
        self.thirdDesButton.pack(side=tk.LEFT)

        self.keysPanel = ttk.Frame(self.centerPanel)
        self.keysPanel.pack(fill=tk.X, pady=5)

        self.des1KeyPanel = ttk.LabelFrame(self.keysPanel, text="First Des key")
        self.des1KeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.desKeyTextField = ttk.Entry(self.des1KeyPanel, textvariable=self.desKeyVar, width=20)
        self.desKeyTextField.pack(padx=5, pady=5)
        self.desKeyTextField.bind('<KeyRelease>', self.keyReleased)

        self.des2KeyPanel = ttk.LabelFrame(self.keysPanel, text="Second Des key")
        self.des2KeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.des2KeyTextField = ttk.Entry(self.des2KeyPanel, textvariable=self.des2KeyVar, width=20)
        self.des2KeyTextField.pack(padx=5, pady=5)
        self.des2KeyTextField.bind('<KeyRelease>', self.keyReleased)

        self.des3KeyPanel = ttk.LabelFrame(self.keysPanel, text="Third Des key")
        self.des3KeyPanel.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.des3KeyTextField = ttk.Entry(self.des3KeyPanel, textvariable=self.des3KeyVar, width=20)
        self.des3KeyTextField.pack(padx=5, pady=5)
        self.des3KeyTextField.bind('<KeyRelease>', self.keyReleased)

        buttonFrame = ttk.Frame(self.centerPanel)
        buttonFrame.pack(pady=10)

        okButton = ttk.Button(buttonFrame, text="确定", command=self.ok_clicked)
        okButton.pack(side=tk.LEFT, padx=5)
        cancelButton = ttk.Button(buttonFrame, text="取消", command=self.cancel_clicked)
        cancelButton.pack(side=tk.LEFT, padx=5)

        self.updateEnabledPanels()

        return self.centerPanel

    def updateEnabledPanels(self):
        if self.roundVar.get() == 1:
            self.roundKeyTextField.config(state='disabled')
        else:
            self.roundKeyTextField.config(state='normal')

    def setDialogValues(self, var1=None, var2=0, var3=0, var4=0, var5=0, var6=0):
        if var1 is not None:
            if var1.data is not None:
                self.datalen = len(var1.data)
                self.inputAndOutput = len(var1.data) >= 16
                self.testInput = self.toLong(var1.data, 0, 8)
                self.testOutput = self.toLong(var1.data, len(var1.data) - 8, 8)
                self.testInput = Des.ip(self.testInput)
                self.testOutput = Des.ip(self.testOutput)
        else:
            self._setDialogValuesInternal()

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
        self.roundKeyString = self.roundKeyVar.get().strip()
        if len(self.roundKeyString) > 0:
            try:
                self.roundKey = int(self.roundKeyString.replace(' ', ''), 16)
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

    def actionPerformed(self, var1=None):
        self.updateEnabledPanels()

    def keyReleased(self, event):
        self.keySize = self.keySizeVar.get()
        tdes = self.tdesVar.get()
        if tdes and self.keySize == 0:
            if event.widget == self.des3KeyTextField:
                self.desKeyVar.set(self.des3KeyVar.get())
            elif event.widget == self.desKeyTextField:
                self.des3KeyVar.set(self.desKeyVar.get())
        self.actionPerformed()

    def select(self, var1):
        attackObj = DesSboxInDefault()
        attackObj.module = self
        attackObj.round = self.round
        attackObj.roundKey = self.roundKey
        var3 = attackObj.GetMidDataHW(var1.data)
        self.round = attackObj.round
        self.roundKey = attackObj.roundKey
        return var3

    def ok_clicked(self):
        if self.checkDialogValues():
            self.getDialogValues()
            if self.window:
                self.window.destroy()

    def cancel_clicked(self):
        if self.window:
            self.window.destroy()

    @staticmethod
    def invPermuteText(var0, var2, var3, var4):
        var5 = [var4] * var3
        var7 = 0
        temp = var0
        while var7 < len(var2):
            var5[var2[len(var2) - 1 - var7] - 1] = '1' if (temp & 1) == 1 else '0'
            temp >>= 1
            var7 += 1
        return ''.join(var5)

    @staticmethod
    def invPermuteTextFromString(var0, var1, var2, var3):
        var4 = [var3] * var2
        var6 = 0
        while var6 < len(var1):
            var4[var1[len(var1) - 1 - var6] - 1] = var0[len(var0) - 1 - var6]
            var6 += 1
        return ''.join(var4)

    def deRotate(self, var1, var2):
        var4 = (self.targetDes == 1) ^ (not self.encrypt)
        if var2 == 1:
            return Des.rotate(var1, 0 if var4 else 1)
        elif var2 == 2:
            return Des.rotate(var1, -1 if var4 else 2)
        elif var2 == 15:
            return Des.rotate(var1, 2 if var4 else -1)
        else:
            return Des.rotate(var1, 1 if var4 else 0)

    def makeCandidateRanking(self):
        var1 = [None] * self.keys
        for var2 in range(self.keys):
            for var3 in range(0, self.numberOfSamples, self.fragmentLength):
                var4 = var3 + self.fragmentLength if self.fragmentLength > 0 else self.numberOfSamples
                if var4 > self.numberOfSamples:
                    var4 = self.numberOfSamples
                var1[var2] = self.makeCandidateRankingInternal(var2, var3, var4)
                if self.fragmentLength == 0:
                    break
        if self.inputAndOutput:
            self.guessNextRoundKey(var1)

    def makeCandidateRankingInternal(self, var1, var2, var3):
        return None

    def report(self, var1, var2, var3, var4, var5=False):
        if not var5:
            self.reportKeyRetrieval(var1, var2)

    def reportKeyRetrieval(self, var1, var2):
        if var1 == 0:
            self.newRoundKey = 0
        var3 = var2[0][2] * self.precision
        var3 = math.floor(var3 + 0.5) / self.precision
        if var3 < 0:
            self.newRoundKey = (self.newRoundKey << 6) + int(var2[1][0])
        else:
            self.newRoundKey = (self.newRoundKey << 6) + int(var2[0][0])

        if var1 >= self.keys - 1:
            var5 = self.formatNumberString(format(self.newRoundKey, 'x').upper(), 2)
            if self.round != 0 and self.round != 3:
                var6 = self.deRotate(self.invPermuteText(self.roundKey, Des.PC2, 56, 'x'),
                                     1 if self.selectedRound == 1 else 16)
                var6 = self.invPermuteTextFromString(var6, Des.PC1, 64, '0')
                var7 = self.deRotate(self.invPermuteText(self.newRoundKey, Des.PC2, 56, 'x'),
                                     2 if self.selectedRound == 1 else 15)
                var7 = self.invPermuteTextFromString(var7, Des.PC1, 64, '0')
                print(f"DES 第 {1 if self.selectedRound == 1 else 16} 轮子密钥: {var6}")
                print(f"DES 第 {2 if self.selectedRound == 1 else 15} 轮子密钥: {var7}")
                var8 = list(var7)
                self.mismatches = 0
                for var9 in range(len(var6)):
                    if var6[var9] != 'x' and var7[var9] != 'x' and var6[var9] != var7[var9]:
                        print(f"第 {var9} 比特不匹配")
                        self.mismatches += 1
                    if var6[var9] != 'x':
                        var8[var9] = var6[var9]
                var5 = ''.join(var8)
                var18 = int(var5, 2)
                var5 = format(var18, 'x').upper()
                while len(var5) < 16:
                    var5 = '0' + var5
                var5 = self.formatNumberString(var5, 2)
                var10 = var18.to_bytes((var18.bit_length() + 7) // 8, 'big')
                if self.targetDes == 0:
                    self.set(self.DES_1_KEY,
                             self.toLong(var10) if len(var10) <= 8 else self.toLong(var10, len(var10) - 8, 8))
                    if self.keySize == 0:
                        self.set(self.DES_3_KEY,
                                 self.toLong(var10) if len(var10) <= 8 else self.toLong(var10, len(var10) - 8, 8))
                elif self.targetDes == 1:
                    self.set(self.DES_2_KEY,
                             self.toLong(var10) if len(var10) <= 8 else self.toLong(var10, len(var10) - 8, 8))
                else:
                    self.set(self.DES_3_KEY,
                             self.toLong(var10) if len(var10) <= 8 else self.toLong(var10, len(var10) - 8, 8))
                    if self.keySize == 0:
                        self.set(self.DES_1_KEY,
                                 self.toLong(var10) if len(var10) <= 8 else self.toLong(var10, len(var10) - 8, 8))
            else:
                self.set(self.ROUND_KEY, self.newRoundKey)
                print(f"轮密钥: {var5}")

    def guessNextRoundKey(self, var1):
        var2 = False
        var3 = -1
        var5 = 0
        var7 = 0

        if self.round != 0 and self.round != 3:
            var28 = 0 if self.round == 1 else 15
            var9 = 1 if self.round == 1 else 14
            var33 = (~(Des.invRotate(Des.invPermute(281474976710655, Des.PC2, 56), var28) ^
                       Des.invRotate(Des.invPermute(281474976710655, Des.PC2, 56), var9))) & 72057594037927935
            var12 = Des.invRotate(Des.invPermute(self.roundKey, Des.PC2, 56), var28)
            var14 = (var12 ^ Des.invRotate(Des.invPermute(self.newRoundKey, Des.PC2, 56), var9)) & var33
            var16 = 0
            for var17 in range(8):
                var16 <<= 1
                var18 = Des.invRotate(Des.invPermute(63 << ((7 - var17) * 6), Des.PC2, 56), var9)
                if (var14 & var18) != 0:
                    var16 += 1
                var14 &= ~var18 & 72057594037927935
            var35 = self.hw(var16)
            if var35 > 0:
                print(f"{self.mismatches} 第{var35}个S盒子对应的子密钥不匹配")
            var36 = 1
            while True:
                var19 = int(math.pow(var36, var35))
                if var19 < 1000000 and var36 < self.max and var36 < 64:
                    var36 += 1
                else:
                    break
            var20 = -1
            for var7 in range(var19):
                if var2:
                    break
                var5 = self.makeKey(var1, var7, var16, var36)
                var22 = Des.invRotate(Des.invPermute(var5, Des.PC2, 56), var9)
                if ((var12 ^ var22) & var33) == 0:
                    var3 = var12 | var22
                    if var20 < 0:
                        var20 = var3
                    var24 = Des.fastDesEncrypt(var3, self.testInput) if (
                                self.encrypt ^ (self.targetDes == 1)) else Des.fastDesDecrypt(var3, self.testInput)
                    var2 = (var24 == self.testOutput) or (not self.inputAndOutput)
            if not var2:
                var3 = var20
        else:
            for var7 in range(256):
                if var2:
                    break
                var5 = self.makeKey(var1, var7, 255, 2)
                if self.round == 0:
                    var27 = Des.invRotate(Des.invPermute(var5, Des.PC2, 56), 0)
                    for var32 in range(256):
                        if var2:
                            break
                        var3 = var27 | Des.counterToMissingBitsInFirstRoundKey(var32)
                        if self.encrypt ^ (self.targetDes == 1):
                            var2 = Des.fastDesEncrypt(var3, self.testInput) == self.testOutput
                        else:
                            var2 = Des.fastDesDecrypt(var3, self.testInput) == self.testOutput
                else:
                    var8 = Des.invRotate(Des.invPermute(var5, Des.PC2, 56), 15)
                    for var10 in range(256):
                        if var2:
                            break
                        var3 = var8 | Des.counterToMissingBitsInLastRoundKey(var10)
                        if self.encrypt ^ (self.targetDes == 1):
                            var2 = Des.fastDesEncrypt(var3, self.testInput) == self.testOutput
                        else:
                            var2 = Des.fastDesDecrypt(var3, self.testInput) == self.testOutput

        var29 = bytearray(9)
        temp_ba = self.toByteArray(Des.invPermute(var3, Des.PC1, 64))
        for i in range(8):
            var29[i + 1] = temp_ba[i]
        var30 = int.from_bytes(var29, 'big').to_bytes(9, 'big').hex().upper()
        var30 = var30.lstrip('0')
        while len(var30) < 16:
            var30 = '0' + var30
        var30 = self.formatNumberString(var30, 2)

        if var2:
            if var7 != 1:
                var34 = self.formatNumberString(format(var5, 'x').upper(), 2)
                if self.round == 0 or self.round == 3:
                    self.set(self.ROUND_KEY, var5)
                print(f"攻击成功的轮子密钥为: {var34}")
            if var7 != 0:
                print(f"找到匹配和验证的DES密钥: {var30}")
        elif self.round != 0 and self.round != 3 and var3 >= 0:
            print(f"找到匹配的 DES密钥: {var30}")
        else:
            print("没有匹配的DES密钥")

    def makeKey(self, var1, var2, var3, var4):
        var5 = 0
        var7 = 0
        for var8 in range(self.keys - 1, -1, -1):
            var9 = 0
            if ((var3 >> var8) & 1) == 1:
                var9 = var2 % var4
                var2 //= var4
            var10 = var1[var7][var9][2] * self.precision
            var10 = math.floor(var10 + 0.5) / self.precision
            if var10 < 0:
                var5 = (var5 << self.keyBits) + int(var1[var7][(var9 + 1) % var4][0])
            else:
                var5 = (var5 << self.keyBits) + int(var1[var7][var9][0])
            var7 += 1
        return var5

    def generate(self, var1):
        if self.targets > 1:
            title = f"Candidate {(var1 // self.targets) % self.candidates} of S-box {(var1 // (self.candidates * self.targets)) + 1} for target {var1 % self.targets}"
        else:
            title = f"Candidate {var1 % self.candidates} of S-box {(var1 // self.candidates) + 1}"
        trace = Trace()
        trace.setTitle(title)
        return trace

    def keyPressed(self, var1):
        pass

    def keyTyped(self, var1):
        pass

    @staticmethod
    def toLong(ba, offset=0, length=8):
        if ba is None:
            return 0
        result = 0
        for i in range(length):
            result <<= 8
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
            print("模块设置错误:", "下面参数设置错误：", '\n'.join(message))
            return False
        if self.max < 2 or self.max > 64:
            message.append("候选密钥个数为[2,64]")
        if self.round == 1:
            if not self.isInteger(self.roundKeyString):
                message.append("第一轮的轮子密钥应为48比特！")
                if len(message) == 0:
                    return True
                print("模块设置错误:", "下面参数设置错误：", '\n'.join(message))
                return False
            if self.roundKeyTextField.get().strip() == "":
                message.append("请先输入第一轮的轮子密钥！")
        if len(message) == 0:
            return True
        print("模块设置错误:", "下面参数设置错误：", '\n'.join(message))
        return False


class DesSboxInDefault:
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
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    app = DesSboxIn(root)
    app.initModule()
    app.initDialog()
    root.mainloop()