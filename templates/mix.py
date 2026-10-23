# -*- coding: utf-8 -*-
"""
mix.py —— 混音，输出 mix.wav
口播版：人声叠加 + BGM 闪避；无口播版（offsets.json 里 novoice=true）：只出 BGM。
用法： python mix.py <音频目录> <输出目录>

依赖 build.py 生成的 offsets.json（每句的起始时间）。
"""
import io, os, sys, json, wave
import numpy as np

SR = 24000
HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_tts")
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "项目")

meta = json.load(io.open(os.path.join(OUT_DIR, "offsets.json"), encoding="utf-8"))
TOTAL = float(meta["total"])
NOVOICE = bool(meta.get("novoice", False))


def bgm_only():
    """无口播：只出 BGM，首尾各 0.8 秒淡入淡出，整体归一。"""
    bp = os.path.join(OUT_DIR, "bgm_24k.wav")
    n = int(SR * TOTAL)
    if os.path.exists(bp):
        with wave.open(bp, "rb") as f:
            x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        x = x[:n]
        if len(x) < n:
            x = np.pad(x, (0, n - len(x)))
    else:
        raise SystemExit("mix: 无口播模式需要 %s（先跑 synth_bgm.py 并转成 24k 单声道）" % bp)
    f0 = int(0.8 * SR)
    x[:f0] *= np.linspace(0, 1, f0)
    x[-f0:] *= np.linspace(1, 0, f0)
    x = x / (float(np.max(np.abs(x))) or 1.0) * 0.82
    out = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT_DIR, "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
    print("mix ok (无口播) total %.1f" % TOTAL)
    sys.exit(0)



if NOVOICE:
    bgm_only()

# ── 防错：音频目录必须和 offsets.json 对得上 ──
_missing = [n for n, _ in meta["offsets"] if not os.path.exists(os.path.join(AUDIO_DIR, "e%02d" % n, "audio.wav"))]
if _missing:
    raise SystemExit("mix: 音频缺失 e%02d …（目录：%s）" % (_missing[0], AUDIO_DIR))

# 每句音频长度不能超过它分到的时间槽，否则很可能用错了音频目录
_slot_violation = []
for _i, (_n, _off) in enumerate(meta["offsets"]):
    _next = meta["offsets"][_i + 1][1] if _i + 1 < len(meta["offsets"]) else TOTAL
    _slot = _next - _off
    with wave.open(os.path.join(AUDIO_DIR, "e%02d" % _n, "audio.wav"), "rb") as _f:
        _len = _f.getnframes() / float(_f.getframerate())
    if _len > _slot + 0.6:
        _slot_violation.append((_n, round(_len, 2), round(_slot, 2)))
if _slot_violation:
    raise SystemExit("mix: 第 %d 句音频 %.2fs 超过时间槽 %.2fs —— 多半是音频目录用错了（%s）"
                     % (_slot_violation[0][0], _slot_violation[0][1], _slot_violation[0][2], AUDIO_DIR))

def read_wav(p):
    with wave.open(p, "rb") as f:
        ch, fr = f.getnchannels(), f.getframerate()
        raw = f.readframes(f.getnframes())
    d = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        d = d.reshape(-1, ch).mean(axis=1)
    if fr != SR:
        n = int(len(d) * SR / fr)
        d = np.interp(np.linspace(0, len(d) - 1, n), np.arange(len(d)), d)
    return d


def trim(x, thr=0.0035):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(0.04 * SR))
    b = min(len(x), idx[-1] + int(0.11 * SR))
    return x[a:b]


buf = np.zeros(int(SR * TOTAL) + SR, dtype=np.float32)
info = []
for n, off in meta["offsets"]:
    p = os.path.join(AUDIO_DIR, "e%02d" % n, "audio.wav")
    x = trim(read_wav(p))
    x = x / (float(np.max(np.abs(x))) or 1.0) * 0.86
    i0 = int(off * SR)
    buf[i0:i0 + len(x)] += x
    info.append((off, off + len(x) / SR))

voice = buf[: int(SR * TOTAL)]

# BGM：可选
bgm_path = os.path.join(OUT_DIR, "bgm_24k.wav")
if os.path.exists(bgm_path):
    bg = read_wav(bgm_path)[: len(voice)]
    if len(bg) < len(voice):
        bg = np.pad(bg, (0, len(voice) - len(bg)))
    env = np.abs(voice)
    block = int(0.05 * SR)
    nb = max(1, len(env) // block)
    env = env[: nb * block].reshape(nb, block).mean(axis=1)
    env = np.repeat(env, block)
    env = np.pad(env, (0, len(voice) - len(env)))
    duck = 1.0 - 0.35 * np.clip(env / (np.max(env) + 1e-9) * 6, 0, 1)
    mixv = voice + bg * 0.26 * duck
else:
    mixv = voice

mixv = mixv / (float(np.max(np.abs(mixv))) or 1.0) * 0.92
fade = int(1.0 * SR)
mixv[-fade:] *= np.linspace(1, 0, fade)

out = (np.clip(mixv, -1, 1) * 32767).astype(np.int16)
with wave.open(os.path.join(OUT_DIR, "mix.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes(out.tobytes())

gaps = [round(info[i][0] - info[i - 1][1], 2) for i in range(1, len(info))]
print("mix ok · total %.1fs · max gap %.2fs · tail %.2fs" % (TOTAL, max(gaps), TOTAL - info[-1][1]))
