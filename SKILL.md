---
name: plainframe-skill
description: 用 HTML + GSAP 做中文科普短视频，两条路线：口播版（Edge TTS 配音）与无口播版（字幕 / 拍表驱动，只出 BGM）。内置 18 套可套用的风格参数（鎏金 / 丝印 / 示波器 / 蓝图 / 霓虹 / 极光 / 黑板 / 暗场几何 / 报纸 / 深空 / 水彩 / 等距 / 录像 / 冰窟蓝 / 像素 / 终端 / 极简白 / 胶片），含逐句动效引擎、构建与混音脚本、拍表转换、抽帧联系表、自动自检与踩坑清单。当用户要做科普/知识类短视频、出分镜、出成片，或修改 HyperFrames 工程时使用。
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
