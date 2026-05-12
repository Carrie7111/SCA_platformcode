package sms4;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.util.Arrays;
import java.util.regex.Pattern;

import javax.swing.ButtonGroup;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;

import com.module.util.Message;

public class Sms4 {
    public static final long WORD_MASK = 0xFFFFFFFFL;

    public static final long CK[] = {
        0x00070e15L, 0x1c232a31L, 0x383f464dL, 0x545b6269L,
        0x70777e85L, 0x8c939aa1L, 0xa8afb6bdL, 0xc4cbd2d9L,
        0xe0e7eef5L, 0xfc030a11L, 0x181f262dL, 0x343b4249L,
        0x50575e65L, 0x6c737a81L, 0x888f969dL, 0xa4abb2b9L,
        0xc0c7ced5L, 0xdce3eaf1L, 0xf8ff060dL, 0x141b2229L,
        0x30373e45L, 0x4c535a61L, 0x686f767dL, 0x848b9299L,
        0xa0a7aeb5L, 0xbcc3cad1L, 0xd8dfe6edL, 0xf4fb0209L,
        0x10171e25L, 0x2c333a41L, 0x484f565dL, 0x646b7279L
    };

    public static final int Sbox[] = {
        0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,
        0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
        0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,
        0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,
        0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,
        0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,
        0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,
        0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,
        0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,
        0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,
        0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,
        0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,
        0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,
        0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,
        0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
        0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48
    };

    public static final long FK[] = {
        0xA3B1BAC6L, 0x56AA3350L, 0x677D9197L, 0xB27022DCL
    };

    private static final int[] INV_SBOX = buildInvSbox();
    private static final Pattern WORD_PATTERN = Pattern.compile("(?i)[0-9a-f]{8}");

    private Sms4() {
    }

    public static long u32(long v) {
        return v & WORD_MASK;
    }

    public static long t(long A) {
        long value = 0L;
        for (int i = 0; i < 4; i++) {
            int b = (int) ((A >>> (i * 8)) & 0xFFL);
            value |= ((long) Sbox[b]) << (i * 8);
        }
        return u32(value);
    }

    public static long ROL(long x, int y) {
        int n = y & 31;
        long v = u32(x);
        return n == 0 ? v : u32((v << n) | (v >>> (32 - n)));
    }

    public static long T1(long A) {
        long B = t(A);
        return u32(B ^ ROL(B, 2) ^ ROL(B, 10) ^ ROL(B, 18) ^ ROL(B, 24));
    }

    public static long T2(long A) {
        long B = t(A);
        return u32(B ^ ROL(B, 13) ^ ROL(B, 23));
    }

    public static void SMS4_KeyExpansion(long MK[], long rk[]) {
        checkWords(MK, 4, "MK");
        checkWords(rk, 32, "rk");

        long K[] = new long[4];
        for (int i = 0; i < 4; i++) {
            K[i] = u32(MK[i] ^ FK[i]);
        }
        for (int i = 0; i < 32; i++) {
            K[i % 4] = u32(K[i % 4] ^ T2(K[(i + 1) % 4] ^ K[(i + 2) % 4] ^ K[(i + 3) % 4] ^ CK[i]));
            rk[i] = K[i % 4];
        }
    }

    public static void SMS4_Encryption(long X[], long rk[], long Y[]) {
        checkWords(X, 4, "X");
        checkWords(rk, 32, "rk");
        checkWords(Y, 4, "Y");

        long tempX[] = X.clone();
        for (int i = 0; i < 4; i++) {
            tempX[i] = u32(tempX[i]);
        }
        for (int i = 0; i < 32; i++) {
            tempX[i % 4] = u32(tempX[i % 4] ^ T1(tempX[(i + 1) % 4] ^ tempX[(i + 2) % 4] ^ tempX[(i + 3) % 4] ^ rk[i]));
        }
        for (int i = 0; i < 4; i++) {
            Y[i] = tempX[3 - i];
        }
    }

    public static void SMS4_Decryption(long X[], long rk[], long Y[]) {
        checkWords(X, 4, "X");
        checkWords(rk, 32, "rk");
        checkWords(Y, 4, "Y");

        long tempX[] = X.clone();
        for (int i = 0; i < 4; i++) {
            tempX[i] = u32(tempX[i]);
        }
        for (int i = 0; i < 32; i++) {
            tempX[i % 4] = u32(tempX[i % 4] ^ T1(tempX[(i + 1) % 4] ^ tempX[(i + 2) % 4] ^ tempX[(i + 3) % 4] ^ rk[31 - i]));
        }
        for (int i = 0; i < 4; i++) {
            Y[i] = tempX[3 - i];
        }
    }

