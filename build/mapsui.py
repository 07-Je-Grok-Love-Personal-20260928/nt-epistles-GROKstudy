# -*- coding: utf-8 -*-
"""互动地图 HTML + 离线概念图。真实底图由 docs/assets/maps.js（本地 Leaflet）负责。"""
import json, html as H
from geo import C, WP, JOURNEYS, ll
from common import md

def esc(s): return H.escape(s, quote=True)

# 罗马帝国行省约主后 60 年（尼禄朝）示意多边形，供教学定位，非精密边界。
PROV = [
 ("Italia","意大利","#f5b942",[[9.2,44.2],[13.5,45.6],[13.8,43.8],[14.3,42.5],[15.6,41.8],[16.6,41.3],[15.9,39.6],[16.6,38.9],[17.4,40.6],[18.5,40.3],[18.4,39.8],[16.2,38.0],[15.2,36.7],[13.0,37.1],[12.4,37.8],[11.8,42.0],[10.3,42.8],[8.6,44.0]]),
 ("Sicilia","西西里","#e8a317",[[12.4,38.3],[15.3,38.35],[15.3,36.6],[12.5,36.65],[12.4,38.3]]),
 ("Achaia","亚该亚","#4fb3ff",[[21.0,39.2],[23.5,39.4],[24.5,38.6],[24.3,36.3],[23.0,36.2],[21.2,36.4],[20.0,37.5],[20.4,38.8]]),
 ("Macedonia","马其顿","#6ec8ff",[[20.4,42.2],[24.6,42.3],[24.8,40.3],[23.0,39.7],[21.2,39.8],[20.2,40.6],[20.4,42.2]]),
 ("Asia","亚细亚","#3fd39a",[[26.0,40.3],[29.6,40.4],[30.0,38.0],[29.4,36.6],[27.2,36.5],[26.0,37.2],[25.6,38.6],[26.0,40.3]]),
 ("Bithynia","庇推尼","#2dd4bf",[[28.6,41.6],[32.4,41.5],[32.3,40.3],[29.0,40.2],[28.6,41.6]]),
 ("Pontus","本都","#22c3b0",[[32.6,41.8],[38.6,41.6],[38.2,40.4],[32.8,40.5],[32.6,41.8]]),
 ("Galatia","加拉太","#a78bfa",[[30.4,40.5],[34.8,40.6],[35.2,38.2],[32.6,37.4],[30.6,38.0],[30.4,40.5]]),
 ("Cappadocia","加帕多家","#8b6cff",[[34.8,39.8],[38.4,39.6],[38.5,37.3],[35.0,37.2],[34.8,39.8]]),
 ("Cilicia","基利家","#c4b5fd",[[32.3,37.3],[36.5,37.2],[36.5,36.3],[32.3,36.3],[32.3,37.3]]),
 ("Lycia","吕家·旁非利亚","#34d399",[[29.2,37.2],[32.2,37.15],[32.1,36.2],[29.1,36.2],[29.2,37.2]]),
 ("Cyprus","塞浦路斯","#fbbf24",[[32.2,35.75],[34.7,35.75],[34.65,34.55],[32.2,34.55],[32.2,35.75]]),
 ("Syria","叙利亚","#fb7185",[[35.7,37.4],[38.8,37.1],[38.6,32.6],[36.0,32.8],[35.5,35.4],[35.7,37.4]]),
 ("Judaea","犹太","#ff6b8b",[[34.15,33.25],[35.75,33.25],[35.7,30.85],[34.2,30.85],[34.15,33.25]]),
 ("Creta","克里特","#fda4af",[[23.5,35.7],[26.4,35.65],[26.35,34.85],[23.5,34.85],[23.5,35.7]]),
 ("Aegyptus","埃及","#f59e0b",[[29.4,31.6],[32.7,31.55],[32.6,29.4],[29.5,29.4],[29.4,31.6]]),
 ("Cyrenaica","古利奈","#f97316",[[19.6,33.1],[23.4,32.8],[23.2,31.0],[19.7,31.2],[19.6,33.1]]),
 ("Thracia","色雷斯","#38bdf8",[[24.8,42.7],[28.3,42.5],[28.0,40.9],[25.0,40.9],[24.8,42.7]]),
]
PETER5={"Bithynia","Pontus","Galatia","Cappadocia","Asia"}
SEVEN=["ephesus","smyrna","pergamum","thyatira","sardis","philadelphia","laodicea"]

