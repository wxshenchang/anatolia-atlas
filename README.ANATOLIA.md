# 安纳托利亚时序 · Anatolia Chronicle

交互式**小亚细亚（安纳托利亚）历史地图时间轴** —— 前 3500 年苏美尔城邦到现代，含埃及、黎凡特与两河。

仿 [jiangshan-map](https://github.com/DeanChensj/jiangshan-map)（江山时序，GPL-3.0）的前端引擎重制，
地名、疆域、史料、地形全部换成安纳托利亚，本仓库按 **GPL-3.0** 分发（见 `LICENSE`）。

---

## 一、现在有什么

| 维度 | 数量 |
|---|---|
| 历史时代 | 15（新增「两河与尼罗河的黎明」前 3500—前 1650）|
| 阶段快照（时间轴采样点） | 92 |
| 政权要素 | **140 个**：每个都有成立年 / 灭亡年 / 简介 / 依据（`_build/data_polity_info.py`）|
| 宗教分期 | 146 条（政权 × 时期 + 出处；只有卡什卡诸部无考据、页面不显示该行）|
| 古今地名 | 78 |
| 编年纪事 | 171（每条带背景/经过/影响详解 + 出处） |
| 地理范围 | 24–48°E / **29.0–44.5°N**（含巴比伦、泰西封、开罗） |
| 名关通道 | 7 |
| 路线站点（可点卡片） | 74 |
| 旅行者路线 | 7 |
| 人物 | 30 |
| 省界底块 | 土耳其 81 省 + 周边 11 块陆地 |

功能：时间轴拖动/自动播放/倍速、点击溯源（古今政区沿革）、搜索（人物/古今地名/年号）、
古地名寻址测验（10 题一轮）、语音讲解（浏览器 Web Speech API）、图层开关（地形/水系/现代省界/古今地名）、图例、比例尺、简繁切换。

**已移除**：背景音乐、英文模式（`i18n_dict.js` 与 `event_pinyin.js` 仍留在磁盘但**运行时不再加载**）。

---

## 一·五、考据与出处规则（重要）

站内**每一个史事与每一个数据条目都必须带出处**，页面会把出处显示出来。当前覆盖（脚本可直接复核）：

| 类别 | 数量 | 带出处 | 页面显露位置 |
|---|---|---|---|
| 历史事件 | 178 | 178 | 事件浮签「出处」+ 详解末尾 |
| 政权档案（成立/灭亡/简介） | 140 | 140 | 右侧政权面板「据 …」|
| 宗教分期（政权 × 时期） | 146 | 146 | 面板「宗教」行（起止年 · 据 …）|
| 聚落（古今地名对照） | 147 | 147 | 城市悬停提示「据 …」|
| 人物 | 30 | 30 | 人物卡副标题「据 …」|
| 关隘 | 7 | 7 | 关隘悬停提示「据 …」|
| 旅行路线站点 | 74 | 74 | 站点卡片「出处」|
| 地名志 | 97 | 97 | 搜索结果 / 沿革（统一书目）|
| 时代参考书目 | 15 个时代 | 16 个 JSON | 侧栏「史料来源」区块按时代加载 |

规则：

1. **不写没有出处的数字**。年代取学界通行纪年；青铜时代按中年代（浮差 ±30 年属正常），
   若仅有单方文献（如卡什卡诸部），简介里直接写「无确切纪年」，宗教干脆不显示。
2. **出处是「参考著作 / 一手史料」，不是逐句引文页码**。例如赫梯条目据 Bryce《赫梯王国》与哈图沙泥板，
   罗马条目据《剑桥古代史》与卡西乌斯·狄奥、普罗可比等，奥斯曼条目据 TDV《İslâm Ansiklopedisi》与 Zürcher。
3. **疆域是规则化近似**：81 个土耳其省 + 11 个邻国 admin0（后扩到含埃及/黎凡特 21 块）按 24 个历史地理区
   归并成色块，**不是测绘边界**；页面底部有免责声明。
4. **地形**据 Terrarium DEM（AWS elevation-tiles-prod）重烘，配色与夸张系数沿用上游作者。
5. 新增条目若找不到可靠出处：**留空并在简介里说明**，不要凭印象补数字。

## 二、目录结构

```
anatolia-atlas/
├── index.html                 # 单页入口（含 OG / JSON-LD / 隐藏 SEO 目录）
├── css/style.css              # 引擎样式 + 本项目的移动端修补（文件末尾）
├── js/
│   ├── app.js                 # 引擎主控（14 处本地化改动见第五节）
│   ├── map_data.js            # ★ 生成：DYNASTY_DATA(14 时代/48 阶段) + CORRIDOR_DATA(7 路线)
│   ├── lore_core.js           # ★ 生成：人物/地名志/政权/关隘/纪年
│   ├── china_geo_data.js      # ★ 生成：省界 + 水系（文件名沿用上游，内容是安纳托利亚）
│   ├── atlas_snapshots.js     # ★ 由 scripts/build_atlas.js 打包生成
│   ├── atlas_boot.js          # ★ 同上
│   └── atlas_{api,search,trace,quiz,narrator,track}.js   # 上游引擎模块（未改语义）
├── data/
│   ├── atlas/<snapKey>/s_<snapKey>.geojson   # ★ 生成：每阶段政权多边形
│   └── sources/*.json                        # 史料来源（按时代）
├── assets/
│   ├── terrain/{5,6,7}/<x>/<y>.webp          # ★ 生成：地形晕渲瓦片
│   ├── terrain_relief.webp                   # ★ 生成：基础晕渲（RGBA，海面透明）
│   ├── audio/*.mp3                           # 上游中国古琴曲（音乐功能已移除，可删）
│   └── …
├── _build/                    # 数据生产管线（开发期用，不进 Docker 镜像）
│   ├── raw/                   # Natural Earth 原始 GeoJSON
│   ├── dem/                   # Terrarium 高程瓦片（22 MB，可重新下载）
│   ├── vlq.py                 # VLQ 编解码（x1000）
│   └── gen_*.py               # 见下节
├── scripts/
│   ├── build_terrain_tiles.py # 上游脚本，投影常量已改成本区
│   └── build_atlas.js         # 打包 GeoJSON → js/atlas_snapshots.js + 刷新 index.html 资源 hash
├── Dockerfile.static / docker-compose.static.yml / deploy-nginx.conf
└── sitemap.xml / robots.txt   # ★ 生成
```

★ = 本项目的生成物，**不要手改**，改生成器重跑。

**已废弃、不要运行**（第一版留下的，会被上面流程覆盖或产生错误结果）：
`_build/gen_atlas.py`（旧 15 时期版，被 `gen_atlas2.py` 取代）、
`_build/gen_content.py`（同上，被 `gen_content2.py` 取代）、
`_build/gen_relief.py`（自写 shader，已被 `build_terrain_tiles.py --base` 取代）、
`_build/gen_i18n.py`（英文模式已移除）、
`_build/rebrand.py`（一次性改文案，已执行完）。
诊断用（只读）：`_build/check_registration.py`（底图与矢量配准体检）。

---

## 三、重建流程（顺序不能乱）

```bash
cd ~/projects/anatolia-atlas
PY=_build/venv/bin/python          # 需要 shapely / numpy / pillow

# 0) 一次性：虚拟环境 + 原始数据
python3 -m venv _build/venv && _build/venv/bin/pip install shapely numpy pillow
#    _build/raw/*.geojson 来自 Natural Earth 1:10m（admin1 / countries / rivers / lakes / coastline）

# 1) 高程瓦片（需代理，AWS 直连不稳）
$PY _build/fetch_dem.py            # z6/z7 宽框 + z8 窄框，共 259 张 ≈ 22 MB

# 2) 地形晕渲：瓦片 + 基础底图（--base 会顺带重写 terrain_relief.webp）
$PY scripts/build_terrain_tiles.py --dem _build/dem --zooms 5,6,7 --base

# 3) 疆域快照：规则驱动（SPANS = 政权×地理区×年代；SNAPS = 采样年份）
rm -rf data/atlas/* && $PY _build/gen_atlas2.py     # → data/atlas/<key>/s_<key>.geojson

# 4) 内容层：时代分组 + 旅行者路线 + 史料
$PY _build/gen_content2.py                          # → js/map_data.js, data/sources/*.json

# 5) 打包快照（同时刷新 index.html 里所有 ?v= hash）
PATH=~/.nvm/versions/node/v22.23.2/bin:$PATH node scripts/build_atlas.js

# 6) 底图矢量：81 省 + 11 块周边陆地 + 河流湖泊（VLQ x1000）
$PY _build/gen_basemap.py                           # → js/china_geo_data.js

# 7) 文史数据：人物/地名志/政权/关隘/纪年
$PY _build/gen_lore.py                              # → js/lore_core.js

# 8) SEO：JSON-LD / 隐藏目录 / 默认时代文案 / sitemap / robots
$PY _build/gen_seo.py

# 9) 只改前端代码后：刷新资源 hash 并重启
PATH=~/.nvm/versions/node/v22.23.2/bin:$PATH node scripts/build_atlas.js
docker restart anatolia-atlas
```

> 仓库挂载进容器（`docker-compose.static.yml` 的开发期配置），改 `js/css/html` 后**只需 `docker restart`**，不用重建镜像。
> 改了 `deploy-nginx.conf` 才需要 `docker compose -f docker-compose.static.yml up -d --build`。

---

## 四、数据与史料

**地理底块**：Natural Earth 1:10m（公有领域）admin-1 / admin-0。
**高程**：AWS Terrain Tiles（Terrarium 编码，源自 SRTM / GMTED2010）。
**疆域**：土耳其 81 省 + 周边国家一级行政区为底块，按文献归属合并 —— **示意性近似**，误差可达数十公里，不是测绘边界。

**史料**（`data/sources/<时期>.json`，覆盖多国学界成果，具体见每份 JSON）：
Bryce《赫梯王国》、Beckman《赫梯外交文书》、《剑桥古代史》、Briant《从居鲁士到亚历山大》、
Magie《罗马在小亚细亚的统治》、Mitchell《安纳托利亚》、Ostrogorsky《拜占庭国家史》、
Cahen《前奥斯曼土耳其》、Peacock《大塞尔柱帝国》、《剑桥土耳其史》、EI²、
土耳其 TDV《İslâm Ansiklopedisi》、Zürcher《现代土耳其史》，以及希罗多德、斯特拉波、阿里安、安娜·科穆宁娜等原始史料。

**授权**：引擎与快照格式来自 jiangshan-map（GPL-3.0）；Natural Earth 公有领域；
地形晕渲由高程数据本地渲染，仅发布渲染图不发布原始高程网格。

---

## 五、相对上游的关键改动（踩过的坑，别改回去）

1. **投影**：`js/app.js` `MercatorProjector(1000, 700, {west:24, east:48, south:33.5, north:44.5})`。
   上游是 `66/142/14/55`（中国）。
2. **地形脚本的投影常量**：`scripts/build_terrain_tiles.py` 里 `PROJ_W/H/WEST/EAST/SOUTH/NORTH` 同样是上游的中国范围，
   不改就会把底图按中国投影烘出来。
3. **底图必须是 RGBA、海面 alpha=0**：上游的做法是把陆地合成到旧底图上（旧图的海带底色），
   会把 `index.html#ocean-bg`（`--water-fill: #aecfdb`）整块盖住 → 海和纸一个颜色。
4. **周边陆地要有矢量**：`PROVINCE_OUTLINES` 只有本国省界，塞浦路斯/希腊/叙利亚会变成"悬空的晕渲"。
   `_build/gen_basemap.py` 追加 11 块邻国 admin-0，带 `caption:false`（`app.js` 生成省名标注处要 `continue`）。
5. **塞浦路斯在 NE 里是三块**（`Cyprus` / `N. Cyprus` / `Cyprus U.N. Buffer Zone`），
   不合并会渲染出 1974 年绿线的"分离长条"。
6. **矢量精度**：`simplify(0.002/0.004)` + VLQ `x1000`（上游是 `0.01/0.02` + `x100`，约 1.1 km 误差）。
   JS 侧 `dec()` 的 `x/100` 必须同步改 `x/1000`。
7. **缓存**：`assets/terrain*` 是固定文件名，nginx 单独设 `max-age=3600, must-revalidate`；
   `js|css|json` 设 300s；否则换地形/改代码后老访客看不到新版。
   引用 URL 还带版本号（`?v=YYYYMMDDx`），换地形时**记得同时改版本号**。
8. **SEO**：`index.html` 的 canonical / og:url 会被 `js/app.js` 的 `baseSiteUrl`（两处）在运行时改写 ——
   只改 HTML 不生效。JSON-LD 已整块重建（WebSite + Map + ItemList + FAQPage）。
9. **语音**：`atlas_narrator.js` 探测不到音色时**不要**永久禁用按钮（Chrome 首屏常先返回空列表），
   只标记 `_ttsNoVoices`，点击时重探。
10. **年份下限**：`index.html` 的 `#inp-year` `min` 与 `#scrubber-track` 的 `aria-valuemin` 都是 `-1650`。
11. **图外事件**：维也纳、塞夫勒、开罗、卡尔洛维茨等 13 条事件发生地在投影范围（24–48°E / 33.5–44.5°N）之外，
    浮签会被画到画布外。`_getMilestoneAnchors` 用 `_inMapBounds` 判定后，把锚点换成**当时的都城**（`_capitalAnchor`），
    并在浮签头部标注「图外 · 真实地点 → 都城 X」；地点 pill 仍保留真实地名，点地溯源照常可用。
12. **每个政权必须有三件事**：成立年 / 灭亡年（`from`/`to`）、简介（`intro`）、依据（`source`），
    数据放在 `_build/data_polity_info.py`，由 `gen_lore.py` 读入写成 `js/lore_core.js` 的 `POLITY_INFO`；
    面板里按「存续 → 简介 → 宗教 → 疆域」四行显示。**新增政权时三处都要加**：`gen_atlas2.SPANS`（图上色块）、
    `data_polity_info`（档案）、`gen_lore.RELIGION_SPANS`（宗教），否则会出现「有色块但点开没有介绍」。
    ❗带括注的变体名（`奥斯曼帝国（埃及行省）`、`马木留克王朝（黎凡特）`）**不要**在 `_isEraMainPolity` 里被
    去掉括注当成时代主体，否则点它会退化成时代综述、看不到自己的档案。
13. **新加政权前先确认有快照覆盖它的年代**：`gen_atlas2.SPANS` 里年代区间内若没有任何 `SNAPS` 采样点，
    这个政权永远不会出现在图上（曾有 苏美尔城邦/阿卡德帝国/乌尔第三王朝/伊辛与拉尔萨/卡迪·布尔汉丁国 五例）。
    补法：加采样年 + 在 `gen_content2.ERAS` 里挂到对应时代（挂错时代会因阶段 `until` 排序导致显示成别的年份的局面）。
14. **投影南界决定哪些帝国进图**：当前 `south: 29.0`。巴比伦 32.54、泰西封 33.09、开罗 30.04 都在界内；
    开罗（30.04）距下边缘约 6%，再往南的下埃及与上埃及会被裁掉——这是把安纳托利亚当主体的必然取舍，
    要完整埃及得把南界压到 22°N，安纳托利亚会缩到一半。改南界必须同步改三处：
    `js/app.js` 的 `MercatorProjector`、`scripts/build_terrain_tiles.py` 的 `PROJ_*` 常量、`_build/gen_seo.py` 的 GeoShape，
    并重跑 `fetch_dem.py`（宽框南界 28.0）+ `build_terrain_tiles.py --base`，否则地形和新边界对不上。
13. **新区块（埃及/黎凡特）靠 NEIGH 取整块国家多边形**：`_build/fetch_ne.py` 按
    `21–51°E / 26.5–47.5°N` 切片 Natural Earth；`gen_atlas2.py` 的 `NEIGH` 里
    `egypt/israel/palestine/lebanon/jordan` 用 `ADM0_A3`（埃及 EGY、以色列 ISR、巴勒斯坦 **PSX**、黎巴嫩 LBN、约旦 JOR），
    注意巴勒斯坦的 `ISO_A3` 是 PSE 而 `ADM0_A3` 才是 PSX，代码读的是后者。`gen_basemap.py` 的邻国裁剪框也要放到 28.2°N，
    否则南半部只有晕渲没有海岸线。
14. **政权宗教必须是分期的**：`_build/gen_lore.py` 的 `RELIGION_SPANS = [[政权, 起年, 止年, 信仰, 依据], …]`，
    `js/app.js` 的 `polityReligionInfo(name, year)` 按**当前时间轴年份**取最具体的一条（跨度最短优先）。
    ❗ 千万不要退回「一国一教」的静态映射：那会让公元前就出现基督教（亚美尼亚 301 年才定基督教、
    罗马 380 年才以基督教为国教、罗马行省到 4 世纪仍以多神教为主）。同一政权要按改宗节点拆开写。
    ❗ **无考据不写**：该时期找不到可靠分期依据时返回 `{none:true}`，页面显示「该时期暂无考据」或干脆不显示该行
    （例如卡什卡诸部史料仅存赫梯一方记载，就没有写）。每条必须带 `source`，页面会显示「（起止年 · 据 X）」。
13. **事件详解**：每条里程碑在 `_build/gen_content.py` 的 `MILESTONE_DETAIL` 里带 `detail`（背景→经过→影响）与 `source`；
    `gen_content2.py` 读 `gc.CONTENT` 前必须调 `gc.attach_details()`（它原本只在 `gen_content.main()` 里跑，容易漏）。
    ⚠️ `MILESTONE_DETAIL` 的键是**内容的 key**（如 `diadochi`、`roman_empire`），不是时代 key（`alexander`、`roman`），写错会静默不生效。
12. **地图上的政权要与事件文本一致**：事件里提到的政权若图上没有，读者会困惑。已补 `马其顿帝国`（亚历山大本人的政权，
    之前只有继业者）、`埃及新王国`（占据叙利亚区，卡迭石时期与赫梯同屏）、`花剌子模`（1220–1231 札兰丁据东部）、
    `帖木儿帝国`（1402 安卡拉之战后的短暂宗主权）。**图外**且无独立区域的政权（哈布斯堡、塞尔维亚、匈牙利、斯巴达、
    雅典、热那亚、可萨、罗斯、克里米亚汗国、英法德意）**故意不加**，事件文本里另有地点说明。
13. **路线逐站卡片**：站点数据在 `_build/gen_content2.py` 的 `ROUTE_STOPS`（每条路线 8–15 站，含年份/说明/出处），
    生成后写进 `CORRIDOR_DATA[].stops`；`js/app.js` 在画路线时顺带画点（可见 r=3.2 + 透明热区 r=7），
    渲染进独立的 `#grp-route-stops`（挂在 camera-rig 末尾，避免被聚落 hover 提示抢点击）。
    ⚠️ **点击必须用 window 捕获阶段的代理**：地图在 `svg` 上 `setPointerCapture`，
    pointerup/click 会被改派到 svg 根，子元素自己的 `click` 永远收不到（这是踩过的坑）。

---

## 六、部署

```bash
# 容器（restart: unless-stopped，开机自启）
docker compose -f docker-compose.static.yml up -d --build   # → localhost:38602

# 隧道 + 证书（阿里云 frps + Caddy 通配符证书）
#   frp 映射 anatolia → 38602
```

详见 `~/.hermes/skills/devops/frp-tunnel-manager/SKILL.md`。

---

## 七、已知限制

- 疆域边界是**示意性近似**（省块级），不是测绘边界。
- 时间轴是**采样快照**（48 个），不是逐年连续变化。
- 语音讲解依赖浏览器 TTS，无可用音色的环境（如无语音包的系统）不会朗读。
- 手机端（≤640px）触控热区已抬到 32–44px，但底部时间轴 + 图例仍占约 1/5 屏高。
- 英文模式与背景音乐已移除；`js/i18n_dict.js`、`js/event_pinyin.js`、`assets/audio/*.mp3` 已成死资源，可删。

---

## 八、开发常用命令

```bash
# 看容器状态 / 重启
docker ps --filter name=anatolia-atlas
docker restart anatolia-atlas

# 语法检查
node --check js/app.js

# 首屏负载实测（在 crawl4ai 容器里跑 playwright）
docker cp ~/anat-payload.py crawl4ai:/tmp/ && docker exec crawl4ai python /tmp/anat-payload.py
```