    public static JPanel initSM4Dialog(JTextField maxTextField, JTextField roundKeyTextField[],
                                       JPanel roundKeyPanel[], JPanel roundPanel,
                                       JPanel candidatePanel, JRadioButton roundButton[]) {
        ButtonGroup roundGroup = new ButtonGroup();
        JPanel centerPanel = new JPanel(new GridLayout(1, 2));
        JPanel southPanel = new JPanel(new GridLayout(1, 3));

        roundPanel.setBorder(new TitledBorder("轮数"));
        for (int i = 0; i < 4; i++) {
            roundButton[i].setToolTipText("利用S盒输入的中间值" + (i + 1));
            roundGroup.add(roundButton[i]);
            roundPanel.add(roundButton[i]);
        }
        if (roundButton.length > 0 && roundGroup.getSelection() == null) {
            roundButton[0].setSelected(true);
        }

        candidatePanel.setLayout(new BorderLayout());
        candidatePanel.setBorder(new TitledBorder("候选密钥的个数"));
        maxTextField.setToolTipText("列出的可能密钥的个数");
        candidatePanel.add(maxTextField, BorderLayout.CENTER);
        centerPanel.add(candidatePanel);
        centerPanel.add(roundPanel);

        for (int j = 0; j < 3; j++) {
            roundKeyPanel[j] = new JPanel(new BorderLayout());
            roundKeyPanel[j].setBorder(new TitledBorder("第" + (j + 1) + "轮攻击结果"));
            roundKeyPanel[j].add(roundKeyTextField[j], BorderLayout.CENTER);
            southPanel.add(roundKeyPanel[j]);
        }

        JPanel resultPanel = new JPanel(new GridLayout(2, 1));
        resultPanel.add(centerPanel);
        resultPanel.add(southPanel);
        resultPanel.setPreferredSize(new Dimension(340, 170));
        return resultPanel;
    }

    public static JPanel initSM4Dialog(JTextField roundKeyTextFieldone, JTextField roundKeyTextFieldtwo,
                                       JTextField roundKeyTextFieldthree, JPanel roundKeyPanelone,
                                       JPanel roundKeyPaneltwo, JPanel roundKeyPanelthree,
                                       JPanel roundPanel) {
        ButtonGroup roundGroup = new ButtonGroup();
        JPanel centerPanel = new JPanel(new GridLayout(2, 0));
        roundPanel.setBorder(new TitledBorder("轮数"));
        for (int i = 0; i < 4; i++) {
            String round = String.valueOf(i + 1);
            JRadioButton roundButton = new JRadioButton(round);
            roundButton.setToolTipText("利用S盒输入的中间值" + round);
            roundGroup.add(roundButton);
            roundPanel.add(roundButton);
            if (i == 0) {
                roundButton.setSelected(true);
            }
        }
        roundKeyPanelone.setLayout(new BorderLayout());
        roundKeyPanelone.setBorder(new TitledBorder("第一轮攻击结果"));
        roundKeyPanelone.add(roundKeyTextFieldone, BorderLayout.CENTER);
        roundKeyPaneltwo.setLayout(new BorderLayout());
        roundKeyPaneltwo.setBorder(new TitledBorder("第二轮攻击结果"));
        roundKeyPaneltwo.add(roundKeyTextFieldtwo, BorderLayout.CENTER);
        roundKeyPanelthree.setLayout(new BorderLayout());
        roundKeyPanelthree.setBorder(new TitledBorder("第三轮攻击结果"));
        roundKeyPanelthree.add(roundKeyTextFieldthree, BorderLayout.CENTER);
        centerPanel.add(roundPanel);
        centerPanel.add(roundKeyPanelone);
        centerPanel.add(roundKeyPaneltwo);
        centerPanel.add(roundKeyPanelthree);
        centerPanel.setPreferredSize(new Dimension(340, 170));
        return centerPanel;
    }

    public static boolean examineResult(long plaintext[], long ciphertext[], long key[]) {
        checkWords(plaintext, 4, "plaintext");
        checkWords(ciphertext, 4, "ciphertext");
        checkWords(key, 4, "key");

        long rk[] = new long[32];
        long result[] = new long[4];
        SMS4_KeyExpansion(key, rk);
        SMS4_Encryption(plaintext, rk, result);
        return Arrays.equals(result, ciphertext);
    }

    public static long readWord(byte[] data, int offset) {
        if (data == null || data.length < offset + 4) {
            throw new IllegalArgumentException("数据长度不足，无法读取32位字");
        }
        return ((data[offset] & 0xFFL) << 24)
             | ((data[offset + 1] & 0xFFL) << 16)
             | ((data[offset + 2] & 0xFFL) << 8)
             | (data[offset + 3] & 0xFFL);
    }

    public static boolean readPlainCipher(byte[] data, long[] plain, long[] cipher) {
        if (data == null || data.length < 32) {
            return false;
        }
        checkWords(plain, 4, "plain");
        checkWords(cipher, 4, "cipher");
        for (int i = 0; i < 4; i++) {
            plain[i] = readWord(data, i * 4);
            cipher[i] = readWord(data, 16 + i * 4);
        }
        return true;
    }

    public static long repeatByteWord(int value) {
        long b = value & 0xFFL;
        return (b << 24) | (b << 16) | (b << 8) | b;
    }

    public static long[] buildRepeatedByteWords() {
        long[] out = new long[256];
        for (int i = 0; i < out.length; i++) {
            out[i] = repeatByteWord(i);
        }
        return out;
    }

