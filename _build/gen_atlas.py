#!/usr/bin/env python3
"""安纳托利亚历史地图集 —— 第一阶段数据生成器

思路：以土耳其 81 省 + 邻国一级行政区为"底块"，按历史文献把每个时期各底块归属到政权，
再用 shapely 合并同政权底块 → 生成 data/atlas/<时期>/s_<时期>.geojson（江山时序格式）。
边界为"近似示意"，非测绘边界；出处见 data/sources/*.json。
"""
import json
import os
from collections import defaultdict

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "_build", "raw")
OUT_ATLAS = os.path.join(ROOT, "data", "atlas")
OUT_SRC = os.path.join(ROOT, "data", "sources")

admin1 = json.load(open(os.path.join(RAW, "admin1.geojson")))
countries = json.load(open(os.path.join(RAW, "countries.geojson")))

prov = {}      # 省名 -> shapely
for f in admin1["features"]:
    p = f["properties"]
    if p.get("adm0_a3") == "TUR":
        prov[p["name"]] = shape(f["geometry"])

ctry = {}      # 国家 ISO3 -> shapely（用于邻区示意块）
for f in countries["features"]:
    p = f["properties"]
    iso = p.get("ADM0_A3") or p.get("SOV_A3")
    if iso:
        ctry[iso] = shape(f["geometry"])

# ---------------------------------------------------------------- 历史地理分区
# 每个分区 = 若干现代省（边界近似历史地理区，非精确）
ZONES = {
    "thrace":       ["Edirne", "Kirklareli", "Tekirdag", "Istanbul"],
    "troad_mysia":  ["Çanakkale", "Balikesir"],
    "ionia":        ["Izmir", "Aydin"],
    "lydia":        ["Manisa", "Usak"],
    "caria":        ["Mugla", "Denizli"],
    "lycia":        ["Antalya"],
    "pisidia":      ["Isparta", "Burdur"],
    "phrygia":      ["Afyonkarahisar", "Kütahya", "Eskisehir", "Bilecik"],
    "bithynia":     ["Bursa", "Kocaeli", "Sakarya", "Düzce", "Bolu", "Yalova"],
    "paphlagonia":  ["Kastamonu", "Sinop", "Bartın", "Karabük", "Zinguldak"],
    "pontus":       ["Samsun", "Ordu", "Giresun", "Trabzon", "Rize", "Artvin",
                     "Tokat", "Amasya", "Gümüshane", "Bayburt"],
    "cappadocia":   ["Nevsehir", "Kayseri", "Nigde", "Aksaray", "Kirsehir", "Kinkkale"],
    "galatia":      ["Ankara", "Yozgat", "Çorum", "Çankiri"],
    "lycaonia":     ["Konya", "Karaman"],
    "cilicia":      ["Mersin", "Adana", "Osmaniye", "Hatay", "K. Maras"],
    "armenia_min":  ["Sivas", "Erzincan", "Elazig", "Tunceli"],
    "armenia_maj":  ["Kars", "Ardahan", "Iğdir", "Erzurum", "Agri", "Mus", "Bingöl"],
    "urartu":       ["Van", "Bitlis", "Hakkari", "Siirt", "Sirnak"],
    "upper_mes":    ["Diyarbakir", "Mardin", "Batman", "Sanliurfa", "Adiyaman", "Gaziantep", "Kilis"],
}

# 邻区示意块（用现代国家边界粗块表示，仅用于表现周边大帝国的大致范围）
NEIGHBORS = {
    "greece": "GRC", "bulgaria": "BGR", "georgia": "GEO", "armenia": "ARM",
    "nakhchivan": "AZE", "iran": "IRN", "iraq": "IRQ", "syria": "SYR", "cyprus": "CYP",
}

ZONE_GEOM = {}
for z, provinces in ZONES.items():
    parts = [prov[n] for n in provinces if n in prov]
    missing = [n for n in provinces if n not in prov]
    if missing:
        print(f"  !! 分区 {z} 缺省: {missing}")
    if parts:
        ZONE_GEOM[z] = unary_union(parts)
for z, iso in NEIGHBORS.items():
    if iso in ctry:
        ZONE_GEOM[z] = ctry[iso]

