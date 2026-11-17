#!/usr/bin/env python3
"""重写 index.html 的 SEO 区块（JSON-LD / 隐藏目录索引 / 默认时代文案）+ sitemap + robots。
原版的这些区块全是中国内容：canonical 指向 deanchen.me、JSON-LD 里是战国十八朝、
隐藏目录是 34 个中国专题链接 —— 搜索引擎会把这个站当镜像，而且关键词全错。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("ATLAS_SITE_URL", "https://example.com")
NAME = "安纳托利亚时序"
TAGLINE = "小亚细亚历史地图时间轴（赫梯至现代）"

ERA_EN = {
    "hittite": "Hittite Era", "post_hittite": "Early Iron Age", "iron": "Early Iron Age",
    "lydia": "Lydia & the Eastern Kingdoms",
    "achaemenid": "Achaemenid Persia", "alexander": "Alexander & the Diadochi",
    "hellenistic": "Hellenistic Kingdoms", "roman": "Roman Anatolia",
    "byzantine": "Byzantine Anatolia", "seljuk": "Turks & the Crusades",
    "mongol": "Mongol Suzerainty", "beylik": "Beyliks & Ottoman Rise",
    "ottoman": "Ottoman Zenith", "ottoman_late": "Late Ottoman", "republic": "Republic of Türkiye",
}


def load_dyn():
    s = open(os.path.join(ROOT, "js/map_data.js"), encoding="utf-8").read()
    i = s.index("DYNASTY_DATA")
    start = s.index("[", i)
    depth, j, instr, esc = 0, start, False, False
    while j < len(s):
        c = s[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c in "[{":
                depth += 1
            elif c in "]}":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    return json.loads(s[start:j + 1])


def year_label(y):
    return f"前{-y}" if y < 0 else f"{y}"


def build_jsonld(dyn):
    graph = [
        {
            "@type": "WebSite",
            "@id": f"{SITE}/#website",
            "url": f"{SITE}/",
            "name": f"{NAME} · {TAGLINE}",
            "alternateName": "Anatolia Atlas · Historical Atlas of Asia Minor",
            "inLanguage": ["zh-CN", "en"],
            "description": f"交互式{NAME}：赫梯、弗里吉亚、乌拉尔图、吕底亚、阿契美尼德、希腊化诸王国、罗马、拜占庭、罗姆苏丹国、蒙古宗主权、诸贝伊国、奥斯曼与土耳其共和国，48 个阶段疆域快照、78 处古今地名沿革、7 处名关通道与 7 条旅行者路线，附各国学术文献出处。",
        },
        {
            "@type": "Map",
            "@id": f"{SITE}/#map",
            "name": f"{NAME} · {TAGLINE}",
            "url": f"{SITE}/",
            "mapType": "https://schema.org/HistoricalMap",
            "spatialCoverage": {
                "@type": "Place",
                "name": "安纳托利亚 / 小亚细亚 (Anatolia, Asia Minor)",
                "geo": {"@type": "GeoShape", "box": "29.0 24.0 44.5 48.0"},
            },
            "temporalCoverage": "-1650/2026",
            "isAccessibleForFree": True,
            "license": "https://www.gnu.org/licenses/gpl-3.0.html",
            "creator": {"@type": "Organization", "name": NAME},
        },
        {
            "@type": "ItemList",
            "name": "安纳托利亚历史时期目录 / Anatolian periods",
            "numberOfItems": len(dyn),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": f"{d['title']}（{year_label(d['fromYear'])}—{year_label(d['toYear'])} · {ERA_EN.get(d['key'], '')}）",
                    "url": f"{SITE}/?year={d['focusYear']}",
                }
                for i, d in enumerate(dyn)
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "这是什么地图？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"{NAME}（{SITE}/）是一个开源免费的交互式小亚细亚（安纳托利亚）历史地图时间轴，覆盖公元前 1650 年赫梯时代至现代共 14 个历史时代、48 个阶段疆域快照，可拖动时间轴查看各时期政权疆域、古今地名沿革、名关通道与旅行者路线。",
                    },
                },
                {
                    "@type": "Question",
                    "name": "疆域边界是精确的测绘边界吗？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "不是。历史疆域按土耳其 81 省与周边国家一级行政区为底块、依据文献归属合并而成，属于示意性近似（近似误差可达数十公里），仅供历史地理参考，不可作为测绘或法律依据。地形晕渲基于 SRTM/GMTED2010 公开高程数据。",
                    },
                },
                {
                    "@type": "Question",
                    "name": "史料来源有哪些？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "覆盖多国学界成果：Bryce《赫梯王国》、Beckman《赫梯外交文书》、《剑桥古代史》、Briant《从居鲁士到亚历山大》、Magie《罗马在小亚细亚的统治》、Mitchell《安纳托利亚》、Ostrogorsky《拜占庭国家史》、Cahen《前奥斯曼土耳其》、Peacock《大塞尔柱帝国》、《剑桥土耳其史》、EI²、土耳其 TDV《İslâm Ansiklopedisi》、Zürcher《现代土耳其史》，以及希罗多德、斯特拉波、阿里安、安娜·科穆宁娜等原始史料。",
                    },
                },
            ],
        },
    ]
    return {"@context": "https://schema.org", "@graph": graph}


def build_directory(dyn):
    lines = [
        f'    <nav id="seo-atlas-directory" class="sr-only-seo" aria-hidden="true" aria-label="安纳托利亚历代疆域、点地溯源与名关通道索引">',
        f"      <h2>{NAME}：安纳托利亚历代疆域地图、古今地名对照与历史事件全览（前 1650 年—现代）</h2>",
        f"      <p>本交互式小亚细亚历史地图时间轴涵盖赫梯、铁器早期、吕底亚与东方诸国、阿契美尼德波斯、亚历山大与继业者、希腊化诸王国、罗马、拜占庭、突厥与十字军、蒙古宗主权、诸贝伊国与奥斯曼、奥斯曼鼎盛与晚期直到土耳其共和国，共 14 个历史时代、48 个阶段疆域快照、78 处古今地名沿革、7 处名关通道与 7 条旅行者路线。</p>",
        "      <section>",
        "        <h3>一、历代疆域时间轴目录（Periods &amp; Territories）</h3>",
        "        <ul>",
    ]
    for d in dyn:
        seat = d.get("seat") or ""
        summary = (d.get("summary") or "").strip()
        summary = re.sub(r"\s+", " ", summary)[:170]
        lines.append(
            f'          <li><a href="{SITE}/?year={d["focusYear"]}"><strong>{d["title"]}（{year_label(d["fromYear"])}—{year_label(d["toYear"])} · {ERA_EN.get(d["key"], "")}）</strong></a>'
            + (f" — 都城：{seat}。" if seat else " — ")
            + f"{summary}</li>"
        )
    lines += ["        </ul>", "      </section>"]

    # 名关通道
    lore = open(os.path.join(ROOT, "js/lore_core.js"), encoding="utf-8").read()
    m = re.search(r'"STRATEGIC_PASSES":\s*(\[)', lore)
    start = m.end() - 1
    depth, j, instr, esc = 0, start, False, False
    while j < len(lore):
        c = lore[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c in "[{":
                depth += 1
            elif c in "]}":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    passes = json.loads(lore[start:j + 1])
    lines += ["      <section>", "        <h3>二、名关雄隘与战略通道（Strategic Passes）</h3>", "        <ul>"]
    for p in passes:
        lines.append(
            f'          <li><a href="{SITE}/?year={p.get("focusYear", -1300)}&amp;place={p["ancientZh"]}"><strong>{p["ancientZh"]}（{p.get("ancientEn", "")} · 今{p.get("modernZh", "")}）</strong></a></li>'
        )
    lines += ["        </ul>", "      </section>"]

    # 旅行者路线
    corridors = None
    m2 = re.search(r'CORRIDOR_DATA\s*=\s*(\[)', open(os.path.join(ROOT, "js/map_data.js"), encoding="utf-8").read())
    if m2:
        s2 = open(os.path.join(ROOT, "js/map_data.js"), encoding="utf-8").read()
        st = m2.end() - 1
        depth, k, instr, esc = 0, st, False, False
        while k < len(s2):
            c = s2[k]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    instr = False
            else:
                if c == '"':
                    instr = True
                elif c in "[{":
                    depth += 1
                elif c in "]}":
                    depth -= 1
                    if depth == 0:
                        break
            k += 1
        corridors = json.loads(s2[st:k + 1])
    if corridors:
        lines += ["      <section>", "        <h3>三、旅行者与行迹路线（Traveler Routes）</h3>", "        <ul>"]
        for c in corridors:
            span = c.get("span") or ""
            lines.append(
                f'          <li><a href="{SITE}/?year={c.get("fromYear", -400)}"><strong>{c["title"]}（{span}）</strong></a> — {str(c.get("desc") or c.get("summary") or "")[:110]}</li>'
            )
        lines += ["        </ul>", "      </section>"]
    lines.append("    </nav>")
    return "\n".join(lines)


def main():
    path = os.path.join(ROOT, "index.html")
    html = open(path, encoding="utf-8").read()
    dyn = load_dyn()

    # 1) 域名：canonical / hreflang / og:url / 专题链接
    html = html.replace("https://deanchen.me/jiangshan-map/", SITE + "/")
    html = html.replace("https://deanchen.me/", SITE + "/")

    # 2) JSON-LD 整块重建
    jsonld = json.dumps(build_jsonld(dyn), ensure_ascii=False, indent=2)
    html, n1 = re.subn(
        r'<script type="application/ld\+json">.*?</script>',
        '<script type="application/ld+json">\n' + jsonld + "\n  </script>",
        html, count=1, flags=re.S)

    # 3) 隐藏目录导航整块重建
    html, n2 = re.subn(
        r'    <nav id="seo-atlas-directory".*?</nav>',
        build_directory(dyn), html, count=1, flags=re.S)

    # 4) 首屏默认时代文案：战国 → 赫梯时代
    first = dyn[0]
    html = re.sub(r'(<h2 id="dynasty-title">)[^<]*(</h2>)', r"\g<1>" + first["title"] + r"\g<2>", html, count=1)
    html = re.sub(r'(<p id="dynasty-summary" class="dynasty-desc">)[^<]*(</p>)',
                  r"\g<1>" + re.sub(r"\s+", " ", first["summary"]).strip() + r"\g<2>", html, count=1)
    # 年份输入框下限
    html = html.replace('min="-403" max="2026" step="1" value="-403"', 'min="-1650" max="2026" step="1" value="-1650"')

    open(path, "w", encoding="utf-8").write(html)
    print(f"index.html 重写：JSON-LD {n1} 块、目录 {n2} 块、域名已换")

    # 5) sitemap
    urls = [f"{SITE}/"]
    urls += [f"{SITE}/?year={d['focusYear']}" for d in dyn]
    urls += [f"{SITE}/?lang=en"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == f"{SITE}/" else "0.8"
        sm.append(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
    print(f"sitemap.xml: {len(urls)} 条")

    # 6) robots
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("robots.txt 已写")


if __name__ == "__main__":
    main()