def _place(k, role=""):
    if k in C:
        n,lo,la,_,_,_=C[k]; return {"id":k,"n":n,"lon":lo,"lat":la,"role":role}
    lo,la=WP[k]; return {"id":k,"n":k,"lon":lo,"lat":la,"role":role}

def _route(jid,name,color,keys):
    return {"id":jid,"name":name,"color":color,"pts":[{"k":k,"lon":ll(k)[0],"lat":ll(k)[1]} for k in keys]}

def imap(mid, title, cfg, schematic, lead="", prefer="carto"):
    cfg.setdefault("prefer", prefer)
    cfg.setdefault("center", [36.5, 26.0])
    cfg.setdefault("zoom", 5)
    data=esc(json.dumps(cfg, ensure_ascii=False, separators=(",",":")))
    lead_h=f'<p class="maplead">{md(lead)}</p>' if lead else ""
    return (f'<section class="mapduo" id="{mid}">'
            f'<h3 id="{mid}-t">{title}</h3>{lead_h}'
            f'<div class="duo">'
            f'<figure class="sche">{schematic}<figcaption>概念讲解图 · 离线 SVG，不依赖网络</figcaption></figure>'
            f'<div class="imap" id="imap-{mid}" data-cfg="{data}">'
            f'<div class="imap-bar"><label>底图</label><select class="imap-src" aria-label="选择底图来源"></select>'
            f'<button type="button" class="btn sm imap-play">▶ 播放路线</button>'
            f'<span class="imap-st" aria-live="polite"></span></div>'
            f'<div class="imap-canvas" role="application" aria-label="{esc(title)}"></div>'
            f'<p class="imap-foot">可切换 12 种全球底图；某一来源超时或出错时自动换下一个。全部失败则使用本站打包的 Natural Earth 离线矢量，地图不会空白。</p>'
            f'</div></div></section>')

# ---------- schematics ----------
def _svg(w,h,body,label):
    return f'<svg class="sche-svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">{body}</svg>'

def sch_empire():
    chips=[("意大利",130,70),("马其顿",360,60),("庇推尼",540,60),("本都",730,60),
           ("亚该亚",360,220),("亚细亚",540,200),("加拉太",730,180),
           ("克里特",200,340),("塞浦路斯",400,340),("叙利亚",600,290),("犹太",730,350),("埃及",400,395)]
    b=['<defs><radialGradient id="rg" cx="30%" cy="30%"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="#c47b00"/></radialGradient></defs>',
       '<rect width="840" height="420" rx="20" fill="#0b1733"/>']
    for i,(n,x,y) in enumerate(chips):
        b.append(f'<line class="pulse" x1="200" y1="200" x2="{x}" y2="{y}" stroke="#f5c44d" stroke-opacity=".45" stroke-dasharray="6 6" style="animation-delay:{i*.12}s"/>')
        b.append(f'<g class="pop" style="animation-delay:{.2+i*.08}s"><rect x="{x-50}" y="{y-16}" width="100" height="32" rx="16" fill="#1a2a4d" stroke="#f5c44d"/><text x="{x}" y="{y+5}" text-anchor="middle" fill="#ffe08a" font-size="14">{n}</text></g>')
    b.append('<circle cx="200" cy="200" r="58" fill="url(#rg)"/><text x="200" y="194" text-anchor="middle" font-size="16" font-weight="700" fill="#1a1300">SPQR</text><text x="200" y="214" text-anchor="middle" font-size="11" fill="#1a1300">主后约 60 年</text>')
    return _svg(840,420,"".join(b),"罗马帝国行省概念图")

def sch_journey(n, color, stops):
    # horizontal pilgrimage of numbered stops with icons
    w=max(760, 80+len(stops)*70); h=220
    b=[f'<rect width="{w}" height="{h}" rx="20" fill="#0b1733"/>',
       f'<path class="drawline" d="M50,110 H{w-50}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round"/>']
    for i,(ic,name) in enumerate(stops):
        x=50+i*(w-100)/(len(stops)-1)
        b.append(f'<g class="pop" style="animation-delay:{i*.1}s"><circle cx="{x}" cy="110" r="18" fill="{color}"/><text x="{x}" y="116" text-anchor="middle" font-size="16">{ic}</text>'
                 f'<text x="{x}" y="{70 if i%2==0 else 160}" text-anchor="middle" fill="#f3f1ff" font-size="13">{name}</text></g>')
    b.append(f'<text x="24" y="28" fill="{color}" font-size="16" font-weight="700">{n}</text>')
    return _svg(w,h,"".join(b),n)

