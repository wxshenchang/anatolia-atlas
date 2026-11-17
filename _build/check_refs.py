#!/usr/bin/env python3
"""检查 index.html 里引用的本地资源是否都在仓库里（CI 用）。

跳过：外链、data:/mailto:、以 # 开头的锚点、以及目录自身引用（./ 与 /）。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

SKIP = {"./", ".", "/", "", "index.html"}
missing = []
checked = 0
for m in re.finditer(r'(?:src|href)="([^"#?]+)(?:\?[^"]*)?"', html):
    u = m.group(1).strip()
    if u.startswith(("http", "//", "data:", "mailto:", "#")):
        continue
    if u in SKIP:
        continue
    checked += 1
    if not os.path.exists(os.path.join(ROOT, u.lstrip("./"))):
        missing.append(u)

print(f"index.html 本地引用 {checked} 个")
if missing:
    print("引用但仓库里没有：")
    for x in missing:
        print("  ", x)
    sys.exit(1)
print("全部存在 ✓")
