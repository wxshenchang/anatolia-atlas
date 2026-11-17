#!/usr/bin/env python3
"""安纳托利亚历史地图集 v2 —— 规则驱动生成器（45 个快照）
思路：
  ZONES      = 24 个历史地理区（省界合并，沿海另做海陆裁剪）
  POLITY_SPANS = [政权, 颜色, [地理区], 起始年, 终止年]  ← 加一行规则就多一段历史
  SNAP_YEARS   = 采样年份 + 文案
生成：data/atlas/<key>/s_<key>.geojson + index.json
精度处理：
  1) 所有多边形与陆地求交（不越海）
  2. simplify 0.004（比 v1 的 0.01 细一倍多）
  3. 关键河道边界（哈里斯河、幼发拉底河）按河流缓冲带切分地理区
"""
import json
import os

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "_build", "raw")
OUT_ATLAS = os.path.join(ROOT, "data", "atlas")

admin1 = json.load(open(os.path.join(RAW, "admin1.geojson")))
countries = json.load(open(os.path.join(RAW, "countries.geojson")))
rivers = json.load(open(os.path.join(RAW, "rivers.geojson")))

prov = {}
for f in admin1["features"]:
    p = f["properties"]
    if p.get("adm0_a3") == "TUR":
        prov[p["name"]] = shape(f["geometry"])

ctry = {}
ctry_by_name = {}
for f in countries["features"]:
    p = f["properties"]
    iso = p.get("ADM0_A3")
    g = shape(f["geometry"])
    if iso:
        ctry[iso] = g
    nm = p.get("NAME")
    if nm:
        ctry_by_name[nm] = g

LAND = unary_union([g for g in ctry.values() if not g.is_empty])

# ---------------------------------------------------------------- 24 个历史地理区
ZONES = {
    "thrace":       ["Edirne", "Kirklareli", "Tekirdag", "Istanbul"],
    "troad":        ["Çanakkale"],
    "mysia":        ["Balikesir"],
    "ionia":        ["Izmir"],
    "lydia":        ["Manisa", "Usak", "Aydin"],
    "caria":        ["Mugla", "Denizli"],
    "lycia":        ["Antalya"],
    "pisidia":      ["Isparta", "Burdur"],
    "phrygia":      ["Afyonkarahisar", "Kütahya", "Eskisehir"],
    "bithynia":     ["Bursa", "Bilecik", "Yalova", "Kocaeli"],
    "paphlagonia":  ["Kastamonu", "Sinop", "Bartın", "Karabük", "Zinguldak", "Sakarya", "Düzce", "Bolu"],
    "pontus":       ["Samsun", "Ordu", "Giresun", "Trabzon", "Rize", "Artvin",
                     "Tokat", "Amasya", "Gümüshane", "Bayburt"],
    "cappadocia":   ["Nevsehir", "Kayseri", "Nigde", "Aksaray", "Kirsehir", "Kinkkale"],
    "galatia":      ["Ankara", "Yozgat", "Çorum", "Çankiri", "Karaman"],
    "lycaonia":     ["Konya"],
    "cilicia":      ["Mersin", "Adana", "Osmaniye", "K. Maras"],
    "hatay":        ["Hatay"],
    "armenia_min":  ["Sivas", "Erzincan", "Elazig", "Tunceli"],
    "armenia_maj":  ["Kars", "Ardahan", "Iğdir", "Erzurum", "Agri", "Mus", "Bingöl"],
    "urartu":       ["Van", "Bitlis", "Hakkari", "Siirt", "Sirnak"],
    "upper_mes":    ["Diyarbakir", "Mardin", "Batman", "Sanliurfa", "Adiyaman", "Gaziantep", "Kilis"],
    "greece":       [], "bulgaria": [], "georgia": [], "armenia": [],
    "iran": [], "iraq": [], "syria": [], "cyprus": [], "nakhchivan": [],
    # 南界扩到 29.5°N 后新增：埃及与黎凡特（整块国家多边形，见 NEIGH）
    "egypt": [], "israel": [], "palestine": [], "lebanon": [], "jordan": [],
}
NEIGH = {"greece": "GRC", "bulgaria": "BGR", "georgia": "GEO", "armenia": "ARM",
         "iran": "IRN", "iraq": "IRQ", "syria": "SYR", "cyprus": ["CYP", "CYN"], "nakhchivan": "AZE",
         # 南界扩到 29.5°N 后新增：埃及与黎凡特
         "egypt": "EGY", "israel": "ISR", "palestine": "PSX", "lebanon": "LBN", "jordan": "JOR"}

ZONE_G = {}
# 塞浦路斯的联合国缓冲区单独是一个多边形，并进去才是一整座岛
_CY_EXTRA = []
for z, names in ZONES.items():
    if z in NEIGH:
        codes = NEIGH[z]
        codes = codes if isinstance(codes, (list, tuple)) else [codes]
        gs = [ctry[c] for c in codes if c in ctry]
        if z == "cyprus":
            # 整座岛：Cyprus + N. Cyprus + 联合国缓冲区（NE 拆成三块）
            gs = [g for nm, g in ctry_by_name.items() if str(nm).startswith("Cyprus")] or gs
        if gs:
            ZONE_G[z] = unary_union(gs)
        continue
    parts = [prov[n] for n in names if n in prov]
    if parts:
        ZONE_G[z] = unary_union(parts)