def sch_voyage():
    b=['<rect width="840" height="300" rx="20" fill="#071428"/>',
       '<path class="drawline" d="M70,80 C160,70 200,90 250,120 C320,170 400,230 480,190 C560,150 620,90 710,80 C760,74 790,90 800,140" fill="none" stroke="#ff6b8b" stroke-width="4"/>',
       '<text x="70" y="64" fill="#ffe08a" font-size="14">⚓ 凯撒利亚</text>',
       '<text x="240" y="108" fill="#9aa3c0" font-size="13">西顿 · 每拉</text>',
       '<g class="bob"><text x="400" y="250" font-size="28">🌊</text><text x="430" y="255" fill="#ff8fab" font-size="14">风暴 · 美港</text></g>',
       '<g class="bob" style="animation-delay:.6s"><text x="500" y="170" font-size="26">🔥</text><text x="530" y="175" fill="#ffd36b" font-size="14">米利大：船难与火</text></g>',
       '<text x="690" y="64" fill="#9aa3c0" font-size="13">叙拉古 · 部丢利</text>',
       '<text x="760" y="170" fill="#ffe08a" font-size="14">🏛️ 罗马</text>',
       '<text x="24" y="284" fill="#9aa3c0" font-size="13">徒 27–28：押解不是中断宣教，而是把福音送进帝国心脏（参见腓 1:12-13）。</text>']
    return _svg(840,300,"".join(b),"押解罗马航海情景图")

def sch_peter():
    names=["本都","加拉太","加帕多家","亚细亚","庇推尼"]
    b=['<rect width="840" height="300" rx="20" fill="#0b1733"/>',
       '<text x="420" y="44" text-anchor="middle" fill="#ffe08a" font-size="18" font-weight="700">彼得前书 1:1 的五个行省</text>']
    for i,n in enumerate(names):
        x=90+i*150
        b.append(f'<g class="pop" style="animation-delay:{i*.12}s"><ellipse cx="{x}" cy="150" rx="62" ry="44" fill="#1b2a4d" stroke="#2dd4bf" stroke-width="2"/>'
                 f'<text x="{x}" y="156" text-anchor="middle" fill="#2ee6c7" font-size="16">{n}</text></g>')
    b.append('<text x="420" y="250" text-anchor="middle" fill="#c4b5fd" font-size="14">一张“寄居者”的地图：分散的群羊，同一位大牧人（彼前 5:4）。</text>')
    b.append('<text x="420" y="278" text-anchor="middle" fill="#9aa3c0" font-size="13">写作地传统为“巴比伦”＝罗马；收信地是小亚北部与西部。</text>')
    return _svg(840,300,"".join(b),"彼得前书五省概念图")

def sch_seven():
    # seven lampstands in an arc
    labs=["以弗所","士每拿","别迦摩","推雅推喇","撒狄","非拉铁非","老底嘉"]
    b=['<rect width="840" height="300" rx="20" fill="#0b1733"/>',
       '<text x="420" y="36" text-anchor="middle" fill="#ffe08a" font-size="17" font-weight="700">亚细亚七教会（启 2–3）· 约翰书信的邻里</text>']
    for i,n in enumerate(labs):
        x=80+i*110; on=n in ("以弗所","老底嘉")
        b.append(f'<g class="flick" style="animation-delay:{i*.15}s"><text x="{x}" y="120" text-anchor="middle" font-size="32">{"🕯️" if on else "🪔"}</text>'
                 f'<text x="{x}" y="160" text-anchor="middle" fill="{"#ffe08a" if on else "#d0d7ee"}" font-size="14">{n}</text></g>')
    b.append('<text x="420" y="220" text-anchor="middle" fill="#9aa3c0" font-size="14">以弗所是保罗三年工场，也是提前、以弗所书与约翰书信的中心。</text>')
    b.append('<text x="420" y="252" text-anchor="middle" fill="#9aa3c0" font-size="13">老底嘉紧邻歌罗西；西 4:16 要求两地互换书信。</text>')
    return _svg(840,300,"".join(b),"亚细亚七教会灯台图")

