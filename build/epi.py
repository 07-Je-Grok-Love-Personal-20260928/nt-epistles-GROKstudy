# -*- coding: utf-8 -*-
from common import md, esc, cq, verse_card, vtext
from geo import minimap
GN = {"major":("保罗 · 四大书信","#f5b942"),"early":("保罗 · 帖撒罗尼迦书信","#4fb3ff"),"prison":("保罗 · 狱中书信","#a78bfa"),
      "pastoral":("保罗 · 教牧书信","#3fd39a"),"heb":("希伯来书","#ff6b8b"),"gen":("大公书信","#2dd4bf")}
def flow(steps, end):
    s='<div class="flow">'
    for i,t in enumerate(steps): s+=f'<div class="fstep"><span class="n">{i+1}</span>{md(t)}</div><i class="farr">➜</i>'
    return s+f'<div class="fstep end">✉️ {md(end)}</div></div>'
def sbar(ol):
    tot=sum(w for _,_,w in ol)
    seg="".join(f'<div class="seg" style="flex:{w/tot*100:.1f}" title="{esc(r)} {esc(t)}"><b>{esc(r)}</b><span>{esc(t)}</span></div>' for r,t,w in ol)
    return f'<div class="sbar">{seg}</div>'
def epistle(e):
    i=e["id"]; gname,col=GN[e["g"]]
    facts=[("✍️","作者",e["au"]),("📅","写作时间",e["date"]),("📍","写作地点",e["place"]),("📬","收信人",e["to"]),("🔗","相关经文",e["acts"]),("📏","篇幅",f'{e["ch"]} 章')]
    fx="".join(f'<div class="fact"><span class="fi">{a}</span><b>{b}</b><p>{md(c)}</p></div>' for a,b,c in facts)
    angs="".join(f'<div class="ang"><b>{k}</b><p>{md(v)}</p></div>' for k,v in e["ang"].items())
    keys="".join(f'<li>{md(k)}</li>' for k in e["key"])
    hards="".join(f'<details class="hardq"><summary>⚠️ {md(q)}</summary><p>{md(a)}</p></details>' for q,a in e["hard"])
    confs="".join(cq(c) for c in e["conf"])
    apps="".join(f'<li>{md(a)}</li>' for a in e["app"])
    ol="".join(f'<li><b>{esc(r)}</b> {md(t)}</li>' for r,t,_ in e["ol"])
    return f'''<section class="ep" id="{i}" style="--gc:{col}">
<h2 id="{i}-t" class="ep-h"><span class="ei">{e["ic"]}</span>{e["n"]} <small>{e["en"]} · {gname}</small></h2>
<div class="ep-banner glass reveal"><div class="kwbox"><span class="kwl">钥字</span><span class="kw">{e["kw"]}</span></div><p class="core">💎 {md(e["core"])}</p>{verse_card(e["kv"])}</div>
<div class="facts-wrap"><div class="facts">{fx}</div><figure class="mm glass">{minimap(e)}<figcaption>✍ 写作地 → 📬 收信地（真实底图：Natural Earth；位置按经纬度）</figcaption></figure></div>
<h3 id="{i}-bg">🏺 背景与真实情境</h3><div class="two"><div class="card glass"><h4>历史背景</h4><p>{md(e["bg"])}</p></div><div class="card glass culture"><h4>🌍 文化区域特征</h4><p>{md(e["cul"])}</p></div></div>
<h3 id="{i}-why">❓ 为什么写（前因后果）</h3>{flow(e["why"], "于是写下《"+e["n"]+"》")}
<h3 id="{i}-what">📐 写了什么（结构）</h3>{sbar(e["ol"])}<ol class="outline">{ol}</ol><div class="angs">{angs}</div>
<h3 id="{i}-bt">📜 圣经神学：在整本圣经中的位置</h3><div class="card glass bt"><p>{md(e["bt"])}</p></div>
<h3 id="{i}-ct">🤝 圣约神学</h3><div class="card glass ct"><p>{md(e["ct"])}</p></div>
<h3 id="{i}-kh">🎯 重点与难点</h3><div class="two"><div class="card glass"><h4>⭐ 重点</h4><ul class="keys">{keys}</ul></div><div class="card glass"><h4>⚠️ 难点（点开看改革宗解答）</h4>{hards}</div></div>
<h3 id="{i}-cf">📘 信条对照（CCI 逐字）</h3><div class="confs">{confs}</div>
<h3 id="{i}-ap">🌱 应用与记忆</h3><div class="two"><div class="card glass"><h4>今天怎样活</h4><ul class="apps">{apps}</ul></div><div class="flip" tabindex="0" role="button" aria-label="翻转记忆卡"><div class="fi-in"><div class="ff"><span>🧠 记忆钩</span><b>{e["n"]}</b><em>点按翻转</em></div><div class="fb"><p>{md(e["mn"])}</p></div></div></div></div>
</section>'''
def mindtree(title, eps):
    br="".join(f'<li style="--gc:{GN[e["g"]][1]}"><a href="#{e["id"]}" class="mt-b">{e["ic"]} {e["n"]} · <b>{e["kw"]}</b></a><ul>'+"".join(f'<li><span>{t}</span></li>' for _,t,_ in e["ol"][:4])+'</ul></li>' for e in eps)
    return f'<div class="mtree glass reveal"><div class="mt-root">{title}</div><ul class="mt-l1">{br}</ul></div>'
def gtable(eps):
    rows="".join(f'<tr style="--gc:{GN[e["g"]][1]}"><td><a href="#{e["id"]}">{e["ic"]} {e["n"]}</a></td><td><b class="kwt">{e["kw"]}</b></td><td>{md(e["date"])}</td><td>{md(e["place"])}</td><td>{md(e["core"])}</td></tr>' for e in eps)
    return f'<div class="tbl"><table><thead><tr><th>书卷</th><th>钥字</th><th>时间</th><th>地点</th><th>一句话核心</th></tr></thead><tbody>{rows}</tbody></table></div>'