# ---------------------------------------------------------------- 政权 × 地理区 × 年代
# 一行 = 一个政权在若干地理区、某一时段的控制（安纳托利亚历史的骨架）
# 注意：同一区在同一年份如有多条命中，按列表顺序前者优先（越早定义越“强”）
W = "#"  # 占位，避免误读
SPANS = [
    # 赫梯
    ("赫梯帝国", "#a8452f", ["galatia", "cappadocia", "lycaonia", "armenia_min", "upper_mes"], -1650, -1400),
    ("赫梯帝国", "#a8452f", ["galatia", "cappadocia", "lycaonia", "armenia_min", "upper_mes", "cilicia", "hatay"], -1400, -1180),
    ("阿尔扎瓦诸国", "#6f8f4e", ["ionia", "lydia", "caria", "lycia", "pisidia", "mysia"], -1650, -1300),
    ("卡什卡诸部", "#7a6a8a", ["paphlagonia", "pontus"], -1650, -1180),
    ("米坦尼", "#c1913a", ["syria"], -1500, -1260),
    ("阿黑亚瓦", "#5f8f9f", ["troad"], -1400, -1180),
    ("迈锡尼希腊", "#4f7f7f", ["greece"], -1650, -1100),
    ("埃及新王国", "#3f6f8f", ["hatay"], -1500, -1180),
    ("埃及新王国", "#3f6f8f", ["syria"], -1550, -1170),
    ("阿拉西亚", "#5f7f8f", ["cyprus"], -1650, -1150),
    ("塞浦路斯诸城邦", "#6f8f7f", ["cyprus"], -1150, -545),
    ("罗马行省·塞浦路斯", "#8f3f3f", ["cyprus"], -58, 330),
    ("拜占庭（塞浦路斯）", "#8f5f7f", ["cyprus"], 688, 965),
    ("塞浦路斯军区", "#8f3f6f", ["cyprus"], 965, 1191),
    ("卢西尼昂塞浦路斯", "#b8892f", ["cyprus"], 1191, 1489),
    ("威尼斯共和国", "#8f3f4f", ["cyprus"], 1489, 1571),
    ("奥斯曼帝国", "#a8452f", ["cyprus"], 1683, 1878),
    # 崩溃与铁器早期
    ("卢维新赫梯诸邦", "#9a7a3a", ["upper_mes", "cilicia", "hatay"], -1180, -717),
    ("弗里吉亚", "#8a5a2b", ["phrygia", "galatia", "lydia", "mysia", "troad"], -1180, -695),
    ("乌拉尔图", "#5f6f9f", ["urartu", "armenia_maj", "armenia_min"], -860, -590),
    ("吕基亚与卡里亚", "#6f8f4e", ["lycia", "caria", "pisidia"], -1180, -546),
    ("爱奥尼亚城邦", "#3f7f7f", ["ionia"], -1180, -546),
    ("亚述帝国", "#a8452f", ["iraq", "syria"], -911, -609),
    ("希腊城邦", "#4f6f8f", ["greece"], -1100, -338),
    ("色雷斯诸部", "#7a6a5a", ["thrace"], -1180, -510),
    ("比提尼亚与帕弗拉戈尼亚", "#5f7f6f", ["bithynia", "paphlagonia"], -1180, -546),
    ("本都与卡帕多细亚", "#8f7f4a", ["pontus", "cappadocia"], -1180, -546),
    # 吕底亚 / 米底 / 新巴比伦
    ("吕底亚王国", "#b8892f", ["lydia", "ionia", "mysia", "troad", "phrygia", "caria", "pisidia"], -680, -546),
    ("埃兰", "#b07a3a", ["iran"], -3200, -660),
    ("米底王国", "#7a5a8a", ["armenia_maj", "armenia_min", "urartu", "iran", "upper_mes"], -678, -549),
    ("古巴比伦", "#9a7a3a", ["iraq"], -1894, -1595),
    ("古巴比伦", "#9a7a3f", ["syria"], -1750, -1595),
    ("新巴比伦", "#8f5a3a", ["syria", "iraq"], -626, -539),
    ("吕基亚", "#6f8f4e", ["lycia"], -680, -546),
    ("奇里乞亚诸邦", "#9a7a5a", ["cilicia", "hatay"], -1180, -334),
    # 阿契美尼德
    ("阿契美尼德帝国", "#9a5f8f", ["lydia", "ionia", "mysia", "troad", "phrygia", "caria", "lycia",
                                  "pisidia", "bithynia", "paphlagonia", "pontus", "cappadocia",
                                  "galatia", "lycaonia", "armenia_min", "armenia_maj",
                                  "iran", "iraq", "syria", "upper_mes", "urartu", "thrace", "cyprus"], -546, -334),
    ("斯基泰与高加索诸部", "#7a7a6a", ["georgia"], -700, -330),
    ("希腊城邦", "#4f6f8f", ["greece"], -338, -146),
    # 希腊化
    ("马其顿帝国", "#8f6f3f", ["thrace", "troad", "mysia", "ionia", "lydia", "caria", "phrygia",
                              "bithynia", "paphlagonia", "cappadocia", "lycaonia", "cilicia",
                              "iran", "iraq", "syria"],
     -330, -323),
    ("利西马科斯王国", "#8f6f3f", ["thrace", "troad", "mysia", "ionia", "lydia", "phrygia", "bithynia"], -323, -281),
    ("塞琉古王国", "#b8892f", ["cappadocia", "galatia", "lycaonia", "upper_mes", "syria", "iraq",
                              "iran", "cilicia", "hatay", "armenia_maj"], -312, -140),
    ("帕加马王国", "#b8892f", ["troad", "mysia", "ionia", "lydia", "caria", "phrygia", "pisidia"], -281, -133),
    ("本都王国", "#a8452f", ["pontus", "paphlagonia", "armenia_min"], -281, -63),
    ("比提尼亚王国", "#5f7f6f", ["bithynia"], -281, -74),
    ("卡帕多细亚王国", "#8f7f4a", ["cappadocia", "lycaonia"], -332, 17),
    ("加拉太诸部", "#7a6a5a", ["galatia"], -278, -25),
    ("吕基亚联盟", "#6f8f4e", ["lycia"], -168, -43),
    ("亚美尼亚王国", "#5f6f9f", ["armenia_maj", "urartu", "georgia"], -321, 428),
    ("罗马共和国", "#8f3f3f", ["greece"], -146, -27),
    ("托勒密埃及", "#a8942f", ["cyprus", "syria"], -301, -58),
    # 罗马
    ("罗马亚细亚行省", "#8f3f3f", ["troad", "mysia", "ionia", "lydia", "caria", "phrygia", "pisidia", "lycia"], -133, 330),
    ("罗马比提尼亚与本都", "#a8452f", ["bithynia", "paphlagonia", "pontus"], -63, 330),
    ("罗马奇里乞亚", "#9a5f4f", ["cilicia", "hatay"], -64, 330),
    ("罗马东部行省", "#8f3f3f", ["cappadocia", "galatia", "lycaonia", "armenia_min", "upper_mes",
                                       "thrace", "armenia_maj"], 17, 330),
    ("科马基尼王国", "#7a6a5a", ["upper_mes"], -163, 72),
    ("帕提亚帝国", "#7a5a8a", ["iraq", "iran"], -141, 224),
    ("萨珊波斯", "#7a5a8a", ["iraq", "iran", "urartu"], 224, 651),
    # 拜占庭
    ("拜占庭帝国", "#8f3f6f", ["thrace", "troad", "mysia", "ionia", "lydia", "caria", "lycia", "pisidia",
                              "phrygia", "bithynia", "paphlagonia", "pontus", "cappadocia", "galatia",
                              "lycaonia", "cilicia", "hatay", "armenia_min", "greece", "cyprus"], 330, 1071),
    ("阿拉伯哈里发国", "#3f7f6f", ["syria", "iraq", "iran", "upper_mes", "armenia_maj"], 636, 1055),
    ("亚美尼亚诸国", "#5f6f9f", ["armenia_maj", "urartu", "georgia"], 428, 1071),
    ("保加尔汗国", "#7a5a5a", ["bulgaria"], 632, 1018),
    # 塞尔柱
    ("罗姆苏丹国", "#3f8f6a", ["lycaonia", "cappadocia", "galatia", "phrygia", "pisidia", "hatay"], 1077, 1308),
    ("丹麦门德王朝", "#8f6f3f", ["pontus", "armenia_min", "paphlagonia"], 1071, 1178),
    ("拜占庭帝国", "#8f3f6f", ["thrace", "troad", "mysia", "ionia", "lydia", "caria", "lycia", "bithynia"], 1071, 1204),
    ("花剌子模", "#4f7f8f", ["iran"], 1194, 1231),
    ("花剌子模", "#4f7f8f", ["urartu", "armenia_maj"], 1220, 1231),
    ("尼西亚帝国", "#6f5f8f", ["bithynia", "mysia", "troad", "ionia", "lydia"], 1204, 1261),
    ("特拉比松帝国", "#5f8f9f", ["pontus"], 1204, 1461),
    ("奇里乞亚亚美尼亚", "#a8942f", ["cilicia"], 1198, 1375),
    ("拜占庭帝国", "#8f3f6f", ["thrace", "bithynia", "mysia"], 1261, 1453),
    ("阿尤布王朝", "#7a7a3a", ["syria", "upper_mes"], 1171, 1260),
    ("大塞尔柱帝国", "#9a5f5f", ["iran"], 1037, 1194),
    ("十字军国家", "#b8892f", ["cyprus", "hatay"], 1098, 1291),
    # 蒙古与贝伊国
    ("伊儿汗国宗主权", "#7a5a8a", ["galatia", "cappadocia", "lycaonia", "armenia_min", "urartu",
                                "armenia_maj", "iran", "iraq", "upper_mes", "georgia"], 1243, 1335),
    ("卡拉曼贝伊国", "#3f8f6a", ["lycaonia", "cilicia", "pisidia", "hatay"], 1256, 1487),
    ("格尔米扬贝伊国", "#8f7f4a", ["phrygia"], 1300, 1429),
    ("艾登与门泰塞贝伊国", "#5f8f8f", ["ionia", "lydia", "caria"], 1300, 1426),
    ("奥斯曼贝伊国", "#a8452f", ["bithynia"], 1299, 1362),
    ("卡迪·布尔汉丁国", "#7a5a8a", ["armenia_min", "cappadocia"], 1381, 1398),
    ("黑羊王朝", "#5a5a7a", ["iran"], 1375, 1468),
    ("白羊王朝", "#9a7a5a", ["iran"], 1468, 1508),
    ("白羊王朝", "#9a7a5a", ["upper_mes", "urartu", "armenia_maj"], 1378, 1508),
    ("马木留克王朝", "#7a7a3a", ["syria", "hatay"], 1250, 1517),
    # 奥斯曼
    ("帖木儿帝国", "#7a5a4a", ["cappadocia", "armenia_min", "urartu", "upper_mes", "galatia",
                              "armenia_maj"], 1402, 1404),
    ("帖木儿帝国", "#7a5a4a", ["iran"], 1381, 1404),
    ("奥斯曼帝国", "#a8452f", ["thrace", "troad", "mysia", "ionia", "lydia", "phrygia", "bithynia",
                              "paphlagonia", "pisidia"], 1362, 1453),
    ("奥斯曼帝国", "#a8452f", ["thrace", "troad", "mysia", "ionia", "lydia", "phrygia", "bithynia",
                              "paphlagonia", "pisidia", "pontus", "galatia", "cappadocia", "lycaonia",
                              "caria", "lycia", "cilicia", "hatay", "armenia_min"], 1461, 1517),
    ("奥斯曼帝国", "#a8452f", ["thrace", "troad", "mysia", "ionia", "lydia", "phrygia", "bithynia",
                              "paphlagonia", "pisidia", "pontus", "galatia", "cappadocia", "lycaonia",
                              "caria", "lycia", "cilicia", "hatay", "armenia_min", "armenia_maj",
                              "urartu", "upper_mes", "syria", "iraq", "cyprus", "greece", "bulgaria"], 1517, 1683),
    ("奥斯曼帝国", "#a8452f", ["thrace", "troad", "mysia", "ionia", "lydia", "phrygia", "bithynia",
                              "paphlagonia", "pisidia", "pontus", "galatia", "cappadocia", "lycaonia",
                              "caria", "lycia", "cilicia", "hatay", "armenia_min", "armenia_maj",
                              "urartu", "upper_mes", "syria", "iraq"], 1683, 1922),
    ("萨法维波斯", "#7a5a8a", ["iran", "georgia"], 1501, 1736),
    ("阿夫沙尔王朝", "#8a6a4a", ["iran"], 1736, 1747),
    ("赞德王朝", "#8a7a5a", ["iran"], 1747, 1794),
    ("恺加王朝", "#8a5a6a", ["iran"], 1794, 1925),
    ("巴列维王朝", "#6a6a8a", ["iran"], 1925, 1935),
    ("俄罗斯帝国", "#5f6f9f", ["georgia", "armenia_maj"], 1801, 1917),
    ("希腊王国", "#4f6f8f", ["greece"], 1832, 1924),
    ("希腊共和国", "#3f5f7f", ["greece"], 1924, 1935),
    ("希腊王国", "#4f6f8f", ["greece"], 1935, 1973),
    ("希腊共和国", "#3f5f7f", ["greece"], 1973, 2026),
    ("保加利亚", "#7a5a5a", ["bulgaria"], 1878, 2026),
    ("英属塞浦路斯", "#8f5f8f", ["cyprus"], 1878, 1960),
    # 共和国
    ("土耳其共和国", "#a8452f", ["thrace", "troad", "mysia", "ionia", "lydia", "phrygia", "bithynia",
                                "paphlagonia", "pisidia", "pontus", "galatia", "cappadocia", "lycaonia",
                                "caria", "lycia", "cilicia", "hatay", "armenia_min", "armenia_maj",
                                "urartu", "upper_mes"], 1923, 2026),
    ("叙利亚", "#3f7f6f", ["syria"], 1946, 2026),
    ("伊拉克", "#7a7a3a", ["iraq"], 1932, 2026),
    ("伊朗", "#7a5a8a", ["iran"], 1935, 2026),
    ("亚美尼亚", "#9a7a5a", ["armenia"], 1991, 2026),
    ("格鲁吉亚", "#5f6f9f", ["georgia"], 1991, 2026),
    ("塞浦路斯", "#b8892f", ["cyprus"], 1960, 2026),
    # ================================================================ 南界扩展：埃及
    ("古埃及", "#c9a227", ["egypt"], -3100, -1550),
    ("埃及新王国", "#3f6f8f", ["egypt"], -1550, -1070),
    ("埃及第三中间期诸王朝", "#b0952f", ["egypt"], -1070, -664),
    ("埃及后王朝", "#b0952f", ["egypt"], -664, -525),
    ("阿契美尼德帝国（埃及行省）", "#9a5f8f", ["egypt"], -525, -404),
    ("埃及本土诸王朝", "#b0952f", ["egypt"], -404, -343),
    ("阿契美尼德帝国（埃及行省）", "#9a5f8f", ["egypt"], -343, -332),
    ("托勒密埃及", "#a8942f", ["egypt"], -332, -30),
    ("罗马埃及行省", "#8f3f3f", ["egypt"], -30, 395),
    ("拜占庭埃及", "#8f3f6f", ["egypt"], 395, 641),
    ("阿拉伯哈里发国（埃及）", "#3f7f6f", ["egypt"], 641, 969),
    ("法蒂玛王朝", "#3f8f6a", ["egypt"], 969, 1171),
    ("阿尤布王朝", "#7a7a3a", ["egypt"], 1171, 1250),
    ("马木留克王朝", "#7a7a3a", ["egypt"], 1250, 1517),
    ("奥斯曼帝国（埃及行省）", "#a8452f", ["egypt"], 1517, 1805),
    ("穆罕默德·阿里王朝", "#8f7f4a", ["egypt"], 1805, 1882),
    ("英属埃及", "#8f5f8f", ["egypt"], 1882, 1922),
    ("埃及王国", "#c9a227", ["egypt"], 1922, 1953),
    ("埃及", "#c9a227", ["egypt"], 1953, 2026),
    # ================================================================ 迦南与腓尼基
    ("埃及新王国（迦南）", "#3f6f8f", ["israel", "palestine", "lebanon"], -1550, -1170),
    ("早期迦南诸城邦", "#c1913a", ["israel", "palestine"], -3500, -1550),
    ("比布鲁斯与腓尼基早期城邦", "#5f7f8f", ["lebanon"], -3000, -1550),
    ("外约旦早期诸部", "#b08f4a", ["jordan"], -3500, -1200),
    ("迦南诸城邦", "#c1913a", ["israel", "palestine"], -1170, -1020),
    ("腓尼基城邦", "#5f7f8f", ["lebanon"], -1550, -539),
    ("以色列王国与犹大王国", "#6f8f4e", ["israel", "palestine"], -1020, -586),
    ("新巴比伦（黎凡特）", "#8f5a3a", ["israel", "palestine", "lebanon", "jordan"], -586, -539),
    ("阿契美尼德帝国（黎凡特）", "#9a5f8f", ["israel", "palestine", "lebanon", "jordan"], -539, -332),
    ("马其顿帝国（黎凡特）", "#8f6f3f", ["israel", "palestine", "lebanon", "jordan"], -332, -323),
    ("继业者割据（黎凡特）", "#8f7f4f", ["israel", "palestine", "lebanon", "jordan"], -323, -312),
    ("塞琉古王国（黎凡特）", "#b8892f", ["israel", "palestine", "lebanon"], -312, -140),
    ("哈斯蒙尼王国", "#7a8f4e", ["israel", "palestine"], -140, -63),
    ("罗马犹太行省", "#8f3f3f", ["israel", "palestine", "lebanon", "jordan"], -63, 395),
    ("拜占庭帝国（黎凡特）", "#8f3f6f", ["israel", "palestine", "lebanon"], 395, 636),
    ("阿拉伯哈里发国（黎凡特）", "#3f7f6f", ["israel", "palestine", "lebanon", "jordan"], 636, 1099),
    ("耶路撒冷王国", "#b8892f", ["israel", "palestine", "lebanon", "jordan"], 1099, 1291),
    ("马木留克王朝（黎凡特）", "#7a7a3a", ["israel", "palestine", "lebanon", "jordan"], 1291, 1517),
    ("奥斯曼帝国（黎凡特）", "#a8452f", ["israel", "palestine", "lebanon", "jordan"], 1517, 1920),
    ("英属巴勒斯坦托管地", "#8f5f8f", ["israel", "palestine", "jordan"], 1920, 1948),
    ("英属巴勒斯坦托管地", "#8f5f8f", ["lebanon"], 1920, 1923),
    ("以色列", "#4f6f8f", ["israel"], 1948, 2026),
    ("约旦与埃及占领区", "#9a8f6a", ["palestine"], 1948, 1988),
    ("巴勒斯坦", "#4f8f6f", ["palestine"], 1988, 2026),
    ("黎巴嫩", "#8f4f5f", ["lebanon"], 1943, 2026),
    ("法属叙利亚托管地", "#8f5f8f", ["lebanon", "syria"], 1920, 1943),
    # ================================================================ 外约旦
    ("外约旦诸王国（亚扪、摩押、以东）", "#c1913a", ["jordan"], -1200, -582),
    ("新巴比伦（外约旦）", "#8f5a3a", ["jordan"], -582, -539),
    ("阿契美尼德帝国（外约旦）", "#9a5f8f", ["jordan"], -539, -332),
    ("马其顿帝国（外约旦）", "#8f6f3f", ["jordan"], -332, -312),
    ("塞琉古与纳巴泰", "#b8892f", ["jordan"], -312, -168),
    ("纳巴泰王国", "#a8742f", ["jordan"], -168, 106),
    ("罗马阿拉伯行省", "#8f3f3f", ["jordan"], 106, 395),
    ("拜占庭阿拉伯行省", "#8f3f6f", ["jordan"], 395, 636),
    ("阿拉伯哈里发国（外约旦）", "#3f7f6f", ["jordan"], 636, 1099),
    ("耶路撒冷王国（外约旦）", "#b8892f", ["jordan"], 1099, 1187),
    ("阿尤布王朝（外约旦）", "#7a7a3a", ["jordan"], 1187, 1291),
    ("马木留克王朝（外约旦）", "#7a7a3a", ["jordan"], 1291, 1517),
    ("奥斯曼帝国（外约旦）", "#a8452f", ["jordan"], 1517, 1920),
    ("约旦", "#8f8f4a", ["jordan"], 1946, 2026),
    # ================================================================ 两河南部（巴比伦尼亚）
    ("苏美尔城邦", "#b8952f", ["iraq"], -3500, -2334),
    ("阿卡德帝国", "#9a6f3f", ["iraq", "syria"], -2334, -2154),
    ("乌尔第三王朝", "#a8852f", ["iraq"], -2112, -2004),
    ("伊辛与拉尔萨", "#9a7a3a", ["iraq"], -2004, -1894),
    ("加喜特巴比伦", "#8a6a3a", ["iraq"], -1595, -1155),
    ("巴比伦与亚述并立", "#8a6a3a", ["iraq"], -1155, -911),
    ("英属美索不达米亚", "#8f5f8f", ["iraq"], 1920, 1932),
    # ================================================================ 叙利亚补缺
    ("埃勃拉与马里", "#c1913a", ["syria"], -2400, -1600),
    ("阿拉米大马士革", "#8f6f4a", ["syria"], -1180, -732),
    ("罗马叙利亚行省", "#8f3f3f", ["syria"], -63, 395),
    ("拜占庭叙利亚行省", "#8f3f6f", ["syria"], 395, 636),
    ("叙利亚塞尔柱诸王公", "#9a5f5f", ["syria"], 1055, 1127),
    ("赞吉王朝", "#8f5f4f", ["syria"], 1127, 1171),
]

