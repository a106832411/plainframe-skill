# plainframe-skill · 单文件版
> 这是整个技能打包成的单文件，任何模型读完即可按流程工作。
> 需要可运行样例时，再取仓库里的 `styles/` 与 `templates/`。
## 元信息
```json
{
  "name": "plainframe-skill",
  "displayName": "plainframe · 中文科普短视频技能",
  "version": "2.1.0",
  "updated": "2026-10-22",
  "entry": "SKILL.md",
  "singleFile": "dist/plainframe-all.md",
  "summary": "用代码做中文科普短视频：两条路线（口播 / 无口播），18 套风格，自带自检工具。",
  "keywords": [
    "科普短视频",
    "HyperFrames",
    "GSAP",
    "分镜",
    "TTS",
    "抖音",
    "explainer"
  ],
  "requires": {
    "node": ">=22",
    "ffmpeg": true,
    "python": [
      "numpy"
    ],
    "npm": [
      "msedge-tts（仅口播版需要）"
    ],
    "cli": [
      "hyperframes"
    ],
    "browser": "chrome-headless-shell（通过 HYPERFRAMES_BROWSER_PATH 指定）"
  },
  "install": {
    "doubao": "把整个文件夹放到工作区，让 Agent 阅读 SKILL.md",
    "deepseek": "把 SKILL.md 或 dist/plainframe-all.md 作为上下文/知识库导入",
    "workbuddy": "把文件夹放进 skills 目录，触发词：科普视频 / 分镜 / 出片",
    "qoder": "把文件夹放进项目 .qoder/skills/ 或直接 @SKILL.md",
    "generic": "任何能读文件的 Agent：读 SKILL.md 即可（单文件版见 dist/plainframe-all.md）"
  },
  "layout": {
    "SKILL.md": "主文档：工作流 + 18 套风格 + 动效引擎 + 文字排布 + 画面密度 + 两条路线 + 踩坑",
    "CHECKLIST.md": "出片前逐项检查",
    "styles/": "18 套可运行风格样例（5 秒单场景）",
    "templates/": "脚手架：骨架 / 构建 / 配音 / 混音 / 抽帧",
    "dist/plainframe-all.md": "把所有内容打成一个文件，方便一键喂给模型",
    "_tools/": "开发用脚本（生成风格、打包），使用时可忽略",
    "tools/": "beats.py（拍表→时间线）、sheet.py（抽帧联系表）、qa.py（自动自检）",
    "previews/": "18 张风格预览图",
    "MEMORY.md": "一页规则：写作、画面、踩坑、交付、命令",
    "platforms/": "四个平台的插件/组合包清单",
    "docs/插件打包.md": "组合包声明与打包命令"
  },
  "memory": "MEMORY.md",
  "howto_plugin": "平台提示「没有声明组合包」时：把 platforms/<平台>/ 下的清单复制到包根目录并按平台要求改名"
}
```
---
# plainframe-skill · 科普短视频（16:9 · 逐句动效）

> 新会话先读根目录的 `MEMORY.md`（一页规则），再读本文件。

## 这套流程解决什么

把「一段能听懂的中文口播 + 一套统一的视觉语言 + 每句话一个动作」做成 60–90 秒的横屏科普片。

产物固定三件：

| 产物 | 说明 |
|---|---|
| `项目目录/index.html` | 唯一的合成文件（HTML + GSAP 时间线） |
| `项目目录/silent.mp4` | 无声轨渲染 |
| `deliverables/<中文名>.mp4` | 混音后的成片 |

---


## 安装与「一键学习」

这个技能不依赖特定平台，只要能读文件就能用。三种接入方式，任选：

### 方式一：整包放入（推荐，豆包 / WorkBuddy / Qoder）

```
把 plainframe-skill/ 整个文件夹放进工作区或 skills 目录
让 Agent 读 SKILL.md（或直接 @SKILL.md）
```

| 平台 | 放哪里 | 触发 |
|---|---|---|
| 豆包（本地电脑模式） | 工作区任意目录 | 「按 plainframe 做一条 XX 主题」 |
| WorkBuddy | `skills/plainframe-skill/` | 同上 |
| Qoder | 项目内 `.qoder/skills/plainframe-skill/` | `@SKILL.md` |
| DeepSeek（对话） | 把 `dist/plainframe-all.md` 上传/粘贴 | 直接说主题 |

### 方式二：单文件喂给模型（最省事）

`dist/plainframe-all.md` 把主文档、检查清单、全部模板源码打成一个文件（约 50 KB）。
任何支持长上下文的模型，读这一个文件就能完整复现流程。

### 方式三：只取风格

只要 `styles/01`–`13` 里的任意一个 html，改几个 token 就是新风格；
或者读 `skill.json` 里的 `summary` 与 `layout`，让 Agent 自己定位文件。


### 作为插件 / 组合包安装

平台提示「没有声明组合包」时，用 `platforms/` 下对应的清单：

| 平台 | 清单 | 改名成 |
|---|---|---|
| 豆包 | `platforms/doubao/manifest.json` | `manifest.json` |
| WorkBuddy | `platforms/workbuddy/plugin.json` | `plugin.json` |
| Qoder | `platforms/qoder/qoder.json` | `qoder.json` |
| DSH | `platforms/dsh/skill.json` | `skill.json` |

清单里的 `bundle` 段就是「组合包声明」，列出 skill / prompt / asset / script / doc 五类成员。详见 `docs/插件打包.md`。

### 依赖自检

```bash
node -v            # ≥ 22
ffmpeg -version
npx hyperframes -v
npm i msedge-tts   # 配音
python -c "import numpy"
```
渲染前设置浏览器路径：
```powershell
$env:HYPERFRAMES_BROWSER_PATH = "<chrome-headless-shell 路径>"
```

## 一、工作流（六步，按顺序走）

### 1. 定文案（先文案，后画面）

- 一句一行，**20–24 行**，每行 8–16 字，念出来 1.8–3.7 秒；
- 逻辑必须接得上：**上句的结尾是下句的起点**，不要跳话题；
- 不用「所以你看」「记住这句话」这类说教收尾；
- 数字要具体（12 毫秒、500 毫秒、六成），不要「很快」「很多」；
- 每 3–4 行留一个「反常识」的钩子。

**自检**：把 24 行连起来读一遍，如果某两行之间需要读者自己脑补一个因果，就是断的，重写。

### 2. 分镜（10 场，一场 2–3 句）

固定 10 场，场与句的对应写进表里再动手：

| 场 | 承担的功能 |
|---|---|
| 01 | 钩子：一个具体场景 + 一个反常现象 |
| 02 | 片名：主标题 + 一句副题 |
| 03–06 | 抛出机制：两个对比、两条路径、三个通道 |
| 07–08 | 机制成立：解释回路、加速 |
| 09 | 放大器：个体差异、外部变量、数字 |
| 10 | 收尾：把开头那句话重新解释一遍 |

**每场只允许一个「主装置」**（一个圆环、一个仪表盘、一摞积木），不要堆三个图形。

### 3. 搭骨架（base.tpl）

- 每个 `<section class="f" id="sN">` 一个场景，CSS `.f{opacity:0}`；
- 场景公共层固定：`gra`（网格）、`gra2`（细网格）、`cx/cy`（中线）、`noise`、`scan`、`vig`（暗角）；
- 左上 `kick`（章节/场号）、右上 `idx`（CH 编号）、左下或右下 `ro`（技术小字）；
- 需要动效的元素先写静态终态，再加 `id`，动效只改 `opacity / transform / stroke-dashoffset`；
- **`data-duration` 先占位，由构建脚本算完总时长后回写**。

