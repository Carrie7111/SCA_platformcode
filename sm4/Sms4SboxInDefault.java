package com.module.useredit.sys;

import sms4.Sms4;

/**
 * SM4 S 盒输入模型的默认参考量计算。
 * 数据格式：前 16 字节为明文，后 16 字节为密文。
 */
public class Sms4SboxInDefault extends Sms4SboxInBase {

    private static final int WORD_COUNT = 4;
    private static final int CANDIDATES = 256;
    private static final int OUTPUT_SIZE = WORD_COUNT * CANDIDATES;
    private static final long WORD_MASK = 0xFFFFFFFFL;

    public float[] GetMidDataHW(byte[] data) {
        long[] block = readPlainBlock(data);
        if (block == null) {
            return null;
        }

        int currentRound = normalizeRound(round);
        long[] state = block.clone();
        long sIn = prepareRoundState(state, currentRound);

        float[] midDataHw = new float[OUTPUT_SIZE];
        for (int candidate = 0; candidate < CANDIDATES; candidate++) {
            long sBoxIn = u32(sIn ^ repeatByte(candidate));
            fillWordHammingWeight(midDataHw, candidate, sBoxIn);
        }
        return midDataHw;
    }

    private long prepareRoundState(long[] state, int currentRound) {
        if (currentRound >= 1) {
            state[0] = u32(state[0] ^ Sms4.T1(state[1] ^ state[2] ^ state[3] ^ roundKeyone));
        }
        if (currentRound >= 2) {
            state[1] = u32(state[1] ^ Sms4.T1(state[2] ^ state[3] ^ state[0] ^ roundKeytwo));
        }
        if (currentRound >= 3) {
            state[2] = u32(state[2] ^ Sms4.T1(state[3] ^ state[0] ^ state[1] ^ roundKeythree));
        }

        switch (currentRound) {
            case 0:
                return u32(state[1] ^ state[2] ^ state[3]);
            case 1:
                return u32(state[2] ^ state[3] ^ state[0]);
            case 2:
                return u32(state[3] ^ state[0] ^ state[1]);
            case 3:
                return u32(state[0] ^ state[1] ^ state[2]);
            default:
                return 0L;
        }
    }

    private static long[] readPlainBlock(byte[] data) {
        if (data == null || data.length < 32) {
            return null;
        }

        long[] block = new long[WORD_COUNT];
        for (int i = 0; i < WORD_COUNT; i++) {
            int offset = i * 4;
            block[i] = ((data[offset] & 0xFFL) << 24)
                    | ((data[offset + 1] & 0xFFL) << 16)
                    | ((data[offset + 2] & 0xFFL) << 8)
                    | (data[offset + 3] & 0xFFL);
        }
        return block;
    }

    private static void fillWordHammingWeight(float[] output, int candidate, long value) {
        for (int byteIndex = 0, shift = 24; byteIndex < WORD_COUNT; byteIndex++, shift -= 8) {
            int pos = candidate + byteIndex * CANDIDATES;
            output[pos] = hammingWeight((value >>> shift) & 0xFFL) - 4;
        }
    }

    private static int normalizeRound(int value) {
        if (value < 0) {
            return 0;
        }
        if (value > 3) {
            return 3;
        }
        return value;
    }

    private static long repeatByte(int value) {
        long b = value & 0xFFL;
        return (b << 24) | (b << 16) | (b << 8) | b;
    }

    private static int hammingWeight(long value) {
        return Long.bitCount(value & 0xFFL);
    }

    private static long u32(long value) {
        return value & WORD_MASK;
    }
}
