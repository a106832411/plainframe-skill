# -*- coding: utf-8 -*-
"""18 套风格的样例：每套独立构图、独立母题、独立文案。

不再「同一句话换颜色」。每套有：
- layout：6 种构图骨架（A 左文右图 / B 居中 / C 底文 / D 竖排 / E 全屏图形 / F 分栏）
- motif：专属图形
- copy：与该风格气质匹配的一句话
"""
import io, os

ROOT = r"C:\Users\49820\Desktop\plainframe-skill\styles"

S = [
    dict(no="01", name="鎏金暗场", en="GOLD NO.01", layout="A", bg="#0B0908", fg="#EDE3D0", ac="#DDBD74", ac2="#D9583C",
         fam="YH", weight=900, ls=2, size=112, title="先生气<br>后找理由", sub="情绪为什么失控",
         motif="wave", note="深底 + 鎏金字 + 一点朱红"),
    dict(no="02", name="复古丝印", en="SILKSCREEN", layout="F", bg="#F0E3C8", fg="#1A1710", ac="#D63A2C", ac2="#184A9E",
         fam="YH", weight=900, ls=-2, size=132, title="先热<br>后想", sub="先有反应，再有解释",
         motif="split", note="纸色 + 双色套印，左右对比"),
    dict(no="03", name="示波器", en="OSCILLOSCOPE", layout="E", bg="#030C0A", fg="#5FE8C8", ac="#FFB347", ac2="#1E4A42",
         fam="Mono", weight=700, ls=5, size=96, title="声音进来<br>先抄近路", sub="12ms",
         motif="trace", note="磷光绿 + 网格，波形铺满画面"),
    dict(no="04", name="蓝图", en="SCHEMATIC", layout="C", bg="#0A1A2E", fg="#CFE3F7", ac="#6FA8DC", ac2="#FFB347",
         fam="Mono", weight=700, ls=3, size=104, title="两条通路<br>一快一慢", sub="SECTION A-A",
         motif="blueprint", note="蓝底白线 + 尺寸标注"),
    dict(no="05", name="霓虹", en="NEON", layout="E", bg="#07040C", fg="#FFE9F4", ac="#FF3D8B", ac2="#38E8FF",
         fam="YH", weight=900, ls=3, size=108, title="这行字<br>你不一定看得清", sub="NEON / 24H",
         motif="ring", note="黑底霓虹管 + 同心环"),
    dict(no="06", name="极光", en="AURORA", layout="E", bg="#04080F", fg="#E6FBF6", ac="#46E0C0", ac2="#7C6BFF",
         fam="YH", weight=800, ls=2, size=150, title="会失控", sub="它自己会走下去",
         motif="aurora", note="渐层柔光，几乎没有硬边"),
    dict(no="07", name="黑板粉笔", en="BLACKBOARD", layout="B", bg="#1E2A24", fg="#EDEDE3", ac="#F2C14E", ac2="#B9C8B4",
         fam="Kai", weight=700, ls=10, size=220, title="熵", sub="只增不减",
         motif="chalk", note="楷体手写 + 粉笔毛边"),
    dict(no="08", name="暗场几何", en="DARK GEOMETRY", layout="A", bg="#12100E", fg="#EFE6D6", ac="#C98553", ac2="#5B8FBF",
         fam="YH", weight=900, ls=-2, size=104, title="水面<br>被盖住了", sub="水位还在涨",
         motif="water", note="暖黑 + 米白线 + 咖啡棕"),
    dict(no="09", name="报纸黑白", en="NEWSPRINT", layout="D", bg="#F4F1EA", fg="#15130F", ac="#B03A2E", ac2="#15130F",
         fam="Song", weight=900, ls=1, size=96, title="没有任何事故", sub="早上 7:40 · 环线",
         motif="columns", note="衬线大标题 + 分栏 + 一点红"),
    dict(no="10", name="深空星图", en="DEEP FIELD", layout="E", bg="#05070E", fg="#DCE8FF", ac="#4D8CFF", ac2="#FF7A3D",
         fam="YH", weight=800, ls=2, size=110, title="尺度<br>比你想的大", sub="1 : 10¹⁸",
         motif="stars", note="星点 + 轨道 + 尺度标尺"),
    dict(no="11", name="手绘水彩", en="WATERCOLOR", layout="C", bg="#FBF8F1", fg="#3A3A3A", ac="#C98A5B", ac2="#7FA8C9",
         fam="YH", weight=800, ls=2, size=104, title="它是<br>慢慢变的", sub="没有一步是突然的",
         motif="blob", note="纸白 + 晕染，边界是软的"),
    dict(no="12", name="等距白模", en="ISOMETRIC", layout="A", bg="#ECEAE4", fg="#1F2A33", ac="#E07A3F", ac2="#7C9AA8",
         fam="YH", weight=800, ls=2, size=108, title="三层结构", sub="拆开看",
         motif="iso", note="浅灰白 + 30° 轴测方块"),
    dict(no="13", name="复古录像", en="VHS 1987", layout="E", bg="#0B0B0B", fg="#F5F5F0", ac="#38E8FF", ac2="#FF6A3D",
         fam="Mono", weight=700, ls=3, size=100, title="这一段<br>被录下来了", sub="REC 00:00:30",
         motif="vhs", note="青橙色差 + 扫描线"),
    dict(no="14", name="冰窟蓝", en="ICE CAVE", layout="A", bg="#08121A", fg="#DCEBF5", ac="#F2A65A", ac2="#7FD3E8",
         fam="YH", weight=900, ls=-2, size=100, title="热水<br>先结冰", sub="90℃ / 20℃ · 同一个冰箱",
         motif="cup", note="冷底 + 冰白 + 唯一暖色"),
    dict(no="15", name="像素 8bit", en="PIXEL 8BIT", layout="B", bg="#101018", fg="#E8E8F0", ac="#FFD23F", ac2="#3FBF8F",
         fam="Mono", weight=700, ls=6, size=150, title="8-BIT", sub="PRESS START",
         motif="pixel", note="有限色板 + 方块构图"),
    dict(no="16", name="终端绿", en="TERMINAL", layout="D", bg="#070B07", fg="#8CFF7A", ac="#C8FF3D", ac2="#2F6B33",
         fam="Mono", weight=700, ls=3, size=92, title="loading", sub="> _",
         motif="terminal", note="磷光绿 + 光标 + 扫描线"),
    dict(no="17", name="极简白", en="SWISS", layout="F", bg="#FAFAF7", fg="#111111", ac="#111111", ac2="#E03E36",
         fam="YH", weight=700, ls=-1, size=140, title="少<br>即是多", sub="LESS, BUT BETTER",
         motif="swiss", note="白底黑字，只有一条线和一个点"),
    dict(no="18", name="胶片棕", en="35MM", layout="C", bg="#171008", fg="#EADCC0", ac="#D89B5A", ac2="#8B6A45",
         fam="Song", weight=700, ls=2, size=112, title="1987 年<br>夏天", sub="KODAK 400",
         motif="film", note="暖褐 + 颗粒 + 齿孔"),
]