### 4. 时间线（用 python 生成，不手写）

不要手写 200 行 GSAP。写 `build.py`：读 `base.tpl` → 算每句起止 → 生成 `cut()` / 逐句动效 / `SUBS` → 写到 `index.html`。

核心：**所有时间点都从 TTS 实际时长推导**，改文案后重跑一次就自动对齐。

### 5. 配音与混音

1. `msedge-tts` 逐句生成 mp3（`zh-CN-XiaoxiaoNeural`，`rate:"-6%"`，`pitch:"-3Hz"`）；
2. ffmpeg 转 24k 单声道 wav；
3. python 逐句测有效区间（首尾静音裁掉），按时间点叠加；
4. BGM 由合成器生成（避免版权），量化到 24k 单声道；
5. 人声轨 50 ms 包络做 ducking（-35%），总限幅 0.92。

### 6. 校验与出片

```powershell
$env:HYPERFRAMES_BROWSER_PATH = "<项目>/_tools/chrome-headless-shell-win64/chrome-headless-shell.exe"
hyperframes lint                    # 必须 0 error
hyperframes render -o silent.mp4
ffmpeg -y -i silent.mp4 -i mix.wav -c:v libx264 -crf 21 -preset medium `
       -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest "deliverables/<名字>.mp4"
```

出片后**逐场抽帧检查**（每场 1 帧，加上每个动效的关键时刻 2 帧），确认没有元素提前出现、没有重影、没有文字压在字幕上。

---

## 二、风格库（18 套，选一套贯穿全片）

每套给：底色 / 主色 / 强调色 / 字体 / 图形语汇 / 动效语汇 / 适合题材。

### A. 鎏金暗场

| 项 | 值 |
|---|---|
| 底 | `#0B0908` → `#140F0B` 渐变 |
| 主色 | 金 `#DDBD74` |
| 强调 | 朱 `#D9583C` |
| 正文 | 象牙 `#E8E3D9` |
| 字体 | 宋体（标题）/ 黑体（正文） |
| 图形 | 细金线、印章方块、同心圆、刻度、纸张纹理 |
| 动效 | 金线描边、印章落下、缓慢推镜、微光呼吸 |
| 适合 | 人文、历史、定律、深时间、情绪 |

### B. 复古丝印

| 项 | 值 |
|---|---|
| 底 | 纸色 `#F0E3C8` |
| 主色 | 朱红 `#D63A2C` |
| 副色 | 靛蓝 `#184A9E` |
| 字体 | 粗黑体，字号大、字距紧 |
| 图形 | 套色错位、网点、粗描边、票据边框 |
| 动效 | 硬切、压印位移、颜色叠印、抖动 |
| 适合 | 观点、社会现象、反常识、需要力量感的题材 |

### C. 示波器（本片用的就是这套）

| 项 | 值 |
|---|---|
| 底 | `#030C0A` |
| 主色 | 薄荷 `#5FE8C8` |
| 强调 | 琥珀 `#FFB347` |
| 弱色 | `#6E9A90` |
| 字体 | Consolas / 等宽，中文用思源黑 |
| 图形 | 400px 网格、20px 细网格、扫描线、暗角、等宽标签 |
| 动效 | 波形描出、光点沿路径、计数器、扫描线、指针摆动 |
| 适合 | 生理机制、时间尺度、实验数据、因果链 |

### D. 蓝图

| 项 | 值 |
|---|---|
| 底 | `#0A1A2E` |
| 线 | `#6FA8DC` |
| 文字 | `#E6F1FF` |
| 字体 | 等宽 + 细黑体 |
| 图形 | 40px 坐标网格、虚线尺寸标注、剖面线、图签框 |
| 动效 | 线条逐段绘制、尺寸标注弹出、图纸平移 |
| 适合 | 结构、装置、流程、工程类解释 |

### E. 霓虹

| 项 | 值 |
|---|---|
| 底 | `#07040C` |
| 主色 | 品红 `#FF3D8B` |
| 副色 | 青 `#38E8FF`、紫 `#A06BFF` |
| 字体 | 粗黑体 + 等宽混排 |
| 图形 | 发光描边、故障切片、噪点、扫描带 |
| 动效 | 闪、抖、RGB 错位、光晕脉冲 |
| 适合 | 强节奏、年轻向、网络现象 |

### F. 极光

| 项 | 值 |
|---|---|
| 底 | `#04080F` |
| 主色 | 青绿 `#46E0C0` |
| 副色 | 紫 `#7C6BFF` |
| 字体 | 细黑体，字距宽 |
| 图形 | 大面积渐变、柔光球、粒子、极细线 |
| 动效 | 渐变流动、景深推移、粒子飘移 |
| 适合 | 抽象概念、宇宙、心理、冥想感题材 |

### G. 黑板粉笔

| 项 | 值 |
|---|---|
| 底 | 板绿 `#1E2A24`（中心略亮，四周压暗） |
| 主色 | 粉笔白 `#EDEDE3` |
| 强调 | 粉笔黄 `#F2C14E` |
| 字体 | **楷体**（KaiTi / STKaiti），正文可用等宽 |
| 图形 | 手画圈、下划线、箭头、粉笔灰、板擦痕、粉笔槽 |
| 动效 | 逐笔写出（clip 横向擦）、描线、轻微手抖 |
| 适合 | 推导、教学、汉字/语言、需要「有人在你面前写」的题材 |

粗糙边缘的做法：给文字/线条套一个 SVG 滤镜
`feTurbulence(fractalNoise, 0.9) + feDisplacementMap(scale 2.6)`，
粉笔的颗粒感就出来了，不需要贴图。

**选风格的口径**：题材决定风格，不要反过来。机制/数据 → C 或 D；人文/历史 → A 或 B；抽象/氛围 → F；年轻/网络 → E。

---

### 补充风格（H–R）

| 编号 | 名称 | 底 / 主 / 强调 | 母题 | 适合 |
|---|---|---|---|---|
| H | 暗场几何 | `#12100E` / `#EFE6D6` / `#C98553` + `#5B8FBF` | 容器、水面、盖板 | 机制、隐喻、连续过程 |
| I | 报纸黑白 | `#F4F1EA` / `#15130F` / `#B03A2E` | 分栏、粗标题、柱状 | 调查、事实、社会议题 |
| J | 深空星图 | `#05070E` / `#DCE8FF` / `#4D8CFF` + `#FF7A3D` | 星点、轨道、尺度标尺 | 宇宙、时间、概率 |
| K | 手绘水彩 | `#FBF8F1` / `#3A3A3A` / `#C98A5B` + `#7FA8C9` | 晕染色块、纸纹 | 自然、生物、生长 |
| L | 等距白模 | `#ECEAE4` / `#1F2A33` / `#E07A3F` | 30° 轴测方块 | 原理、装置、流程 |
| M | 复古录像 | `#0B0B0B` / `#F5F5F0` / `#38E8FF` + `#FF6A3D` | 扫描线、时间码、色差 | 影像、记忆、往事 |
| N | 冰窟蓝 | `#08121A` / `#DCEBF5` / `#F2A65A` + `#7FD3E8` | 冷容器、温度曲线、冰层 | 冷、实验、时间尺度 |
| O | 像素 8bit | `#101018` / `#E8E8F0` / `#FFD23F` + `#3FBF8F` | 方块像素、有限色板 | 游戏、算法 |
| P | 终端绿 | `#070B07` / `#8CFF7A` / `#C8FF3D` | 磷光绿、光标 | 代码、协议 |
| Q | 极简白 | `#FAFAF7` / `#111111` / `#E03E36` | 白底黑字、细线 | 概念、定义 |
| R | 胶片棕 | `#171008` / `#EADCC0` / `#D89B5A` | 颗粒、齿孔 | 人物、档案 |

