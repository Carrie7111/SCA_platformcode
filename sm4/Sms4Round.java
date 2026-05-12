package sms4;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Vector;

import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JTextField;

import com.module.core.ModuleDesc;
import com.module.core.Trace;

import crypto.DifferentialAnalysis;

@ModuleDesc(pkgName="SM4", name="SM4 轮输出攻击分析", desc="", isVisible=true)
public class Sms4Round extends DifferentialAnalysis implements ActionListener {

    private static final long serialVersionUID = 1L;
    private static final long[] BYTE_GUESS = Sms4.buildRepeatedByteWords();

    private byte[] savedData;
    private long lastSIn;
    private long roundOut;
    private final long[] plain = new long[4];
    private final long[] cipher = new long[4];

    public static final String TRACK = "trackbit";
    public static final String MAX = "max";
    public static final String ROUND = "round";
    public static final String ROUND_KEY_ONE = "roundone.key";
    public static final String ROUND_KEY_TWO = "roundtwo.key";
    public static final String ROUND_KEY_THREE = "roundthree.key";
    public static final String SMS4_KEY = "sms4.key";
    public static final String DEFAULT_ROUND_KEY = "";

    JPanel candidatePanel, roundPanel;
    JPanel roundKeyPanel[] = new JPanel[3];
    int track, round;
    JTextField maxTextField;
    JTextField roundKeyTextField[] = new JTextField[3];
    JRadioButton roundButton[] = new JRadioButton[4];
    long roundKeyone, roundKeytwo, roundKeythree, newRoundKey;
    String SMS4key;

    public void initModule() {
        prefix = "SM4128 analysis results";
        moduleDescription = "Perform first order differential analysis on SMS4128";
        moduleVersion = "1.1";
        helpFile = "doc/modulesSMS4128Analysis.html";
        selectWindow = false;
        keys = 4;
        candidates = 256;
        dataLength = keys * candidates;
        keyOffset = 1;
        candidateStringLength = (int) StrictMath.ceil(Math.log(candidates - 1) / LOG10);
        keyTitle = "S盒";
        candidateTitle = "子密钥";
        titleSpace = 30;

        set(TRACK, track = 8);
        set(MAX, max);
        set(ROUND, round = 0);
        set(ROUND_KEY_ONE, roundKeyone = -1);
        set(ROUND_KEY_TWO, roundKeytwo = -1);
        set(ROUND_KEY_THREE, roundKeythree = -1);
        set(SMS4_KEY, DEFAULT_ROUND_KEY);
    }

    public JPanel initDialog() {
        roundPanel = new JPanel();
        for (int i = 0; i < 3; i++) {
            roundKeyPanel[i] = new JPanel();
            roundKeyTextField[i] = new JTextField("");
            roundKeyTextField[i].setEditable(false);
            roundButton[i] = new JRadioButton(String.valueOf(i + 1));
            roundButton[i].addActionListener(this);
        }
        roundButton[3] = new JRadioButton("4");
        roundButton[3].addActionListener(this);
        candidatePanel = new JPanel();
        maxTextField = new JTextField("");
        return Sms4.initSM4Dialog(maxTextField, roundKeyTextField, roundKeyPanel,
                roundPanel, candidatePanel, roundButton);
    }

    public void getDialogValues() {
        track = 8;
        max = parseInt(maxTextField, MAX);
        round = getInt(roundPanel, ROUND);
        bitGroup = track < 8 ? 1 : 8;
        roundKeyone = parseLong(roundKeyTextField[0], ROUND_KEY_ONE, -1, 16);
        roundKeytwo = parseLong(roundKeyTextField[1], ROUND_KEY_TWO, -1, 16);
        roundKeythree = parseLong(roundKeyTextField[2], ROUND_KEY_THREE, -1, 16);
    }

    public void setDialogValues() {
        setInt(maxTextField, MAX);
        setInt(roundPanel, ROUND);
        roundKeyone = getLong(ROUND_KEY_ONE);
        if (roundKeyone > -1) {
            roundKeyTextField[0].setText(formatNumberString(Long.toString(Sms4.u32(roundKeyone), 16).toUpperCase(), 2));
        }
        roundKeytwo = getLong(ROUND_KEY_TWO);
        if (roundKeytwo > -1) {
            roundKeyTextField[1].setText(formatNumberString(Long.toString(Sms4.u32(roundKeytwo), 16).toUpperCase(), 2));
        }
        roundKeythree = getLong(ROUND_KEY_THREE);
        if (roundKeythree > -1) {
            roundKeyTextField[2].setText(formatNumberString(Long.toString(Sms4.u32(roundKeythree), 16).toUpperCase(), 2));
        }
        refreshRoundKeyFields();
    }

    private int hw(int v) {
        return Integer.bitCount(v & 0xFF);
    }

