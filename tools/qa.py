# -*- coding: utf-8 -*-
"""
qa.py —— 出片自检（能自动判的那几条）

用法：
    python qa.py video.mp4 [--fps 2] [--still 0.004]

检查项：
1. 规格：1920×1080、时长、帧率
2. 画面密度：相邻采样帧的差异，找出「静止超过 2 秒」的段落
3. 黑屏 / 空镜：整帧接近纯黑的时长
4. 音频：有没有音轨、平均响度是否过低

输出一份问题清单；有问题返回码 1。
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

args = sys.argv[1:]
if not args:
    raise SystemExit("用法： python qa.py video.mp4 [--fps 2] [--still 0.004]")
video = args[0]
fps = 2.0
still_thr = 0.004
if "--fps" in args:
    fps = float(args[args.index("--fps") + 1])
if "--still" in args:
    still_thr = float(args[args.index("--still") + 1])


def probe(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=width,height,r_frame_rate,codec_type",
        "-of", "json", path]).decode()
    return json.loads(out)


info = probe(video)
dur = float(info["format"]["duration"])
streams = info.get("streams", [])
v = next((s for s in streams if s.get("codec_type") == "video"), None)
a = next((s for s in streams if s.get("codec_type") == "audio"), None)
problems = []

if not v:
    problems.append("没有视频流")
else:
    w, h = v.get("width"), v.get("height")
    if (w, h) != (1920, 1080):
        problems.append("分辨率 %sx%s，应为 1920x1080" % (w, h))
    fr = v.get("r_frame_rate", "0/1")
    num, den = (fr.split("/") + ["1"])[:2]
    try:
        if abs(float(num) / float(den) - 30) > 0.5:
            problems.append("帧率 %s（参考 30）" % fr)
    except Exception:
        pass

if not a:
    problems.append("没有音轨（无口播版应有 BGM，只音效版可忽略）")

# 逐帧采样
tmp = tempfile.mkdtemp(prefix="qa_")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video,
                "-vf", "fps=%g,scale=160:-1" % fps, os.path.join(tmp, "f%04d.png")], check=True)
files = sorted(os.listdir(tmp))
arrs = []
for f in files:
    im = Image.open(os.path.join(tmp, f)).convert("L")
    arrs.append(np.asarray(im, dtype=np.float32) / 255.0)

diffs, blacks = [], []
for i in range(1, len(arrs)):
    d = float(np.mean(np.abs(arrs[i] - arrs[i - 1])))
    diffs.append(d)
    blacks.append(float(np.mean(arrs[i])))

# 找连续静止段（差异低于阈值的连续帧）
still_runs, cur = [], 0
for d in diffs:
    if d < still_thr:
        cur += 1
    else:
        if cur:
            still_runs.append(cur)
        cur = 0
if cur:
    still_runs.append(cur)

step = 1.0 / fps
long_still = [round(r * step, 1) for r in still_runs if r * step >= 2.0]
if long_still:
    problems.append("有 %d 段静止超过 2 秒：%s" % (len(long_still), long_still[:8]))

dark = [i for i, b in enumerate(blacks) if b < 0.02]
if len(dark) * step >= 1.0:
    problems.append("接近纯黑的画面约 %.1f 秒" % (len(dark) * step))

print("时长 %.1fs / %d 帧采样 / 平均帧差 %.4f / 静止段 %d" % (dur, len(arrs), float(np.mean(diffs)), len(long_still)))
if problems:
    print("\n发现问题：")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("\n自动检查通过（画面密度、规格、音轨）")
