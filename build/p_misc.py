# -*- coding: utf-8 -*-
from common import md, esc, cq, verse_card, VER, DATE, CREEDS
from epi import GN, mindtree
from p_mem import PG
def index(eps):
    b=['<div class="intro2 glass reveal"><p>'+md("书信是复活升天的基督藉着使徒对祂教会说的话。本站先从**整本圣经与圣约**看书信的位置，再走进**时间、故事与地图**，然后逐卷深读 21 卷书信（背景、为什么写、写了什么、圣经神学、==圣约神学==、!!难点!!、信条对照、应用），最后用**教义主题**、**三大信经**与**记忆自测**把它们收拢。")+'</p></div>']
    b.append('<h2 id="i1">📚 21 卷书信一览</h2><div class="bgrid">'+"".join(f'<a class="bk glass reveal" href="{PG[e["g"]]}#{e["id"]}" style="--gc:{GN[e["g"]][1]}"><span class="bi">{e["ic"]}</span><b>{e["n"]}</b><small>{e["kw"]} · {e["ch"]} 章</small></a>' for e in eps)+'</div>')
    b.append('<div class="glegend">'+"".join(f'<span style="--gc:{c}">{n}</span>' for n,c in GN.values())+'</div>')
    b.append('<h2 id="i2">🧭 学习路线</h2><div class="flow">'+"".join(f'<a class="fstep" href="{h}"><span class="n">{k+1}</span>{t}</a>'+('<i class="farr">➜</i>' if k<5 else '') for k,(h,t) in enumerate([("bible.html","整本圣经与圣约：书信在救赎历史中的位置"),("history.html","时间线、故事线、地图与文化"),("paul-major.html","逐卷深读（4 个书信组）"),("doctrine.html","十大教义主题 · 信条对照"),("creeds.html","三大信经背诵与比较"),("memory.html","口诀、记忆卡、小考")]))+'</div>')
    b.append('<h2 id="i3">🌳 书信总思维导图</h2>'+mindtree("📨 新约书信 21 卷",eps))
    b.append('<h2 id="i4">✨ 一节总纲</h2>'+verse_card("罗11:36")+'<p class="note">书信的神学从神开始，也以颂赞结束：罗马书 1–11 章的教义在这节颂赞中收尾，12 章起才转入“所以……”的生活。</p>')
    b.append('<h2 id="i5">🎨 颜色与标记</h2><div class="tbl"><table><tbody><tr><td><b class="key">金色粗体</b></td><td>重点：必须掌握的核心教义与钥句</td></tr><tr><td><span class="hard">珊瑚红底</span></td><td>难点：历来争议或容易误解之处（附改革宗解答）</td></tr><tr><td><span class="cov">紫色下划线</span></td><td>圣约神学：恩典之约、应许、记号与印证</td></tr><tr><td><span class="term">青色虚线</span></td><td>术语</td></tr><tr><td><button type="button" class="vs" data-t="例：“义人必因信得生。”（罗1:17）">罗1:17</button></td><td>经文出处，点按弹出和合本经文</td></tr><tr><td>📘📗📕</td><td>海德堡要理问答 · 比利时信条 · 多特信经（CCI 中译，逐字）</td></tr></tbody></table></div>')
    return "".join(b)
def sources(stats):
    S=[("信经与信条（逐字引用来源）",[("CCI 使徒信经",CREEDS["apostles"]["url"]),("CCI 尼西亚信经",CREEDS["nicene"]["url"]),("CCI 亚他那修信经",CREEDS["athanasian"]["url"]),("CCI 海德堡要理问答","https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism"),("CCI 比利时信条","https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession"),("CCI 多特信经","https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort")]),
       ("CCI 相关讲道（延伸阅读）",[("林前系列（讲道 105–112）","https://ccifellowship.org/sermons/text/105"),("彼前系列 2：重生的人专心盼望基督的再来","https://ccifellowship.org/sermons/text/104"),("要结出信实的果子","https://ccifellowship.org/sermons/text/92"),("海德堡要理问答第 46 主日讲道","https://ccifellowship.org/sermons/heidelberg-catechism/lord-day-46")]),
       ("经文与地图",[("和合本（CUV）经文：getBible API","https://api.getbible.net/v2/cus/45/1.json"),("Natural Earth 地图数据（公有领域）","https://www.naturalearthdata.com/")]),
       ("改革宗参考（未直接引用原文，仅供延伸）",[("ccreformed.org","https://www.ccreformed.org/"),("reformedbeginner.net","https://reformedbeginner.net/"),("加拿大改革宗教会 CanRC","https://canrc.org/"),("北美联合改革宗教会 URCNA","https://www.urcna.org/"),("传承改革宗教会 HRC","https://heritagereformed.com/"),("基督教改革宗教会 PRCA","https://prca.org/"),("正统长老会 OPC","https://opc.org/"),("Mid-America Reformed Seminary","https://www.midamerica.edu/"),("Canadian Reformed Theological Seminary","https://crts.ca/"),("Puritan Reformed Theological Seminary","https://prts.edu/")]),
       ("威斯敏斯特标准（比较用）",[("RTF-USA 简体中文译本（贾少彬 译），本站引文取自其数据","https://rtf-usa.org/")])]
    b=['<h2 id="s1">🔖 来源</h2>']
    for k,(t,L) in enumerate(S): b.append(f'<h3 id="s1-{k}">{t}</h3><ul class="src">'+"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n,u in L)+'</ul>')
    b.append('<h2 id="s2">✅ 校验结果（构建时自动生成）</h2><div class="tbl"><table><tbody>'+"".join(f'<tr><td><b>{k}</b></td><td>{v}</td></tr>' for k,v in stats)+'</tbody></table></div>')
    b.append('<h2 id="s3">⚠️ 说明与局限</h2><ul class="src"><li>信条引文逐字取自 ccifellowship.org 的中文译本；其他译本措辞可能不同。</li><li>年代、写作地点、作者问题（如希伯来书）列出改革宗与保守福音派常见观点，学界有其他看法。</li><li>地图路线为依据使徒行传地名连成的示意线，不代表精确的古代道路。</li><li>讲解、口诀与图表为本站学习整理，不是任何教会的正式文件；权威在圣经，其次在教会公认的信条。</li></ul>')
    b.append(f'<h2 id="s4">🗂️ 版本</h2><div class="tbl"><table><thead><tr><th>版本</th><th>日期</th><th>说明</th></tr></thead><tbody><tr><td>{VER}</td><td>{DATE}（台北时间）</td><td>首次发布：21 卷书信深读、整本圣经与圣约、时间线与地图、教义主题、三大信经背诵与比较、记忆自测。</td></tr></tbody></table></div>')
    return "".join(b)
