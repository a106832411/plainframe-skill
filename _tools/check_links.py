# -*- coding: utf-8 -*-
"""check_links.py —— 查仓库内部的路径引用有没有断

用法：
    python _tools/check_links.py          # 有问题返回码 1

它会扫所有 md / json / py 里出现的 docs/、tools/、templates/、styles/、previews/、
platforms/、_tools/ 开头的路径，逐个确认文件真的存在。改了目录结构之后跑一次，
比人眼逐个翻文档可靠。
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "dist", "node_modules", "__pycache__"}
EXTS = (".md", ".json", ".py", ".mjs", ".tpl")

PATTERN = re.compile(
    r"(?<![\w/])"
    r"((?:docs|tools|templates|styles|previews|platforms|_tools)/"
    r"[A-Za-z0-9_\-\u4e00-\u9fff./*%]+)"
)
TRIM = "`）),.;:；：、。\"'"


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(EXTS):
                yield os.path.join(dirpath, fn)


def main():
    missing = []
    checked = 0
    for path in walk():
        rel = os.path.relpath(path, ROOT)
        text = io.open(path, encoding="utf-8", errors="replace").read()
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in PATTERN.finditer(line):
                ref = m.group(1).rstrip(TRIM)
                if not ref or "%s" in ref or "%d" in ref:
                    continue
                checked += 1
                target = os.path.join(ROOT, ref.replace("/", os.sep))
                if "*" in ref:
                    ok = bool(glob.glob(target))
                elif os.path.exists(target):
                    ok = True
                elif "." not in os.path.basename(ref):
                    # 形如 styles/01、docs/流程 这种前缀写法，按前缀 glob 兜一次
                    ok = bool(glob.glob(target + "*"))
                else:
                    ok = False
                if not ok:
                    missing.append("%s:%d  %s" % (rel, lineno, ref))

    print("检查 %d 处内部引用" % checked)
    if missing:
        print("\n断链 %d 处：" % len(missing))
        for m in sorted(set(missing)):
            print("  - " + m)
        return 1
    print("全部有效")
    return 0


if __name__ == "__main__":
    sys.exit(main())
