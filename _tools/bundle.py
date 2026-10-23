# -*- coding: utf-8 -*-
"""把整个技能打成一个 markdown，方便一次性喂给任意模型。

用法： python _tools/bundle.py
输出： dist/plainframe-all.md
"""
import io, os, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist", "plainframe-all.md")


def read(p):
    return io.open(p, encoding="utf-8").read()


def strip_frontmatter(s):
    if s.startswith("---"):
        parts = s.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return s


parts = []
parts.append("# plainframe-skill · 单文件版\n")
parts.append("> 这是整个技能打包成的单文件，任何模型读完即可按流程工作。\n"
             "> 需要可运行样例时，再取仓库里的 `styles/` 与 `templates/`。\n")

meta = json.loads(read(os.path.join(ROOT, "skill.json")))
parts.append("## 元信息\n")
parts.append("```json\n" + json.dumps(meta, ensure_ascii=False, indent=2) + "\n```\n")

parts.append("---\n")
parts.append(strip_frontmatter(read(os.path.join(ROOT, "SKILL.md"))))

parts.append("\n---\n\n## 附录 A · 出片检查清单\n")
parts.append(read(os.path.join(ROOT, "CHECKLIST.md")))

parts.append("\n---\n\n## 附录 B · 模板源码\n")
for p in sorted(glob.glob(os.path.join(ROOT, "templates", "*"))):
    name = os.path.basename(p)
    lang = {"py": "python", "mjs": "javascript", "json": "json",
            "ps1": "powershell", "tpl": "html"}.get(name.rsplit(".", 1)[-1], "")
    parts.append("\n### templates/%s\n\n```%s\n%s\n```\n" % (name, lang, read(p)))

parts.append("\n---\n\n## 附录 C · 风格样例（仅色值与母题，完整代码见 styles/）\n")
parts.append("| 文件 | 说明 |\n|---|---|\n")
for p in sorted(glob.glob(os.path.join(ROOT, "styles", "*.html"))):
    name = os.path.basename(p)
    parts.append("| styles/%s | 可运行 5 秒样例，lint 通过 |\n" % name)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write("".join(parts))
print("wrote", OUT, os.path.getsize(OUT), "bytes")
