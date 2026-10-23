"""合成 Vibe 知识大赏 风格 BGM：77 BPM，A 小调，pad + 钢琴 + kick + shaker"""
import numpy as np
import wave, struct, math

SR = 44100
BPM = 77
DUR = float(__import__("os").environ.get("BGM_DUR", "64.8"))
BEAT = 60.0 / BPM
BAR = BEAT * 4
N = int(SR * DUR)
rng = np.random.default_rng(7)

def note_hz(n):
    # n: 半音相对 A4
    return 440.0 * (2 ** (n / 12.0))

# 和弦（相对 A4 的半音）
CHORDS = [
    ("Am", [-12, -9, -5]),   # A2 C3 E3
    ("F",  [-16, -12, -9]),  # F2 A2 C3
    ("C",  [-9, -5, -2]),    # C3 E3 G3
    ("G",  [-14, -10, -7]),  # G2 B2 D3
]

def env(t, a, d, s_level, s_len, r):
    e = np.ones_like(t)
    e = np.where(t < a, t / a, e)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s_level) * (t - a) / d, e)
    e = np.where(t >= a + d, s_level, e)
    return e

def pad_tone(freq, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    w = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t) + 0.18 * np.sin(2 * np.pi * freq * 3 * t)
    # 慢起慢落
    a = 1.2; r = 1.6
    e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / r))
    return w * e * amp

def piano_tone(freq, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    w = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2 * t)
         + 0.28 * np.sin(2 * np.pi * freq * 3 * t) + 0.14 * np.sin(2 * np.pi * freq * 4 * t))
    e = np.exp(-t * 2.6) * (1 - np.exp(-t * 90))
    return w * e * amp

mix = np.zeros(N, dtype=np.float64)

def add(sig, start):
    i = int(start * SR)
    j = min(N, i + len(sig))
    if i < N:
        mix[i:j] += sig[: j - i]

# 段落织体
def section(t):
    if t < 14: return "pad"
    if t < 46: return "piano"
    if t < 70: return "full"
    if t < 78: return "arp"
    return "outro"

# pad：每 2 小节换和弦
t = 0.0
ci = 0
while t < DUR:
    name, notes = CHORDS[ci % 4]
    dur = min(BAR * 2, DUR - t)
    for k, nn in enumerate(notes):
        add(pad_tone(note_hz(nn), dur + 1.0, 0.09 / (k + 1)), t)
    # 低音
    add(pad_tone(note_hz(notes[0] - 12), dur + 1.0, 0.12), t)
    t += BAR * 2
    ci += 1

# 钢琴：每小节柱式
t = 0.0
ci = 0
while t < DUR:
    sec = section(t)
    if sec in ("piano", "full", "arp", "outro"):
        name, notes = CHORDS[ci % 4]
        dur = min(BAR, DUR - t)
        for k, nn in enumerate(notes):
            add(piano_tone(note_hz(nn), min(3.2, dur), 0.14), t + k * 0.06)
        if sec in ("full", "arp"):
            add(piano_tone(note_hz(notes[2] + 12), 1.6, 0.08), t + BEAT * 2)
    t += BAR
    ci += 1

# kick / shaker
t = 0.0
while t < DUR:
    if section(t) == "full":
        # kick 每 2 拍
        for b in (0, 2):
            tt = t + b * BEAT
            if tt < DUR:
                n = int(0.18 * SR)
                x = np.arange(n) / SR
                f = 62 * np.exp(-x * 18) + 38
                add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 26) * 0.5, tt)
        # shaker 8 分
        for b in range(8):
            tt = t + b * BEAT / 2
            if tt < DUR:
                n = int(0.05 * SR)
                noise = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (0.012 * SR))
                add(noise * 0.05, tt)
    t += BAR

# 淡入淡出
fade = int(1.2 * SR)
mix[:fade] *= np.linspace(0, 1, fade)
mix[-fade:] *= np.linspace(1, 0, fade)

# 响度：目标 RMS ≈ -18 dBFS，峰值限 -1 dB
rms = np.sqrt(np.mean(mix ** 2))
mix *= (10 ** (-18 / 20)) / (rms + 1e-9)
peak = np.max(np.abs(mix))
if peak > 0.89:
    mix *= 0.89 / peak

stereo = np.stack([mix, np.roll(mix, 220)], axis=1)
data = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)

with wave.open(__import__("os").environ.get("BGM_OUT", "bgm.wav"), "wb") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes(data.tobytes())
print("bgm ok", round(DUR, 1), "s  rms", round(20 * math.log10(np.sqrt(np.mean(mix ** 2)) + 1e-9), 1), "dBFS")