    public static RoundState buildRoundState(long[] block, int round, long rk1, long rk2, long rk3) {
        checkWords(block, 4, "block");
        if (round < 0 || round > 3) {
            throw new IllegalArgumentException("轮数范围应为1到4");
        }

        long[] x = block.clone();
        for (int i = 0; i < 4; i++) {
            x[i] = u32(x[i]);
        }
        if (round >= 1) {
            x[0] = u32(x[0] ^ T1(x[1] ^ x[2] ^ x[3] ^ rk1));
        }
        if (round >= 2) {
            x[1] = u32(x[1] ^ T1(x[2] ^ x[3] ^ x[0] ^ rk2));
        }
        if (round >= 3) {
            x[2] = u32(x[2] ^ T1(x[3] ^ x[0] ^ x[1] ^ rk3));
        }

        long sIn;
        switch (round) {
            case 0:
                sIn = x[1] ^ x[2] ^ x[3];
                break;
            case 1:
                sIn = x[2] ^ x[3] ^ x[0];
                break;
            case 2:
                sIn = x[3] ^ x[0] ^ x[1];
                break;
            case 3:
                sIn = x[0] ^ x[1] ^ x[2];
                break;
            default:
                throw new IllegalArgumentException("轮数范围应为1到4");
        }
        return new RoundState(x, u32(sIn));
    }

    public static long inverseT1(long c2) {
        long v = u32(c2);
        return u32(v ^ ROL(v, 2) ^ ROL(v, 4) ^ ROL(v, 8) ^ ROL(v, 12)
                ^ ROL(v, 14) ^ ROL(v, 16) ^ ROL(v, 18) ^ ROL(v, 22)
                ^ ROL(v, 24) ^ ROL(v, 30));
    }

    public static long inverseSboxWord(long value) {
        long out = 0L;
        for (int i = 0; i < 4; i++) {
            int b = (int) ((value >>> (i * 8)) & 0xFFL);
            out |= ((long) INV_SBOX[b]) << (i * 8);
        }
        return u32(out);
    }

    public static long recoverRoundKeyFromTOutput(long tOutput, long sIn) {
        return u32(inverseSboxWord(inverseT1(tOutput)) ^ sIn);
    }

    public static long[] recoverMasterKeyFromRoundKeys(long rk1, long rk2, long rk3, long rk4) {
        long[] K = new long[4];
        K[3] = u32(rk4 ^ T2(rk1 ^ rk2 ^ rk3 ^ CK[3]));
        K[2] = u32(rk3 ^ T2(rk1 ^ rk2 ^ K[3] ^ CK[2]));
        K[1] = u32(rk2 ^ T2(rk1 ^ K[2] ^ K[3] ^ CK[1]));
        K[0] = u32(rk1 ^ T2(K[1] ^ K[2] ^ K[3] ^ CK[0]));
        for (int i = 0; i < 4; i++) {
            K[i] = u32(K[i] ^ FK[i]);
        }
        return K;
    }

    public static boolean checkSM4DialogValues(int round, String roundKeyone, String roundKeytwo, String roundKeythree) {
        StringBuilder message = new StringBuilder();
        switch (round) {
            case 0:
                break;
            case 1:
                if (!isWord(roundKeyone)) {
                    message.append("第一轮的攻击结果应为8位16进制数！");
                }
                break;
            case 2:
                if (!isWord(roundKeyone) || !isWord(roundKeytwo)) {
                    message.append("前两轮的攻击结果应都为8位16进制数！");
                }
                break;
            case 3:
                if (!isWord(roundKeyone) || !isWord(roundKeytwo) || !isWord(roundKeythree)) {
                    message.append("前三轮的攻击结果应都为8位16进制数！");
                }
                break;
            default:
                message.append("轮数范围应为1到4！");
                break;
        }
        if (message.length() == 0) {
            return true;
        }
        Message.errors("模块设置错误", "下面参数设置错误", message.toString());
        return false;
    }

    public static boolean checkSM4DialogValues(int max, int round, String roundKeyone, String roundKeytwo, String roundKeythree) {
        if (max < 2 || max > 256) {
            Message.errors("模块设置错误", "下面参数设置错误", "候选密钥数为[2,256]");
            return false;
        }
        return checkSM4DialogValues(round, roundKeyone, roundKeytwo, roundKeythree);
    }

    private static boolean isWord(String value) {
        return value != null && WORD_PATTERN.matcher(value.trim()).matches();
    }

    private static void checkWords(long[] words, int minLength, String name) {
        if (words == null || words.length < minLength) {
            throw new IllegalArgumentException(name + "长度不足");
        }
    }

    private static int[] buildInvSbox() {
        int[] inv = new int[256];
        Arrays.fill(inv, -1);
        for (int i = 0; i < Sbox.length; i++) {
            inv[Sbox[i] & 0xFF] = i;
        }
        for (int i = 0; i < inv.length; i++) {
            if (inv[i] < 0) {
                throw new IllegalStateException("S盒不是一一映射");
            }
        }
        return inv;
    }

    public static final class RoundState {
        public final long[] x;
        public final long sIn;

        private RoundState(long[] x, long sIn) {
            this.x = x;
            this.sIn = sIn;
        }
    }
}
