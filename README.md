# 安纳托利亚时序 · Anatolia Chronicle

**交互式小亚细亚（安纳托利亚）历史地图时间轴**：前 3500 年苏美尔城邦 → 现代土耳其，覆盖安纳托利亚、埃及、黎凡特与两河。

---

## ⭐ 参考来源与衍生说明（请先读这段）

本项目**不是原创**，它是下列作品的**中文衍生重制**：

| 项目 | 作者 | 许可证 | 本项目用了什么 |
|---|---|---|---|
| [**DeanChensj/jiangshan-map**（江山时序）](https://github.com/DeanChensj/jiangshan-map) | Dean Chensj | **GPL-3.0** | **核心原型**：整套前端可视化引擎、时间轴交互、矢量底图与叠加图层、投影与相机、地名沿革/人物/关隘的交互范式、构建脚本骨架，均来自该项目 |
| [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps) | Andrei Ourednik 等 | GPL-3.0 | 历史政权多边形基底 |
| [Natural Earth 1:10m](https://www.naturalearthdata.com/) | Natural Earth | Public Domain | 国界、省界、海岸线、河湖 |
| [AWS Terrain Tiles (Terrarium)](https://registry.opendata.aws/terrain-tiles/) | Mapzen / AWS Open Data | 见来源声明 | 高程数据（重烘安纳托利亚地形晕渲） |

**许可证**：本项目与其原型一致，按 **GPL-3.0** 分发，见 [`LICENSE`](LICENSE)。原项目全部版权与署名归 Dean Chensj 及各位上游作者；本仓库只对**内容层**（地名、疆域规则、史料、宗教、地形重制）重做并负责。

我做的是把"中国历史"整套换掉：

- 地形：原仓库预烘的是**中国**高程，已用 Terrarium DEM 按同一套 shader 重烘 `24–48°E / 29.0–44.5°N`
- 疆域：81 个土耳其省 + 21 块周边国界，按 24 个历史地理区归并成 **92 个时期快照 / 15 个历史时代**
- 内容：178 条历史事件、146 个政权档案（成立/灭亡 + 简介）、152 条宗教分期、147 处聚落、97 条地名志、74 个路线站点、7 处关隘、30 位人物
- 界面：中文简化字、移动端适配、删除上游的"雅乐"（中国古琴曲）与英文模式

---

## 一、功能

- **时间轴**：前 3500 → 2026，15 个时代 / 92 个快照，可拖动、可播放、可倍速
- **政权色块**：每个快照按历史地理区重组，点开看到「存续 → 简介 → 宗教 → 疆域」
- **历史事件**：178 条，每条带「背景 → 经过 → 影响」+ 出处；发生在图外的事件自动锚定到当时都城并标注「图外」
- **宗教分期**：146 条「政权 × 时期」条目，全部带出处；改宗节点分开写（亚美尼亚 301 年、罗马 380 年、伊儿汗 1295 年…）
- **旅行者路线**：7 条（希罗多德、色诺芬万人远征、亚历山大、保罗、伊本·白图泰、埃夫利亚·切莱比等），74 个可点站点
- **史料来源**：每个时代的参考书目在右侧栏「史料来源」区块按需加载（16 份 JSON）
- **语音讲解 / 搜索 / 人物沿革 / 关隘战史 / 地名今古对照**

移动端（390×844）实测无横向溢出、无 JS 错误。

## 一·六、译名规范（面向中文读者）

采用《中国大百科全书·世界历史》与国内高校世界史教材的通行译名，并尽量贴中文读者已有的认知：

- 中国史书有专名的，以中文史籍名为主：**安息帝国**（帕提亚）、**大食/花剌子模**等
- 常见错译已改：**达尼什曼德王朝**（原误作「丹麦门德」）、**吕西尼昂**（原「卢西尼昂」）、
  **马穆鲁克**（原「马木留克」）、**埃布拉**（原「埃勃拉」）、**亚兰人**（原「阿拉米人」）、
  **阿希亚瓦**（原「阿黑亚瓦」）、**新赫梯诸邦**（原「卢维新赫梯诸邦」）
- 与通名统一：**特拉布宗帝国**（城市与政权同名）、**罗马东方行省**、**伊辛—拉尔萨时期**、
  **哈斯蒙尼王朝**、**罗马塞浦路斯行省**、**埃及第三中间期**
- 地名从今译：**卡尼什**（Kültepe）、**卡赫美什**、**埃克巴坦那**（今哈马丹）、**特拉布宗**

## 二、考据规则

站内**每个史事与每个数据条目都带出处**，页面会显示。当前覆盖：

| 类别 | 数量 | 带出处 | 页面显露位置 |
|---|---|---|---|
| 历史事件 | 178 | 178 | 事件浮签 + 详解末尾 |
| 政权档案 | 146 | 146 | 政权面板「据 …」|
| 宗教分期 | 152 | 152 | 面板「宗教」行（起止年 · 据 …）|
| 聚落 | 147 | 147 | 城市悬停提示 |
| 人物 | 30 | 30 | 人物卡副标题 |
| 关隘 | 7 | 7 | 关隘悬停提示 |
| 路线站点 | 74 | 74 | 站点卡片 |
| 地名志 | 97 | 97 | 搜索/沿革（统一书目）|

- 出处是**参考著作 / 一手史料**（如 Bryce《赫梯王国》、哈图沙泥板、《剑桥古代史》、Briant、Ostrogorsky、Cahen、Zürcher、TDV《İslâm Ansiklopedisi》、希罗多德、阿里安等），**不是逐句引文的页码**。
- 年代取学界通行纪年；青铜时代按中年代，浮差 ±30 年属正常。
- **找不到可靠出处就不写**：例如「卡什卡诸部」仅有赫梯单方文献，宗教行直接不显示，简介里注明"无确切纪年"。
- 疆域是**规则化近似**（省/国界多边形按历史地理区归并），**不是测绘边界**，页面底部有免责声明。

## 三、本地运行

```bash
git clone https://github.com/<you>/anatolia-chronicle.git
cd anatolia-chronicle
docker compose -f docker-compose.static.yml up -d --build
# 打开 http://localhost:38602
```

纯静态也行（nginx 托管仓库根目录即可，见 `deploy-nginx.conf`）。

## 四、重建数据（可选）

`_build/` 下的生成器是数据源，详细流程见 **[README.ANATOLIA.md](README.ANATOLIA.md)**（9 步重建、坑位清单、废弃脚本黑名单）。

```bash
python -m venv _build/venv && _build/venv/bin/pip install shapely
_build/venv/bin/python _build/fetch_ne.py          # 拉 Natural Earth 切片
_build/venv/bin/python _build/fetch_dem.py         # 拉 Terrarium DEM
_build/venv/bin/python _build/gen_atlas2.py        # 政权多边形 → data/atlas
_build/venv/bin/python _build/gen_basemap.py       # 省界/邻国/河湖 → js/china_geo_data.js
_build/venv/bin/python _build/gen_lore.py          # 纪年/关隘/地名/人物/政权/宗教
_build/venv/bin/python _build/gen_content2.py      # 时代/事件/路线 → js/map_data.js
_build/venv/bin/python scripts/build_terrain_tiles.py --dem _build/dem --zooms 5,6,7 --base
node scripts/build_atlas.js                        # 打包快照
_build/venv/bin/python _build/gen_seo.py           # sitemap/robots/JSON-LD
```

## 五、目录

```
index.html            页面骨架
js/                   前端（app.js 主引擎、atlas_trace.js 沿革、map_data.js 内容、lore_core.js 志书）
css/                  样式（含移动端媒体查询）
assets/terrain*/      地形晕渲底图与瓦片（按 29.0–44.5°N 重烘）
data/atlas/           92 个时期快照 geojson（构建输入）
data/sources/         16 份分期参考书目 JSON（页面「史料来源」）
_build/               数据生成器（Python）
scripts/              上游构建脚本（打包快照、地形瓦片、测试）
```

## 六、已知限制

- 埃及只显示到下埃及（三角洲—开罗），南界 29°N 是以安纳托利亚为主体的取舍；要完整埃及需压到 22°N，安纳托利亚会缩一半
- 快照是离散采样，页面年份会吸附到最近的快照（例如 1100 年显示 1120 年局面）
- 边界精度为"历史示意"级别，不可用于任何测绘或主张用途
- 上游遗留的英文模式与音乐已删除，相关 JS/CSS 仍可能残留少量未引用代码

## 七、致谢

- **Dean Chensj** — [jiangshan-map](https://github.com/DeanChensj/jiangshan-map)，没有它就没有本项目
- Natural Earth、Andrei Ourednik、Mapzen/AWS 提供底图与高程
- 各条目出处见站内「史料来源」区块与 `data/sources/`

许可证：**GPL-3.0**（与原型一致）。
