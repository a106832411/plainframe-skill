# -*- coding: utf-8 -*-
"""
build.py —— 读 base.tpl + lines.json，生成 index.html
用法： python build.py <音频目录> [输出目录]
      python build.py . . --novoice     # 无口播：按字数估时长（cps，默认 4.2 字/秒）

它做四件事：
1. 逐句测有效时长（首尾静音裁掉），算出每句起止与场次切换点；
2. 把总时长写回 data-duration；
3. 生成 cut() 转场 + 逐句揭示（.lnN 元素在第 N 句开始时出现）；
4. 生成字幕层，并写出 offsets.json 给 mix.py 用。

约定：
- 场景：<section class="f" id="sN">
- 属于第 N 句的元素加 class="lnN"，CSS 里默认 opacity:0
- 需要描线的元素加 class="draw"（stroke-dasharray 由脚本设置）
- 根节点 id="root"，data-composition-id="<id>"
"""
import io, os, sys, json, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(io.open(os.path.join(HERE, "lines.json"), encoding="utf-8"))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
NOVOICE = "--novoice" in sys.argv or bool(CFG.get("novoice", False))
AUDIO_DIR = ARGS[0] if ARGS else os.path.join(HERE, "_tts")
if not NOVOICE and not os.path.isdir(AUDIO_DIR):
    raise SystemExit("build: 音频目录不存在：%s（先跑 gen_tts.mjs，或用 --novoice）" % AUDIO_DIR)
OUT_DIR = ARGS[1] if len(ARGS) > 1 else os.path.join(HERE, "..", "项目")
# 无口播：按字数估每句停留时间（中文约 4.2 字/秒，含标点）
CPS = float(CFG.get("cps", 4.2))
SR = 24000

GAP = float(CFG.get("gap", 0.5))
START = float(CFG.get("start", 0.6))
TAIL = float(CFG.get("tail", 2.4))


def measure_novoice(text):
    d = len(text) / CPS
    return max(1.6, min(4.4, d))


def measure(n):
    p = os.path.join(AUDIO_DIR, "e%02d" % n, "audio.wav")
    with wave.open(p, "rb") as f:
        fr, ch = f.getframerate(), f.getnchannels()
        x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    idx = np.where(np.abs(x) > 0.0035)[0]
    if len(idx) == 0:
        return len(x) / float(fr)
    a = max(0, idx[0] - int(0.04 * fr))
    b = min(len(x), idx[-1] + int(0.11 * fr))
    return (b - a) / float(fr)


t = START
rows = []
for line in CFG["lines"]:
    d = measure_novoice(line["text"]) if NOVOICE else measure(line["n"])
    rows.append({"n": line["n"], "scene": line["scene"], "text": line["text"],
                 "nosub": bool(line.get("nosub", False)),
                 "start": round(t, 2), "end": round(t + d, 2)})
    t += d + GAP

by_scene = {}
for r in rows:
    by_scene.setdefault(r["scene"], []).append(r)

cuts = {sc: by_scene[sc][0]["start"] for sc in sorted(by_scene) if sc > 1}
total = round(rows[-1]["end"] + TAIL, 1)


def P(x):
    return "%.2f" % x


s = io.open(os.path.join(HERE, "base.tpl"), encoding="utf-8").read()
s = s.replace("__DURATION__", str(total))
s = s.replace("__ID__", CFG.get("id", "demo"))

js = []
js.append("const tl = gsap.timeline({ paused: true });")
js.append("function cut(a, b, t) {")
js.append('  tl.to("#" + a, { opacity: 0, duration: 0.26, ease: "power2.inOut" }, t - 0.32);')
js.append('  tl.to("#" + b, { opacity: 1, duration: 0.26, ease: "power2.inOut" }, t - 0.20);')
js.append("}")
js.append('tl.set("#s1", { opacity: 1 }, 0);')
prev = 1
for sc in sorted(cuts):
    js.append('cut("s%d", "s%d", %s);' % (prev, sc, P(cuts[sc])))
    prev = sc

# 逐句揭示
for r in rows:
    st = r["start"]
    js.append('tl.to(".ln%d", { opacity: 1, y: 0, duration: 0.42, stagger: 0.07, ease: "power2.out" }, %s);'
              % (r["n"], P(st - 0.05)))
    js.append('tl.to(".ln%d.draw", { opacity: 1, strokeDashoffset: 0, duration: %s, ease: "power2.out" }, %s);'
              % (r["n"], P(max(0.6, min(1.8, r["end"] - st))), P(st - 0.05)))

js.append("const SUBS = [")
for r in rows:
    js.append('  [%s, %s, "%s", %s],' % (P(r["start"]), P(r["end"] + 0.25), r["text"],
              "false" if r["nosub"] else "true"))
js.append("];")
js.append("""const sub = document.getElementById("sub");
SUBS.forEach(([a, b, txt, keep]) => {
  // keep=false：画面上已有同义大字，这一句不再压字幕
  if (!keep) { tl.to(sub, { opacity: 0, duration: 0.18, overwrite: "auto" }, a); return; }
  tl.call(() => { sub.textContent = txt; }, null, a);
  tl.fromTo(sub, { opacity: 0 }, { opacity: 1, duration: 0.2, overwrite: "auto" }, a);
  tl.to(sub, { opacity: 0, duration: 0.16, overwrite: "auto" }, b - 0.16);
});
window.__timelines = window.__timelines || {};
window.__timelines["__CID__"] = tl;""")

s = s.replace("/*__TIMELINE__*/", "\n".join("      " + x for x in js))
s = s.replace("__CID__", CFG.get("id", "demo"))

os.makedirs(OUT_DIR, exist_ok=True)
io.open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8", newline="").write(s)
json.dump({"total": total, "novoice": NOVOICE,
           "offsets": [[r["n"], r["start"]] for r in rows]},
          io.open(os.path.join(OUT_DIR, "offsets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("mode %s / total %.1fs / %d 句 / cuts %s" % ("无口播" if NOVOICE else "配音", total, len(rows), {k: round(v, 2) for k, v in cuts.items()}))