# ---------------------------------------------------------------- 45 个采样年份
SNAPS = [
    (-3000, "sumer_dawn", "苏美尔城邦时代", "乌鲁克、乌尔、尼普尔等神庙城市兴起，楔形文字、轮与青铜在此出现，两河南部城邦林立。"),
    (-2334, "akkad_empire", "阿卡德统一", "萨尔贡一世征服诸城邦，建立美索不达米亚第一个帝国，阿卡德语成为官方语言。"),
    (-2112, "ur_third", "乌尔第三王朝", "乌尔纳姆重建统一，颁布现存最早的法典之一，神庙与贡赋体系高度官僚化。"),
    (-1900, "isin_larsa", "伊辛与拉尔萨并立", "乌尔第三王朝崩溃后阿摩利诸王朝分据，巴比伦尚是其中不起眼的一支。"),
    (-1750, "hammurabi", "汉谟拉比统一两河", "汉谟拉比击败拉尔萨与马里，法典刻石传世，巴比伦的马尔杜克升为全国主神。"),
    (-1650, "hittite_old", "赫梯古王国", "哈图西里一世定都哈图沙，赫梯登上安纳托利亚舞台；阿尔扎瓦诸国据西部。"),
    (-1600, "hittite_early", "赫梯早期扩张", "穆尔西里一世南征叙利亚，前 1595 年劫掠巴比伦后因内乱退兵。"),
    (-1595, "babylon_sack", "穆尔西里一世灭古巴比伦", "穆尔西里一世沿幼发拉底南下攻陷巴比伦，古巴比伦第一王朝终结；赫梯因后方空虚随即内乱。"),
    (-1500, "hittite_mid", "赫梯中王国", "帝国中衰，卡什卡诸部南下侵扰北境，米坦尼在叙利亚称雄。"),
    (-1400, "hittite_recovery", "赫梯复兴", "图特哈里二世重整国力，重新插手叙利亚，与米坦尼、埃及三方角力。"),
    (-1350, "hittite_empire", "赫梯帝国鼎盛", "苏庇路里乌玛一世击溃米坦尼，赫梯成为近东两大强权之一。"),
    (-1295, "hittite_late_peak", "穆瓦塔里二世迁都", "迁都塔胡恩塔萨（今土耳其南部），与埃及在叙利亚长期对峙。"),
    (-1274, "qadesh", "卡迭石之战", "穆瓦塔里二世与埃及拉美西斯二世在奥龙特斯河畔会战，前 1259 年缔和。"),
    (-1230, "hittite_twilight", "赫梯晚期", "图特哈里四世应对海上民族与西部卡什卡的压力，帝国衰落但尚未瓦解。"),
    (-1180, "bronze_collapse", "青铜时代崩溃", "海上民族与系统性崩溃终结赫梯帝国，安纳托利亚进入黑暗时代。"),
    (-1100, "post_collapse", "崩溃之后", "新赫梯诸邦在东南延续，弗里吉亚人据中西部，安纳托利亚无统一强权。"),
    (-1000, "dark_age", "铁器早期", "弗里吉亚人、新赫梯诸邦与乌拉尔图在废墟上兴起，东部进入铁器时代。"),
    (-950, "phrygia_rise", "弗里吉亚兴起", "戈尔迪乌姆成为中西部中心，乌拉尔图在凡湖成型。"),
    (-860, "urartu_rise", "乌拉尔图崛起", "图什帕（凡城）为都，乌拉尔图与亚述争雄东部高原。"),
    (-800, "assyria_pressure", "亚述西进", "提格拉特帕拉沙尔三世以降，亚述逼近叙利亚与东南安纳托利亚。"),
    (-750, "phrygia_peak", "弗里吉亚鼎盛", "戈尔迪乌姆的迈达斯王统辖中西部，爱奥尼亚希腊城邦沿海兴起。"),
    (-700, "urartu_peak", "乌拉尔图鼎盛", "阿尔吉什提一世扩张至亚美尼亚高原，与亚述争夺东部霸权。"),
    (-695, "cimmerian", "辛梅里安之乱", "辛梅里安人自高加索南下攻灭弗里吉亚，吕底亚开始崛起。"),
    (-650, "lydia_rise", "吕底亚崛起", "古革斯王朝据萨第斯，与亚述结盟抗辛梅里安；小亚细亚最早的钱币出现。"),
    (-620, "assyria_fall", "亚述灭亡", "尼尼微陷落，米底与新巴比伦瓜分亚述；吕底亚趁势西进。"),
    (-585, "halys_battle", "哈里斯河之战", "吕底亚与米底以克孜勒河为界，日食之年双方罢兵。"),
    (-550, "cyrus_rise", "居鲁士崛起", "波斯人推翻米底，居鲁士二世兵临哈里斯河，吕底亚危在旦夕。"),
    (-546, "cyrus_conquest", "居鲁士灭吕底亚", "萨第斯陷落，安纳托利亚西部并入阿契美尼德帝国。"),
    (-500, "ionian_revolt", "爱奥尼亚起义", "米利都求援雅典，波斯行省体制遭受挑战，希波战争前夜。"),
    (-480, "persian_wars", "希波战争", "薛西斯一世渡赫勒斯滂，萨拉米斯海战后波斯西进受阻。"),
    (-420, "persian_late", "波斯行省晚期", "安纳托利亚诸行省由半独立邦君治理，波斯中央控制松弛。"),
    (-386, "kings_peace", "大王和约", "《安塔尔基达斯和约》把西部希腊城邦交还波斯，阿契美尼德重控安纳托利亚。"),
    (-360, "satrap_revolt", "总督叛乱", "西部总督连年叛乱（大数总督之战），为马其顿东进铺路。"),
    (-334, "alexander", "亚历山大东征", "格拉尼库斯之战后小亚细亚诸城次第归附，波斯统治动摇。"),
    (-325, "alexander_east", "亚历山大末期", "东征结束后继业者整军，安纳托利亚由各将分领。"),
    (-323, "alexander_death", "亚历山大卒", "巴比伦分封，安纳托利亚成为继业者争夺的主战场。"),
    (-301, "ipsus", "伊普苏斯之战", "安提柯阵亡，安纳托利亚三分：利西马科斯、塞琉古、本土王朝并立。"),
    (-281, "curupedium", "库鲁佩迪安之战", "利西马科斯战死，塞琉古短暂统一小亚细亚；帕加马、本都、比提尼亚自立。"),
    (-278, "galatian_invasion", "加拉太人入侵", "凯尔特部族定居安纳托利亚中部，成为各王国的雇佣兵与边患。"),
    (-250, "galatia_settled", "加拉太定局", "凯尔特诸部定居中部高原，成为各王国争相雇佣的兵源。"),
    (-240, "attalid_power", "阿塔罗斯王朝", "阿塔罗斯一世击败加拉太人，帕加马成为西部最强王国。"),
    (-190, "magnesia", "马格尼西亚之战", "罗马击败塞琉古安条克三世，势力首次深入小亚细亚。"),
    (-188, "apamea", "阿帕米亚和约", "塞琉古退出托罗斯山以北，帕加马取得小亚细亚大部。"),
    (-133, "asia_province", "亚细亚行省", "阿塔罗斯三世遗赠帕加马，罗马在亚洲的第一个行省设立。"),
    (-100, "provincial_asia", "行省制成形", "亚细亚行省与比提尼亚、卡帕多细亚等附庸王国并存的结构稳固。"),
    (-88, "mithridatic", "米特里达梯战争", "本都国王发动“亚洲晚祷”，罗马在东方的统治遭重创。"),
    (-63, "pompey_east", "庞培重组东方", "本都王国灭亡、塞琉古被废，比提尼亚-本都与奇里乞亚行省设立。"),
    (-31, "actium", "亚克兴之后", "屋大维战胜安东尼，东方行省重新划分，元首制时代开始。"),
    (-27, "augustus", "奥古斯都时代", "元首制确立，东方行省进入长期和平；以弗所、帕加马繁盛。"),
    (70, "flavian", "弗拉维王朝", "行省城市化推进，道路网与皇帝崇拜庙宇遍布西部城市。"),
    (117, "trajan_peak", "图拉真极盛", "短暂设立亚美尼亚与美索不达米亚行省，帝国东部达波斯湾。"),
    (200, "severan", "塞维鲁时代", "帕提亚转萨珊，东方边境压力上升，军团驻防加重。"),
    (260, "crisis_3c", "三世纪危机", "埃德萨之战瓦勒良被俘，萨珊崛起压迫东方边境。"),
    (300, "tetrarchy", "四帝共治", "戴克里先行省改革细分行省，安纳托利亚被划入多个新行省与教区。"),
    (330, "constantinople", "君士坦丁堡建都", "拜占庭改名君士坦丁堡，帝国重心东移。"),
    (450, "theodosian", "狄奥多西之后", "451 年卡尔西顿公会议确立安纳托利亚教会格局，城市文明稳定。"),
    (550, "justinian", "查士丁尼时代", "收复西部与北非，编《民法大全》；安纳托利亚行省城市繁荣。"),
    (600, "heracleius", "希拉克略时代", "东罗马与萨珊长达三十年的大战，安纳托利亚被反复劫掠。"),
    (640, "arab_conquest", "阿拉伯征服", "雅尔穆克战役后叙利亚失守，安纳托利亚成为拜占庭与哈里发的边境地带。"),
    (700, "arab_raids", "阿拉伯袭掠", "君士坦丁堡两次被围后，边境沿托罗斯山形成无人区与要塞线。"),
    (800, "theme_system", "军区制时代", "安纳托利亚、阿尔梅尼亚克等军区成形，与阿拉伯人长期拉锯。"),
    (900, "byz_recovery", "拜占庭反攻", "收复爱琴海岛屿与东部军区失地，向奇里乞亚推进。"),
    (970, "macedonian", "马其顿王朝中兴", "尼基弗鲁斯二世收复奇里乞亚与安条克，帝国转入反攻。"),
    (1025, "basil_death", "巴西尔二世身后", "帝国疆域极盛而军力内耗，中央集权松弛，边防将领自立。"),
    (1071, "manzikert", "曼齐刻尔特之战", "罗曼努斯四世战败被俘，突厥人进入安纳托利亚腹地。"),
    (1097, "first_crusade", "第一次十字军", "尼西亚、多里莱乌姆之战后拜占庭收复西部沿海，十字军东进。"),
    (1120, "crusader_early", "十字军国家初立", "耶路撒冷王国、安条克公国与的黎波里伯国立足，叙利亚的塞尔柱王公内斗；赞吉王朝尚未兴起。"),
    (1150, "danismend_end", "丹麦门德衰亡", "罗姆苏丹国兼并中北安纳托利亚，突厥人的地方政权趋于统一。"),
    (1176, "myriokephalon", "密列奥塞法隆之战", "曼努埃尔一世败于基利杰阿尔斯兰二世，拜占庭反攻终结。"),
    (1204, "fourth_crusade", "第四次十字军", "君士坦丁堡陷落，尼西亚帝国、特拉比松帝国与拉丁帝国并立。"),
    (1230, "rum_peak", "罗姆苏丹国鼎盛", "阿拉丁·凯库巴德控制地中海与黑海港口，塞尔柱商队网络达顶峰。"),
    (1243, "kosedag", "克塞山之战", "罗姆苏丹国臣属蒙古，安纳托利亚进入伊儿汗国宗主权时代。"),
    (1277, "ilkhanid_direct", "伊儿汗国直辖", "马木留克介入安纳托利亚，蒙古直接征税，经济与人口承压。"),
    (1300, "beyliks", "诸贝伊国时代", "奥斯曼、卡拉曼、格尔米扬、艾登等贝伊国在蒙古宗主权下并起。"),
    (1390, "burhaneddin", "贝伊国并立与布尔汉丁", "帖木儿南下前夜：奥斯曼、卡拉曼、布尔汉丁与白羊诸势力在安纳托利亚并立。"),
    (1402, "ankara_battle", "安卡拉之战", "帖木儿击败巴耶济德一世，奥斯曼进入十一年空位期，贝伊国复立。"),
    (1453, "conquest", "攻陷君士坦丁堡", "穆罕默德二世终结拜占庭，奥斯曼成为跨欧亚帝国。"),
    (1480, "mehmed_late", "穆罕默德二世晚年", "夺取黑海与爱琴海诸岛，行省（eyalet）制度在安纳托利亚铺开。"),
    (1517, "selim_conquests", "塞利姆一世东征", "查尔迪兰击败萨法维，灭马木留克取叙利亚与埃及。"),
    (1566, "suleiman_era", "苏莱曼时代", "帝国鼎盛：贝尔格莱德、罗得岛、巴格达与北非入版图。"),
    (1600, "celali", "杰拉里叛乱年代", "小冰期歉收、人口压力与地方武装，安纳托利亚乡村动荡。"),
    (1750, "ayan", "地方显贵时代", "地方显贵（ayan）以包税制掌握实权，中央对行省控制依赖合作。"),
    (1839, "tanzimat", "坦志麦特改革", "《花厅御诏》启动近代化改革，行省制重整。"),
    (1900, "hamidian", "哈米德时代末期", "铁路铺入安纳托利亚内陆，城市改造与近代行政推行。"),
    (1918, "wwi_end", "一战结束", "穆兹罗斯停战，帝国解体；安纳托利亚成为民族斗争战场。"),
    (1923, "republic_found", "共和国成立", "洛桑条约后土耳其共和国成立，定都安卡拉。"),
    (1935, "ataturk_end", "阿塔图尔克末年", "文字拉丁化、姓氏法、国家主义经济；1938 年凯末尔逝世。"),
    (1960, "cold_war", "冷战年代", "入北约、多党制与三次军事政变，安纳托利亚城市化加速。"),
    (1970, "industrial", "工业化与移民", "计划经济与进口替代推进，向欧洲输出劳务移民。"),
    (1990, "ozal", "厄扎尔时代", "市场化与私有化、欧盟申请，西南沿海城市与旅游业扩张。"),
    (2010, "akp_mid", "正发党中期", "城市化与区域开发工程，叙利亚战争外溢与难民问题。"),
    (2026, "present", "当代土耳其", "8500 万人口的 G20 经济体，欧盟候选国，安纳托利亚仍是文明交汇处。"),
]

