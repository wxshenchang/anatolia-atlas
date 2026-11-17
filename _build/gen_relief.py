#!/usr/bin/env python3
"""生成安纳托利亚版基础晕渲底图 assets/terrain_relief.webp
覆盖 SVG 坐标 (-80,-40)–(1080,740)，与 app.js 的 MercatorProjector（west 24 / east 48 /
south 33.5 / north 44.5）严格对齐，配色与 scripts/build_terrain_tiles.py 一致
（LIGHT #F4ECDC / SHADOW #927C60），高程来自 _build/dem 的 Terrarium 瓦片。
"""
import json
import math
import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEM = os.path.join(ROOT, "_build", "dem")
OUT = os.path.join(ROOT, "assets", "terrain_relief.webp")

W_SVG, H_SVG = 1000, 700
BOUNDS = dict(west=24.0, east=48.0, south=33.5, north=44.5)
RECT = (-80, -40, 1080, 740)        # index.html 里 <image> 的 x,y,width,height 范围
IMG_W, IMG_H = 2320, 1560           # 与原图同尺寸（2 px / SVG 单位）
Z = 7                               # DEM 采样层级
TILE = 256
DEG, R2D = math.pi / 180.0, 180.0 / math.pi
LIGHT = np.array([244, 236, 220], np.float32)
SHADOW = np.array([146, 124, 96], np.float32)
EARTH_M = 40075016.686


def merc(lat):
    return math.log(math.tan(math.pi * 0.25 + lat * DEG * 0.5))


def project(lng, lat, scale, padx, pady, north_merc):
    x = (lng - BOUNDS["west"]) * scale + padx
    y = (north_merc - merc(lat)) * R2D * scale + pady
    return x, y


def unproject(x, y, scale, padx, pady, north_merc):
    lng = (x - padx) / scale + BOUNDS["west"]
    m = north_merc - (y - pady) / (scale * R2D)
    lat = (2 * math.atan(math.exp(m)) - math.pi * 0.5) * R2D
    return lng, lat


def load_mosaic():
    """把 z=Z 的 DEM 瓦片拼成一个全局像素网格，返回 (array, origin_x_px, origin_y_px)"""
    files = []
    for f in os.listdir(os.path.join(DEM, str(Z))):
        if f.endswith(".png"):
            x, y = f[:-4].split("_")
            files.append((int(x), int(y)))
    x0, y0 = min(f[0] for f in files), min(f[1] for f in files)
    x1, y1 = max(f[0] for f in files), max(f[1] for f in files)
    W, H = (x1 - x0 + 1) * TILE, (y1 - y0 + 1) * TILE
    mos = np.zeros((H, W), np.float32)
    filled = np.zeros((H, W), bool)
    for tx, ty in files:
        p = os.path.join(DEM, str(Z), f"{tx}_{ty}.png")
        a = np.asarray(Image.open(p).convert("RGB"), np.float32)
        elev = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
        ys, xs = (ty - y0) * TILE, (tx - x0) * TILE
        mos[ys:ys + TILE, xs:xs + TILE] = elev
        filled[ys:ys + TILE, xs:xs + TILE] = True
    mos[~filled] = 0.0
    return mos, x0 * TILE, y0 * TILE, filled


def main():
    span_lng = BOUNDS["east"] - BOUNDS["west"]
    span_lat = (merc(BOUNDS["north"]) - merc(BOUNDS["south"])) * R2D
    scale = min(W_SVG / span_lng, H_SVG / span_lat)
    padx = (W_SVG - span_lng * scale) * 0.5
    pady = (H_SVG - span_lat * scale) * 0.5
    nm = merc(BOUNDS["north"])
    print(f"投影 scale={scale:.3f} pad=({padx:.1f},{pady:.1f})")

    mos, ox, oy, mask = load_mosaic()
    print(f"DEM 拼图 {mos.shape[1]}x{mos.shape[0]} px @ z{Z}")

    # 输出像素 → SVG 坐标 → 经纬度 → 全局 Mercator 像素 → 双线性采样
    xs_svg = np.linspace(RECT[0], RECT[0] + RECT[2], IMG_W, dtype=np.float64)
    ys_svg = np.linspace(RECT[1], RECT[1] + RECT[3], IMG_H, dtype=np.float64)
    lngs = (xs_svg - padx) / scale + BOUNDS["west"]
    mers = nm - (ys_svg - pady) / (scale * R2D)
    lats = (2 * np.arctan(np.exp(mers)) - math.pi * 0.5) * R2D

    n = TILE * (1 << Z)
    gx = (lngs + 180.0) / 360.0 * n - ox
    gy = (1.0 - np.log(np.tan(lats * DEG) + 1 / np.cos(lats * DEG)) / math.pi) / 2.0 * n - oy

    x0 = np.clip(np.floor(gx).astype(int), 0, mos.shape[1] - 2)
    y0 = np.clip(np.floor(gy).astype(int), 0, mos.shape[0] - 2)
    fx = np.clip(gx - x0, 0, 1)[None, :]
    fy = np.clip(gy - y0, 0, 1)[:, None]

    a = mos[y0][:, x0]
    b = mos[y0][:, x0 + 1]
    c = mos[y0 + 1][:, x0]
    d = mos[y0 + 1][:, x0 + 1]
    elev = (a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy).astype(np.float32)

    # 与 build_terrain_tiles.py 同款夸张系数
    zf = 2.4 * 1.45 ** (9 - Z)
    px_m = EARTH_M / n * np.cos(lats * DEG)
    dzdy, dzdx = np.gradient(elev * zf)
    dzdx = dzdx / px_m[:, None]
    dzdy = dzdy / px_m[:, None]
    slope = np.arctan(np.hypot(dzdx, dzdy))
    aspect = np.arctan2(-dzdx, dzdy)

    def shade(az_deg, alt_deg):
        az, alt = math.radians(az_deg), math.radians(alt_deg)
        return np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)

    s = np.clip(0.62 * shade(315, 45) + 0.38 * shade(270, 28), 0, 1)
    s = s ** 0.92
    rgb = SHADOW[None, None, :] + (LIGHT - SHADOW)[None, None, :] * s[..., None]
    # 低海拔（海面）压向更浅的纸色，避免海底起伏抢戏
    sea = elev < 0
    rgb[sea] = LIGHT * 0.985
    # DEM 覆盖不到的区域（画布外缘）抹成净纸色，避免出现条纹伪影
    valid = mask[np.clip(y0, 0, mask.shape[0] - 1)][:, np.clip(x0, 0, mask.shape[1] - 1)]
    rgb[~valid] = LIGHT * 0.975
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    img.save(OUT, "WEBP", quality=84, method=6)
    print(f"写入 {OUT} ({os.path.getsize(OUT)/1024:.0f} KB, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