# ---------------------------------------------------------------- 时期与归属
# 每期: key, title(中文), fromYear, toYear, focusYear, eras 说明, 各政权 -> (分区列表, 颜色, 锚点名)
PERIODS = [
    dict(key="dawn", title="两河与尼罗河的黎明", fromYear=-3500, toYear=-1650, focusYear=-2334,
         caption="约公元前3500—公元前1650年 · 苏美尔城邦到汉谟拉比，埃及从早王朝到中王国",
         note="两河南部的神庙城市（乌鲁克、乌尔、尼普尔）发明了楔形文字与官僚会计，萨尔贡建立阿卡德帝国，"
              "乌尔第三王朝与伊辛-拉尔萨相继而兴，最后由汉谟拉比统一两河并把马尔杜克推为全国主神。"
              "同一时期埃及由早王朝走向金字塔时代，迦南与腓尼基的沿海城邦（比布鲁斯等）承担木材与铜的转口。"
              "这一千年奠定了后来赫梯、亚述与巴比伦所继承的文字、法律与神庙制度。",
         polities={}),
    dict(key="hittite", title="赫梯帝国", fromYear=-1650, toYear=-1180, focusYear=-1350,
         caption="约公元前1650—公元前1180年 · 赫梯古王国至帝国",
         note="哈图西里一世定都哈图沙，穆尔西里一世公元前1595年劫掠巴比伦；苏庇路里乌玛一世（公元前1344—公元前1322）击溃米坦尼，与埃及拉美西斯二世在卡迭石对峙并于公元前1259年缔结和约。帝国核心在安纳托利亚中部，兼控北叙利亚。公元前1180年前后随“青铜时代崩溃”瓦解。",
         polities={
             "赫梯帝国": (["galatia", "cappadocia", "lycaonia", "cilicia", "upper_mes", "armenia_min"], "#a8452f", "哈图沙"),
             "阿尔扎瓦诸国": (["ionia", "lydia", "caria", "lycia", "pisidia"], "#6f8f4e", "阿帕萨"),
             "卡什卡诸部": (["paphlagonia", "pontus"], "#7a6a8a", "皮拉美特山"),
             "米坦尼": (["syria", "iraq"], "#c1913a", "瓦舒卡尼"),
             "埃及新王国": (["cyprus"], "#3f6f8f", "孟菲斯"),
             "迈锡尼希腊": (["greece"], "#4f7f7f", "迈锡尼"),
             "阿希亚瓦": (["troad_mysia"], "#5f8f9f", "米利都"),
         }),
    dict(key="post_hittite", title="后赫梯时代", fromYear=-1180, toYear=-700, focusYear=-900,
         caption="约公元前1180—公元前700年 · 弗里吉亚、乌拉尔图与新赫梯诸国",
         note="帝国崩溃后安纳托利亚进入多中心时代：弗里吉亚人据中西部（公元前8 世纪以戈尔迪乌姆为都），乌拉尔图在东部凡湖崛起与亚述争雄，东南部为卢维人的新赫梯城邦（卡赫美什、马尔丁），西部爱奥尼亚希腊城邦兴起。公元前696/695 年辛梅里安人攻灭弗里吉亚。",
         polities={
             "弗里吉亚": (["phrygia", "galatia", "lydia", "ionia"], "#8a5a2b", "戈尔迪乌姆"),
             "乌拉尔图": (["urartu", "armenia_maj", "armenia_min"], "#5f6f9f", "图什帕"),
             "新赫梯诸邦": (["upper_mes", "cilicia"], "#9a7a3a", "卡赫美什"),
             "吕基亚与卡里亚": (["lycia", "caria", "pisidia"], "#6f8f4e", "桑索斯"),
             "爱奥尼亚希腊城邦": (["troad_mysia"], "#3f7f7f", "米利都"),
             "亚述帝国": (["iraq", "syria"], "#a8452f", "尼尼微"),
             "希腊本土": (["greece"], "#4f6f8f", "雅典"),
             "色雷斯诸部": (["thrace"], "#7a6a5a", "塞斯图斯"),
         }),
    dict(key="lydia", title="吕底亚与东方诸国", fromYear=-700, toYear=-547, focusYear=-600,
         caption="约公元前700—公元前547年 · 吕底亚、米底与新巴比伦",
         note="辛梅里安人退去后吕底亚以萨第斯为都称霸安纳托利亚西部，公元前7 世纪铸造西方最早的钱币；与米底以哈里斯河（克孜勒河）为界。东部乌拉尔图衰落，亚述于公元前612年亡于米底与新巴比伦，小亚细亚东部归米底；本都、卡帕多细亚诸小邦与希腊殖民城邦（锡诺普、特拉佩祖斯）并存。",
         polities={
             "吕底亚王国": (["lydia", "ionia", "troad_mysia", "phrygia", "caria"], "#b8892f", "萨第斯"),
             "米底王国": (["armenia_maj", "armenia_min", "urartu", "iran", "upper_mes"], "#7a5a8a", "埃克巴坦那"),
             "新巴比伦": (["syria", "iraq"], "#8f5a3a", "巴比伦"),
             "吕基亚": (["lycia", "pisidia"], "#6f8f4e", "桑索斯"),
             "比提尼亚与帕弗拉戈尼亚": (["bithynia", "paphlagonia"], "#5f7f6f", "尼科米底亚"),
             "本都与卡帕多细亚": (["pontus", "cappadocia"], "#8f7f4a", "锡诺普"),
             "奇里乞亚诸邦": (["cilicia"], "#9a7a5a", "塔尔苏斯"),
             "希腊本土": (["greece"], "#4f6f8f", "雅典"),
             "色雷斯王国": (["thrace"], "#7a6a5a", "塞斯图斯"),
             "埃及": (["cyprus"], "#a8942f", "赛伊斯"),
         }),
    dict(key="achaemenid", title="阿契美尼德波斯", fromYear=-547, toYear=-334, focusYear=-450,
         caption="公元前547—公元前334年 · 波斯行省时代",
         note="公元前547/546 年居鲁士二世灭吕底亚，安纳托利亚并入阿契美尼德帝国，分为萨尔迪斯、赫勒斯滂弗里吉亚、卡帕多细亚、亚美尼亚等行省（satrapy）。公元前499—公元前493年爱奥尼亚起义引发希波战争；公元前387/386 年《大王和约》后西部希腊城邦复归波斯。公元前334年亚历山大渡海东征终结波斯统治。",
         polities={
             "阿契美尼德帝国": (["lydia", "ionia", "troad_mysia", "phrygia", "caria", "lycia",
                                "pisidia", "bithynia", "paphlagonia", "pontus", "cappadocia",
                                "galatia", "lycaonia", "armenia_min", "armenia_maj",
                                "iran", "iraq", "syria", "upper_mes"], "#9a5f8f", "萨尔迪斯"),
             "乌拉尔图余部": (["urartu"], "#5f6f9f", "图什帕"),
             "奇里乞亚": (["cilicia"], "#9a7a5a", "塔尔苏斯"),
             "希腊本土": (["greece"], "#4f6f8f", "雅典"),
             "色雷斯王国": (["thrace"], "#7a6a5a", "塞斯图斯"),
             "埃及": (["cyprus"], "#a8942f", "孟菲斯"),
             "斯基泰与高加索诸部": (["georgia"], "#7a7a6a", "科尔基斯"),
         }),
    dict(key="diadochi", title="继业者战争", fromYear=-334, toYear=-281, focusYear=-310,
         caption="公元前334—公元前281年 · 亚历山大东征与继业者割据",
         note="公元前334年亚历山大渡赫勒斯滂，公元前333年伊苏斯之战、公元前331年高加米拉之战灭波斯，公元前323年卒于巴比伦。此后“继业者”（Diadochi）争夺：安提柯、利西马科斯、塞琉古、托勒密，公元前301年伊普苏斯之战后安纳托利亚三分；公元前281年库鲁佩迪安之战利西马科斯阵亡，塞琉古短暂统一小亚细亚。同期比提尼亚、卡帕多细亚、本都本土王朝自立。",
         polities={
             "利西马科斯王国": (["thrace", "troad_mysia", "ionia", "lydia", "phrygia", "bithynia"], "#8f6f3f", "吕西马基亚"),
             "塞琉古王国": (["cappadocia", "galatia", "lycaonia", "upper_mes", "syria", "iraq", "iran", "cilicia"], "#b8892f", "安条克"),
             "安提柯余部": (["paphlagonia", "pontus", "armenia_min"], "#7a5a8a", "凯尔特加拉太"),
             "卡里亚与吕基亚": (["caria", "lycia", "pisidia"], "#6f8f4e", "哈利卡纳苏斯"),
             "本都与卡帕多细亚本土王朝": (["armenia_maj"], "#8f7f4a", "阿马西亚"),
             "乌拉尔图故地": (["urartu"], "#5f6f9f", "阿尔塔沙特"),
             "马其顿本土": (["greece"], "#4f6f8f", "佩拉"),
             "埃及托勒密": (["cyprus"], "#a8942f", "亚历山大里亚"),
             "科尔基斯": (["georgia"], "#7a7a6a", "法息斯"),
         }),
    dict(key="hellenistic", title="希腊化诸王国", fromYear=-281, toYear=-133, focusYear=-200,
         caption="公元前281—公元前133年 · 帕加马、本都、塞琉古与罗马登场",
         note="安纳托利亚进入多王国并立：帕加马阿塔罗斯王朝与罗马结盟，公元前188年《阿帕米亚和约》后取得塞琉古在小亚细亚的大部；本都米特里达梯王朝在黑海南岸崛起，本都战争与罗马三度交锋（公元前88—公元前63）；比提尼亚、卡帕多细亚、加拉太、科马基尼为罗马的缓冲附庸。公元前133年阿塔罗斯三世遗赠帕加马给罗马，亚细亚行省成立。",
         polities={
             "帕加马王国": (["troad_mysia", "ionia", "lydia", "caria", "phrygia", "pisidia"], "#b8892f", "帕加马"),
             "本都王国": (["pontus", "paphlagonia", "armenia_min"], "#a8452f", "锡诺普"),
             "塞琉古王国": (["syria", "iraq", "iran", "upper_mes", "cilicia"], "#8f6f3f", "安条克"),
             "比提尼亚王国": (["bithynia"], "#5f7f6f", "尼科米底亚"),
             "卡帕多细亚王国": (["cappadocia", "galatia", "lycaonia"], "#8f7f4a", "马扎卡"),
             "加拉太诸部": (["galatia"], "#7a6a5a", "安卡拉"),
             "吕基亚联盟": (["lycia"], "#6f8f4e", "桑索斯"),
             "亚美尼亚王国": (["armenia_maj", "urartu"], "#5f6f9f", "阿尔塔沙特"),
             "罗马共和国": (["greece"], "#8f3f3f", "罗马"),
             "埃及托勒密": (["cyprus"], "#a8942f", "亚历山大里亚"),
             "科尔基斯": (["georgia"], "#7a7a6a", "法息斯"),
         }),
    dict(key="roman_conquest", title="罗马入主", fromYear=-133, toYear=-27, focusYear=-80,
         caption="公元前133—公元前27年 · 亚细亚行省与米特里达梯战争",
         note="公元前133年亚细亚行省设立，公元前129年加拉太并入；公元前88—公元前63年三度米特里达梯战争，庞培公元前64年灭本都王国、设比提尼亚与本都联合行省，公元前63年废塞琉古。西塞罗公元前51—公元前50年任奇里乞亚总督。凯撒与庞培的内战（公元前48年法萨卢斯）波及安纳托利亚，公元前27年奥古斯都确立元首制。",
         polities={
             "罗马亚细亚行省": (["troad_mysia", "ionia", "lydia", "caria", "phrygia", "pisidia", "lycia"], "#8f3f3f", "以弗所"),
             "罗马比提尼亚与本都": (["bithynia", "paphlagonia", "pontus"], "#a8452f", "尼科米底亚"),
             "罗马奇里乞亚": (["cilicia"], "#9a5f4f", "塔尔苏斯"),
             "卡帕多细亚王国": (["cappadocia", "galatia", "lycaonia", "armenia_min"], "#8f7f4a", "马扎卡"),
             "科马基尼王国": (["upper_mes"], "#7a6a5a", "萨莫萨塔"),
             "亚美尼亚王国": (["armenia_maj", "urartu", "georgia"], "#5f6f9f", "提格拉诺刻塔"),
             "安息帝国": (["iraq", "iran"], "#7a5a8a", "泰西封"),
             "托勒密埃及": (["cyprus", "syria"], "#a8942f", "亚历山大里亚"),
             "希腊罗马势力": (["greece"], "#6f5f5f", "雅典"),
             "色雷斯王国": (["thrace"], "#7a6a5a", "塞斯图斯"),
         }),
    dict(key="roman_empire", title="罗马帝国", fromYear=-27, toYear=330, focusYear=117,
         caption="公元前27—330 年 · 罗马和平与东方行省",
         note="奥古斯都后小亚细亚进入长期和平：亚细亚、比提尼亚-本都、加拉太、卡帕多细亚、奇里乞亚、吕基亚-潘菲利亚等行省并为帝国东部富庶地带，以弗所、帕加马、萨第斯、安条克为大城市。图拉真 114—117 年短暂设立亚美尼亚与美索不达米亚行省；哈德良时退回。235 年危机后波斯萨珊崛起，260 年沙普尔一世俘获瓦勒良。",
         polities={
             "罗马帝国（东方行省）": (["troad_mysia", "ionia", "lydia", "caria", "lycia", "pisidia",
                                     "phrygia", "bithynia", "paphlagonia", "pontus", "cappadocia",
                                     "galatia", "lycaonia", "cilicia", "armenia_min", "upper_mes",
                                     "thrace", "armenia_maj"], "#8f3f3f", "以弗所"),
             "萨珊波斯": (["iraq", "iran", "urartu"], "#7a5a8a", "泰西封"),
             "亚美尼亚": (["georgia"], "#5f6f9f", "阿尔塔沙特"),
             "罗马本土": (["greece"], "#6f5f5f", "罗马"),
             "塞浦路斯": (["cyprus"], "#a8942f", "帕福斯"),
         }),
    dict(key="byzantine", title="拜占庭安纳托利亚", fromYear=330, toYear=1071, focusYear=950,
         caption="330—1071 年 · 东罗马军区制与伊斯兰边境",
         note="330 年君士坦丁堡建都。602—628 年东罗马-萨珊大战耗尽双方，636 年雅尔穆克战役后阿拉伯人夺取叙利亚，安纳托利亚成为拜占庭与哈里发的“边境地带”（thughūr）。7—9 世纪推行军区（theme）制：安纳托利亚、阿尔梅尼亚克、色雷斯西亚、奥普西金、布凯拉里、卡帕多细亚等军区。9—10 世纪马其顿王朝反攻，963—969 年收复奇里乞亚与安条克。1071 年曼齐刻尔特战败后失中部门户。",
         polities={
             "拜占庭帝国": (["thrace", "troad_mysia", "ionia", "lydia", "caria", "lycia", "pisidia",
                            "phrygia", "bithynia", "paphlagonia", "pontus", "cappadocia", "galatia",
                            "lycaonia", "cilicia", "armenia_min", "greece", "cyprus"], "#8f3f6f", "君士坦丁堡"),
             "阿拉伯哈里发国": (["syria", "iraq", "iran", "upper_mes"], "#3f7f6f", "巴格达"),
             "亚美尼亚诸国": (["armenia_maj", "urartu"], "#5f6f9f", "阿尼"),
             "高加索伊比利亚": (["georgia"], "#7a7a6a", "第比利斯"),
             "保加尔汗国": (["bulgaria"], "#7a5a5a", "普雷斯拉夫"),
         }),
    dict(key="seljuk", title="曼齐刻尔特之后", fromYear=1071, toYear=1243, focusYear=1150,
         caption="1071—1243 年 · 罗姆苏丹国与十字军",
         note="1071 年曼齐刻尔特之战后突厥人涌入，1077 年苏莱曼·伊本·库塔尔米什立罗姆苏丹国（都科尼亚），达尼什曼德王朝据中北部，阿尔图格、萨尔图克、门古哲克诸贝伊国在东部，曼努埃尔一世 1176 年密列奥塞法隆战败。1097 年第一次十字军的尼西亚、多里莱乌姆之战与 1204 年第四次十字军攻陷君士坦丁堡，以及 1204—1261 年尼西亚帝国，重塑小亚细亚政治。1243 年克塞山之战苏丹国臣属蒙古。",
         polities={
             "罗姆苏丹国": (["lycaonia", "cappadocia", "galatia", "phrygia", "pisidia", "cilicia"], "#3f8f6a", "科尼亚"),
             "达尼什曼德王朝": (["pontus", "armenia_min", "paphlagonia"], "#8f6f3f", "锡瓦斯"),
             "拜占庭帝国": (["thrace", "troad_mysia", "ionia", "lydia", "caria", "lycia", "bithynia",
                            "paphlagonia", "greece"], "#8f3f6f", "君士坦丁堡"),
             "特拉布宗帝国": (["artvin", "armenia_maj", "georgia"] if False else ["armenia_maj", "georgia"], "#5f8f8f", "特拉布宗"),
             "亚美尼亚奇里乞亚王国": (["upper_mes"], "#a8942f", "西斯"),
             "阿尤布王朝": (["syria", "iraq"], "#7a7a3a", "大马士革"),
             "塞尔柱大帝国余部": (["iran", "urartu"], "#9a5f5f", "伊斯法罕"),
             "尼西亚帝国": (["bithynia"], "#6f5f8f", "尼西亚"),
             "十字军国家": (["cyprus"], "#b8892f", "安条克"),
             "保加利亚": (["bulgaria"], "#7a5a5a", "特尔诺沃"),
         }),
    dict(key="mongol", title="蒙古宗主权与贝伊国兴起", fromYear=1243, toYear=1300, focusYear=1275,
         caption="1243—1300 年 · 伊儿汗国与诸贝伊",
         note="1243 年克塞山之战后罗姆苏丹国成为蒙古（伊儿汗国）藩属，1277 年巴赫里马穆鲁克介入、1279 年后苏丹国分裂。土库曼诸贝伊国（卡拉曼、格尔米扬、艾登、门泰塞、奥斯曼、萨鲁汗、卡雷西）在西部和中部兴起；东部有特拉布宗帝国与奇里乞亚亚美尼亚王国王国为蒙古-马穆鲁克缓冲。",
         polities={
             "伊儿汗国（宗主权）": (["galatia", "cappadocia", "lycaonia", "armenia_min", "urartu",
                                    "armenia_maj", "iran", "iraq", "upper_mes", "georgia"], "#7a5a8a", "大不里士"),
             "卡拉曼贝伊国": (["lycaonia", "cilicia", "pisidia"], "#3f8f6a", "卡拉曼"),
             "格尔米扬贝伊国": (["phrygia"], "#8f7f4a", "屈塔希亚"),
             "奥斯曼贝伊国": (["bithynia"], "#a8452f", "瑟于特"),
             "艾登与门泰塞诸贝伊": (["ionia", "lydia", "caria"], "#5f8f8f", "比尔吉"),
             "拜占庭帝国": (["thrace", "troad_mysia", "bithynia", "lycia", "greece"], "#8f3f6f", "君士坦丁堡"),
             "特拉布宗帝国": (["pontus", "paphlagonia"], "#5f8f9f", "特拉布宗"),
             "奇里乞亚亚美尼亚王国": (["armenia_min"], "#a8942f", "西斯"),
             "马穆鲁克王朝": (["syria"], "#7a7a3a", "开罗"),
             "塞浦路斯王国": (["cyprus"], "#b8892f", "尼科西亚"),
             "保加利亚": (["bulgaria"], "#7a5a5a", "特尔诺沃"),
         }),
    dict(key="beylik", title="贝伊国与奥斯曼崛起", fromYear=1300, toYear=1453, focusYear=1400,
         caption="1300—1453 年 · 安纳托利亚诸贝伊国与奥斯曼扩张",
         note="奥斯曼一世至穆拉德一世逐步吞并比提尼亚与色雷斯，1389 年科索沃、1396 年尼科波利斯；巴耶济德一世 1397—1402 年兼并中部诸贝伊国，却在 1402 年安卡拉之战败于帖木儿，贝伊国复立、帝国进入 1402—1413 年空位期。穆拉德二世与穆罕默德二世重新整合，1453 年攻陷君士坦丁堡。",
         polities={
             "奥斯曼帝国": (["bithynia", "thrace", "troad_mysia", "phrygia", "galatia", "ionia", "lydia"], "#a8452f", "布尔萨"),
             "卡拉曼贝伊国": (["lycaonia", "cilicia", "pisidia"], "#3f8f6a", "卡拉曼"),
             "卡迪·布尔汉丁国": (["armenia_min", "cappadocia"], "#7a5a8a", "锡瓦斯"),
             "白羊王朝": (["upper_mes", "urartu", "armenia_maj"], "#9a7a5a", "迪亚巴克尔"),
             "拜占庭帝国": (["greece"], "#8f3f6f", "君士坦丁堡"),
             "特拉布宗帝国": (["pontus"], "#5f8f9f", "特拉布宗"),
             "奇里乞亚亚美尼亚王国": (["caria", "lycia"], "#a8942f", "西斯"),
             "威尼斯与热那亚据点": (["cyprus"], "#8f5f8f", "法马古斯塔"),
             "马穆鲁克王朝": (["syria"], "#7a7a3a", "开罗"),
             "帖木儿帝国": (["iran", "iraq", "georgia", "bulgaria"], "#6f5f3f", "撒马尔罕"),
         }),
    dict(key="ottoman", title="奥斯曼帝国鼎盛", fromYear=1453, toYear=1683, focusYear=1566,
         caption="1453—1683 年 · 从伊斯坦布尔到维也纳城下",
         note="1453 年穆罕默德二世取君士坦丁堡，1514 年查尔迪兰之战胜萨法维、1516—1517 年灭马穆鲁克取叙利亚埃及，苏莱曼一世 1529 年围维也纳、1538 年普雷韦扎海战。帝国行省（eyalet）与桑贾克（sancak）制覆盖安纳托利亚与鲁米利亚；1683 年维也纳战败标志扩张终结。",
         polities={
             "奥斯曼帝国": (list(ZONES.keys()) + ["greece", "bulgaria", "syria", "iraq", "cyprus"], "#a8452f", "伊斯坦布尔"),
             "萨法维波斯": (["iran", "georgia"], "#7a5a8a", "伊斯法罕"),
             "克里米亚汗国（奥斯曼藩属）": ([], "#5f6f9f", "巴赫奇萨赖"),
         }),
    dict(key="ottoman_late", title="奥斯曼晚期", fromYear=1683, toYear=1922, focusYear=1880,
         caption="1683—1922 年 · 衰落、坦志麦特与帝国终结",
         note="《卡尔洛维茨条约》(1699) 后帝国转入守势；1839—1876 年坦志麦特改革，1876 年《米德哈特宪法》，1908 年青年土耳其党革命。安纳托利亚成为帝国核心，1915 年亚美尼亚人大规模死亡事件至今争议；一战中 1915 年加里波利之战、1918 年《穆兹罗斯停战协定》、1920 年《色佛尔条约》被 1923 年《洛桑条约》取代。",
         polities={
             "奥斯曼帝国": (list(ZONES.keys()), "#a8452f", "伊斯坦布尔"),
             "英法委任统治": (["syria", "iraq"], "#3f6f8f", "贝鲁特"),
             "英属塞浦路斯": (["cyprus"], "#8f5f8f", "尼科西亚"),
             "俄罗斯帝国": (["georgia", "armenia_maj"], "#5f6f9f", "第比利斯"),
             "卡扎尔波斯": (["iran"], "#7a5a8a", "德黑兰"),
             "希腊王国": (["greece"], "#4f6f8f", "雅典"),
             "保加利亚公国": (["bulgaria"], "#7a5a5a", "索非亚"),
         }),
    dict(key="republic", title="土耳其共和国", fromYear=1923, toYear=2026, focusYear=1938,
         caption="1923 年至今 · 共和国、凯末尔改革与现代土耳其",
         note="1923 年 10 月 29 日共和国成立，凯末尔·阿塔图尔克推行世俗化、文字拉丁化（1928）、姓氏法与妇女参政权（1934）；1939 年并入哈塔伊。1945 年后多党制，1952 年入北约，1960/1971/1980 年三次军事政变，1983 年厄扎尔市场化改革，1999 年欧盟候选国，2002 年后正义与发展党长期执政，2017 年改行总统制。",
         polities={
             "土耳其共和国": (list(ZONES.keys()), "#a8452f", "安卡拉"),
             "叙利亚": (["syria"], "#3f7f6f", "大马士革"),
             "伊拉克": (["iraq"], "#7a7a3a", "巴格达"),
             "伊朗": (["iran"], "#7a5a8a", "德黑兰"),
             "格鲁吉亚": (["georgia"], "#5f6f9f", "第比利斯"),
             "亚美尼亚": (["armenia_maj"], "#9a7a5a", "埃里温"),
             "希腊": (["greece"], "#4f6f8f", "雅典"),
             "保加利亚": (["bulgaria"], "#7a5a5a", "索非亚"),
             "塞浦路斯": (["cyprus"], "#b8892f", "尼科西亚"),
         }),
]