LICENSE_NOTICE = ("Approximate historical boundaries for illustration, not surveyed borders. "
                  "Base blocks: Natural Earth 1:10m (public domain) + aourednik/historical-basemaps (GPL-3.0). "
                  "Period assignments follow the sources in data/sources/. "
                  "Interface adapted from Jiangshan Atlas (GPL-3.0) by DeanChensj.")


def round_coords(o):
    if isinstance(o, (list, tuple)):
        if o and isinstance(o[0], (int, float)):
            return [round(float(o[0]), 2), round(float(o[1]), 2)]
        return [round_coords(x) for x in o]
    return o


def polities_at(year):
    """返回 {政权名: (颜色, [地理区])}，同年重复命中以先定义者优先"""
    out = {}
    taken = set()
    for name, tint, zones, f, t in SPANS:
        if not (f <= year <= t):
            continue
        avail = [z for z in zones if ZONE_G.get(z) is not None and z not in taken]
        if not avail:
            continue
        if name in out:
            out[name][2].extend(avail)
        else:
            out[name] = [tint, None, avail]
        taken |= set(avail)
    return {k: (v[0], v[2]) for k, v in out.items()}


# 同一政权在不同省区的多条规则 → 合并成一条色块与大字标注。
# 只合并「省区变体」；括号本身是名字一部分的（如「外约旦诸王国（亚扪、摩押、以东）」）不合并。
MERGE_ALIAS = {
    "阿契美尼德帝国（埃及行省）": "阿契美尼德帝国",
    "阿契美尼德帝国（黎凡特）": "阿契美尼德帝国",
    "新巴比伦（黎凡特）": "新巴比伦",
    "塞琉古王国（黎凡特）": "塞琉古王国",
    "马其顿帝国（黎凡特）": "马其顿帝国",
    "埃及新王国（迦南）": "埃及新王国",
    "阿拉伯哈里发国（黎凡特）": "阿拉伯哈里发国",
    "阿拉伯哈里发国（埃及）": "阿拉伯哈里发国",
    "拜占庭帝国（黎凡特）": "拜占庭帝国",
    "拜占庭（塞浦路斯）": "拜占庭帝国",
    "马木留克王朝（黎凡特）": "马木留克王朝",
    "奥斯曼帝国（埃及行省）": "奥斯曼帝国",
    "奥斯曼帝国（黎凡特）": "奥斯曼帝国",
}