MOTIF = {
    "wave": '<path d="M 1180 560 L 1260 560 L 1300 450 L 1340 670 L 1380 560 L 1560 560 L 1600 480 L 1640 640 L 1680 560 L 1790 560" fill="none" stroke="{ac}" stroke-width="4"/>',
    "split": '<rect x="960" y="0" width="4" height="1080" fill="{fg}" opacity="0.25"/><circle cx="1290" cy="560" r="150" fill="{ac}" opacity="0.9"/><circle cx="1600" cy="560" r="150" fill="{ac2}" opacity="0.85"/>',
    "trace": '<g opacity="0.4"><line x1="0" y1="300" x2="1920" y2="300" stroke="{fg}" stroke-width="1"/><line x1="0" y1="540" x2="1920" y2="540" stroke="{fg}" stroke-width="1"/><line x1="0" y1="780" x2="1920" y2="780" stroke="{fg}" stroke-width="1"/></g><path d="M 0 560 L 700 560 L 760 380 L 820 760 L 880 560 L 1300 540 L 1360 620 L 1420 500 L 1480 560 L 1920 560" fill="none" stroke="{ac}" stroke-width="4"/>',
    "blueprint": '<rect x="240" y="180" width="1440" height="720" fill="none" stroke="{ac}" stroke-width="2" opacity="0.5"/><line x1="240" y1="540" x2="1680" y2="540" stroke="{ac}" stroke-width="1" stroke-dasharray="10 10" opacity="0.45"/><circle cx="960" cy="540" r="12" fill="{ac2}"/>',
    "ring": '<circle cx="1460" cy="560" r="300" fill="none" stroke="{ac}" stroke-width="6" opacity="0.85"/><circle cx="1460" cy="560" r="230" fill="none" stroke="{ac2}" stroke-width="3" stroke-dasharray="14 12" opacity="0.8"/><circle cx="1460" cy="560" r="14" fill="{ac2}"/>',
    "aurora": '<ellipse cx="1100" cy="360" rx="620" ry="220" fill="{ac}" opacity="0.30"/><ellipse cx="1300" cy="640" rx="560" ry="180" fill="{ac2}" opacity="0.28"/><path d="M 0 860 Q 700 740 1920 840" fill="none" stroke="{fg}" stroke-width="2" opacity="0.3"/>',
    "chalk": '<path d="M 260 300 Q 900 220 1660 320" fill="none" stroke="{fg}" stroke-width="4" opacity="0.45"/><path d="M 260 820 Q 900 760 1660 840" fill="none" stroke="{fg}" stroke-width="4" opacity="0.35"/>',
    "water": '<rect x="1240" y="240" width="480" height="560" fill="none" stroke="{fg}" stroke-width="4"/><rect x="1250" y="470" width="460" height="320" fill="{ac2}" opacity="0.28"/><rect x="1200" y="440" width="560" height="26" fill="{ac}"/>',
    "columns": '<g stroke="{fg}" stroke-width="1" opacity="0.28"><line x1="240" y1="360" x2="1680" y2="360"/><line x1="240" y1="700" x2="1680" y2="700"/><line x1="240" y1="900" x2="1680" y2="900"/><line x1="960" y1="360" x2="960" y2="900"/></g><rect x="240" y="740" width="700" height="12" fill="{ac}"/>',
    "stars": '<circle cx="1300" cy="330" r="3" fill="{fg}"/><circle cx="1450" cy="470" r="4" fill="{fg}"/><circle cx="1150" cy="620" r="3" fill="{fg}"/><circle cx="1600" cy="700" r="3" fill="{fg}"/><circle cx="1000" cy="420" r="4" fill="{fg}"/><circle cx="1400" cy="800" r="3" fill="{fg}"/><circle cx="1250" cy="560" r="150" fill="none" stroke="{ac}" stroke-width="2" stroke-dasharray="10 12"/><circle cx="1250" cy="560" r="14" fill="{ac2}"/>',
    "blob": '<ellipse cx="1180" cy="420" rx="360" ry="260" fill="{ac}" opacity="0.30"/><ellipse cx="1400" cy="640" rx="320" ry="220" fill="{ac2}" opacity="0.28"/>',
    "iso": '<g stroke="{fg}" stroke-width="3" fill="none"><path d="M 1300 300 L 1440 380 L 1300 460 L 1160 380 Z"/><path d="M 1300 460 L 1440 380 L 1440 540 L 1300 620 Z"/><path d="M 1300 460 L 1160 380 L 1160 540 L 1300 620 Z" fill="{ac}" opacity="0.22"/></g>',
    "vhs": '<g opacity="0.5"><rect x="0" y="300" width="1920" height="4" fill="{ac}"/><rect x="0" y="760" width="1920" height="4" fill="{ac2}"/></g><text x="120" y="1000" font-family="Mono" font-size="30" fill="{ac}">REC ● 00:00:30</text>',
    "cup": '<path d="M 1360 300 L 1400 780 L 1700 780 L 1740 300 Z" fill="none" stroke="{ac}" stroke-width="4"/><ellipse cx="1550" cy="300" rx="190" ry="26" fill="none" stroke="{ac}" stroke-width="4"/><rect x="1374" y="520" width="352" height="250" fill="{ac}" opacity="0.16"/><path d="M 1480 260 q -18 -40 8 -76 M 1550 244 q -18 -46 8 -86 M 1620 260 q -18 -40 8 -76" fill="none" stroke="{ac}" stroke-width="4" opacity="0.7"/>',
    "pixel": '<g><rect x="1120" y="360" width="72" height="72" fill="{ac}"/><rect x="1192" y="432" width="72" height="72" fill="{fg}"/><rect x="1264" y="360" width="72" height="72" fill="{fg}"/><rect x="1336" y="432" width="72" height="72" fill="{ac2}"/><rect x="1408" y="360" width="72" height="72" fill="{fg}" opacity="0.55"/><rect x="1480" y="432" width="72" height="72" fill="{ac}"/></g>',
    "terminal": '<rect x="960" y="260" width="820" height="420" fill="none" stroke="{ac2}" stroke-width="2"/><text x="1000" y="330" font-family="Mono" font-size="24" fill="{ac}">$ run explain</text><text x="1000" y="386" font-family="Mono" font-size="24" fill="{fg}" opacity="0.7">loading ....... ok</text><rect x="1000" y="420" width="20" height="30" fill="{ac}"/>',
    "swiss": '<circle cx="1420" cy="520" r="180" fill="none" stroke="{fg}" stroke-width="2"/><circle cx="1420" cy="520" r="18" fill="{ac2}"/><line x1="240" y1="820" x2="1680" y2="820" stroke="{fg}" stroke-width="2"/>',
    "film": '<rect x="120" y="120" width="1680" height="840" fill="none" stroke="{fg}" stroke-width="2" opacity="0.3"/><g fill="{ac2}"><rect x="140" y="180" width="18" height="26"/><rect x="140" y="300" width="18" height="26"/><rect x="140" y="420" width="18" height="26"/><rect x="140" y="540" width="18" height="26"/><rect x="140" y="660" width="18" height="26"/><rect x="1760" y="180" width="18" height="26"/><rect x="1760" y="300" width="18" height="26"/><rect x="1760" y="420" width="18" height="26"/><rect x="1760" y="540" width="18" height="26"/><rect x="1760" y="660" width="18" height="26"/></g><circle cx="960" cy="540" r="120" fill="none" stroke="{ac}" stroke-width="3" opacity="0.45"/>',
}

