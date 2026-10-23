# -*- coding: utf-8 -*-
import json, re
from common import md, esc, vtext
from epi import GN
PG={"major":"paul-major.html","early":"paul-prison.html","prison":"paul-prison.html","pastoral":"paul-pastoral.html","heb":"general.html","gen":"general.html"}
def plain(s): return re.sub(r'\{\{(.+?)\}\}',r'\1',re.sub(r'(\*\*|!!|==|\[\[|\]\])','',s))
def data(eps):
    return [dict(id=e["id"],n=e["n"],ab=e["ab"],ic=e["ic"],kw=e["kw"],kv=e["kv"],kvt=vtext(e["kv"]),place=plain(e["place"]),date=plain(e["date"]),mn=plain(e["mn"]),g=e["g"],c=GN[e["g"]][1],ch=e["ch"],pg=PG[e["g"]]+"#"+e["id"]) for e in eps]
CHRONO=["jas","gal","1th","2th","1co","2co","rom","eph","col","phm","php","1ti","tit","1pe","2ti","2pe","heb","jud","1jn","2jn","3jn"]
def build(eps):
    D=data(eps); by={d["id"]:d for d in D}
    b=['<h2 id="m1">一、书卷顺序口诀</h2><div class="mnem glass reveal"><p class="big">罗 林 林 加 弗 腓 西，<br>帖 帖 提 提 多 门 希；<br>雅 彼 彼 约 约 约 犹。</p><p class="note">按和合本正典顺序：前两句是保罗书信（13 卷）与希伯来书，第三句是七卷大公书信。节奏 7-7-7，正好 21 卷。</p></div>']
    b.append('<div class="chips">'+"".join(f'<a class="chip" href="{d["pg"]}" style="--c:{d["c"]}"><span>{d["ic"]}</span>{d["ab"]}<small>{d["kw"]}</small></a>' for d in D)+'</div>')
    b.append('<h3 id="m1b">📅 写作先后（近似）</h3><div class="chips chrono">'+"".join(f'<a class="chip" href="{by[i]["pg"]}" style="--c:{by[i]["c"]}"><b>{k+1}</b>{by[i]["ab"]}</a>' for k,i in enumerate(CHRONO))+'</div><p class="note">口诀：<b class="key">雅加帖帖林林罗</b>（早期七卷：45–57 年）→ <b class="key">弗西门腓</b>（狱中）→ <b class="key">提多彼提彼</b>（60 年代）→ <b class="key">来犹约约约</b>（晚期）。</p>')
    b.append('<h2 id="m2">二、21 卷钥字 + 记忆钩</h2><div class="tbl"><table><thead><tr><th>书卷</th><th>钥字</th><th>钥节</th><th>记忆钩</th><th>何时 · 何地</th></tr></thead><tbody>'+"".join(f'<tr style="--c:{d["c"]}"><td class="bk"><a href="{d["pg"]}">{d["ic"]} {d["n"]}</a></td><td><b class="key">{d["kw"]}</b></td><td><button type="button" class="vs" data-t="{esc(d["kvt"])}">{d["kv"]}</button></td><td>{esc(d["mn"])}</td><td><small>{esc(d["date"])} · {esc(d["place"])}</small></td></tr>' for d in D)+'</tbody></table></div>')
    b.append('<h2 id="m3">三、记忆卡（点按翻转）</h2><div class="fc-tools"><button id="fcshuf" class="btn">🔀 打乱</button><button id="fcall" class="btn">🔁 全部翻回</button></div><div class="cards" id="fcards">'+"".join(f'<div class="flip sm" tabindex="0" role="button" style="--gc:{d["c"]}"><div class="fi-in"><div class="ff"><span>{d["ic"]}</span><b>{d["n"]}</b><em>钥字？钥节？</em></div><div class="fb"><b class="key">{d["kw"]}</b><p>{esc(d["kvt"])}</p><small>— {d["kv"]}</small></div></div></div>' for d in D)+'</div>')
    b.append('<h2 id="m4">四、钥节填空</h2><div class="cloze" id="cloze"></div><p class="note">随机挖去钥节中的一个词，点按“显示”核对。</p>')
    b.append('<h2 id="m5">五、自测小考</h2><div class="quiz glass" id="quiz"><div class="qz-h"><span id="qzn">第 1 题</span><span id="qzs">得分 0</span></div><p class="qz-q" id="qzq"></p><div class="qz-o" id="qzo"></div><p class="qz-f" id="qzf" aria-live="polite"></p><div class="qz-b"><button class="btn" id="qznext">下一题 ➜</button><button class="btn ghost" id="qzre">重新开始</button></div></div>')
    pal=[("🚪","大门","罗马书","一座法庭：被告（罪人）被宣告为义"),("🛋️","客厅","哥林多前、后书","八个吵架的家人 + 一只瓦器"),("🕊️","阳台","加拉太书","鸽子挣脱锁链（自由）"),("🛏️","卧室","帖前、帖后","闹钟：主再来"),("💍","餐厅","以弗所书","婚礼餐桌：基督与教会"),("😊","厨房","腓立比书","坐牢还在唱歌的厨师"),("👑","书房","歌罗西书","书架顶端放王冠"),("🤝","门廊","腓利门书","主人拥抱逃奴"),("🏠","院子","教牧书信","建房子：根基、柱石、长老执事"),("⛪","圣殿模型","希伯来书","每一样都写着“更美”"),("🌱","花园","雅各书","只听不做的人像照镜子就忘了"),("🪨","岩石路","彼得前后书","活石 + 望远镜（等候新天新地）"),("💡","灯塔","约翰书信","光、爱、真理三盏灯"),("🛡️","城门","犹大书","持盾守城：为真道争辩")]
    b.append('<h2 id="m6">六、记忆宫殿：走一遍你的家</h2><div class="palace">'+"".join(f'<div class="pl glass reveal"><span>{a}</span><b>{c}</b><i>{d}</i><p>{e}</p></div>' for a,c,d,e in pal)+'</div>')
    plan=[(1,"罗1–4"),(2,"罗5–8"),(3,"罗9–16"),(4,"林前1–8"),(5,"林前9–16"),(6,"林后1–7"),(7,"林后8–13"),(8,"加"),(9,"弗"),(10,"腓 + 门"),(11,"西"),(12,"帖前 + 帖后"),(13,"提前"),(14,"提后 + 多"),(15,"来1–7"),(16,"来8–13"),(17,"雅"),(18,"彼前"),(19,"彼后 + 犹"),(20,"约壹二三"),(21,"复习：口诀 + 小考 + 三大信经背诵")]
    b.append('<h2 id="m7">七、21 天通读计划</h2><div class="plan" id="plan">'+"".join(f'<label class="pd glass"><input type="checkbox" data-d="{d}"><b>第 {d} 天</b><span>{t}</span></label>' for d,t in plan)+'</div><p class="note">勾选会保存在本机浏览器（localStorage）。</p>')
    b.append(f'<script id="epdata" type="application/json">{json.dumps(D,ensure_ascii=False).replace("</","<\\/")}</script>')
    return "".join(b)