样例见 `styles/01`–`18`。18 套不是同一版式换色：分六种构图骨架（A 左文右图 / B 居中 / C 底文 / D 竖排 / E 全屏图形 / F 分栏），每套有自己的母题和示例文案。新增风格改 `_tools/gen_styles.py` 里的一条配置即可。

## 三、逐句动效引擎（关键代码）

普通淡入观众感知不到。**每句台词必须对应一个可见动作**，动作幅度要大到能看出来。

```js
// 转场：不看黑，交叉溶解
function cut(a, b, t) {
  tl.to("#" + a, { opacity: 0, duration: 0.26, ease: "power2.inOut" }, t - 0.32);
  tl.to("#" + b, { opacity: 1, duration: 0.26, ease: "power2.inOut" }, t - 0.20);
}

// 描线：用于波形、路径、坐标系
function drawIn(sel, t, dur) {
  const el = document.querySelector(sel);
  if (!el) return;
  const L = el.getTotalLength ? el.getTotalLength() : 800;
  el.style.strokeDasharray = L;
  el.style.strokeDashoffset = L;
  tl.to(el, { strokeDashoffset: 0, duration: dur, ease: "power2.out" }, t);
}

// 计数：0 → N，用于 12ms / 500ms / +60%
function countUp(sel, to, dur, at, prefix) {
  const el = document.querySelector(sel);
  if (!el) return;
  const obj = { v: 0 };
  tl.to(obj, { v: to, duration: dur, ease: "power2.out", onUpdate: () => {
    el.firstChild.textContent = (prefix || "") + Math.round(obj.v);
  } }, at);
}
```

**五类可用的「一个动作」**（每句挑一个，不要重复连用）：

| 类型 | 做法 | 适合 |
|---|---|---|
| 描出 | 路径 `stroke-dashoffset` 归零 | 波形、路线、时间条 |
| 冲出 | 光点/彗星沿路径 0.3–1.5s 掠过 | 信号、快慢对比 |
| 砸入 | `scale 1.6 → 1` + `blur` + 帧闪 | 数字、关键判断 |
| 生长 | `attr width/height` 从 0 到终值 | 条状图、比例 |
| 转起来 | `rotation` + `ease:"power3.in"` | 环、指针、表盘 |

**节奏规则**：句子开始前 0.05–0.1 秒触发动作；动作时长 = 该句时长的 30–60%；不要每句都从头淡入。

---



## 四、文字与衔接（踩过坑的规则）

**1. 逐句文字，不是逐场文字**
一场 2–4 句解说时，画面上的字必须跟着句子换，否则会出现「声音在讲第 4 句、屏幕还挂着第 1 句」。
做法：`lines` 里每句一条 `<div id="L{n}">`，在第 n 句开始时淡入，下一句开口前 0.05 秒淡出。

**2. 大字与字幕不重复**
画面已有同义大字 → 该句不出底部字幕（`nosub`）。

**3. 文字安全区**
- 左栏：x 100–900，垂直居中
- 顶栏：y 130 起，横贯全宽
- **图形左边界 ≥ 960**，否则左侧文字必压图

**4. 自动字号**
| 字数 | 字号 |
|---|---|
| ≤ 8 | 76px |
| 9–11 | 64px |
| ≥ 12 | 54px |

固定字号会导致长句折行、短句太空。

**5. 场景衔接：先出后进**
```
旧场淡出 0.18s，结束在切点前 0.02s
新场淡入 0.20s，从切点后 0.01s 开始
```
留 0.03 秒空档，避免两场同时半透明（双重残影）。

**6. 场内动画延后**
水位、盖板、指针这类"有因果"的动画，等画面亮起来再开始（切点后 0.4–0.5 秒），
不要和淡入同时跑，否则观众看不清它从哪开始。

**7. `fromTo` 的 from 值会提前生效**
`tl.fromTo(el, { opacity: 1, ... })` 在初始化时就把元素设成可见，
会出现"本该第 33 秒出现的光圈，从第 0 秒就挂在那"。
解法：`tl.set(el, {...}, t)` + `tl.to(...)`，或用 `display:none` 门控。

## 五、文字去重规则（重要）

同一句话不要同时出现在**画面大字**和**底部字幕**里——观众会读两遍，节奏就断了。

做法：`lines.json` 里给这句加 `"nosub": true`，`build.py` 生成字幕时跳过它。

```json
{ "n": 3, "scene": 2, "text": "不是尴尬，是默契。", "nosub": true }
```

判断标准：

| 情况 | 处理 |
|---|---|
| 画面上有与台词同义的大字 | 只留大字，**不出字幕** |
| 画面上只有图形、坐标轴、标签 | 大字 + 字幕都给（方便静音观看） |
| 数字、印章、轴标签 | 永远不参与去重 |

**安全区**：底部 140px 内不要放任何图形文字。字幕在 `bottom: 44px`、字号 33px，
大约占 44–90px 这一带；图表标签、注释落到这个区间就会和字幕糊在一起。

## 六、时间线骨架（build.py 的产物形态）

```js
const tl = gsap.timeline({ paused: true });
tl.set("#s1", { opacity: 1 }, 0);
cut("s1", "s2", 6.68);
cut("s2", "s3", 8.30);
// …
drawIn("#p4", 13.70, 0.4);
countUp("#ms4", 12, 0.6, 13.75);
tl.fromTo("#sp1", { scale: 0 }, { scale: 1, duration: 0.35, ease: "back.out(4)" }, 13.75);

const SUBS = [[0.60, 4.10, "第一句"], /* … */];
const sub = document.getElementById("sub");
SUBS.forEach(([a, b, txt]) => {
  tl.call(() => { sub.textContent = txt; }, null, a);
  tl.fromTo(sub, { opacity: 0 }, { opacity: 1, duration: 0.2 }, a);
  tl.to(sub, { opacity: 0, duration: 0.16 }, b - 0.16);
});

window.__timelines["<composition-id>"] = tl;
```

构建脚本要点（python）：

```python
GAP = 0.5           # 句间停顿
START = 0.6         # 首句延后
TAIL = 2.4          # 片尾留白
# 每句有效时长 = 首尾静音裁掉后的长度
# 总时长写回 data-duration，再生成 SUBS 与 cut() 时间点
```

---

## 七、声音（口播 / 无口播）

**口播版**：`gen_tts.mjs` 逐句配音 → `mix.py` 叠人声 + BGM 自动闪避（−35%）。
**无口播版**：跳过配音，`build.py --novoice` 按字数估时长，`mix.py` 只出 BGM（0.8 秒淡入淡出）。
两者混音都能跑，区别只在 `offsets.json` 里有没有 `"novoice": true`。

原「配音与混音」细节：

```js
// gen_tts.mjs
import { MsEdgeTTS, OUTPUT_FORMAT } from "msedge-tts";
const tts = new MsEdgeTTS({ connectionTimeoutMs: 20000, synthesisTimeoutMs: 90000 });
await tts.setMetadata("zh-CN-XiaoxiaoNeural", OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);
await tts.toFile(dir, text, { rate: "-6%", pitch: "-3Hz" });
```

```python
# mix.py 关键：裁剪 + 归一 + 叠加 + ducking
idx = np.where(np.abs(x) > 0.0035)[0]
x = x[max(0, idx[0]-0.04*SR) : idx[-1]+0.11*SR]
x = x / (np.max(np.abs(x)) or 1) * 0.86
buf[i0:i0+len(x)] += x
duck = 1.0 - 0.35 * np.clip(env / (env.max()) * 6, 0, 1)
mix = voice + bg * 0.26 * duck
```