def merge_variants(pol):
    """把省区变体并入基名，返回 {显示名: (颜色, [地理区…])}"""
    out = {}
    for name, (tint, zones) in pol.items():
        disp = MERGE_ALIAS.get(name, name)
        if disp in out:
            out[disp][1].extend(zones)
        else:
            out[disp] = [tint, list(zones)]
    return {k: (v[0], v[1]) for k, v in out.items()}


def build_snapshot(year, key, caption, note):
    pol = merge_variants(polities_at(year))
    feats, names = [], []
    for name, (tint, zones) in pol.items():
        geoms = [ZONE_G[z] for z in zones]
        u = unary_union(geoms).intersection(LAND)
        if u.is_empty:
            continue
        u = u.simplify(0.004, preserve_topology=True)
        g = mapping(u)
        names.append(name)
        feats.append({
            "type": "Feature",
            "id": name,
            "properties": {
                "title": name,
                "role": "main" if not feats else "rival",
                "tint": tint,
                "anchor": None,
            },
            "geometry": {"type": g["type"], "coordinates": round_coords(g["coordinates"])},
        })
    for f in feats:
        c = shape(f["geometry"]).representative_point()
        f["properties"]["anchor"] = [round(c.x, 2), round(c.y, 2)]
    return {
        "type": "FeatureCollection",
        "license": LICENSE_NOTICE,
        "snapshot": {"caption": f"{year} 年 · {caption}" if year > 0 else f"前 {-year} 年 · {caption}",
                     "note": note, "polities": names, "regions": []},
        "features": feats,
    }


def main():
    os.makedirs(OUT_ATLAS, exist_ok=True)
    order = []
    for year, key, caption, note in SNAPS:
        d = os.path.join(OUT_ATLAS, key)
        os.makedirs(d, exist_ok=True)
        fc = build_snapshot(year, key, caption, note)
        fn = f"s_{key}"
        json.dump(fc, open(os.path.join(d, fn + ".geojson"), "w", encoding="utf-8"), ensure_ascii=False)
        order.append(fn)
        print(f"  {year:>6}  {key:20s} {len(fc['features']):2d} 政权")
    json.dump({"boot": order[:1], "order": order},
              open(os.path.join(OUT_ATLAS, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n共 {len(order)} 个快照写入 data/atlas/")


if __name__ == "__main__":
    main()