def sch_diaspora():
    b=['<rect width="840" height="340" rx="20" fill="#0b1733"/>',
       '<circle cx="420" cy="170" r="36" fill="#ffc44d"/><text x="420" y="166" text-anchor="middle" font-size="12" fill="#1a1300">耶路撒冷</text><text x="420" y="182" text-anchor="middle" font-size="11" fill="#1a1300">徒 1:8</text>']
    rays=[("犹太",420,70),("撒玛利亚",300,100),("安提阿",560,80),("塞浦路斯",700,130),("亚细亚",700,220),("希腊",560,290),("罗马",200,80),("埃及",200,260),("地极",120,170)]
    for i,(n,x,y) in enumerate(rays):
        b.append(f'<line class="pulse" x1="420" y1="170" x2="{x}" y2="{y}" stroke="#f5c44d" stroke-opacity=".5" style="animation-delay:{i*.1}s"/>')
        b.append(f'<g class="pop" style="animation-delay:{.15+i*.08}s"><circle cx="{x}" cy="{y}" r="22" fill="#1a2a4d" stroke="#f5c44d"/><text x="{x}" y="{y+5}" text-anchor="middle" fill="#ffe08a" font-size="11">{n}</text></g>')
    return _svg(840,340,"".join(b),"从耶路撒冷到地极的放射图")

def sch_letters():
    # from-to ribbons
    pairs=[("哥林多","罗马","罗马书"),("以弗所","哥林多","林前"),("罗马","以弗所","以弗所书"),("罗马","腓立比","腓立比书"),("耶路撒冷","分散各族","雅各书")]
    b=['<rect width="840" height="280" rx="20" fill="#0b1733"/>','<text x="24" y="32" fill="#ffe08a" font-size="16" font-weight="700">书信是有地址的神学</text>']
    for i,(a,b2,n) in enumerate(pairs):
        y=70+i*38
        b.append(f'<g class="pop" style="animation-delay:{i*.1}s"><rect x="40" y="{y-14}" width="200" height="28" rx="8" fill="#1a2a4d" stroke="#f5c44d"/><text x="140" y="{y+5}" text-anchor="middle" fill="#ffe08a" font-size="13">✍ {a}</text>'
                 f'<path class="drawline" d="M250 {y} H590" stroke="#7dd3fc" stroke-width="2" fill="none" marker-end="url(#ar)"/>'
                 f'<text x="420" y="{y-8}" text-anchor="middle" fill="#9aa3c0" font-size="11">{n}</text>'
                 f'<rect x="600" y="{y-14}" width="200" height="28" rx="8" fill="#1a2a4d" stroke="#2ee6c7"/><text x="700" y="{y+5}" text-anchor="middle" fill="#2ee6c7" font-size="13">📬 {b2}</text></g>')
    b.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7dd3fc"/></marker></defs>')
    return _svg(840,280,"".join(b),"书信写作地与收信地示意")

# ---------- page sections ----------
def _areas(keys=None):
    out=[]
    for pid,name,col,ring in PROV:
        if keys and pid not in keys: continue
        out.append({"id":pid,"n":name,"color":col,"ring":ring})
    return out