def round_coords(obj):
    """递归把坐标四舍五入到两位小数（格式硬性要求）"""
    if isinstance(obj, (list, tuple)):
        if obj and isinstance(obj[0], (int, float)):
            return [round(float(obj[0]), 2), round(float(obj[1]), 2)]
        return [round_coords(x) for x in obj]
    return obj


def zone_geom(z):
    return ZONE_GEOM.get(z)


def make_snapshot(per):
    feats = []
    polity_names = []
    for name, (zones, tint, anchor_name) in per["polities"].items():
        geoms = [zone_geom(z) for z in zones if zone_geom(z) is not None]
        geoms = [g for g in geoms if g is not None and not g.is_empty]
        if not geoms:
            continue
        u = unary_union(geoms)
        # 简化到 2 位小数（格式要求最多两位）
        u = u.simplify(0.01, preserve_topology=True)
        g = mapping(u)
        if g["type"] == "Polygon":
            coords = g["coordinates"]
        else:
            coords = [p for p in g["coordinates"]]
        polity_names.append(name)
        feats.append({
            "type": "Feature",
            "id": name,
            "properties": {
                "title": name,
                "role": "main" if tint == per["polities"][name][1] and len(polity_names) == 1 else "rival",
                "tint": tint,
                "anchor": None,
            },
            "geometry": {"type": g["type"], "coordinates": round_coords(coords)},
        })

    snap = {
        "caption": per["caption"],
        "note": per["note"],
        "polities": polity_names,
        "regions": [],
    }
    return {"type": "FeatureCollection", "license": LICENSE_NOTICE, "snapshot": snap, "features": feats}