**混音三条经验**：句间 0.5 秒最自然；BGM 电平 -26 dB 左右；尾音必须做 1 秒淡出。

---

## 八、踩坑清单（都实际踩过）

| 现象 | 原因 | 解法 |
|---|---|---|
| `ValueError: unsupported format character` | python `%` 格式化遇到 JS 里的 `100%`、`50% 50%` | 字符串拼接或 `%%`；别用 `%` 拼 JS |
| SVG 元素飞出画面 | 用了 `transformOrigin`（按 CSS 盒子算） | SVG 一律用 `svgOrigin: "cx cy"` |
| 元素提前出现 | 只做了 `fromTo`，元素本身没隐藏 | 默认 `display:none` / `opacity:0`，到点用 `tl.set(display:"inline")` 开门 |
| `fromTo` 互相覆盖 | `immediateRender` 会提前写状态 | 同一元素只写一次 `fromTo`，其余用 `set` + `to` |
| 渲染报 `Permission denied` | 成片被播放器占用 | 换文件名输出 |
| lint 报多入口 | 目录里有两个 `data-composition-id` 的 html | 模板改名 `base.tpl`，只留 `index.html` |
| 中文字幕重复/缺失 | 字幕层没插入或文案与画面重复 | 字幕层统一由 `SUBS` 生成；大标题已表达的内容不再上字幕 |
| 成片声音是上一条的 | 混音脚本复用了旧项目的音频目录（`_tts` vs `_tts2`） | 每条片子独立音频目录；`mix.py` 已内置「音频长度超过时间槽」的报错 |
| 时间轴对、声音错 | 画面按 A 的时长排、音频混的是 B 的文件 | 看混音日志：`max gap` 应≈设定的句间停顿，异常就是文件错了 |
| 光圈/元素“从第 0 秒就在” | `fromTo` 的 from 值在初始化就生效 | 用 `set` + `to`，或先 `display:none` 再开门 |
| 两场同时半透明（双重残影） | 淡出与淡入时间重叠 | 先出后进，中间留 0.03s 空档 |
| 文字压住图形 | 只改了文字宽度、没改图形坐标 | 图形左边界 ≥ 960；横贯画面的场把文字挪到顶栏 |
| 长句折行、短句太空 | 固定字号 | 按字数自动选 76/64/54px |
| python 读中文路径乱码 | 脚本按 ANSI 读 UTF-8 | 用 DSH 运行时自带的 python 执行 |

---

## 九、目录结构

```
项目名/
  base.tpl          # 场景结构（不含时间线）
  build.py          # 生成 index.html（时间线 + 字幕 + 总时长）
  index.html        # 产物，唯一入口
  silent.mp4        # 无声渲染
  mix.wav           # 混音轨
  bgm.wav / bgm_24k.wav
  synth_bgm.py      # BGM 生成
  render.log
deliverables/
  中文名.mp4
_tts2/
  <项目>/e01/audio.wav … e24/audio.wav
  gen_tts.mjs
  mix_<项目>.py
```

---

## 十、交付习惯

发布相关：标题 ≤40 字、`Vibe知识大赏｜` 开头；话题 = 大赏 + 领域 + 具体词；封面出 16:9 与 3:4 两张，规则见 `docs/封面与标题.md`，模板见 `templates/cover-16x9.html` / `cover-3x4.html`。

- 成片放 `deliverables/`，文件名用中文描述（如 `情绪为什么失控-章节版.mp4`）；
- 汇报时给：时长、体积、章节表、逐场动作表；
- 主动说清**这版哪里还不理想**，不要假装完美；
- 改一处动效后，必须重新抽帧确认相邻场景没被带坏（元素共用 id 很容易串）。

## 十一、画面密度与自检（借鉴 Vibe 知识大赏）

详见 `docs/参考-Vibe知识大赏.md`。四条能直接用的：

**1. 相邻 2 秒必须有可见变化**
随便截相差 2 秒的两帧，完全一样就是错的。
长句（>4 秒）配持续运动：水位、指针、粒子、计数。

**2. 转场从内容里长出来**
不允许默认淡入淡出、不允许所有元素同时入场。
底线是「先出后进 + 0.03 秒空档」；再上一步是让画面元素本身变成转场。

**3. 主体要叫得出日常名字**
「一串珠子」「中间凹下去的红细胞」可以；「点、线、圈、方框」不行。
自查三问：主体叫什么 / 它的动词在屏上做了吗 / 换个文案这个主体还成立吗（成立就是配图，不是讲解）。

**4. 每五句留一句「不画」**
提问、命名、结论、引文，让画面停住，只留文字和背景微动。
每句都换图，观众没有时间想。

### 出片六维自检（低于 8 分就改）

前 2 秒抓人 / 手机缩放可读 / 动作自然无空拍 / 每 2–4 秒有新东西 / 构图与文字区干净 / 声画对位。
我们额外加两条：文字不压图形、同一句不重复出现两次。

## 十二、两条路线（选一条，不要混）

| | A 口播版 | B 无口播版 |
|---|---|---|
| 文案 | 说出来的话，20–30 句 | 读的字幕，30–45 句，一句 ≤14 字 |
| 时长来源 | 音频实测 | 字数 ÷ 4.2 字/秒，或**拍表** |
| 节奏锚点 | 句子 | 拍（BPM） |
| 音频 | 人声 + BGM 闪避 | 只有 BGM，首尾淡入淡出 |
| 结构 | 钩子 → 解释 → 收尾 | 钩子 → 片名卡 → 案例 → 机制 → **预测题** → 揭晓 → 金句 → 说明卡 |
| 命令 | `python build.py ./_tts .` | `python build.py . . --novoice` |

拍表路线先跑 `tools/beats.py` 把 `beats.json` 换成时间线，再交给 `build.py`。

### 三个工具

| 工具 | 作用 | 用法 |
|---|---|---|
| `tools/beats.py` | 拍表 → 时间线（画面/字幕/转场读同一张表） | `python beats.py beats.json --bpm 100` |
| `tools/sheet.py` | 按时间点抽帧拼联系表 | `python sheet.py out.mp4 --even 12` |
| `tools/qa.py` | 自动自检：规格 / 静止段 / 黑屏 / 音轨 | `python qa.py out.mp4` |

`qa.py` 会直接报出「静止超过 2 秒」的时间点——对应第十一节的画面密度规则。

---

## 附录 A · 出片检查清单
# 出片检查清单

按顺序勾，任何一项不过就别发。

## 一、文案

- [ ] 每行 8–16 字，念出来 1.8–3.7 秒
- [ ] 相邻两句之间不需要观众自己补因果
- [ ] 没有「所以你看」「记住这句话」这类说教
- [ ] 数字具体（12 毫秒 / 六成），不是「很快」「很多」
- [ ] 最后一句回扣开头那句话

## 二、分镜

- [ ] 10 场，每场 2–3 句
- [ ] 每场只有一个主装置（一个圆、一个表、一摞积木）
- [ ] 每场的主体在画面里占 1/3 以上，观众不用找

## 三、动效

- [ ] 每句台词都有一个可见动作（不是只有淡入）
- [ ] 同一套动作没有连续用 3 次以上
- [ ] 数字类元素真的在跳（0 → 目标值）
- [ ] 环/表盘/指针在转，不是静止
- [ ] 没有元素提前出现（用 `display:none` 门控）
- [ ] 没有元素飞出画面（SVG 用 `svgOrigin`）

## 四、声音