def all_maps():
    """maps.html 主体。"""
    from common import md, tip
    out=[]
    out.append('<h2 id="m0">地图怎么用</h2>'+tip("key","双图并列，永不空白",
        "左侧是离线概念图，把历史关系一次讲清；右侧是可缩放的真实地图。底图可在 **OpenStreetMap、CARTO、Esri 卫星/地形、OpenTopoMap、DARE 罗马帝国古图** 等来源间切换；某一来源失败会自动改用下一个，最后一档是本站打包的 Natural Earth 矢量。"))
    out.append(tip("term","DARE 古图","Digital Atlas of the Roman Empire（哥德堡大学）按罗马帝国道路与地名绘图，看保罗时代的地理最直观。若此源超时，会自动切到现代底图或离线矢量。"))

    # 1 empire
    cfg={"center":[36.2,26],"zoom":5,"prefer":"dare","areas":_areas(),
         "places":[_place(k,"city") for k in ("rome","corinth","ephesus","antioch","jerusalem","alexandria","philippi","thessalonica","tarsus")]}
    out.append('<h2 id="m-emp">行省：书信的地址系统</h2>')
    out.append(imap("map-empire","罗马帝国行省（约主后 60 年）",cfg,sch_empire(),
        lead="保罗写信时的“世界”是罗马的行省世界。[[行省]]决定行政、道路、法律与帝王崇拜的压力；书信的收件人就住在这些格子里。",prefer="dare"))
    out.append('<h3 id="m-emp-tbl">行省与书信对照</h3><div class="tbl"><table><thead><tr><th>行省</th><th>关键城市</th><th>相关书信</th><th>当记住的一点</th></tr></thead><tbody>'
               '<tr><td>亚该亚</td><td>哥林多、雅典、坚革哩</td><td>林前、林后；罗马书写于此</td><td>演说、港口、道德混杂</td></tr>'
               '<tr><td>马其顿</td><td>腓立比、帖撒罗尼迦、庇哩亚</td><td>腓、帖前、帖后</td><td>罗马殖民地与大道</td></tr>'
               '<tr><td>亚细亚</td><td>以弗所、歌罗西、老底嘉</td><td>弗、西、门、提前、约壹二三</td><td>亚底米与邪术；教会中心</td></tr>'
               '<tr><td>加拉太</td><td>以哥念、路司得、特庇</td><td>加拉太书</td><td>割礼之争的前线</td></tr>'
               '<tr><td>犹太</td><td>耶路撒冷、凯撒利亚</td><td>雅；被捕地</td><td>圣殿尚存，直到 70 年</td></tr>'
               '<tr><td>意大利</td><td>罗马、部丢利</td><td>罗（收）、狱中书信、提后、彼前</td><td>帝国心脏；尼禄逼迫</td></tr>'
               '</tbody></table></div>')

    # 2-5 journeys
    stops={
      "j1":[("⛵","安提阿"),("🏝️","塞浦路斯"),("⛰️","南加拉太"),("🔁","原路回"),("🏡","安提阿")],
      "j2":[("🕊️","安提阿"),("🌊","特罗亚异象"),("🏛️","腓立比"),("🌅","帖城"),("🔥","哥林多")],
      "j3":[("📚","以弗所三年"),("💰","马其顿捐项"),("✉️","哥林多写罗马书"),("⛓️","耶路撒冷")],
      "j4":[("⚓","凯撒利亚"),("🌊","风暴"),("🔥","米利大"),("🚶","部丢利"),("🏛️","罗马")],
    }
    leads={
      "j1":"第一次旅行解决一个问题：外邦人能否因信进入神的子民。==南加拉太的众教会==成为《加拉太书》的收信人。",
      "j2":"第二次旅行把福音送进欧洲。**帖撒罗尼迦前后书**写于哥林多，是现存保罗最早的书信之一。",
      "j3":"以弗所三年是保罗事工的高峰：**林前**在此写成，**林后**在马其顿，**罗马书**在哥林多。旅行以在圣殿被捕结束。",
      "j4":"押解本身就是宣教。船难、蛇、岛民、凯撒的兵营——**福音在锁链中前进**（提后 2:9）。",
    }
    for jid,name,col,ks in JOURNEYS:
        cfg={"center":[36.5,24 if jid!="j4" else 22],"zoom":5 if jid!="j4" else 5,"prefer":"dare",
             "routes":[_route(jid,name,col,ks)],
             "places":[_place(k) for k in ks if k in C]}
        out.append((" <h2 id=\"m-j\">保罗的行程与航海</h2>" if jid=="j1" else "")+imap(f"map-{jid}",name,cfg,sch_journey(name,col,stops[jid]),lead=leads[jid],prefer="dare"))

    # 6 voyage already j4, add imprisonment context
    out.append(imap("map-prison","从被捕到罗马：锁链中的两年+航程",
        {"center":[36,22],"zoom":5,"prefer":"dare",
         "routes":[_route("j4",JOURNEYS[3][1],JOURNEYS[3][2],JOURNEYS[3][3])],
         "places":[_place(k) for k in ("jerusalem","caesarea","sidon","myra","crete","malta","syracuse","puteoli","rome") if k in C]},
        sch_voyage(),
        lead="主后 57 年在耶路撒冷被捕，凯撒利亚被囚两年（徒 24–26），约 59–60 年航海。抵达后租屋两年，传统认为 **弗、西、门、腓** 写于此。",prefer="dare"))

    # 7 peter
    cfg={"center":[39.2,32],"zoom":6,"prefer":"dare","areas":_areas(PETER5),
         "places":[_place(k) for k in ("ephesus","smyrna","pergamum","ancyra","cappadocia","pontus","bithynia","rome")]}
    out.append('<h2 id="m-rec">收信地：分散的群羊</h2>')
    out.append(imap("map-peter","彼得前书的收信地：小亚五省",cfg,sch_peter(),
        lead="{{彼前1:1}} 点名本都、加拉太、加帕多家、亚西亚、庇推尼。这是 ++寄居者的地图++：分散、受毁谤，却被拣选。传统写作地“巴比伦”指罗马。",prefer="dare"))

    # 8 seven churches
    cfg={"center":[38.2,28.2],"zoom":7,"prefer":"dare",
         "routes":[{"id":"7c","name":"七教会顺序（启2–3）","color":"#ffc44d","pts":[{"k":k,"lon":C[k][1],"lat":C[k][2]} for k in SEVEN]}],
         "places":[_place(k,"church") for k in SEVEN]+[_place("colossae"),_place("patmos")]}
    out.append(imap("map-seven","亚细亚七教会：约翰书信的邻里",cfg,sch_seven(),
        lead="启示录的七城是以弗所邮路上一圈。约翰书信写于以弗所一带，针对否认“耶稣基督是成了肉身来的”的！！敌基督教导！！。歌罗西与老底嘉相邻，西 4:16 要求互换书信。",prefer="dare"))

    # 9 diaspora
    cfg={"center":[36,26],"zoom":5,"prefer":"carto",
         "routes":[{"id":"dia","name":"从耶路撒冷向外","color":"#f5c44d","pts":[
            {"k":"jerusalem","lon":35.23,"lat":31.78},{"k":"caesarea","lon":34.89,"lat":32.50},
            {"k":"antioch","lon":36.16,"lat":36.20},{"k":"ephesus","lon":27.34,"lat":37.94},
            {"k":"corinth","lon":22.88,"lat":37.91},{"k":"rome","lon":12.48,"lat":41.89}]}],
         "places":[_place(k) for k in ("jerusalem","caesarea","antioch","damascus","alexandria","ephesus","corinth","philippi","rome")]}
    out.append(imap("map-dia","从耶路撒冷到地极（徒 1:8 的地理）",cfg,sch_diaspora(),
        lead="**先是耶路撒冷，然后犹太、撒玛利亚，直到地极。** 逼迫使信徒分散（徒 8）；安提阿成为外邦宣教的母会；书信就是这条路线上的“牧养邮件”。",prefer="osm"))

    # 10 letters network
    # built later with eps in build()
    return "".join(out)

