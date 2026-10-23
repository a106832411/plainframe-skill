# -*- coding: utf-8 -*-
"""
sheet.py —— 按时间点抽帧，拼一张联系表

用法：
    python sheet.py video.mp4 3 8 15 22          # 指定秒数
    python sheet.py video.mp4 --even 12          # 均匀取 12 帧
    python sheet.py video.mp4 --even 12 --cols 4 --out sheet.png

输出 PNG，右上角标时间码。依赖 ffmpeg + Pillow。
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

args = sys.argv[1:]
if not args:
    raise SystemExit("用法： python sheet.py video.mp4 3 8 15 | --even 12 [--cols 4] [--out sheet.png]")

video = args[0]
cols = 4
out = "sheet.png"
times = []
i = 1
while i < len(args):
    a = args[i]
    if a == "--cols":
        cols = int(args[i + 1]); i += 2
    elif a == "--out":
        out = args[i + 1]; i += 2
    elif a == "--even":
        n = int(args[i + 1]); i += 2
        dur = float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", video]).decode().strip())
        step = dur / (n + 1)
        times = [round(step * (k + 1), 2) for k in range(n)]
    else:
        times.append(float(a)); i += 1

if not times:
    raise SystemExit("没有给出时间点")

tmp = tempfile.mkdtemp(prefix="sheet_")
frames = []
for idx, t in enumerate(times):
    p = os.path.join(tmp, "f%03d.png" % idx)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video,
                    "-frames:v", "1", "-vf", "scale=480:-1", p], check=True)
    if os.path.exists(p):
        frames.append((t, Image.open(p).convert("RGB")))

if not frames:
    raise SystemExit("抽帧失败")

w, h = frames[0][1].size
rows = (len(frames) + cols - 1) // cols
pad = 6
sheet = Image.new("RGB", (cols * w + (cols + 1) * pad, rows * h + (rows + 1) * pad), (12, 18, 24))
d = ImageDraw.Draw(sheet)
for k, (t, im) in enumerate(frames):
    r, c = divmod(k, cols)
    x = pad + c * (w + pad)
    y = pad + r * (h + pad)
    sheet.paste(im, (x, y))
    d.rectangle([x, y, x + 74, y + 20], fill=(0, 0, 0))
    d.text((x + 4, y + 4), "%.1fs" % t, fill=(242, 166, 90))

sheet.save(out)
print("size %dx%d / %d 帧 → %s" % (sheet.size[0], sheet.size[1], len(frames), out))
