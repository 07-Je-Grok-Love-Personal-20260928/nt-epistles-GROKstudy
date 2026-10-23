# -*- coding: utf-8 -*-
import os, sys, json, re, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common import page, QUOTES, VER, DATE
from eps1 import EPS1; from eps2 import EPS2; from eps3 import EPS3
from epi import epistle, mindtree, gtable, GN
import geo, p_whole, p_hist, p_doc, p_creed, p_mem, p_misc
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(D, "assets", "geo"), exist_ok=True)
geo.base_svg(os.path.join(D, "assets", "geo", "med.svg"))
EPS = EPS1 + EPS2 + EPS3
order = ["rom","1co","2co","gal","eph","php","col","1th","2th","1ti","2ti","tit","phm","heb","jas","1pe","2pe","1jn","2jn","3jn","jud"]
byid = {e["id"]: e for e in EPS}; CAN = [byid[i] for i in order]
def grp(fn, title, sub, eps, intro):
    body = f'<h2 id="ov">🗂️ 本组总览</h2><div class="card glass"><p>{intro}</p></div>' + mindtree(title, eps) + gtable(eps) + "".join(epistle(e) for e in eps)
    W(fn, page(fn, title, sub, body))
def W(fn, html):
    open(os.path.join(D, fn), "w", encoding="utf-8").write(html); print("wrote", fn, len(html)//1024, "KB")
W("index.html", page("index.html", "新约书信深读", "罗马书到犹大书 21 卷 · 整本圣经与圣约 · 时间故事地图 · 欧陆改革宗 · 三项联合信条与三大信经逐字对照", p_misc.index(CAN), "home"))
W("bible.html", page("bible.html", "整本圣经与圣约", "先看全景：书信在创造—堕落—救赎—成全的救赎历史与恩典之约中的位置", p_whole.build()))
W("history.html", page("history.html", "时间 · 故事 · 地图", "主后 30–95 年：使徒行传的故事线、保罗的行程、21 卷书信的写作地与收信地、希腊罗马文化", p_hist.build(CAN)))
from common import md
grp("paul-major.html", "保罗四大书信", "罗马书 · 哥林多前书 · 哥林多后书 · 加拉太书——福音的核心与教会的实际", EPS1,
    md("这四卷写于第一、三次宣教旅行期间（约 48–57 年），篇幅最长、教义最集中：**因信称义**（罗、加）与**十字架下的教会生活**（林前、林后）。读的顺序建议：加拉太书 → 罗马书 → 哥林多前书 → 哥林多后书。"))
grp("paul-prison.html", "帖撒罗尼迦书信 · 狱中书信", "帖前 · 帖后（早期）· 以弗所书 · 腓立比书 · 歌罗西书 · 腓利门书（罗马被囚）", EPS2[:6],
    md("帖撒罗尼迦前后书是保罗最早的书信之一，焦点是**主再来**；四卷狱中书信写于罗马软禁时（徒28:30），焦点是**基督与教会**：基督为首（西）、教会是身体（弗）、在基督里喜乐（腓）、在基督里接纳（门）。"))
grp("paul-pastoral.html", "教牧书信", "提摩太前书 · 提摩太后书 · 提多书——神的家、纯正的道、交棒", EPS2[6:],
    md("保罗晚年写给同工的三封信：怎样在神的家中行事（**提前3:15**）、怎样设立长老、怎样守住所托付的善道。提摩太后书是保罗最后的书信。"))
grp("general.html", "希伯来书 · 大公书信", "希伯来书 · 雅各书 · 彼得前后书 · 约翰一二三书 · 犹大书", EPS3,
    md("这八卷写给分散各地的信徒（因此称“大公”或“普通”书信）。希伯来书证明基督“更美”；雅各书要真信心结出行为；彼得书信教导在苦难中盼望；约翰书信给出得救确据的试验；犹大书呼吁为真道争辩。"))
W("doctrine.html", page("doctrine.html", "教义主题 · 信条对照", "十大教义主题，从书信经文到三项联合信条（CCI 逐字）与威斯敏斯特标准", p_doc.build()))
W("creeds.html", page("creeds.html", "三大普世信经", "使徒信经 · 尼西亚信经 · 亚他那修信经：干净背诵版、深度对比、为何有三份", p_creed.build()))
W("memory.html", page("memory.html", "记忆 · 自测", "口诀、钥字、记忆卡、钥节填空、小考、记忆宫殿与 21 天计划", p_mem.build(CAN)))
json.dump([[k, str(a), b] for k, a, b in QUOTES], open(os.path.join(ROOT, "build", "quotes.json"), "w"), ensure_ascii=False, indent=0)
stats_f = os.path.join(ROOT, "build", "verify_stats.json")
stats = json.load(open(stats_f)) if os.path.exists(stats_f) else [["状态", "尚未运行 verify.py"]]
W("sources.html", page("sources.html", "来源 · 校验", "引用来源、逐字校验结果、局限说明与版本记录", p_misc.sources(stats)))
open(os.path.join(D, ".nojekyll"), "w").write("")
print("quotes:", len(QUOTES))