- [ ] 第一句语音属于本条片子（不是上一条的残留）
- [ ] 句间停顿 0.5 秒左右
- [ ] 没有人声被 BGM 压住
- [ ] 尾音有 1 秒淡出
- [ ] 首句不在 0 秒就开始（留 0.6 秒）

## 五、画面

- [ ] 字幕不压主体图形
- [ ] 同一句话没有被大字和字幕重复两遍（用 `nosub`）
- [ ] 底部 140px 内没有图形文字
- [ ] 暗场没有死黑，亮部没有过曝
- [ ] 中文字体在 1080p 上不虚（用系统字体，不用 Google Fonts 中文）

## 六、技术

- [ ] `hyperframes lint` 0 error
- [ ] `data-duration` 与实际时长一致
- [ ] 目录里只有一个 `index.html`（模板改名 `base.tpl`）
- [ ] 出片后逐场抽帧看过

## 七、发布

- [ ] 标题 ≤40 字（含 `Vibe知识大赏｜` 前缀），前 12 字有信息
- [ ] 标签 3 个（大/中/精准各一，大赏标签固定）
- [ ] 封面大字和标题不重复
- [ ] 封面出了两张：16:9（1920×1080）与 3:4（1080×1440）
- [ ] 两张封面的标题、副题、标签一致，只换版式
- [ ] 封面放在工程 `发布/`，没有混进 `成品/`
- [ ] 置顶评论补一个数据或一个反问

## 八、画面密度（借鉴 Vibe 知识大赏）

- [ ] 任意相隔 2 秒的两帧，画面有可见变化
- [ ] 没有超过 4 秒的静止画面
- [ ] 转场不是纯淡入淡出（至少有元素级变化）
- [ ] 每场主体叫得出日常名字（不是点线框）
- [ ] 约 1/5 的句子「不画」，让画面停住
- [ ] 文字不压图形、同一句不重复出现

## 九、六维自检

- [ ] 前 2 秒抓人
- [ ] 缩到 1/4 仍可读
- [ ] 无匀速滑动 / 无空拍
- [ ] 每 2–4 秒有新东西
- [ ] 构图干净、字幕区无遮挡
- [ ] 说到哪个词，画面在动哪个东西

---

## 附录 B · 模板源码

