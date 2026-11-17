#!/usr/bin/env python3
"""底图配准体检：把「晕渲水/陆」与 Natural Earth 陆地面比较，并搜索最佳平移量
若最佳平移明显偏离 (0,0)，说明底图和矢量层存在系统错位。
"""
import json
import math
import os

import numpy as np
from PIL import Image
from shapely.geometry import Point, shape
from shapely.ops import unary_union
from shapely.prepared import prep

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = dict(west=24.0, east=48.0, south=33.5, north=44.5)
DEG, R2D = math.pi / 180, 180 / math.pi
merc = lambda lat: math.log(math.tan(math.pi * 0.25 + lat * DEG * 0.5))
span_lng = B["east"] - B["west"]
span_lat = (merc(B["north"]) - merc(B["south"])) * R2D
scale = min(1000 / span_lng, 700 / span_lat)
padx = (1000 - span_lng * scale) / 2
pady = (700 - span_lat * scale) / 2
NM = merc(B["north"])
RECT = (-80, -40, 1160, 780)


def svg(lon, lat):
    return (lon - B["west"]) * scale + padx, (NM - merc(lat)) * R2D * scale + pady


def main():
    land = unary_union([shape(f["geometry"]) for f in
                        json.load(open(os.path.join(ROOT, "_build/raw/countries.geojson")))["features"]])
    lp = prep(land)
    im = Image.open(os.path.join(ROOT, "assets/terrain_relief.webp")).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(np.float32)
    # 平坦度图（7x7 窗口标准差），预计算
    g = a.mean(2)
    win = 3
    pad = np.pad(g, win, mode="edge")
    flat = np.zeros_like(g)
    for dy in range(-win, win + 1):
        for dx in range(-win, win + 1):
            flat += np.abs(g - pad[win + dy:win + dy + g.shape[0], win + dx:win + dx + g.shape[1]])
    flat = flat / ((2 * win + 1) ** 2)

    rng = np.random.default_rng(7)
    pts = []
    for _ in range(4000):
        lon = rng.uniform(B["west"] + 1, B["east"] - 1)
        lat = rng.uniform(B["south"] + 1, B["north"] - 1)
        pts.append((lon, lat))
    truth = [lp.contains(Point(lon, lat)) for lon, lat in pts]

    def score(dx_px, dy_px):
        agree = 0
        n = 0
        for (lon, lat), is_land in zip(pts, truth):
            x, y = svg(lon, lat)
            px = (x - RECT[0]) / RECT[2] * W + dx_px
            py = (y - RECT[1]) / RECT[3] * H + dy_px
            if not (8 <= px < W - 8 and 8 <= py < H - 8):
                continue
            is_flat = flat[int(py), int(px)] < 1.6      # 平坦 → 水
            agree += (is_flat != is_land)               # 水对应非陆地
            n += 1
        return agree / max(1, n), n

    base, n = score(0, 0)
    print(f"无平移一致率: {base*100:.1f}%  (样本 {n})")
    best = (base, 0, 0)
    for dy in range(-40, 41, 4):
        for dx in range(-40, 41, 4):
            s, _ = score(dx, dy)
            if s > best[0]:
                best = (s, dx, dy)
    print(f"最佳平移: ({best[1]:+d}, {best[2]:+d}) px → 一致率 {best[0]*100:.1f}%  "
          f"(提升 {(best[0]-base)*100:+.1f} 个百分点)")
    # 换算成公里（底图 2320 px / 24° 经度 ≈ 0.0103°/px）
    if best[1] or best[2]:
        print(f"  ≈ 经度 {best[1]*24/1000*1:+.3f}° / 纬度 {best[2]*24/1000*1:+.3f}° (粗算)")
    if best[0] - base < 0.01:
        print("结论: 配准良好，底图与矢量层无系统错位。")


if __name__ == "__main__":
    main()
