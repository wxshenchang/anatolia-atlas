#!/usr/bin/env python3
"""把 index.html / manifest / sitemap 的中国历史文案换成安纳托利亚版本。"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("ATLAS_SITE_URL", "https://example.com")
NAME = "安纳托利亚时序"
TITLE = "安纳托利亚时序 · 小亚细亚历史地图时间轴（赫梯至现代）"
DESC = ("交互式小亚细亚历史地图时间轴：从赫梯帝国、弗里吉亚与乌拉尔图、吕底亚、阿契美尼德波斯、"
        "希腊化诸王国、罗马与拜占庭，到罗姆苏丹国、蒙古宗主权、安纳托利亚诸贝伊国、奥斯曼帝国与土耳其共和国，"
        "15 个时期疆域快照、古今地名沿革、名关通道与人物纪事，附各国学术文献出处。")
KEYS = ("安纳托利亚时序,小亚细亚历史地图,土耳其历史地图,赫梯帝国地图,吕底亚,阿契美尼德,希腊化王国,"
        "罗马亚细亚行省,拜占庭军区,罗姆苏丹国,奥斯曼帝国地图,土耳其共和国,古今地名对照,历史地图时间轴,"
        "Anatolia,Asia Minor,Historical Atlas of Anatolia,Hittite Empire,Ottoman Empire Map")


def rw_index():
    p = os.path.join(ROOT, "index.html")
    h = open(p, encoding="utf-8").read()
    orig = len(h)

    h = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", h, count=1)
    h = re.sub(r'(<meta name="description" id="meta-description" content=")[^"]*(")',
               lambda m: m.group(1) + DESC + m.group(2), h)
    h = re.sub(r'(<meta name="keywords" content=")[^"]*(")',
               lambda m: m.group(1) + KEYS + m.group(2), h)
    h = h.replace('content="江山时序 · 中国历史地图时间轴"', f'content="{NAME}"')
    h = re.sub(r'(id="og-title" content=")[^"]*(")', lambda m: m.group(1) + TITLE + m.group(2), h)
    h = re.sub(r'(id="og-description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), h)
    h = re.sub(r'(id="tw-title" content=")[^"]*(")', lambda m: m.group(1) + TITLE + m.group(2), h)
    h = re.sub(r'(id="tw-description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), h)
    h = h.replace("江山时序 · 中国历史地图时间轴预览", "安纳托利亚时序 · 小亚细亚历史地图预览")

    # JSON-LD 里的 name/description
    h = re.sub(r'"name": "江山时序[^"]*"', f'"name": "{TITLE}"', h)
    h = re.sub(r'"description": "交互式中国历史地图时间轴[^"]*"', f'"description": "{DESC}"', h)
    h = re.sub(r'"url": "https://[^"]*jiangshan[^"]*"', f'"url": "{SITE}/"', h)
    h = h.replace("https://github.com/DeanChensj/jiangshan-map", "https://github.com/DeanChensj/jiangshan-map")

    # 页面里可见的中文品牌名
    h = h.replace("江山时序", "安纳托利亚时序")
    h = h.replace("中国历史", "小亚细亚历史")
    open(p, "w", encoding="utf-8").write(h)
    print(f"index.html {orig} → {len(h)} 字节")


def rw_manifest():
    p = os.path.join(ROOT, "manifest.webmanifest")
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        d = {}
    d["name"] = TITLE
    d["short_name"] = NAME
    d["description"] = DESC
    d["start_url"] = "./"
    d["scope"] = "./"
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("manifest.webmanifest 已更新")


def rw_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f'  <url><loc>{SITE}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
           '</urlset>\n')
    open(p, "w", encoding="utf-8").write(xml)
    print("sitemap.xml 重写为单页")


def drop_topics():
    t = os.path.join(ROOT, "topics")
    if os.path.isdir(t):
        shutil.rmtree(t)
        print("已删除 topics/（原为中国战役专题页）")


def rw_robots():
    p = os.path.join(ROOT, "robots.txt")
    open(p, "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("robots.txt 已更新")


def rw_llms():
    p = os.path.join(ROOT, "llms.txt")
    if os.path.exists(p):
        open(p, "w", encoding="utf-8").write(
            f"# {NAME}（{TITLE}）\n\n"
            f"{DESC}\n\n"
            f"- 站点: {SITE}/\n"
            "- 数据格式: data/atlas/<period>/s_<period>.geojson（江山时序兼容）\n"
            "- 史料: data/sources/<period>.json（各国学术文献）\n"
            "- 底图: Natural Earth 1:10m（public domain）；疆域底块: historical-basemaps (GPL-3.0)\n"
            "- 界面: 改编自 Jiangshan Atlas（GPL-3.0, github.com/DeanChensj/jiangshan-map）\n")
        print("llms.txt 已更新")


if __name__ == "__main__":
    rw_index()
    rw_manifest()
    rw_sitemap()
    rw_robots()
    rw_llms()
    drop_topics()
