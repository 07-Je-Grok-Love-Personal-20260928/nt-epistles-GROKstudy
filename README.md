# 新约书信深读-20261114-v2.0.0-GROKstudy

> **主题**：圣经《新约书信》全部 21 卷（罗马书—犹大书）深度解读 · 欧陆改革宗正统 · 圣经神学与圣约神学  
> **时间**：2026-11-14（台北时间）　**版本**：v2.0.0　**标识**：GROKstudy  
> 固定还原点：v1.0.0（2026-10-23）标签仍保留，可随时回退。

## 🔗 本版（v2.0.0）链接

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/nt-epistles-GROKstudy/ |
| Surge | https://nt-epistles-20261114-v2-grokstudy.surge.sh |
| Netlify | https://nt-epistles-20261114-v2-grokstudy.netlify.app |
| 源代码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/nt-epistles-GROKstudy |
| v2.0.0 发布 | https://github.com/07-Je-Grok-Love-Personal-20260928/nt-epistles-GROKstudy/releases/tag/v2.0.0 |
| v1.0.0 发布（还原点） | https://github.com/07-Je-Grok-Love-Personal-20260928/nt-epistles-GROKstudy/releases/tag/v1.0.0 |

## ✨ v2.0.0 更新说明（相对 v1.0.0）

1. **地图馆（新页面）**：每张专题地图都是「离线概念讲解图 + 可缩放真实地图」成对出现。真实地图使用本地打包的 Leaflet（无 CDN），可选 12 种全球底图（OpenStreetMap、OSM Humanitarian、OSM DE、CARTO Positron/Voyager/Dark、Esri 卫星/地形/National Geographic、OpenTopoMap、DARE 罗马帝国古图、Natural Earth 离线矢量）。某一来源超时或出错会自动切换下一个；全部失败则使用本站打包的 Natural Earth 矢量，**地图不会空白**。新增专题：罗马帝国行省（约主后 60 年）、四次宣教旅行、押解罗马航海、彼得前书小亚五省、亚细亚七教会、从耶路撒冷到地极、21 卷书信写作地→收信地。各书卷页的迷你图下也可展开互动地图。
2. **顺滑度**：去掉卡片上的大面积 `backdrop-filter`（毛玻璃只留在顶栏、目录、弹出层等少数固定层）；分区 `content-visibility`；只做 transform/opacity 动画；本地打包 Lenis 惯性滚动（尊重 `prefers-reduced-motion`，不劫持目录和地图）；MPA 视图过渡。测量见下。
3. **笔记标记**：全站统一六色体系——重点（金、实线、底纹）、难点（珊瑚、波浪线）、圣约（紫、虚线）、术语（青、点线）、应用（绿、实线）、记忆（橙、双下划线）；另有六种色条呼出块。首页有完整图例。
4. **内容**：压缩空话，把历史地理的本质放进地图馆与呼出块；信条引文仍全部逐字取自 ccifellowship.org。
5. **配色与动效**：更高饱和但仍克制的夜/日双主题；概念图带 CSS 动画（路线勾绘、灯台闪烁、航海颠簸）。

## 📏 性能（Playwright，1440×900，本地静态服务，滚动一遍）

| 页面 | v1 FCP / 长任务 | v2 FCP / 长任务 | CLS |
|---|---|---|---|
| 首页 | 344 ms / 215 ms | 212 ms / 88 ms | 0 |
| 时间线 | 152 ms / 61 ms | 136 ms / 50 ms | 0 |
| 四大书信 | 204 ms / 118 ms | 216 ms / 70 ms | 0 |
| 三大信经 | 116 ms / 0 | 136 ms / 0 | 0 |
| 记忆 | 168 ms / 55 ms | 376 ms / 166 ms | 0 |
| 地图馆（新） | — | 172 ms / 431 ms（含首次拉瓦片） | 0.117 |

首页长任务明显下降；地图馆首次进入会加载 Leaflet 与底图，长任务和轻微 CLS 是预期代价（画布已预留高度）。记忆页数字有波动，且该页脚本更重（题库与翻卡）。

## ✅ 校验与 QA

- 信条引文：93 块 / 122 段，与 ccifellowship.org 现场页面及本地 JSON **122/122 逐字通过**；三大信经背诵版 3/3；威斯敏斯特 9/9；正文引号片段（≥7 字）未匹配 0 处。
- Playwright 视口：360、390、768、1024、1440、1920；12 页；另在 390 与 1440 再跑一轮交互（目录开关、主题、折叠、翻卡、时间线筛选、图层、底图切换、信经背诵模式）。横向溢出 / 裁切 / 页头重叠 / JS 错误：交互修正后通过。1920 宽下翻卡 3D 变换曾有 5px 越界，已用 `overflow:hidden` 修掉并复检。
- 地图：切断 OSM/CARTO/Esri/OTM/DARE 瓦片后，底图在约 1 秒内落到「离线矢量（Natural Earth）」，矢量路径仍在，画面不为空。中途单源失败会先自动改用下一在线源（例如 DARE → CARTO）。

## 📚 页面

| 页面 | 内容 |
|---|---|
| 首页 | 21 卷一览、学习路线、思维导图、笔记图例 |
| 圣经·圣约 | 救赎历史、两个世代、预表、恩典之约、海德堡三段、多特五要点 |
| 时间线 | 可筛选时间线、年代图、故事线、离线总图、文化区域 |
| 地图馆（新） | 概念图 + 多源互动地图（见上） |
| 四大 / 狱中 / 教牧 / 大公书信 | 逐卷深读；迷你图下可展开互动地图 |
| 教义、三大信经、记忆、来源 | 同 v1，并套用新标记与配色 |

## 🛠️ 构建

```bash
python3 build/build.py      # 生成 docs/
python3 build/verify.py     # 引文校验（会联网抓取 CCI）
python3 build/build.py      # 把校验结果写入来源页
python3 tools/qa.py         # Playwright
```

静态站点在 `docs/`。Leaflet、Lenis、Natural Earth GeoJSON 均本地打包。

## 📝 版本记录

| 版本 | 日期（台北时间） | 说明 | 访问 |
|---|---|---|---|
| v2.0.0 | 2026-11-14 | 地图馆、多源底图自动回退、离线矢量兜底、笔记六色标记、滚动与毛玻璃优化、配色刷新 | [Pages](https://07-je-grok-love-personal-20260928.github.io/nt-epistles-GROKstudy/) · [Surge](https://nt-epistles-20261114-v2-grokstudy.surge.sh) · [Netlify](https://nt-epistles-20261114-v2-grokstudy.netlify.app) |
| v1.0.0 | 2026-10-23 | 首次发布：21 卷深读、圣约、时间线、教义、信经、记忆自测 | [Surge v1](https://nt-epistles-20261023-v1-grokstudy.surge.sh) · [Netlify v1](https://nt-epistles-20261023-v1-grokstudy.netlify.app) · [标签](https://github.com/07-Je-Grok-Love-Personal-20260928/nt-epistles-GROKstudy/releases/tag/v1.0.0) |

## ⚖️ 说明

信经与信条中文引文版权属 ccifellowship.org（CCI）及其译者，本站仅逐字引用并注明出处；和合本经文为公有领域；地图数据来自 Natural Earth（公有领域）。在线底图版权归 OpenStreetMap、CARTO、Esri、OpenTopoMap、DARE（哥德堡大学）各自所有，仅在用户选择时由浏览器直接请求。行省范围与航线为教学示意，不是精密复原。讲解、图表与口诀为学习整理，不是任何教会的正式文件。
