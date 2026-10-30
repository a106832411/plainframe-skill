# -*- coding: utf-8 -*-
"""contact_sheet.py —— 从成片里等间隔抽帧，拼成一张接触表

用法：
    python tools/contact_sheet.py out.mp4                 # 默认 10 帧 5×2
    python tools/contact_sheet.py out.mp4 -n 12 -c 6      # 12 帧 6×2
    python tools/contact_sheet.py out.mp4 --at 3,15,27    # 指定秒数

输出：与视频同目录的 <名字>-contact.png
"""
import argparse
import os
import subprocess
import sys


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def build(mp4, out, n, cols, at):
    dur = probe_duration(mp4)
    if at:
        times = [float(x) for x in at.split(",") if x.strip()]
        n = len(times)
        # 用 select 表达式抽取指定时间点
        expr = "+".join(["eq(t\\,%.3f)" % t for t in times])
        vf = "select='%s',scale=384:-1,tile=%dx%d" % (expr, cols, (n + cols - 1) // cols)
    else:
        fps = n / dur
        vf = "fps=%.6f,scale=384:-1,tile=%dx%d" % (fps, cols, (n + cols - 1) // cols)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", mp4,
           "-vf", vf, "-frames:v", "1", out]
    subprocess.run(cmd, check=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("-n", "--frames", type=int, default=10)
    ap.add_argument("-c", "--cols", type=int, default=5)
    ap.add_argument("--at", default="", help="逗号分隔的秒数，给了就忽略 -n")
    ap.add_argument("-o", "--out", default="")
    a = ap.parse_args()
    if not os.path.exists(a.video):
        sys.exit("找不到视频：%s" % a.video)
    out = a.out or os.path.splitext(a.video)[0] + "-contact.png"
    build(a.video, out, a.frames, a.cols, a.at)
    print("ok", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
