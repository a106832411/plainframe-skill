# -*- coding: utf-8 -*-
"""
beats.py —— 拍表 → 时间线

无口播路线的核心：所有画面、字幕、转场都读同一张拍表，不再各自算时间。

用法：
    python beats.py beats.json [--bpm 100] [--out beats.json.timing]

beats.json 格式：
{
  "bpm": 100,
  "id": "mpemba-novoice",
  "lines": [
    {"beat": 0,  "beats": 3, "scene": 1, "text": "热水比冷水先结冰"},
    {"beat": 3,  "beats": 2, "scene": 1, "text": "这不是段子"}
  ]
}

输出：
{
  "bpm": 100, "total": 90.0,
  "lines": [{"n":1, "beat":0, "start":0.0, "end":1.8, "scene":1, "text":"..."}],
  "cuts": {"2": 12.0}
}
"""
import io, json, os, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    raise SystemExit("用法： python beats.py beats.json [--bpm 100]")

src = args[0]
cfg = json.load(io.open(src, encoding="utf-8"))
bpm = float(cfg.get("bpm", 100))
bps = 60.0 / bpm                      # 每拍秒数

lines = []
rows = []
for i, ln in enumerate(cfg["lines"], 1):
    b0 = float(ln.get("beat", 0))
    nb = float(ln.get("beats", 3))
    st = round(b0 * bps, 2)
    en = round((b0 + nb) * bps, 2)
    rows.append({"n": i, "beat": b0, "beats": nb, "start": st, "end": en,
                 "scene": int(ln.get("scene", 1)), "text": ln.get("text", "")})

cuts = {}
for r in rows:
    cuts.setdefault(r["scene"], r["start"])
total = round(rows[-1]["end"] + float(cfg.get("tail", 1.2)), 1)

out = {"bpm": bpm, "total": total,
       "cuts": {str(k): v for k, v in sorted(cuts.items()) if k > 1},
       "lines": rows}

dst = src.replace(".json", ".timing.json")
json.dump(out, io.open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 顺手打一张人看的表
print("bpm %g / 每拍 %.3fs / 总长 %.1fs / %d 句" % (bpm, bps, total, len(rows)))
for r in rows:
    print("  拍%5.1f  %5.1fs–%5.1fs  场%d  %s" % (r["beat"], r["start"], r["end"], r["scene"], r["text"]))
print("写出 %s" % dst)
