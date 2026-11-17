#!/usr/bin/env python3
"""时期分组（14 个时代 × 48 个快照）+ 旅行者路线 + 史料，生成 js/map_data.js
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(mod, path):
    spec = importlib.util.spec_from_file_location(mod, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ga = load("ga", os.path.join(ROOT, "_build", "gen_atlas.py"))        # 旧的 15 期文案（summary 复用）
gc = load("gc", os.path.join(ROOT, "_build", "gen_content.py"))       # 里程碑 / 古今地名 / 史料
g2 = load("g2", os.path.join(ROOT, "_build", "gen_atlas2.py"))        # 48 个快照年份

SNAP_YEAR = {k: y for y, k, cap, note in g2.SNAPS}
SNAP_CAP = {k: cap for y, k, cap, note in g2.SNAPS}
SNAP_NOTE = {k: note for y, k, cap, note in g2.SNAPS}

# 14 个时代，每个含若干快照（原项目 18 朝代 / 164 快照的同构做法）
ERAS = [
    dict(key="dawn", title="两河与尼罗河的黎明", badge="青铜早期", fromYear=-3500, toYear=-1650, focusYear=-2334,
         tint="#b8952f", seat="乌鲁克 · 乌尔 · 巴比伦", content="dawn",
         snaps=["sumer_dawn",
               "akkad_empire",
               "ur_third",
               "isin_larsa",
               "hammurabi"]),
    dict(key="hittite", title="赫梯时代", badge="赫梯", fromYear=-1650, toYear=-1180, focusYear=-1350,
         tint="#a8452f", seat="哈图沙（博阿兹卡莱）", content="hittite",
         snaps=["hittite_old",
               "hittite_early",
               "babylon_sack",
               "hittite_mid",
               "hittite_recovery",
               "hittite_empire",
               "hittite_late_peak",
               "qadesh",
               "hittite_twilight",
               "bronze_collapse"]),
    dict(key="post_hittite", title="铁器早期", badge="黑暗时代", fromYear=-1180, toYear=-660, focusYear=-900,
         tint="#8a5a2b", seat="戈尔迪乌姆 · 图什帕 · 卡赫美士", content="post_hittite",
         snaps=["post_collapse",
               "dark_age",
               "phrygia_rise",
               "urartu_rise",
               "assyria_pressure",
               "phrygia_peak",
               "urartu_peak",
               "cimmerian"]),
    dict(key="lydia", title="吕底亚与东方诸国", badge="吕底亚", fromYear=-660, toYear=-546, focusYear=-600,
         tint="#b8892f", seat="萨第斯", content="lydia",
         snaps=["lydia_rise",
               "assyria_fall",
               "halys_battle",
               "cyrus_conquest"]),
    dict(key="achaemenid", title="阿契美尼德波斯", badge="波斯行省", fromYear=-546, toYear=-334, focusYear=-480,
         tint="#9a5f8f", seat="萨尔迪斯 · 达斯基雷翁", content="achaemenid",
         snaps=["cyrus_rise",
               "ionian_revolt",
               "persian_wars",
               "persian_late",
               "kings_peace",
               "satrap_revolt"]),
    dict(key="alexander", title="亚历山大与继业者", badge="继业者", fromYear=-334, toYear=-281, focusYear=-323,
         tint="#8f6f3f", seat="吕西马基亚 · 安条克", content="diadochi",
         snaps=["alexander",
               "alexander_east",
               "alexander_death",
               "ipsus",
               "curupedium"]),
    dict(key="hellenistic", title="希腊化诸王国", badge="希腊化", fromYear=-281, toYear=-133, focusYear=-188,
         tint="#b8892f", seat="帕加马 · 锡诺普 · 尼科米底亚", content="hellenistic",
         snaps=["galatian_invasion",
               "galatia_settled",
               "attalid_power",
               "magnesia",
               "apamea",
               "asia_province",
               "mithridatic"]),
    dict(key="roman", title="罗马安纳托利亚", badge="罗马", fromYear=-133, toYear=330, focusYear=117,
         tint="#8f3f3f", seat="以弗所 · 尼科米底亚 · 安条克", content="roman_empire",
         snaps=["provincial_asia",
               "pompey_east",
               "actium",
               "augustus",
               "flavian",
               "trajan_peak",
               "severan",
               "crisis_3c",
               "tetrarchy",
               "constantinople"]),
    dict(key="byzantine", title="拜占庭安纳托利亚", badge="拜占庭", fromYear=330, toYear=1071, focusYear=970,
         tint="#8f3f6f", seat="君士坦丁堡", content="byzantine",
         snaps=["theodosian",
               "justinian",
               "heracleius",
               "arab_conquest",
               "arab_raids",
               "theme_system",
               "byz_recovery",
               "macedonian",
               "basil_death"]),
    dict(key="seljuk", title="突厥入主与十字军", badge="罗姆苏丹国", fromYear=1071, toYear=1243, focusYear=1176,
         tint="#3f8f6a", seat="科尼亚 · 尼西亚 · 锡瓦斯", content="seljuk",
         snaps=["manzikert",
               "first_crusade",
               "crusader_early",
               "danismend_end",
               "myriokephalon",
               "fourth_crusade",
               "rum_peak"]),
    dict(key="mongol", title="蒙古宗主权", badge="伊儿汗", fromYear=1243, toYear=1300, focusYear=1275,
         tint="#7a5a8a", seat="科尼亚（藩属）· 大不里士", content="mongol",
         snaps=["kosedag",
               "ilkhanid_direct",
               "beyliks"]),
    dict(key="beylik", title="贝伊国与奥斯曼崛起", badge="贝伊国", fromYear=1300, toYear=1453, focusYear=1402,
         tint="#a8452f", seat="布尔萨 · 埃迪尔内", content="beylik",
         snaps=["burhaneddin",
               "ankara_battle"]),
    dict(key="ottoman", title="奥斯曼帝国鼎盛", badge="奥斯曼", fromYear=1453, toYear=1683, focusYear=1566,
         tint="#a8452f", seat="伊斯坦布尔", content="ottoman",
         snaps=["conquest",
               "mehmed_late",
               "selim_conquests",
               "suleiman_era",
               "celali"]),
    dict(key="ottoman_late", title="奥斯曼晚期", badge="晚期奥斯曼", fromYear=1683, toYear=1922, focusYear=1880,
         tint="#a8452f", seat="伊斯坦布尔", content="ottoman_late",
         snaps=["ayan",
               "tanzimat",
               "hamidian",
               "wwi_end"]),
    dict(key="republic", title="土耳其共和国", badge="共和国", fromYear=1923, toYear=2026, focusYear=1938,
         tint="#a8452f", seat="安卡拉", content="republic",
         snaps=["republic_found",
               "ataturk_end",
               "cold_war",
               "industrial",
               "ozal",
               "akp_mid",
               "present"]),
]

# ---------------------------------------------------------------- 旅行者路线

# ---------------------------------------------------------------- 路线逐站卡片
# 每站：名称 / 坐标 / 年份 / 一句话说明 / 出处（第一手或代表性研究）
ROUTE_STOPS = {
 "xenophon_anabasis": [
  {
   "name": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "year": -401,
   "note": "小居鲁士在萨第斯起兵，万人希腊雇佣军由此东进。",
   "source": "《长征记》i.2"
  },
  {
   "name": "刻莱奈",
   "coord": [
    29.98,
    38.07
   ],
   "year": -401,
   "note": "小居鲁士在此检阅希腊军，许诺加倍军饷，并展示「王的女人」以激励士气。",
   "source": "《长征记》i.2.9"
  },
  {
   "name": "塔尔苏斯",
   "coord": [
    34.9,
    36.92
   ],
   "year": -401,
   "note": "希腊军得知此行真正目标是波斯大王，拒绝继续东进，几近哗变。",
   "source": "《长征记》i.3"
  },
  {
   "name": "伊苏斯",
   "coord": [
    36.2,
    36.85
   ],
   "year": -401,
   "note": "在伊苏斯清点兵力：希腊重装步兵约 1.04 万、轻装 2300。",
   "source": "《长征记》i.4"
  },
  {
   "name": "库纳克萨",
   "coord": [
    43.35,
    33.32
   ],
   "year": -401,
   "note": "小居鲁士战死；希腊将领应邀赴会，被波斯总督提萨费尼斯诱杀。",
   "source": "《长征记》ii.5"
  },
  {
   "name": "底格里斯渡口",
   "coord": [
    42.6,
    37.2
   ],
   "year": -400,
   "note": "沿底格里斯河东岸北撤，遭波斯骑兵与当地部族袭扰。",
   "source": "《长征记》iii.4"
  },
  {
   "name": "亚美尼亚高原",
   "coord": [
    41.27,
    39.9
   ],
   "year": -400,
   "note": "踏雪翻越卡杜奇人与亚美尼亚高地，冻伤与雪盲者众。",
   "source": "《长征记》iv.5"
  },
  {
   "name": "特拉布宗",
   "coord": [
    39.72,
    41.0
   ],
   "year": -400,
   "note": "前锋登上特凯山望见黑海，全军高呼「塔拉塔！塔拉塔！」（海！海！）。",
   "source": "《长征记》iv.7.21"
  },
  {
   "name": "锡诺普",
   "coord": [
    35.15,
    42.03
   ],
   "year": -400,
   "note": "在锡诺普希腊殖民城邦补给，并就撤军路线与科尔基斯人交涉。",
   "source": "《长征记》vi.1"
  },
  {
   "name": "拜占庭",
   "coord": [
    28.98,
    41.01
   ],
   "year": -400,
   "note": "残部抵达拜占庭；色诺芬此后返乡，将全程写成《长征记》。",
   "source": "《长征记》vii"
  }
 ],
 "alexander_route": [
  {
   "name": "赫勒斯滂",
   "coord": [
    26.4,
    40.2
   ],
   "year": -334,
   "note": "亚历山大渡赫勒斯滂，先赴特洛伊祭阿喀琉斯墓。",
   "source": "阿里安《远征记》i.11"
  },
  {
   "name": "格拉尼库斯河",
   "coord": [
    27.25,
    40.13
   ],
   "note": "首战击溃波斯诸总督联军，小亚细亚门户洞开。",
   "year": -334,
   "source": "阿里安 i.13—16"
  },
  {
   "name": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "year": -334,
   "note": "萨第斯不战而降，吕底亚与波斯金库尽入其手。",
   "source": "阿里安 i.17"
  },
  {
   "name": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "year": -334,
   "note": "恢复以弗所民主政制，并承诺阿耳忒弥斯神庙赋税归神庙。",
   "source": "阿里安 i.17"
  },
  {
   "name": "米利都",
   "coord": [
    27.28,
    37.53
   ],
   "year": -334,
   "note": "米利都围城战，波斯舰队被堵在港外无法解围。",
   "source": "阿里安 i.18—19"
  },
  {
   "name": "哈利卡纳苏斯",
   "coord": [
    27.42,
    37.04
   ],
   "year": -334,
   "note": "久攻哈利卡纳苏斯；波斯总督奥龙托巴特斯焚城后撤守海上。",
   "source": "阿里安 i.20—23"
  },
  {
   "name": "戈尔迪乌姆",
   "coord": [
    31.98,
    39.65
   ],
   "year": -333,
   "note": "在戈尔迪乌姆斩断「戈尔迪乌姆之结」，并于此冬营。",
   "source": "阿里安 ii.3"
  },
  {
   "name": "奇里乞亚门",
   "coord": [
    34.79,
    37.28
   ],
   "year": -333,
   "note": "穿越奇里乞亚门山口进入叙利亚平原。",
   "source": "阿里安 ii.4"
  },
  {
   "name": "伊苏斯",
   "coord": [
    36.2,
    36.85
   ],
   "year": -333,
   "note": "伊苏斯之战，大流士三世弃车而逃，家眷被俘。",
   "source": "阿里安 ii.6—13"
  },
  {
   "name": "高加米拉",
   "coord": [
    43.55,
    36.55
   ],
   "year": -331,
   "note": "高加米拉决战，阿契美尼德波斯帝国覆灭。",
   "source": "阿里安 iii.8—15"
  },
  {
   "name": "巴比伦",
   "coord": [
    44.42,
    32.54
   ],
   "year": -323,
   "note": "卒于巴比伦，年 32；继业者战争随即爆发。",
   "source": "阿里安 vii.24—28"
  }
 ],
 "paul_journeys": [
  {
   "name": "安条克",
   "coord": [
    36.16,
    36.2
   ],
   "year": 46,
   "note": "叙利亚安条克教会差派巴拿巴与扫罗（保罗）出行，首次传道之旅起点。",
   "source": "《使徒行传》13:1—3"
  },
  {
   "name": "塞琉西亚·皮埃里亚",
   "coord": [
    35.93,
    36.12
   ],
   "year": 46,
   "note": "自塞琉西亚港登船，横渡至塞浦路斯。",
   "source": "徒 13:4"
  },
  {
   "name": "帕福斯",
   "coord": [
    32.42,
    34.76
   ],
   "year": 46,
   "note": "在帕福斯使方伯士求保罗信主，术士以吕马暂盲。",
   "source": "徒 13:6—12"
  },
  {
   "name": "佩尔吉",
   "coord": [
    30.85,
    36.96
   ],
   "year": 46,
   "note": "在旁非利亚的佩尔吉上岸，约翰马可离队折返耶路撒冷。",
   "source": "徒 13:13"
  },
  {
   "name": "皮西迪亚的安条克",
   "coord": [
    31.19,
    38.31
   ],
   "year": 46,
   "note": "在会堂讲道后被逐出城，转向外邦人传道。",
   "source": "徒 13:14—52"
  },
  {
   "name": "以哥念",
   "coord": [
    32.48,
    37.87
   ],
   "year": 47,
   "note": "以哥念遭迫害，转往路司得与特庇。",
   "source": "徒 14:1—6"
  },
  {
   "name": "路司得",
   "coord": [
    32.36,
    37.58
   ],
   "year": 47,
   "note": "治好生来瘸腿者，群众以为是宙斯与赫尔墨斯降临，随后几乎被石击。",
   "source": "徒 14:8—20"
  },
  {
   "name": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "year": 54,
   "note": "在推喇奴学房每日讲道两年，银匠底米丢因神像生意煽动骚乱。",
   "source": "徒 19"
  },
  {
   "name": "米利都",
   "coord": [
    27.28,
    37.53
   ],
   "year": 57,
   "note": "在米利都请以弗所长老来，辞别：「你们以后不得再见我的面。」",
   "source": "徒 20:17—38"
  },
  {
   "name": "凯撒利亚",
   "coord": [
    34.9,
    32.5
   ],
   "year": 58,
   "note": "在凯撒利亚被囚两年，向亚基帕王与腓斯都分诉。",
   "source": "徒 24—26"
  },
  {
   "name": "罗马",
   "coord": [
    12.5,
    41.9
   ],
   "year": 60,
   "note": "经米拉、克里特、马耳他海难抵罗马，在软禁中继续传道。",
   "source": "徒 27—28"
  }
 ],
 "ibn_battuta": [
  {
   "name": "阿拉尼亚",
   "coord": [
    32.0,
    36.54
   ],
   "year": 1330,
   "note": "自叙利亚渡海抵阿拉尼亚，记述当地土库曼贝伊的统治与港口。",
   "source": "《游记》第二卷"
  },
  {
   "name": "科尼亚",
   "coord": [
    32.49,
    37.87
   ],
   "year": 1330,
   "note": "访科尼亚，记蒙古宗主权下诸贝伊并立的局面与梅夫拉维教团。",
   "source": "《游记》"
  },
  {
   "name": "开塞利",
   "coord": [
    35.49,
    38.73
   ],
   "year": 1330,
   "note": "记开塞利至埃尔祖鲁姆的驿路、突厥部落与沿途物价。",
   "source": "《游记》"
  },
  {
   "name": "锡瓦斯",
   "coord": [
    37.02,
    39.75
   ],
   "year": 1330,
   "note": "锡瓦斯时为伊儿汗国行省治所，记其蒙古驻军与税制。",
   "source": "《游记》"
  },
  {
   "name": "埃尔祖鲁姆",
   "coord": [
    41.27,
    39.9
   ],
   "year": 1330,
   "note": "在埃尔祖鲁姆觐见苏丹穆罕默德·乌兹别克，记其礼仪。",
   "source": "《游记》"
  },
  {
   "name": "阿马西亚",
   "coord": [
    35.83,
    40.65
   ],
   "year": 1331,
   "note": "经阿马西亚北行，记当地突厥埃米尔的宫廷与学人。",
   "source": "《游记》"
  },
  {
   "name": "伊兹尼克",
   "coord": [
    29.72,
    40.43
   ],
   "year": 1331,
   "note": "见奥斯曼贝伊奥尔汗，评其「拥有最优良的军队」。",
   "source": "《游记》"
  },
  {
   "name": "布尔萨",
   "coord": [
    29.06,
    40.19
   ],
   "year": 1331,
   "note": "在布尔萨逗留，时为奥斯曼新都，记其市集与苏丹陵墓。",
   "source": "《游记》"
  },
  {
   "name": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "year": 1332,
   "note": "觐见拜占庭皇帝安德洛尼卡三世，记圣索菲亚与宫廷。",
   "source": "《游记》"
  }
 ],
 "evliya_celebi": [
  {
   "name": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "year": 1640,
   "note": "《游记》第一卷记帝都风物、宫廷仪式与行会巡游。",
   "source": "《Seyahatnâme》i"
  },
  {
   "name": "布尔萨",
   "coord": [
    29.06,
    40.19
   ],
   "year": 1640,
   "note": "记布尔萨温泉、奥斯曼早期陵墓与丝业。",
   "source": "《Seyahatnâme》ii"
  },
  {
   "name": "伊兹密尔",
   "coord": [
    27.14,
    38.42
   ],
   "year": 1650,
   "note": "记士麦那的欧洲商人社区（Franks）与港口贸易。",
   "source": "《Seyahatnâme》ix"
  },
  {
   "name": "马尼萨",
   "coord": [
    27.43,
    38.61
   ],
   "year": 1650,
   "note": "记马尼萨的甜食、梅夫拉维道堂与地方名流。",
   "source": "《Seyahatnâme》ix"
  },
  {
   "name": "屈塔希亚",
   "coord": [
    29.49,
    39.42
   ],
   "year": 1660,
   "note": "记屈塔希亚埃米尔的矿山、瓷器与驻军。",
   "source": "《Seyahatnâme》ix"
  },
  {
   "name": "阿菲永卡拉希萨尔",
   "coord": [
    30.54,
    38.76
   ],
   "year": 1660,
   "note": "记鸦片（afyon）产地与商路。",
   "source": "《Seyahatnâme》ix"
  },
  {
   "name": "科尼亚",
   "coord": [
    32.49,
    37.87
   ],
   "year": 1660,
   "note": "记科尼亚梅夫拉纳陵墓、托钵僧仪轨与集市。",
   "source": "《Seyahatnâme》iii"
  },
  {
   "name": "阿达纳",
   "coord": [
    35.32,
    37.0
   ],
   "year": 1671,
   "note": "随军经阿达纳入叙利亚，记丘库罗瓦平原的农产。",
   "source": "《Seyahatnâme》ix"
  },
  {
   "name": "阿勒颇",
   "coord": [
    37.16,
    36.2
   ],
   "year": 1671,
   "note": "记阿勒颇商队、黎凡特贸易与城中各教派社区。",
   "source": "《Seyahatnâme》ix"
  },
  {
   "name": "迪亚巴克尔",
   "coord": [
    40.23,
    37.91
   ],
   "year": 1670,
   "note": "记迪亚巴克尔（阿米达）黑玄武岩城墙与卫戍。",
   "source": "《Seyahatnâme》iv"
  },
  {
   "name": "比特利斯",
   "coord": [
    42.11,
    38.4
   ],
   "year": 1670,
   "note": "记比特利斯库尔德埃米尔的城堡与赋税。",
   "source": "《Seyahatnâme》iv"
  },
  {
   "name": "凡城",
   "coord": [
    43.38,
    38.49
   ],
   "year": 1670,
   "note": "记凡湖、凡城要塞与亚美尼亚社区。",
   "source": "《Seyahatnâme》iv"
  },
  {
   "name": "埃尔祖鲁姆",
   "coord": [
    41.27,
    39.9
   ],
   "year": 1645,
   "note": "记埃尔祖鲁姆帕夏的宴饮、城防与冬营。",
   "source": "《Seyahatnâme》ii"
  },
  {
   "name": "特拉布宗",
   "coord": [
    39.72,
    41.0
   ],
   "year": 1640,
   "note": "记黑海港口与外高加索、克里米亚贸易。",
   "source": "《Seyahatnâme》ii"
  },
  {
   "name": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "year": 1670,
   "note": "记安卡拉山羊绒（mohair）纺织业与商队。",
   "source": "《Seyahatnâme》"
  }
 ],
 "herodotus": [
  {
   "name": "哈利卡纳苏斯",
   "coord": [
    27.42,
    37.04
   ],
   "year": -484,
   "note": "希罗多德出生于卡里亚的哈利卡纳苏斯，《历史》开篇即声明写作目的。",
   "source": "《历史》i.1"
  },
  {
   "name": "萨摩斯",
   "coord": [
    26.9,
    37.7
   ],
   "year": -460,
   "note": "据传因政治斗争流亡萨摩斯，习伊奥尼亚方言并搜集材料。",
   "source": "《历史》传记传统"
  },
  {
   "name": "米利都",
   "coord": [
    27.28,
    37.53
   ],
   "year": -450,
   "note": "米利都为伊奥尼亚学术中心，是其地理与民族志材料的重要来源。",
   "source": "《历史》v.28 等"
  },
  {
   "name": "雅典",
   "coord": [
    23.73,
    37.98
   ],
   "year": -447,
   "note": "在雅典公开诵读《历史》，据传获城邦重赏；与伯里克利圈交往。",
   "source": "普鲁塔克《伯里克利传》"
  },
  {
   "name": "德尔斐",
   "coord": [
    22.5,
    38.48
   ],
   "year": -440,
   "note": "大量引用德尔斐神谕与祭司传统，为其史料骨架之一。",
   "source": "《历史》i.46—48"
  },
  {
   "name": "埃及",
   "coord": [
    31.2,
    29.9
   ],
   "year": -450,
   "note": "游历埃及，记尼罗河泛滥、木乃伊制作与诸神庙。",
   "source": "《历史》ii"
  },
  {
   "name": "巴比伦",
   "coord": [
    44.42,
    32.54
   ],
   "year": -450,
   "note": "记巴比伦城墙、幼发拉底商路与「巴比伦卖婚」风俗。",
   "source": "《历史》i.178—199"
  },
  {
   "name": "图里伊",
   "coord": [
    16.6,
    39.7
   ],
   "year": -444,
   "note": "参与雅典在南意大利建图里伊殖民城，晚年在此写作《历史》。",
   "source": "《历史》i.1 传统"
  }
 ],
 "silk_caravan": [
  {
   "name": "大不里士",
   "coord": [
    46.29,
    38.07
   ],
   "year": 1300,
   "note": "伊儿汗国都城，丝路西段总汇，安纳托利亚货物在此转口。",
   "source": "伊儿汗国史料 / Pegolotti《商业手册》"
  },
  {
   "name": "埃尔祖鲁姆",
   "coord": [
    41.27,
    39.9
   ],
   "year": 1300,
   "note": "自大不里士入安纳托利亚第一站，征收商队税。",
   "source": "塞尔柱-伊儿汗税册"
  },
  {
   "name": "埃尔津詹",
   "coord": [
    39.49,
    39.75
   ],
   "year": 1300,
   "note": "驿站与商队客栈（han）集中，跨幼发拉底上游的要冲。",
   "source": "商队路线的考古调查"
  },
  {
   "name": "锡瓦斯",
   "coord": [
    37.02,
    39.75
   ],
   "year": 1240,
   "note": "塞尔柱商队驿站网络枢纽，今存 Şifaiye 与多种 han 遗构。",
   "source": "塞尔柱建筑与瓦克夫文书"
  },
  {
   "name": "开塞利",
   "coord": [
    35.49,
    38.73
   ],
   "year": 1240,
   "note": "苏丹商队客栈与地方市场，连接科尼亚与东部的干道。",
   "source": "《剑桥土耳其史》"
  },
  {
   "name": "科尼亚",
   "coord": [
    32.49,
    37.87
   ],
   "year": 1240,
   "note": "罗姆苏丹国都城，丝路安纳托利亚段的政治与商业中心。",
   "source": "Cahen《前奥斯曼土耳其》"
  },
  {
   "name": "阿克萨赖",
   "coord": [
    34.03,
    38.37
   ],
   "year": 1240,
   "note": "苏丹罕客栈（Sultanhanı, 1229）保存至今，为最完整的塞尔柱商队客栈。",
   "source": "建筑铭文 1229"
  },
  {
   "name": "布尔萨",
   "coord": [
    29.06,
    40.19
   ],
   "year": 1400,
   "note": "奥斯曼时期丝绸业中心，向欧洲市场供应生丝与织物。",
   "source": "奥斯曼档案研究"
  },
  {
   "name": "伊兹密尔",
   "coord": [
    27.14,
    38.42
   ],
   "year": 1600,
   "note": "爱琴海出口港，欧洲商人（Franks）在此设站收购安纳托利亚物产。",
   "source": "黎凡特贸易研究"
  },
  {
   "name": "特拉布宗",
   "coord": [
    39.72,
    41.0
   ],
   "year": 1300,
   "note": "黑海港口，接高加索与北方草原商路，特拉比松帝国税源。",
   "source": "拜占庭黑海贸易研究"
  }
 ]
}

ROUTES = [
    dict(key="xenophon_anabasis", kind="route", title="色诺芬《长征记》：万人军撤退（前 401—前 400）",
         span=[-401, -399],
         summary="小居鲁士在库纳克萨战死后，希腊雇佣军万人自美索不达米亚北撤，经亚美尼亚高原抵黑海，"
                 "高呼「塔拉塔！塔拉塔！（海！海！）」，再沿海南下至拜占庭。色诺芬《长征记》(Anabasis) 是第一手记录。",
         labelAt=[39.5, 38.6],
         segments=[[[28.04, 38.48], [30.52, 38.10], [32.86, 39.93], [34.90, 36.92],
                    [36.20, 36.85], [42.00, 37.00], [43.30, 34.60], [44.40, 33.31],
                    [42.50, 37.20], [41.27, 39.90], [39.72, 41.00], [35.15, 42.03],
                    [32.49, 37.87], [28.98, 41.01]]]),
    dict(key="alexander_route", kind="route", title="亚历山大东征路线（前 334—前 323）",
         span=[-334, -323],
         summary="自赫勒斯滂渡海，经特洛伊、格拉尼库斯河、萨第斯、以弗所、米利都、哈利卡纳苏斯，"
                 "北上戈尔迪乌姆斩断“戈尔迪之结”，经安卡拉、奇里乞亚门南下伊苏斯决战，再经叙利亚、埃及至高加米拉灭波斯。",
         labelAt=[33.5, 37.2],
         segments=[[[26.40, 40.20], [26.24, 39.96], [27.25, 40.13], [28.04, 38.48],
                    [27.34, 37.94], [27.28, 37.53], [27.42, 37.04], [30.30, 37.20],
                    [31.98, 39.65], [32.86, 39.93], [34.79, 37.28], [34.90, 36.92],
                    [36.20, 36.85], [36.16, 36.20], [35.20, 31.50], [30.00, 31.20],
                    [43.55, 36.55], [44.42, 32.54]]]),
    dict(key="paul_journeys", kind="route", title="圣保罗传道之旅（约 46—58 年）",
         span=[46, 60],
         summary="据《使徒行传》，保罗自叙利亚安条克出发，多次遍历塞浦路斯、佩尔吉、皮西迪亚安条克、以哥念、"
                 "路司得、特庇与以弗所，最后在耶路撒冷被捕、经凯撒利亚海路解送罗马。小亚细亚南部与西部"
                 "因此成为早期基督教最重要的城市网络。",
         labelAt=[31.0, 37.6],
         segments=[[[36.16, 36.20], [35.90, 36.10], [34.00, 35.20], [32.42, 34.77],
                    [30.85, 36.96], [31.19, 38.31], [32.48, 37.87], [32.36, 37.58],
                    [33.30, 37.30], [27.34, 37.94], [26.16, 39.55], [27.28, 37.53],
                    [34.90, 32.50], [23.70, 37.95], [12.48, 41.89]]]),
    dict(key="ibn_battuta", kind="route", title="伊本·白图泰的安纳托利亚（约 1330—1332）",
         span=[1330, 1332],
         summary="摩洛哥旅行家伊本·白图泰经阿拉尼亚登陆，北上科尼亚、开塞利、锡瓦斯、埃尔祖鲁姆，"
                 "再西行阿马西亚、尼刻、布尔萨直到伊斯坦布尔。他的《游记》(Rihla) 记录了 14 世纪"
                 "安纳托利亚诸贝伊国的城镇、教团与商路。",
         labelAt=[35.5, 39.0],
         segments=[[[32.00, 36.54], [32.49, 37.87], [35.49, 38.73], [37.02, 39.75],
                    [39.32, 39.67], [41.27, 39.90], [37.50, 40.20], [35.83, 40.65],
                    [29.72, 40.43], [29.06, 40.19], [28.98, 41.01]]]),
    dict(key="evliya_celebi", kind="route", title="埃夫利亚·切莱比《游记》安纳托利亚行程（1640—1671）",
         span=[1640, 1671],
         summary="奥斯曼宫廷旅行家埃夫利亚·切莱比十年间遍历帝国，十卷《游记》(Seyahatnâme) 详细记载"
                 "安纳托利亚的城池、市场、行会与族群。本线为其安纳托利亚主干：伊斯坦布尔—布尔萨—"
                 "爱琴海诸城—科尼亚—阿达纳—阿勒颇—迪亚巴克尔—凡城—埃尔祖鲁姆—特拉布宗。",
         labelAt=[37.0, 38.4],
         segments=[[[28.98, 41.01], [29.06, 40.19], [27.14, 38.42], [28.18, 38.76],
                    [29.98, 39.42], [30.65, 38.62], [32.49, 37.87], [35.32, 37.00],
                    [34.90, 36.92], [36.16, 36.20], [40.23, 37.91], [42.00, 38.40],
                    [43.38, 38.49], [41.27, 39.90], [39.72, 41.00], [38.15, 39.75],
                    [37.02, 39.75], [32.86, 39.93], [28.98, 41.01]]]),
    dict(key="herodotus", kind="route", title="希罗多德的足迹（约前 450—前 430）",
         span=[-450, -430],
         summary="《历史》作者希罗多德生于哈利卡纳苏斯，据其自述与后世考证，他游历萨摩斯、埃及、"
                 "两河、黑海北岸与希腊本土，最后参与图里伊殖民。书中对吕底亚、波斯行省、"
                 "安纳托利亚诸民族的记述，是本研究区最早的系统民族志。",
         labelAt=[27.5, 38.6],
         segments=[[[27.42, 37.04], [26.90, 37.70], [27.28, 37.53], [26.24, 39.96],
                    [28.98, 41.01], [23.73, 37.98], [22.50, 37.50], [31.20, 30.05],
                    [44.40, 33.31], [16.60, 39.70]]]),
    dict(key="silk_caravan", kind="route", title="安纳托利亚商队干线（丝绸之路西段，13—17 世纪）",
         span=[1240, 1683],
         summary="大不里士—埃尔祖鲁姆—埃尔津詹—锡瓦斯—开塞利—科尼亚—阿达纳/士麦那，"
                 "与特拉布宗黑海港口相连。塞尔柱与奥斯曼沿途修筑商队驿站（caravansaray），"
                 "如苏丹哈尼（1229）与阿赫沙拉伊（13 世纪），构成欧亚贸易的西端。",
         labelAt=[36.0, 39.3],
         segments=[[[46.29, 38.07], [44.09, 39.19], [41.27, 39.90], [39.32, 39.67],
                    [37.02, 39.75], [35.49, 38.73], [34.70, 37.93], [32.49, 37.87],
                    [33.86, 38.38], [32.00, 36.54], [30.70, 36.89], [27.14, 38.42]]]),
]


# 事件详情由 gen_content.attach_details() 挂载（gen_content2 不跑 gen_content.main()）
if hasattr(gc, "attach_details"):
    gc.attach_details()


# 时代 → data/sources/*.json（本时期参考书目，界面「史料来源」区块会加载）
ERA_SOURCE_FILES = {
    "dawn": ["dawn"],
    "hittite": ["hittite"],
    "post_hittite": ["post_hittite"],
    "lydia": ["lydia"],
    "achaemenid": ["achaemenid"],
    "alexander": ["diadochi"],
    "hellenistic": ["hellenistic"],
    "roman": ["roman_conquest", "roman_empire"],
    "byzantine": ["byzantine"],
    "seljuk": ["seljuk"],
    "mongol": ["mongol"],
    "beylik": ["beylik"],
    "ottoman": ["ottoman"],
    "ottoman_late": ["ottoman_late"],
    "republic": ["republic"],
}


def build_dynasty():
    out = []
    for e in ERAS:
        content = next((c for c in gc.CONTENT if c["key"] == e["content"]), None)
        phases = []
        for i, sk in enumerate(e["snaps"]):
            y = SNAP_YEAR[sk]
            phases.append({
                "until": y,
                "snap": f"s_{sk}",
                "overview": f"{y if y > 0 else '前 ' + str(-y)} 年 · {SNAP_CAP[sk]}：{SNAP_NOTE[sk]}",
            })
        note = next((p["note"] for p in ga.PERIODS if p["key"] == e["content"]), "")
        out.append({
            "key": e["key"], "title": e["title"], "badge": e["badge"],
            "fromYear": e["fromYear"], "toYear": e["toYear"], "focusYear": e["focusYear"],
            "tint": e["tint"], "seat": e["seat"], "summary": note,
            "sourceFiles": ERA_SOURCE_FILES.get(e["key"], []),
            "phases": phases,
            "milestones": content["milestones"] if content else [],
            "settlements": content["settlements"] if content else [],
        })
    return out


def main():
    dyn = build_dynasty()
    for _r in ROUTES:
        _r["stops"] = ROUTE_STOPS.get(_r["key"], [])

    js = ("window.DYNASTY_DATA = [\n" +
          ",\n".join("  " + json.dumps(d, ensure_ascii=False) for d in dyn) +
          "\n];\n\nwindow.CORRIDOR_DATA = [\n" +
          ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in ROUTES) +
          "\n];\n")
    open(os.path.join(ROOT, "js", "map_data.js"), "w", encoding="utf-8").write(js)
    total_phases = sum(len(d["phases"]) for d in dyn)
    print(f"js/map_data.js：{len(dyn)} 个时代 / {total_phases} 个快照阶段 / {len(ROUTES)} 条旅行者路线")


if __name__ == "__main__":
    main()
