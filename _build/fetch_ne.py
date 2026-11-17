#!/usr/bin/env python3
"""按新的地图范围重新切片 Natural Earth 1:10m 数据。

边界从 (24–48E, 33.5–44.5N) 扩到 (24–48E, 29.5–44.5N) 之后，
需要把埃及、以色列、巴勒斯坦、黎巴嫩、约旦、科威特、沙特北部纳入切片，
否则这些国家在新露出的南半部没有矢量海岸线与陆地面。

输出 _build/raw/*.geojson（覆盖旧文件）
"""
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "_build", "raw")
os.makedirs(RAW, exist_ok=True)

# 切片框：比地图范围各留 3 度余量
W, S, E, N = 21.0, 26.5, 51.0, 47.5

BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FILES = {
    "countries.geojson": "ne_10m_admin_0_countries.geojson",
    "lakes.geojson": "ne_10m_lakes.geojson",
    "rivers.geojson": "ne_10m_rivers_lake_centerlines.geojson",
    "coastline.geojson": "ne_10m_coastline.geojson",
}

OP = urllib.request.build_opener(urllib.request.ProxyHandler({
    "https": "http://127.0.0.1:1080",
    "http": "http://127.0.0.1:1080"}))


def bbox_of(geom):
    xs, ys = [], []

    def walk(c):
        if isinstance(c, (int, float)):
            return
        if c and isinstance(c[0], (int, float)):
            xs.append(c[0])
            ys.append(c[1])
            return
        for x in c:
            walk(x)

    walk(geom["coordinates"])
    return (min(xs), min(ys), max(xs), max(ys))


def overlaps(b):
    return not (b[2] < W or b[0] > E or b[3] < S or b[1] > N)


def main():
    for out, src in FILES.items():
        path = os.path.join(RAW, out)
        url = BASE + src
        print(f"{out}: 下载 {src} …")
        with OP.open(url, timeout=180) as r:
            data = json.load(r)
        kept = []
        for f in data.get("features", []):
            g = f.get("geometry")
            if not g or not g.get("coordinates"):
                continue
            if overlaps(bbox_of(g)):
                kept.append(f)
        json.dump({"type": "FeatureCollection", "features": kept},
                  open(path, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"  全域 {len(data.get('features', []))} → 本区 {len(kept)} 个要素, "
              f"{os.path.getsize(path)//1024} KB")

    c = json.load(open(os.path.join(RAW, "countries.geojson")))
    names = sorted({f["properties"].get("NAME") or f["properties"].get("name")
                    for f in c["features"]})
    print(f"\n国家清单（{len(names)}）：{names}")
    codes = sorted({f["properties"].get("ISO_A3") for f in c["features"] if f["properties"].get("ISO_A3")})
    print(f"ISO_A3 数量 {len(codes)}；含 EGY={'EGY' in codes} ISR={'ISR' in codes} "
          f"PSX={'PSX' in codes} LBN={'LBN' in codes} JOR={'JOR' in codes}")


if __name__ == "__main__":
    main()