LICENSE_NOTICE = ("Approximate historical boundaries for illustration, not surveyed borders. "
                  "Base blocks derive from Natural Earth (public domain) and aourednik/historical-basemaps (GPL-3.0); "
                  "period assignments follow the sources listed in data/sources/. "
                  "Interface adapted from Jiangshan Atlas (GPL-3.0) by DeanChensj.")


def main():
    os.makedirs(OUT_ATLAS, exist_ok=True)
    os.makedirs(OUT_SRC, exist_ok=True)
    order = []
    for per in PERIODS:
        key = per["key"]
        d = os.path.join(OUT_ATLAS, key)
        os.makedirs(d, exist_ok=True)
        fc = make_snapshot(per)
        # anchor 用各分区的省界质心近似（政权的几何质心）
        for f in fc["features"]:
            geom = shape(f["geometry"])
            c = geom.representative_point()
            f["properties"]["anchor"] = [round(c.x, 2), round(c.y, 2)]
        fn = f"s_{key}"
        json.dump(fc, open(os.path.join(d, fn + ".geojson"), "w", encoding="utf-8"),
                  ensure_ascii=False)
        order.append(fn)
        print(f"  {key:16s} {len(fc['features']):2d} 个政权  → data/atlas/{key}/{fn}.geojson")

    idx = {"boot": order[:1], "order": order}
    json.dump(idx, open(os.path.join(OUT_ATLAS, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\nindex.json 写入 {len(order)} 个快照")


if __name__ == "__main__":
    main()
