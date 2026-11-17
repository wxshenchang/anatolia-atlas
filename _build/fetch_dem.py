#!/usr/bin/env python3
"""下载 Terrarium 高程瓦片（AWS elevation-tiles-prod，公开免密钥）
分三档、每档各自的覆盖框，够 build_terrain_tiles.py 输出 5/6/7 级：
  z6 ← 宽框（20–52E, 30–47N）  → 出 z5
  z7 ← 宽框                    → 出 z6
  z8 ← 窄框（25–45E, 35–43N）  → 出 z7（安纳托利亚本体高清）
输出 _build/dem/{z}/{x}_{y}.png
"""
import math
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

OP = urllib.request.build_opener(urllib.request.ProxyHandler(
    {"https": "http://127.0.0.1:1080", "http": "http://127.0.0.1:1080"}))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dem")
WIDE = (20.0, 28.0, 52.0, 47.0)
NARROW = (25.0, 35.0, 45.0, 43.0)
PLAN = {6: WIDE, 7: WIDE, 8: NARROW}


def tile_x(lon, z):
    return int(math.floor((lon + 180.0) / 360.0 * (1 << z)))


def tile_y(lat, z):
    r = math.radians(lat)
    return int(math.floor((1.0 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2.0 * (1 << z)))


def jobs():
    out = []
    for z, (w, s, e, n) in PLAN.items():
        for x in range(tile_x(w, z), tile_x(e, z) + 1):
            for y in range(tile_y(n, z), tile_y(s, z) + 1):
                out.append((z, x, y))
    return out


def fetch(t):
    z, x, y = t
    d = os.path.join(OUT, str(z))
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{x}_{y}.png")
    if os.path.exists(p) and os.path.getsize(p) > 500:
        return "skip"
    try:
        with OP.open(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png", timeout=90) as r:
            open(p, "wb").write(r.read())
        return "ok"
    except Exception as ex:
        return f"fail {z}/{x}_{y} {str(ex)[:50]}"


if __name__ == "__main__":
    js = jobs()
    print(f"需下载 {len(js)} 个 DEM 瓦片（z6/z7 宽框 + z8 窄框）")
    ok = skip = 0
    fails = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        for r in ex.map(fetch, js):
            if r == "ok":
                ok += 1
            elif r == "skip":
                skip += 1
            else:
                fails.append(r)
    print(f"完成: 新下 {ok}, 已有 {skip}, 失败 {len(fails)}")
    for f in fails[:5]:
        print("  ", f)
