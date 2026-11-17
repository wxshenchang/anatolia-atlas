#!/usr/bin/env python3
"""生成安纳托利亚底图：替换 js/china_geo_data.js
 - PROVINCE_OUTLINES: 土耳其 81 省（现代省界，中文名）
 - HYDRO_DATA: 河流 / 湖泊 / 水体注记
格式与江山时序完全一致（VLQ delta，两位小数）。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vlq import encode  # noqa: E402

# 坐标量化：江山时序原版是 x100（≈1.1 km），这里提到 x1000（≈110 m），
# 配合放宽的简化容差，让矢量海岸线能贴住栅格地形。
SCALE = 1000

from shapely.geometry import shape, mapping  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "_build", "raw")

# 土耳其 81 省中文名（NE 名称 → 中文）
PROV_ZH = {
    "Adana": "阿达纳", "Adiyaman": "阿德亚曼", "Afyonkarahisar": "阿菲永卡拉希萨尔", "Agri": "阿勒",
    "Aksaray": "阿克萨赖", "Amasya": "阿马西亚", "Ankara": "安卡拉", "Antalya": "安塔利亚",
    "Ardahan": "阿尔达汉", "Artvin": "阿尔特温", "Aydin": "艾登", "Balikesir": "巴勒克埃西尔",
    "Bartın": "巴尔滕", "Batman": "巴特曼", "Bayburt": "巴伊布尔特", "Bilecik": "比莱吉克",
    "Bingöl": "宾格尔", "Bitlis": "比特利斯", "Bolu": "博卢", "Burdur": "布尔杜尔",
    "Bursa": "布尔萨", "Çanakkale": "恰纳卡莱", "Çankiri": "昌克勒", "Çorum": "乔鲁姆",
    "Denizli": "代尼兹利", "Diyarbakir": "迪亚巴克尔", "Düzce": "迪兹杰", "Edirne": "埃迪尔内",
    "Elazig": "埃拉泽", "Erzincan": "埃尔津詹", "Erzurum": "埃尔祖鲁姆", "Eskisehir": "埃斯基谢希尔",
    "Gaziantep": "加济安泰普", "Giresun": "吉雷松", "Gümüshane": "居米什哈内", "Hakkari": "哈卡里",
    "Hatay": "哈塔伊", "Iğdir": "厄德尔", "Isparta": "伊斯帕尔塔", "Istanbul": "伊斯坦布尔",
    "Izmir": "伊兹密尔", "K. Maras": "卡赫拉曼马拉什", "Karabük": "卡拉比克", "Karaman": "卡拉曼",
    "Kars": "卡尔斯", "Kastamonu": "卡斯塔莫努", "Kayseri": "开塞利", "Kilis": "基利斯",
    "Kinkkale": "克勒克卡莱", "Kirklareli": "克尔克拉雷利", "Kirsehir": "克尔谢希尔", "Kocaeli": "科贾埃利",
    "Konya": "科尼亚", "Kütahya": "屈塔希亚", "Malatya": "马拉蒂亚", "Manisa": "马尼萨",
    "Mardin": "马尔丁", "Mersin": "梅尔辛", "Mugla": "穆拉", "Mus": "穆什",
    "Nevsehir": "内夫谢希尔", "Nigde": "尼代", "Ordu": "奥尔杜", "Osmaniye": "奥斯曼尼耶",
    "Rize": "里泽", "Sakarya": "萨卡里亚", "Samsun": "萨姆松", "Sanliurfa": "尚勒乌尔法",
    "Siirt": "锡尔特", "Sinop": "锡诺普", "Sirnak": "舍尔纳克", "Sivas": "锡瓦斯",
    "Tekirdag": "泰基尔达", "Tokat": "托卡特", "Trabzon": "特拉布宗", "Tunceli": "通杰利",
    "Usak": "乌沙克", "Van": "凡城", "Yalova": "亚洛瓦", "Yozgat": "约兹加特",
    "Zinguldak": "宗古尔达克", "Karabük ": "卡拉比克",
}

# 主要水体中文注记（zh / en / coord / kind / rot）
WATER_LABELS = [
    {"zh": "黑 海", "en": "Black Sea", "coord": [34.0, 42.6], "kind": "trunk", "rot": 0},
    {"zh": "地 中 海", "en": "Mediterranean", "coord": [31.5, 35.3], "kind": "trunk", "rot": 0},
    {"zh": "爱 琴 海", "en": "Aegean Sea", "coord": [25.3, 38.6], "kind": "trunk", "rot": -72},
    {"zh": "马 尔 马 拉 海", "en": "Sea of Marmara", "coord": [28.2, 40.7], "kind": "lake", "rot": 0},
    {"zh": "克 孜 勒 河", "en": "Kızılırmak R.", "coord": [34.6, 40.1], "kind": "trunk", "rot": -18},
    {"zh": "幼 发 拉 底 河", "en": "Euphrates R.", "coord": [38.4, 37.6], "kind": "trunk", "rot": -55},
    {"zh": "底 格 里 斯 河", "en": "Tigris R.", "coord": [42.0, 37.4], "kind": "trunk", "rot": -62},
    {"zh": "萨 卡 里 亚 河", "en": "Sakarya R.", "coord": [30.9, 40.3], "kind": "river", "rot": -70},
    {"zh": "门 德 雷 斯 河", "en": "B. Menderes R.", "coord": [28.3, 37.9], "kind": "river", "rot": -62},
    {"zh": "塞 伊 汉 河", "en": "Seyhan R.", "coord": [35.5, 37.2], "kind": "river", "rot": -25},
    {"zh": "杰 伊 汉 河", "en": "Ceyhan R.", "coord": [36.2, 37.5], "kind": "river", "rot": -20},
    {"zh": "哈 里 斯 河", "en": "Halys R.", "coord": [35.2, 39.3], "kind": "river", "rot": -10},
    {"zh": "凡 湖", "en": "Lake Van", "coord": [43.0, 38.6], "kind": "lake", "rot": 0},
    {"zh": "图 兹 湖", "en": "Lake Tuz", "coord": [33.4, 38.75], "kind": "lake", "rot": 0},
    {"zh": "贝 伊 谢 希 尔 湖", "en": "L. Beyşehir", "coord": [31.5, 37.7], "kind": "lake", "rot": 0},
    {"zh": "埃 伊 尔 迪 尔 湖", "en": "L. Eğirdir", "coord": [30.9, 38.0], "kind": "lake", "rot": 0},
    {"zh": "博 斯 普 鲁 斯 海 峡", "en": "Bosporus", "coord": [29.05, 41.12], "kind": "lake", "rot": -80},
    {"zh": "达 达 尼 尔 海 峡", "en": "Dardanelles", "coord": [26.4, 40.2], "kind": "lake", "rot": -70},
    {"zh": "塞 浦 路 斯 岛", "en": "Cyprus", "coord": [33.2, 35.05], "kind": "lake", "rot": 0},
]


# 邻国/周边陆地中文名（countries.geojson）——没有这些矢量，周边地形就是"悬空的晕渲"
NEIGHBOR_ZH = {
    "Greece": "希腊", "Bulgaria": "保加利亚", "Georgia": "格鲁吉亚", "Armenia": "亚美尼亚",
    "Azerbaijan": "阿塞拜疆", "Iran": "伊朗", "Iraq": "伊拉克", "Syria": "叙利亚",
    "Cyprus": "塞浦路斯", "N. Cyprus": "塞浦路斯", "Northern Cyprus": "塞浦路斯",
    "Lebanon": "黎巴嫩", "Israel": "以色列",
    "Jordan": "约旦", "Egypt": "埃及", "Russia": "俄罗斯", "Ukraine": "乌克兰", "Moldova": "摩尔多瓦",
    "Romania": "罗马尼亚", "Serbia": "塞尔维亚", "Kosovo": "科索沃", "North Macedonia": "北马其顿",
    "Albania": "阿尔巴尼亚", "Turkmenistan": "土库曼斯坦", "Kuwait": "科威特", "Saudi Arabia": "沙特阿拉伯",
}

RIVER_KEEP = ["Kızılırmak", "Kizilirmak", "Sakarya", "Euphrates", "Fırat", "Tigris", "Dicle",
              "Seyhan", "Ceyhan", "Büyük Menderes", "B. Menderes", "Gediz", "Yeşilırmak",
              "Yeşil", "Aras", "Çoruh", "Coruh", "Manavgat", "Göksu", "Orontes", "Asi"]


def rings_of(geom):
    """把 Polygon/MultiPolygon 展平为外环+内环列表（每个环 = 坐标数组）"""
    out = []
    if geom.geom_type == "Polygon":
        out.append(list(geom.exterior.coords))
        for r in geom.interiors:
            out.append(list(r.coords))
    elif geom.geom_type == "MultiPolygon":
        for p in geom.geoms:
            out.append(list(p.exterior.coords))
            for r in p.interiors:
                out.append(list(r.coords))
    return out


def polys_of(geom):
    """返回 [[外环, 内环...], ...]：每个多边形一组环"""
    out = []
    geoms = [geom] if geom.geom_type == "Polygon" else (
        list(geom.geoms) if geom.geom_type == "MultiPolygon" else [])
    for g in geoms:
        rings = [list(g.exterior.coords)]
        rings += [list(r.coords) for r in g.interiors]
        out.append(rings)
    return out


def lines_of(geom):
    out = []
    if geom.geom_type == "LineString":
        out.append(list(geom.coords))
    elif geom.geom_type == "MultiLineString":
        for l in geom.geoms:
            out.append(list(l.coords))
    return out


def main():
    admin1 = json.load(open(os.path.join(RAW, "admin1.geojson")))
    provinces = []
    for f in admin1["features"]:
        p = f["properties"]
        if p.get("adm0_a3") != "TUR":
            continue
        name = p["name"]
        g = shape(f["geometry"]).simplify(0.002, preserve_topology=True)
        c = g.centroid
        provinces.append({
            "title": PROV_ZH.get(name, name),
            "code": int(p["iso_3166_2"].replace("TR-", "")) if p.get("iso_3166_2") else 0,
            "hub": [round(c.x, 2), round(c.y, 2)],
            "rings": [[encode(r, scale=SCALE) for r in poly_rings] for poly_rings in polys_of(g)],
            "name_en": name,
        })
    print(f"省份 {len(provinces)} 个, 环 {sum(len(p['rings']) for p in provinces)} 个")

    # 周边国家陆地：让地形晕渲有对应的矢量海岸线与边界（塞浦路斯、希腊、叙利亚等）
    import shapely.geometry as sgeom
    from shapely.geometry import box as sbox
    view = sbox(22.0, 28.2, 50.5, 46.5)
    cty = json.load(open(os.path.join(RAW, "countries.geojson")))
    neigh_n = 0
    # 塞浦路斯在 NE 里被拆成 CYP + CYN（北塞），中间还有联合国缓冲区缝隙。
    # 历史地图不该出现 1974 年的绿线，先并成一座完整岛。
    CYPRUS_KEYS = {"Cyprus", "N. Cyprus", "Northern Cyprus", "Cyprus U.N. Buffer Zone"}
    cyprus_geoms = [shape(f["geometry"]) for f in cty["features"]
                    if (f["properties"].get("NAME") or "") in CYPRUS_KEYS]
    merged = {}
    if cyprus_geoms:
        from shapely.ops import unary_union
        merged = {"Cyprus": unary_union(cyprus_geoms)}
    for f in cty["features"]:
        p = f["properties"]
        if p.get("ADM0_A3") == "TUR":
            continue
        name = p.get("NAME") or p.get("NAME_EN") or ""
        if name in CYPRUS_KEYS:
            if name not in merged:
                continue
            name = "Cyprus"
            g = merged.pop("Cyprus").intersection(view)
        else:
            if name not in NEIGHBOR_ZH:
                continue
            g = shape(f["geometry"]).intersection(view)
        if g.is_empty or g.area < 0.005:
            continue
        g = g.simplify(0.004, preserve_topology=True)
        c = g.representative_point()
        provinces.append({
            "title": NEIGHBOR_ZH[name],
            "code": f"N{neigh_n}",
            "hub": [round(c.x, 2), round(c.y, 2)],
            "rings": [[encode(r, scale=SCALE) for r in poly_rings] for poly_rings in polys_of(g)],
            "name_en": name,
            "caption": False,
        })
        neigh_n += 1
    print(f"周边陆地 {neigh_n} 块 (共 {len(provinces)} 个多边形组)")

    # 河流
    rv = json.load(open(os.path.join(RAW, "rivers.geojson")))
    rivers = []
    for f in rv["features"]:
        p = f["properties"]
        nm = p.get("name") or ""
        if not any(k.lower() in nm.lower() for k in RIVER_KEEP):
            continue
        g = shape(f["geometry"]).simplify(0.004, preserve_topology=True)
        ls = lines_of(g)
        if not ls:
            continue
        rivers.append({"n": nm, "k": min(int(p.get("scalerank") or 5), 5),
                       "l": [encode(l, scale=SCALE) for l in ls]})
    print(f"河流 {len(rivers)} 条")

    # 湖泊
    lk = json.load(open(os.path.join(RAW, "lakes.geojson")))
    lakes = []
    for f in lk["features"]:
        p = f["properties"]
        g = shape(f["geometry"])
        if g.area < 0.02:
            continue
        g = g.simplify(0.002, preserve_topology=True)
        rs = rings_of(g)
        if not rs:
            continue
        lakes.append({"n": p.get("name") or "lake", "k": min(int(p.get("scalerank") or 3), 5),
                      "r": [encode(r, scale=SCALE) for r in rs]})
    print(f"湖泊 {len(lakes)} 个")

    js = f'''/**
 * 安纳托利亚底图（现代省界 + 水系） — Lossless VLQ Delta-Encoded
 * 数据源: Natural Earth 1:10m (public domain) admin-1 / rivers / lakes
 * 格式与江山时序 (github.com/DeanChensj/jiangshan-map, GPL-3.0) 一致
 */
(function () {{
  'use strict';
  const A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-';
  const R = new Uint8Array(128);
  for (let i = 0; i < 64; i++) R[A.charCodeAt(i)] = i;
  function dec(s) {{
    const r = [];
    let i = 0, n = s.length, x = 0, y = 0;
    while (i < n) {{
      let b, sh = 0, v = 0;
      do {{ b = R[s.charCodeAt(i++)]; v |= (b & 31) << sh; sh += 5; }} while (b >= 32);
      x += (v & 1) ? ~(v >>> 1) : (v >>> 1);
      sh = 0; v = 0;
      do {{ b = R[s.charCodeAt(i++)]; v |= (b & 31) << sh; sh += 5; }} while (b >= 32);
      y += (v & 1) ? ~(v >>> 1) : (v >>> 1);
      r.push([x / 1000, y / 1000]);
    }}
    return r;
  }}
  const P = {json.dumps(provinces, ensure_ascii=False)};
  for (let i = 0; i < P.length; i++) {{
    P[i].rings = P[i].rings.map((poly) => poly.map(dec));
  }}
  window.PROVINCE_OUTLINES = P;
  const HR = {json.dumps(rivers, ensure_ascii=False)};
  const HL = {json.dumps(lakes, ensure_ascii=False)};
  const HT = {json.dumps(WATER_LABELS, ensure_ascii=False)};
  window.HYDRO_DATA = {{
    rivers: HR.map((r) => ({{ name: r.n, rank: r.k, appear: r.a, vanish: r.v, lines: r.l.map(dec) }})),
    lakes: HL.map((l) => ({{ name: l.n, rank: l.k, appear: l.a, vanish: l.v, rings: l.r.map(dec) }})),
    labels: HT,
    paleoSea: [],
  }};
}})();
'''
    dst = os.path.join(ROOT, "js", "china_geo_data.js")
    open(dst, "w", encoding="utf-8").write(js)
    print(f"写入 {dst} ({os.path.getsize(dst)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