    public float[] select(Trace t) {
        byte[] data = t == null ? null : t.getData();
        if (!Sms4.readPlainCipher(data, plain, cipher)) {
            return null;
        }

        float[] selected = new float[dataLength];
        Sms4.RoundState state = Sms4.buildRoundState(plain, round, roundKeyone, roundKeytwo, roundKeythree);
        lastSIn = state.sIn;

        for (int guess = 0; guess < 256; guess++) {
            long value = Sms4.u32(state.x[round] ^ BYTE_GUESS[guess]);
            fillSelection(selected, guess, value);
        }
        savedData = data.clone();
        return selected;
    }

    public void report(int key, Vector<float[]> best, int fragmentOffset, int fragmentEnd) {
        super.report(key, best, fragmentOffset, fragmentEnd);
        if (key == 0) {
            roundOut = 0;
        }
        roundOut = Sms4.u32((roundOut << 8) | chooseByte(best));

        if (key < keys - 1) {
            return;
        }

        newRoundKey = Sms4.recoverRoundKeyFromTOutput(roundOut, lastSIn);
        String s = formatNumberString(Long.toHexString(newRoundKey).toUpperCase(), 2);
        if (round < 3) {
            saveRoundKey(s);
            return;
        }

        long[] K = Sms4.recoverMasterKeyFromRoundKeys(roundKeyone, roundKeytwo, roundKeythree, newRoundKey);
        outputRoundKeys();
        SMS4key = formatKey(K[0]) + " " + formatKey(K[1]) + " " + formatKey(K[2]) + " " + formatKey(K[3]);
        outputMasterKey(K);
    }

    private void fillSelection(float[] selected, int guess, long value) {
        if (track < 8) {
            for (int j = 3, p = guess, q = 31 - track; j >= 0; j--, p += 256, q -= 8) {
                selected[p] = 2 * ((value >> q) & 1) - 1;
            }
            return;
        }
        for (int j = 3, p = guess, q = 24; j >= 0; j--, p += 256, q -= 8) {
            selected[p] = hw((int) (value >> q)) - 4;
        }
    }

    private int chooseByte(Vector<float[]> best) {
        if (best == null || best.isEmpty() || best.get(0).length < 3) {
            return 0;
        }
        float[] first = best.get(0);
        float[] picked = first;
        if (first[2] < 0 && best.size() > 1 && best.get(1).length > 0) {
            picked = best.get(1);
        }
        return ((int) picked[0]) & 0xFF;
    }

    private void saveRoundKey(String s) {
        switch (round) {
            case 0:
                set(ROUND_KEY_ONE, newRoundKey);
                break;
            case 1:
                set(ROUND_KEY_TWO, newRoundKey);
                break;
            case 2:
                set(ROUND_KEY_THREE, newRoundKey);
                break;
            default:
                break;
        }
        out("轮密钥: " + s);
    }

    private void outputRoundKeys() {
        out("第1轮轮密钥: " + formatNumberString(Long.toHexString(Sms4.u32(roundKeyone)).toUpperCase(), 2));
        out("第2轮轮密钥: " + formatNumberString(Long.toHexString(Sms4.u32(roundKeytwo)).toUpperCase(), 2));
        out("第3轮轮密钥: " + formatNumberString(Long.toHexString(Sms4.u32(roundKeythree)).toUpperCase(), 2));
        out("第4轮轮密钥: " + formatNumberString(Long.toHexString(Sms4.u32(newRoundKey)).toUpperCase(), 2));
    }

    private void outputMasterKey(long[] K) {
        long[] p = new long[4];
        long[] c = new long[4];
        if (savedData != null && Sms4.readPlainCipher(savedData, p, c) && Sms4.examineResult(p, c, K)) {
            out("SM4主密钥: " + SMS4key);
        } else {
            out("无匹配的密钥");
        }
    }

    private String formatKey(long key) {
        String hex = Long.toHexString(Sms4.u32(key)).toUpperCase();
        while (hex.length() < 8) {
            hex = "0" + hex;
        }
        return formatNumberString(hex, 2);
    }

    public Trace generate(int index) {
        Trace t = super.generate(index);
        t.setTitle("Candidate " + (index % candidates) + " of S-box " + ((index / candidates) + 1));
        return t;
    }

    @Override
    protected boolean checkDialogValues() {
        String s1 = trim(roundKeyTextField[0].getText());
        String s2 = trim(roundKeyTextField[1].getText());
        String s3 = trim(roundKeyTextField[2].getText());
        return Sms4.checkSM4DialogValues(max, round, s1, s2, s3);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        refreshRoundKeyFields();
    }

    private void refreshRoundKeyFields() {
        for (int i = 0; i < roundButton.length; i++) {
            if (roundButton[i].isSelected()) {
                for (int j = 0; j < 3; j++) {
                    roundKeyTextField[j].setEditable(j < i);
                }
                return;
            }
        }
    }
}
