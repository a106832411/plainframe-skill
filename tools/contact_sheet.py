# -*- coding: utf-8 -*-
"""contact_sheet.py —— 抽帧、拼联系表（唯一的抽帧工具）

用法：
    python tools/contact_sheet.py out.mp4                    # 等间隔 10 帧，5 列
    python tools/contact_sheet.py out.mp4 -n 16 -c 4         # 16 帧，4 列
    python tools/contact_sheet.py out.mp4 --at 3,9.5,13.6    # 指定时间点
    python tools/contact_sheet.py out.mp4 -n 12 --frames-dir frames
                                                             # 同时把单帧落到 frames/

输出：./<视频名>-contact.png（每帧右上角带时间码）。依赖 ffmpeg + Pillow。

默认落在**当前目录**而不是视频旁边——成片文件夹只该放成片，接触表留在工程目录。

`--frames-dir` 就是原来 templates/check_frames.ps1 干的事（逐场抽单帧仔细看），
合到这里，不再维护第二套抽帧脚本。
"""
import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def probe_duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path])
    return float(out.decode().strip())


def pick_times(dur, frames, at):
    if at:
        return [float(x) for x in at.replace(" ", "").split(",") if x]
    step = dur / (frames + 1)
    return [round(step * (k + 1), 2) for k in range(frames)]


def grab(video, t, size, out_path):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video,
         "-frames:v", "1", "-vf", "scale=%d:-1" % size, out_path],
        check=True)
    return os.path.exists(out_path)


def tile(frames, cols, out, label_h=22, pad=6):
    w, h = frames[0][1].size
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB",
                      (cols * w + (cols + 1) * pad, rows * h + (rows + 1) * pad),
                      (12, 18, 24))
    d = ImageDraw.Draw(sheet)
    for k, (t, im) in enumerate(frames):
        r, c = divmod(k, cols)
        x = pad + c * (w + pad)
        y = pad + r * (h + pad)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 76, y + label_h], fill=(0, 0, 0))
        d.text((x + 5, y + 5), "%.1fs" % t, fill=(242, 166, 90))
    sheet.save(out)
    return sheet.size


def main():
    ap = argparse.ArgumentParser(description="抽帧拼联系表")
    ap.add_argument("video")
    ap.add_argument("-n", "--frames", type=int, default=10, help="等间隔取样帧数（默认 10）")
    ap.add_argument("-c", "--cols", type=int, default=5, help="每行几帧（默认 5）")
    ap.add_argument("--at", default="", help="逗号分隔的秒数，给了就忽略 -n")
    ap.add_argument("--width", type=int, default=480, help="单帧宽度（默认 480）")
    ap.add_argument("-o", "--out", default="", help="输出 PNG，默认 <视频名>-contact.png")
    ap.add_argument("--frames-dir", default="", help="额外把单帧存进这个目录")
    a = ap.parse_args()

    if not os.path.exists(a.video):
        sys.exit("找不到视频：%s" % a.video)

    out = a.out or os.path.basename(os.path.splitext(a.video)[0]) + "-contact.png"
    times = pick_times(probe_duration(a.video), a.frames, a.at)
    if not times:
        sys.exit("没有可用的时间点")

    if a.frames_dir:
        os.makedirs(a.frames_dir, exist_ok=True)

    tmp = tempfile.mkdtemp(prefix="sheet_")
    shots = []
    for i, t in enumerate(times):
        p = os.path.join(tmp, "f%03d.png" % i)
        if not grab(a.video, t, a.width, p):
            continue
        shots.append((t, Image.open(p).convert("RGB")))
        if a.frames_dir:
            Image.open(p).convert("RGB").save(
                os.path.join(a.frames_dir, "f%02d_%.1fs.jpg" % (i + 1, t)), quality=92)

    if not shots:
        sys.exit("抽帧失败")

    size = tile(shots, a.cols, out)
    print("%d 帧 / %dx%d → %s" % (len(shots), size[0], size[1], out))
    if a.frames_dir:
        print("单帧 → %s" % a.frames_dir)


if __name__ == "__main__":
    main()
