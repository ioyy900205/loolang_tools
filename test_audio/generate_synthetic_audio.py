#!/usr/bin/env python3
import os
import math
import random
import wave
from array import array
from pathlib import Path

SAMPLE_RATE = 16000
CLEAN_SECONDS = 30.0
IR_SECONDS = 0.2
AMPLITUDE = 0.2  # for clean sines


def write_wav_int16(path: Path, samples: list[int], sr: int = SAMPLE_RATE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sr)
        wf.writeframes(array('h', samples).tobytes())


def write_wav_int16_multich(path: Path, samples_by_channel: list[list[int]], sr: int = SAMPLE_RATE):
    path.parent.mkdir(parents=True, exist_ok=True)
    num_channels = len(samples_by_channel)
    if num_channels == 0:
        raise ValueError("samples_by_channel must have at least 1 channel")
    n = min(len(ch) for ch in samples_by_channel)
    # ensure equal length
    channels = [ch[:n] for ch in samples_by_channel]
    interleaved: list[int] = []
    for i in range(n):
        for c in range(num_channels):
            interleaved.append(channels[c][i])
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(array('h', interleaved).tobytes())


def float_to_int16(x: float) -> int:
    x = max(-1.0, min(1.0, x))
    return int(round(x * 32767.0))


def gen_sine(freq_hz: float, seconds: float, amp: float = AMPLITUDE, sr: int = SAMPLE_RATE) -> list[int]:
    n = int(seconds * sr)
    return [float_to_int16(amp * math.sin(2.0 * math.pi * freq_hz * (i / sr))) for i in range(n)]


def gen_ir_decay(seconds: float = IR_SECONDS, sr: int = SAMPLE_RATE) -> list[int]:
    # simple exponential decay impulse response with light noise
    n = int(seconds * sr)
    samples: list[int] = []
    for i in range(n):
        t = i / sr
        decay = math.exp(-6.0 * t)  # fairly short decay
        noise = (random.random() * 2.0 - 1.0) * 0.1
        val = (1.0 if i == 0 else 0.0) * 0.8 + noise * decay
        samples.append(float_to_int16(val))
    return samples


def gen_ir_decay_multi(seconds: float = IR_SECONDS, sr: int = SAMPLE_RATE, num_channels: int = 4) -> list[list[int]]:
    # 4-zone: 生成4通道IR
    n = int(seconds * sr)
    channels: list[list[int]] = []
    for c in range(num_channels):
        base = gen_ir_decay(seconds=seconds, sr=sr)
        # add small channel-dependent delay
        delay = c * 8  # samples
        ch = [0] * delay + base
        ch = ch[:n]
        # slight per-channel scaling
        scale = 1.0 - 0.1 * c
        ch = [int(max(-32768, min(32767, int(s * scale)))) for s in ch]
        channels.append(ch)
    return channels


def main():
    base = Path(__file__).resolve().parent
    clean_dir = base / 'clean'
    ir_dir = base / 'ir'

    # Clean wavs (mono)
    write_wav_int16(clean_dir / 'clean1.wav', gen_sine(440.0, CLEAN_SECONDS))
    write_wav_int16(clean_dir / 'clean2.wav', gen_sine(660.0, CLEAN_SECONDS))

    # IR folders matching expected zone keywords (4-channel IRs for 4-zone tests)
    for zone in ['zhujia', 'fujia', 'zhujiahoupai', 'fujiahoupai']:
        write_wav_int16_multich(ir_dir / zone / 'ir1.wav', gen_ir_decay_multi(num_channels=4))
        write_wav_int16_multich(ir_dir / zone / 'ir2.wav', gen_ir_decay_multi(num_channels=4))

    print(f"Clean and IR test WAVs written under: {base}")


if __name__ == '__main__':
    main() 