def letters_map(eps):
    routes=[]
    for e in eps:
        if e["fr"]==e["dest"]: continue
        a,b=ll(e["fr"]),ll(e["dest"])
        routes.append({"id":e["id"],"name":e["n"],"color":{"major":"#f5b942","early":"#4fb3ff","prison":"#a78bfa","pastoral":"#3fd39a","heb":"#ff6b8b","gen":"#2dd4bf"}[e["g"]],
                       "pts":[{"k":e["fr"],"lon":a[0],"lat":a[1]},{"k":e["dest"],"lon":b[0],"lat":b[1]}]})
    keys=sorted({e["fr"] for e in eps}|{e["dest"] for e in eps})
    cfg={"center":[36.5,24],"zoom":5,"prefer":"carto","routes":routes,"places":[_place(k) for k in keys if k in C]}
    lead="每一封书信都有**写作地**与**收信地**。点按城市或路线查看。左侧概念图先建立“有地址的神学”这一观念。"
    return imap("map-letters","21 卷书信：写作地 → 收信地",cfg,sch_letters(),lead=lead,prefer="carto")

def letter_imap(e):
    """供各书卷页：SVG 迷你图下方可展开的互动地图。"""
    a,b=ll(e["fr"]),ll(e["dest"])
    routes=[]
    if e["fr"]!=e["dest"]:
        routes=[{"id":e["id"],"name":e["n"],"color":"#ffc44d","pts":[{"k":e["fr"],"lon":a[0],"lat":a[1]},{"k":e["dest"],"lon":b[0],"lat":b[1]}]}]
    midlat,midlon=((a[1]+b[1])/2,(a[0]+b[0])/2)
    cfg={"center":[midlat,midlon],"zoom":6,"prefer":"carto","routes":routes,
         "places":[_place(e["fr"],"from"),_place(e["dest"],"to")]}
    data=esc(json.dumps(cfg,ensure_ascii=False,separators=(",",":")))
    return (f'<details class="imap-d"><summary>🗺️ 打开互动地图（可切换底图 · 离线可回退）</summary>'
            f'<div class="imap compact" id="imap-{e["id"]}" data-cfg="{data}">'
            f'<div class="imap-bar"><label>底图</label><select class="imap-src" aria-label="选择底图来源"></select><span class="imap-st" aria-live="polite"></span></div>'
            f'<div class="imap-canvas" style="height:320px" role="application" aria-label="{esc(e["n"])}互动地图"></div></div></details>')