### templates/base.tpl

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>__ID__</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      /* 骨架默认用「示波器」风格；换风格时只改这一段色值 + 字体 */
      @font-face { font-family: "YH"; src: local("Microsoft YaHei"); }
      @font-face { font-family: "Mono"; src: local("Consolas"); }
      * { box-sizing: border-box; }
      html, body { margin: 0; background: #000; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden;
        background: #030C0A; font-family: YH, sans-serif; color: #E6FFFA; }
      .f { position: absolute; inset: 0; opacity: 0; overflow: hidden; }
      .gra { position: absolute; inset: 0;
        background-image: linear-gradient(rgba(95,232,200,0.085) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(95,232,200,0.085) 1px, transparent 1px);
        background-size: 400px 400px; }
      .gra2 { position: absolute; inset: 0;
        background-image: linear-gradient(rgba(95,232,200,0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(95,232,200,0.03) 1px, transparent 1px);
        background-size: 20px 20px; }
      .scan { position: absolute; inset: 0; opacity: 0.55; mix-blend-mode: multiply;
        background: repeating-linear-gradient(to bottom, rgba(0,0,0,0.22) 0 1px, transparent 1px 3px); }
      .noise { position: absolute; inset: 0; opacity: 0.35;
        background-image: radial-gradient(rgba(230,255,250,0.05) 1px, transparent 1px); background-size: 3px 3px; }
      .vig { position: absolute; inset: 0;
        background: radial-gradient(ellipse at 50% 50%, transparent 26%, rgba(0,8,6,0.9) 100%); }
      .cx { position: absolute; left: 0; right: 0; top: 50%; height: 1px; background: rgba(95,232,200,0.10); }
      .cy { position: absolute; top: 0; bottom: 0; left: 50%; width: 1px; background: rgba(95,232,200,0.10); }
      .kick { position: absolute; left: 88px; top: 48px; font-family: Mono; font-size: 13px;
        letter-spacing: 6px; color: #5FE8C8; }
      .idx { position: absolute; right: 88px; top: 48px; font-family: Mono; font-size: 12px;
        letter-spacing: 5px; color: rgba(95,232,200,0.45); }
      .ro { position: absolute; left: 88px; bottom: 52px; font-family: Mono; font-size: 12px;
        letter-spacing: 3px; color: rgba(95,232,200,0.5); }
      .h { font-weight: 900; letter-spacing: -3px; line-height: 1.06; }
      .mono { font-family: Mono; letter-spacing: 3px; }
      .amber { color: #FFB347; }
      .dim { color: #6E9A90; }
      .glow { filter: drop-shadow(0 0 10px rgba(95,232,200,0.65)) drop-shadow(0 0 30px rgba(95,232,200,0.28)); }
      .glowA { filter: drop-shadow(0 0 10px rgba(255,179,71,0.6)); }
      /* 逐句揭示：默认隐藏，由 build.py 在对应句开始时点亮 */
      .ln { opacity: 0; transform: translateY(16px); }
      .draw { stroke-dasharray: 3000; stroke-dashoffset: 3000; }
      #sub { position: absolute; left: 150px; right: 150px; bottom: 44px; text-align: center;
        font-size: 33px; letter-spacing: 2px; color: #DFFFF7; opacity: 0; z-index: 99;
        text-shadow: 0 0 24px rgba(3,12,10,0.95), 0 2px 10px rgba(3,12,10,0.9); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="__ID__" data-width="1920" data-height="1080" data-duration="__DURATION__">

      <!-- 01 钩子 -->
      <section class="f" id="s1">
        <div class="gra"></div><div class="gra2"></div><div class="cx"></div><div class="cy"></div>
        <div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">01 / 钩子</div><div class="idx">CH1 · 01</div>
        <div class="ro">SAMPLE 240 Hz</div>
        <svg width="1800" height="400" viewBox="0 0 1800 400" style="position:absolute;left:60px;top:290px">
          <path class="draw ln1" d="M 0 200 L 300 200 L 340 132 L 380 268 L 420 200 L 760 200 L 800 168 L 840 232 L 880 200 L 1200 200 L 1240 84 L 1280 324 L 1320 200 L 1800 200"
                fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
        </svg>
        <div style="position:absolute;left:88px;top:700px">
          <div class="h ln ln1" style="font-size:100px">第一句的画面文字</div>
          <div class="h ln ln2" style="font-size:100px;color:#FFB347;margin-top:4px">第二句的画面文字</div>
        </div>
      </section>

      <!-- 02 片名 -->
      <section class="f" id="s2">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div style="position:absolute;left:0;right:0;top:300px;text-align:center">
          <div class="h ln ln3" style="font-size:132px">片名第一行</div>
          <div class="h ln ln3 glow" style="font-size:132px;color:#5FE8C8;margin-top:4px">片名第二行</div>
        </div>
      </section>

      <!-- 03 对比 -->
      <section class="f" id="s3">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">02 / 对比</div>
        <div style="position:absolute;left:96px;top:230px;width:560px">
          <div class="h ln ln4" style="font-size:72px">第四句</div>
          <div class="h ln ln5" style="font-size:72px;color:#FFB347;margin-top:2px">第五句</div>
        </div>
        <svg width="1120" height="520" viewBox="0 0 1120 520" style="position:absolute;left:720px;top:300px">
          <rect class="ln ln4" x="60" y="106" width="180" height="40" fill="rgba(95,232,200,0.28)" stroke="#5FE8C8" stroke-width="2" />
          <rect class="ln ln5" x="60" y="286" width="620" height="40" fill="rgba(255,179,71,0.18)" stroke="#FFB347" stroke-width="2" />
        </svg>
      </section>

      <!-- 04 快路 -->
      <section class="f" id="s4">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">03 / 快路</div>
        <div style="position:absolute;left:88px;top:260px;width:560px">
          <div class="h ln ln6" style="font-size:84px">第六句</div>
          <div class="mono amber ln ln7" style="font-size:110px;margin-top:30px">12<span style="font-size:38px">ms</span></div>
          <div class="mono dim ln ln8" style="margin-top:12px;font-size:14px">第八句的注释</div>
        </div>
        <svg width="1000" height="480" viewBox="0 0 1000 480" style="position:absolute;left:820px;top:360px">
          <path class="draw ln6" d="M 100 250 L 840 230" fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
          <circle class="ln ln6" cx="100" cy="250" r="26" fill="#030C0A" stroke="#5FE8C8" stroke-width="2" />
          <circle class="ln ln7" cx="840" cy="230" r="28" fill="none" stroke="#FFB347" stroke-width="2" class="glowA" />
        </svg>
      </section>

      <!-- 05 慢路 -->
      <section class="f" id="s5">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">04 / 慢路</div>
        <div style="position:absolute;left:88px;top:250px;width:560px">
          <div class="h ln ln9" style="font-size:84px">第九句</div>
          <div class="mono ln ln10" style="font-size:110px;margin-top:34px">≈500<span style="font-size:38px">ms</span></div>
          <div class="mono dim ln ln11" style="margin-top:12px;font-size:14px">第十一句的注释</div>
        </div>
        <svg width="1000" height="480" viewBox="0 0 1000 480" style="position:absolute;left:820px;top:340px">
          <path class="draw ln9" d="M 100 250 Q 340 40 660 110 Q 800 150 840 220" fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
        </svg>
      </section>

      <!-- 06 三条通道 -->
      <section class="f" id="s6">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">05 / 身体</div>
        <div style="position:absolute;left:96px;top:250px;width:520px">
          <div class="h ln ln12" style="font-size:74px">第十二句</div>
          <div class="h ln ln13" style="font-size:74px;margin-top:2px">第十三句</div>
          <div class="h ln ln14" style="font-size:56px;color:#5FE8C8;margin-top:18px">第十四句</div>
        </div>
        <svg width="1080" height="560" viewBox="0 0 1080 560" style="position:absolute;left:760px;top:300px">
          <path class="draw ln12" d="M 200 110 L 360 110 L 380 50 L 400 170 L 420 110 L 620 110 L 640 60 L 660 160 L 680 110 L 1070 110"
                fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
          <path class="draw ln13" d="M 200 290 Q 330 220 460 290 Q 590 360 720 290 Q 850 220 980 290"
                fill="none" stroke="rgba(95,232,200,0.75)" stroke-width="2.5" />
          <path class="draw ln14" d="M 200 470 L 420 470 L 440 420 L 460 510 L 480 470 L 760 470 L 780 430 L 800 505 L 820 470 L 1070 470"
                fill="none" stroke="rgba(255,179,71,0.9)" stroke-width="2.5" class="glowA" />
        </svg>
      </section>

      <!-- 07 解释 -->
      <section class="f" id="s7">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">06 / 解释</div>
        <div style="position:absolute;left:96px;top:250px;width:500px">
          <div class="h ln ln15" style="font-size:70px">第十五句</div>
        </div>
        <svg width="1080" height="560" viewBox="0 0 1080 560" style="position:absolute;left:720px;top:280px">
          <rect class="ln ln16" x="40" y="40" width="640" height="120" fill="rgba(255,179,71,0.06)" stroke="#FFB347" stroke-width="3" />
          <text class="ln ln16" x="70" y="116" fill="#FFB347" font-size="46" font-weight="700">第十六句</text>
        </svg>
      </section>

      <!-- 08 循环 -->
      <section class="f" id="s8">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">07 / 循环</div>
        <div style="position:absolute;left:96px;top:250px;width:520px">
          <div class="h ln ln17" style="font-size:78px">第十七句</div>
          <div class="h ln ln18" style="font-size:78px;margin-top:2px">第十八句</div>
          <div class="h ln ln19" style="font-size:56px;color:#FFB347;margin-top:16px">第十九句</div>
        </div>
        <svg width="900" height="620" viewBox="0 0 900 620" style="position:absolute;left:880px;top:230px">
          <circle class="ln ln17" cx="430" cy="310" r="210" fill="none" stroke="#5FE8C8" stroke-width="4"
                  stroke-dasharray="440 880" transform="rotate(-90 430 310)" class="glow" />
        </svg>
      </section>

      <!-- 09 放大器 -->
      <section class="f" id="s9">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">08 / 放大器</div>
        <div style="position:absolute;left:96px;top:230px;width:520px">
          <div class="h ln ln20" style="font-size:62px">第二十句</div>
          <div class="mono amber ln ln21" style="font-size:96px;margin-top:24px">+60<span style="font-size:38px">%</span></div>
          <div class="mono dim ln ln21" style="margin-top:12px;font-size:15px">第二十一句的注记</div>
          <div class="mono dim ln ln22" style="margin-top:8px;font-size:15px">第二十二句的注记</div>
        </div>
      </section>

      <!-- 10 收尾 -->
      <section class="f" id="s10">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">09 / 收尾</div>
        <div style="position:absolute;left:96px;top:250px;width:580px">
          <div class="h ln ln23" style="font-size:62px">第二十三句</div>
          <div class="h ln ln24" style="font-size:62px;color:#5FE8C8;margin-top:2px">第二十四句</div>
        </div>
      </section>

      <div id="sub"></div>
    </div>

    <script>
      /*__TIMELINE__*/
    </script>
  </body>
</html>

```

### templates/build.py

```python
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
    js.append('tl.to(".ln%d", { opacity: 1, duration: 0.42, stagger: 0.07, ease: "power2.out" }, %s);'
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

```

### templates/check_frames.ps1

```powershell
# 逐场抽帧检查
# 用法： .\check_frames.ps1 -Video deliverables\成片.mp4 -Out frames
param(
  [string]$Video = "silent.mp4",
  [string]$Out = "frames",
  [double]$Step = 6.5
)

New-Item -ItemType Directory -Force -Path $Out | Out-Null
$dur = [double](ffprobe -v error -show_entries format=duration -of csv=p=0 $Video)
$t = 1.0
$i = 0
while ($t -lt $dur - 0.3) {
  $i++
  $f = Join-Path $Out ("f{0:D2}_{1:N1}.jpg" -f $i, $t)
  ffmpeg -y -loglevel error -ss $t -i $Video -frames:v 1 -q:v 2 $f
  $t += $Step
}
Write-Output "duration=$dur frames=$i out=$Out"

```

### templates/cover-16x9.html

```
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <style>
      @font-face { font-family: "YH"; src: local("Microsoft YaHei"); }
      @font-face { font-family: "Mono"; src: local("Consolas"); }
      * { box-sizing: border-box; margin: 0; padding: 0; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #05070E; }
      #c { position: relative; width: 1920px; height: 1080px; overflow: hidden;
        background: linear-gradient(180deg,#05070E 0%,#0A1430 30%,#2A1F4A 52%,#7A3020 74%,#D0653A 90%,#F2A65A 100%);
        font-family: YH, sans-serif; color: #EAF2FF; }
      .grain { position: absolute; inset: 0; opacity: 0.35;
        background-image: radial-gradient(rgba(220,232,255,0.05) 1px, transparent 1px); background-size: 3px 3px; }
      .vig { position: absolute; inset: 0;
        background: radial-gradient(ellipse at 46% 45%, transparent 42%, rgba(0,0,0,0.55) 100%); }
      .top { position: absolute; left: 96px; top: 64px; font-family: Mono; font-size: 22px;
        letter-spacing: 8px; color: #4D8CFF; }
      .no { position: absolute; right: 96px; top: 64px; font-family: Mono; font-size: 20px;
        letter-spacing: 6px; color: rgba(234,242,255,0.45); }
      h1 { position: absolute; left: 96px; top: 250px; font-size: 112px; font-weight: 900;
        line-height: 1.14; letter-spacing: -3px; }
      h1 .b { color: #7FB6FF; }
      h1 .o { color: #FFB27A; }
      .sub { position: absolute; left: 100px; top: 560px; font-size: 40px; letter-spacing: 1px;
        color: rgba(234,242,255,0.85); }
      .tag { position: absolute; left: 98px; top: 634px; display: inline-block; padding: 12px 24px;
        border: 2px solid rgba(255,178,122,0.7); border-radius: 8px; font-size: 30px;
        letter-spacing: 2px; color: #FFB27A; }
      .line { position: absolute; left: 0; right: 0; top: 880px; height: 1px;
        background: rgba(255,217,160,0.35); }
      .sun { position: absolute; left: 1400px; top: 750px; width: 260px; height: 130px;
        border-radius: 260px 260px 0 0; background: #FFD9A0;
        box-shadow: 0 0 90px rgba(255,180,110,0.5); }
      .foot { position: absolute; left: 98px; bottom: 52px; font-family: Mono; font-size: 22px;
        letter-spacing: 5px; color: rgba(234,242,255,0.55); }
    </style>
  </head>
  <body>
    <div id="c">
      <div class="grain"></div><div class="vig"></div>
      <div class="top">SKY · 79s</div>
      <div class="no">大气 · 光 · 颜色</div>
      <h1>天空为什么是<span class="b">蓝</span>的<br />日落为什么是<span class="o">红</span>的</h1>
      <div class="sub">同一束光，走了 38 倍的路</div>
      <div class="tag">蓝光被抢走，红橙才到你眼睛</div>
      <div class="line"></div>
      <div class="sun"></div>
      <div class="foot">看完你就知道，抬头该看什么</div>
    </div>
  </body>
</html>

```

### templates/cover-3x4.html

```
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <style>
      @font-face { font-family: "YH"; src: local("Microsoft YaHei"); }
      @font-face { font-family: "Mono"; src: local("Consolas"); }
      * { box-sizing: border-box; margin: 0; padding: 0; }
      html, body { width: 1080px; height: 1440px; overflow: hidden; background: #05070E; }
      #c { position: relative; width: 1080px; height: 1440px; overflow: hidden;
        background: linear-gradient(180deg,#05070E 0%,#0A1430 26%,#2A1F4A 46%,#7A3020 68%,#D0653A 84%,#F2A65A 100%);
        font-family: YH, sans-serif; color: #EAF2FF; }
      .grain { position: absolute; inset: 0; opacity: 0.4;
        background-image: radial-gradient(rgba(220,232,255,0.05) 1px, transparent 1px); background-size: 3px 3px; }
      .vig { position: absolute; inset: 0;
        background: radial-gradient(ellipse at 50% 42%, transparent 40%, rgba(0,0,0,0.55) 100%); }
      .top { position: absolute; left: 72px; top: 64px; font-family: Mono; font-size: 24px;
        letter-spacing: 8px; color: #4D8CFF; }
      .no { position: absolute; right: 72px; top: 64px; font-family: Mono; font-size: 22px;
        letter-spacing: 6px; color: rgba(234,242,255,0.45); }
      h1 { position: absolute; left: 70px; top: 260px; font-size: 104px; font-weight: 900;
        line-height: 1.16; letter-spacing: -3px; }
      h1 .b { color: #7FB6FF; }
      h1 .o { color: #FFB27A; }
      .sub { position: absolute; left: 74px; top: 640px; font-size: 42px; letter-spacing: 1px;
        color: rgba(234,242,255,0.85); }
      .tag { position: absolute; left: 74px; top: 720px; display: inline-block; padding: 14px 26px;
        border: 2px solid rgba(255,178,122,0.7); border-radius: 8px; font-size: 32px;
        letter-spacing: 2px; color: #FFB27A; }
      .line { position: absolute; left: 0; right: 0; top: 1150px; height: 1px;
        background: rgba(255,217,160,0.35); }
      .sun { position: absolute; left: 540px; top: 1020px; width: 260px; height: 130px;
        border-radius: 260px 260px 0 0; background: #FFD9A0;
        box-shadow: 0 0 90px rgba(255,180,110,0.55); }
      .foot { position: absolute; left: 74px; bottom: 56px; font-family: Mono; font-size: 24px;
        letter-spacing: 5px; color: rgba(234,242,255,0.55); }
    </style>
  </head>
  <body>
    <div id="c">
      <div class="grain"></div><div class="vig"></div>
      <div class="top">SKY · 79s</div>
      <div class="no">大气 · 光 · 颜色</div>
      <h1>天空为什么是<span class="b">蓝</span>的<br />日落为什么是<span class="o">红</span>的</h1>
      <div class="sub">同一束光，走了 38 倍的路</div>
      <div class="tag">蓝光被抢走，红橙才到你眼睛</div>
      <div class="line"></div>
      <div class="sun"></div>
      <div class="foot">看完你就知道，抬头该看什么</div>
    </div>
  </body>
</html>

```

### templates/gen_tts.mjs

```javascript
/**
 * 逐句配音：读取 lines.json，为每句生成 mp3 + 24k 单声道 wav
 * 用法：node gen_tts.mjs <音频目录>
 * 依赖：npm i msedge-tts
 */
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { MsEdgeTTS, OUTPUT_FORMAT } from "msedge-tts";

const cfg = JSON.parse(fs.readFileSync(new URL("./lines.json", import.meta.url), "utf8"));
const outRoot = process.argv[2] || "./_tts";
fs.mkdirSync(outRoot, { recursive: true });

for (const line of cfg.lines) {
  const dir = path.join(outRoot, "e" + String(line.n).padStart(2, "0"));
  fs.mkdirSync(dir, { recursive: true });

  const tts = new MsEdgeTTS({ connectionTimeoutMs: 20000, synthesisTimeoutMs: 90000 });
  await tts.setMetadata(cfg.voice, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);
  await tts.toFile(dir, line.text, { rate: cfg.rate, pitch: cfg.pitch });

  // 转 24k 单声道 wav
  execFileSync("ffmpeg", ["-y", "-loglevel", "error",
    "-i", path.join(dir, "audio.mp3"),
    "-ar", "24000", "-ac", "1", path.join(dir, "audio.wav")], { stdio: "ignore" });

  console.log("ok", line.n, line.text);
}
console.log("done →", outRoot);
process.exit(0);

```

### templates/lines.json

```json
{
  "gap": 0.5,
  "start": 0.6,
  "tail": 2.4,
  "novoice": false,
  "cps": 4.2,
  "voice": "zh-CN-XiaoxiaoNeural",
  "rate": "-6%",
  "pitch": "-3Hz",
  "lines": [
    {
      "n": 1,
      "scene": 1,
      "text": "有句话没说好，脸先热了。",
      "nosub": true
    },
    {
      "n": 2,
      "scene": 1,
      "text": "然后才反应过来：我生气了。",
      "nosub": true
    },
    {
      "n": 3,
      "scene": 2,
      "text": "顺序反了。"
    },
    {
      "n": 4,
      "scene": 3,
      "text": "不是先想明白，再生气。"
    },
    {
      "n": 5,
      "scene": 3,
      "text": "是先热，再找理由。"
    },
    {
      "n": 6,
      "scene": 4,
      "text": "声音进来，先抄一条近路。"
    },
    {
      "n": 7,
      "scene": 4,
      "text": "从耳朵到杏仁核，十二毫秒。"
    },
    {
      "n": 8,
      "scene": 4,
      "text": "这十二毫秒里，还没轮到你想。"
    },
    {
      "n": 9,
      "scene": 5,
      "text": "要绕到皮层，才叫想明白。"
    },
    {
      "n": 10,
      "scene": 5,
      "text": "差不多半秒。"
    },
    {
      "n": 11,
      "scene": 5,
      "text": "这半秒，够身体做完决定。"
    },
    {
      "n": 12,
      "scene": 6,
      "text": "心跳上去。"
    },
    {
      "n": 13,
      "scene": 6,
      "text": "肩膀绷住。"
    },
    {
      "n": 14,
      "scene": 6,
      "text": "呼吸变浅。"
    },
    {
      "n": 15,
      "scene": 7,
      "text": "然后脑子才开始解释。"
    },
    {
      "n": 16,
      "scene": 7,
      "text": "他就是故意的。"
    },
    {
      "n": 17,
      "scene": 8,
      "text": "这个解释，又让身体紧一点。"
    },
    {
      "n": 18,
      "scene": 8,
      "text": "紧一点，理由就更硬一点。"
    },
    {
      "n": 19,
      "scene": 8,
      "text": "转几圈，就停不下来了。"
    },
    {
      "n": 20,
      "scene": 9,
      "text": "每个人的圈，转速不一样。"
    },
    {
      "n": 21,
      "scene": 9,
      "text": "一晚没睡，杏仁核反应强六成。"
    },
    {
      "n": 22,
      "scene": 9,
      "text": "饿着肚子，也更容易上火。"
    },
    {
      "n": 23,
      "scene": 10,
      "text": "所以那天那句话，不是原因。"
    },
    {
      "n": 24,
      "scene": 10,
      "text": "它只是最后一下。"
    }
  ],
  "_comment": "nosub=true 表示这一句画面已有同义大字，底部不再重复显示字幕"
}

```

### templates/mix.py

```python
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

```

### templates/synth_bgm.py

```python
﻿"""合成 Vibe 知识大赏 风格 BGM：77 BPM，A 小调，pad + 钢琴 + kick + shaker"""
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

```

---

## 附录 D · 封面与标题
# 封面与标题

发布前最后一步：标题、话题、两张封面。这套规则和 `templates/cover-16x9.html`、`templates/cover-3x4.html` 配套用。

---

## 一、标题

固定开头 `Vibe知识大赏｜`，后面接三段式：

```
Vibe知识大赏｜【现象】，不是【误因】，是因为【机制】。
```

示例：

> Vibe知识大赏｜傍晚太阳压到地平线，整片天变橙红，不是太阳自己变红了，是因为蓝光在半路就被空气弹光，只剩红橙走到你眼睛里。

**判据：**

| 项 | 要求 |
|---|---|
| 现象 | 具体、能在画面上看到（“整片天变橙红”，不是“天空变色”） |
| 误因 | 观众真会那么想的（“太阳自己变红了”）；没人信就整句塌 |
| 机制 | 不许出现术语，用动作或比喻（“蓝光被弹光”） |
| 长度 | ≤40 字（含 `Vibe知识大赏｜` 前缀）；抖音只露前两行，前两行要能独立成立 |

---

## 二、话题

三条，第一条固定，后两条按片子换：

```
#Vibe知识大赏 #<领域> #<具体词>
```

| 位置 | 作用 | 示例 |
|---|---|---|
| 第一条 | 活动话题，**固定**，每条必带 | `#Vibe知识大赏` |
| 第二条 | 领域，按选题换 | `#科普` `#天文` `#工程` `#人体` |
| 第三条 | 具体词，越具体越容易被搜到 | `#瑞利散射` `#晚霞` `#影子` |

换选题时只换后两个。想要泛流量可以把第三条换成 `#冷知识`、`#涨知识`，但**默认用具体词**：具体词搜索量小，转化更准。

三条都别写死在文件里，按每条片子的选题填。

---

## 三、封面

两种规格，同一套版式：

两张都放工程 `发布/`，**不进 `成品/`**（成品只放成片）。

| 规格 | 尺寸 | 用在哪 | 模板 |
|---|---|---|---|
| 16:9 | 1920×1080 | 横屏发布、播放页、B 站 / 西瓜 | `templates/cover-16x9.html` |
| 3:4 | 1080×1440 | 抖音信息流、主页封面 | `templates/cover-3x4.html` |

**版式规则：**

- 左边标题：两行，主色词单独上色（“蓝”用蓝、“红”用橙），字号 16:9 用 112px、3:4 用 104px。
- 标题下一行副题（一句机制），再下面一个描边标签框（一句结论）。
- 右边或底部放主视觉（太阳、地平线），地平线压到画面 80% 高度，太阳只露半轮。
- 顶部 mono 小字放时长/编号，底部留一句“看完得到什么”。
- 背景用片子同一套渐变，不要另起一套色。

**出图：**

```powershell
$chrome = "<chrome-headless-shell 路径>"
& $chrome --headless --disable-gpu --hide-scrollbars `
  --window-size=1920,1080 --screenshot="封面-16x9.png" --virtual-time-budget=4000 "cover-16x9.html"
& $chrome --headless --disable-gpu --hide-scrollbars `
  --window-size=1080,1440 --screenshot="封面-3x4.png" --virtual-time-budget=4000 "cover-3x4.html"
```

**检查：**

- 缩到手机宽度（约 375px）时，标题是否还能读清；
- 标题不压太阳、不压地平线；
- 两张封面的标题、副标题、标签必须一致，只换版式。

---

## 附录 C · 风格样例（仅色值与母题，完整代码见 styles/）
| 文件 | 说明 |
|---|---|
| styles/01-鎏金暗场.html | 可运行 5 秒样例，lint 通过 |
| styles/02-复古丝印.html | 可运行 5 秒样例，lint 通过 |
| styles/03-示波器.html | 可运行 5 秒样例，lint 通过 |
| styles/04-蓝图.html | 可运行 5 秒样例，lint 通过 |
| styles/05-霓虹.html | 可运行 5 秒样例，lint 通过 |
| styles/06-极光.html | 可运行 5 秒样例，lint 通过 |
| styles/07-黑板粉笔.html | 可运行 5 秒样例，lint 通过 |
| styles/08-暗场几何.html | 可运行 5 秒样例，lint 通过 |
| styles/09-报纸黑白.html | 可运行 5 秒样例，lint 通过 |
| styles/10-深空星图.html | 可运行 5 秒样例，lint 通过 |
| styles/11-手绘水彩.html | 可运行 5 秒样例，lint 通过 |
| styles/12-等距白模.html | 可运行 5 秒样例，lint 通过 |
| styles/13-复古录像.html | 可运行 5 秒样例，lint 通过 |
| styles/14-冰窟蓝.html | 可运行 5 秒样例，lint 通过 |
| styles/15-像素 8bit.html | 可运行 5 秒样例，lint 通过 |
| styles/16-终端绿.html | 可运行 5 秒样例，lint 通过 |
| styles/17-极简白.html | 可运行 5 秒样例，lint 通过 |
| styles/18-胶片棕.html | 可运行 5 秒样例，lint 通过 |