CSS_COMMON = '''      @font-face {{ font-family: "YH"; src: local("Microsoft YaHei"); }}
      @font-face {{ font-family: "Mono"; src: local("Consolas"); }}
      @font-face {{ font-family: "Kai"; src: local("KaiTi"); }}
      @font-face {{ font-family: "Song"; src: local("SimSun"); }}
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; background: #000; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
        background: {bg}; font-family: {fam}, sans-serif; color: {fg}; }}
      .kick {{ position: absolute; left: 96px; top: 64px; font-family: Mono; font-size: 14px; letter-spacing: 7px; color: {ac}; }}
      .idx {{ position: absolute; right: 96px; top: 64px; font-family: Mono; font-size: 12px; letter-spacing: 5px; color: {fg}; opacity: 0.42; }}
      .rule {{ position: absolute; left: 96px; right: 96px; height: 1px; background: {fg}; opacity: 0.15; }}
      .title {{ font-weight: {weight}; letter-spacing: {ls}px; line-height: 1.08; font-size: {size}px; }}
      .sub {{ font-family: Mono; font-size: 26px; letter-spacing: 3px; opacity: 0.6; }}
      .note {{ position: absolute; font-size: 22px; letter-spacing: 2px; opacity: 0.5; }}
'''

LAYOUTS = {
    "A": """
      <div class="kick">{no} · {name}</div><div class="idx">{en}</div>
      <div class="rule" style="top:150px"></div><div class="rule" style="top:980px"></div>
      <div class="title" id="t" style="position:absolute;left:96px;top:330px;width:900px">{title}</div>
      <div class="sub" id="s" style="position:absolute;left:100px;top:660px">{sub}</div>
      <div class="note" style="left:100px;bottom:70px">{note}</div>""",
    "B": """
      <div class="kick">{no} · {name}</div><div class="idx">{en}</div>
      <div class="rule" style="top:150px"></div><div class="rule" style="top:980px"></div>
      <div class="title" id="t" style="position:absolute;left:0;right:0;top:390px;text-align:center">{title}</div>
      <div class="sub" id="s" style="position:absolute;left:0;right:0;top:680px;text-align:center">{sub}</div>
      <div class="note" style="left:0;right:0;bottom:70px;text-align:center">{note}</div>""",
    "C": """
      <div class="kick">{no} · {name}</div><div class="idx">{en}</div>
      <div class="rule" style="top:150px"></div>
      <div class="title" id="t" style="position:absolute;left:96px;bottom:250px;width:1000px">{title}</div>
      <div class="sub" id="s" style="position:absolute;left:100px;bottom:190px">{sub}</div>
      <div class="note" style="left:100px;bottom:26px">{note}</div>""",
    "D": """
      <div class="kick">{no} · {name}</div><div class="idx">{en}</div>
      <div class="rule" style="top:150px"></div><div class="rule" style="top:980px"></div>
      <div class="title" id="t" style="position:absolute;right:150px;top:250px;width:130px;writing-mode:vertical-rl;letter-spacing:14px">{title}</div>
      <div class="sub" id="s" style="position:absolute;left:110px;top:300px;writing-mode:vertical-rl">{sub}</div>
      <div class="note" style="left:110px;bottom:80px">{note}</div>""",
    "E": """
      <div class="kick">{no} · {name}</div><div class="idx">{en}</div>
      <div class="title" id="t" style="position:absolute;left:96px;top:250px;width:1100px">{title}</div>
      <div class="sub" id="s" style="position:absolute;left:100px;top:640px">{sub}</div>
      <div class="note" style="left:100px;bottom:70px">{note}</div>""",
    "F": """
      <div class="kick">{no} · {name}</div><div class="idx">{en}</div>
      <div class="rule" style="top:150px"></div><div class="rule" style="top:980px"></div>
      <div class="title" id="t" style="position:absolute;left:96px;top:320px;width:820px">{title}</div>
      <div class="sub" id="s" style="position:absolute;left:100px;top:680px">{sub}</div>
      <div class="note" style="left:100px;bottom:70px">{note}</div>""",
}

TPL = '''<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <title>{no} {name}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
    <style>
{css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="style-{no}" data-width="1920" data-height="1080" data-duration="5">
{layout}
      <svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;inset:0">
        {motif}
      </svg>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.from("#t", {{ y: 30, opacity: 0, duration: 0.7, ease: "power3.out" }}, 0.1);
      tl.from("#s", {{ y: 14, opacity: 0, duration: 0.5, ease: "power2.out" }}, 0.4);
      tl.from("svg *", {{ opacity: 0, duration: 0.8, stagger: 0.05, ease: "power2.out" }}, 0.45);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["style-{no}"] = tl;
    </script>
  </body>
</html>
'''

for st in S:
    css = CSS_COMMON.format(**st)
    motif = MOTIF[st["motif"]].format(**st)
    layout = LAYOUTS[st["layout"]].format(**st)
    d = dict(st)
    d["css"] = css
    d["layout"] = layout
    d["motif"] = motif
    html = TPL.format(**d)
    io.open(os.path.join(ROOT, "%s-%s.html" % (st["no"], st["name"])), "w", encoding="utf-8", newline="").write(html)
    print("wrote", st["no"], st["name"], st["layout"])
