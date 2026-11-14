# Playwright QA v2: overflow, clip, header overlap, JS errors, interactions, tile fallback
import asyncio, json, os, sys, subprocess, time, socket
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,"docs"); OUT=os.path.join(ROOT,"build","qa"); os.makedirs(OUT,exist_ok=True)
PAGES=[f for f in sorted(os.listdir(D)) if f.endswith(".html")]
VIEWS=((360,800),(390,844),(768,1024),(1024,768),(1440,900),(1920,1080))
JS=r"""()=>{const de=document.documentElement,vw=de.clientWidth,res={sw:de.scrollWidth,vw:vw,off:[],clip:[],hdr:[],js:0};
const skip=n=>{for(let p=n;p;p=p.parentElement){const s=getComputedStyle(p);if(p===document.body||p===de)break;if(/(auto|scroll|hidden)/.test(s.overflowX+' '+s.overflowY+' '+s.overflow)||p.id==='toc'||p.id==='tocwrap'||p.id==='navdrop'||p.classList.contains('leaflet-container')||p.classList.contains('imap-canvas')||p.classList.contains('mapscroll')||p.classList.contains('mainnav'))return true}return false};
document.querySelectorAll('main *, header.top *').forEach(n=>{
  if(n.closest&& (n.closest('.leaflet-container')||n.closest('#toc')||n.closest('#tocwrap')||n.closest('.navdrop'))) return;
  const r=n.getBoundingClientRect(); if(!r.width||!r.height) return;
  const pos=getComputedStyle(n).position; if(pos==='fixed'||pos==='sticky') return;
  if((r.right>vw+2||r.left<-2)&&!skip(n)) res.off.push((n.className||n.tagName+'').toString().slice(0,40)+' '+Math.round(r.left)+'→'+Math.round(r.right));
  const s=getComputedStyle(n);
  if(['P','LI','TD','B','H2','H3','H4','SMALL','FIGCAPTION'].includes(n.tagName)&&s.overflowX==='visible'&&n.scrollWidth>n.clientWidth+3&&n.clientWidth>40&&s.display!=='inline'&&!skip(n))
    res.clip.push(n.tagName+':'+n.textContent.slice(0,18));
});
const hs=[...document.querySelectorAll('.top > *')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.getBoundingClientRect());
for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.right>b.left+2&&b.right>a.left+2&&a.bottom>b.top+2&&b.bottom>a.top+2)res.hdr.push(i+'x'+j)}
res.off=res.off.slice(0,6);res.clip=res.clip.slice(0,6);return res}"""

async def interact(pg, fname):
    async def safe(fn):
        try: await fn()
        except Exception: pass
    await safe(lambda: pg.locator("#tocbtn").click(timeout=2500))
    await pg.wait_for_timeout(150)
    tx=pg.locator("#tocx")
    if await tx.count():
        try:
            if await tx.is_visible():
                await tx.click(timeout=2500, force=True)
        except Exception: pass
    await safe(lambda: pg.locator("#themebtn").click(timeout=2500))
    await pg.wait_for_timeout(100)
    await safe(lambda: pg.locator("#themebtn").click(timeout=2500))
    opened=0
    for d in await pg.locator("details").all():
        if opened>=2: break
        try:
            if await d.is_visible():
                await d.locator("summary").first.click(timeout=2000); opened+=1; await pg.wait_for_timeout(80)
        except Exception: pass
    for fl in (await pg.locator(".flip").all())[:4]:
        try:
            if await fl.is_visible(): await fl.click(timeout=1500); await pg.wait_for_timeout(50)
        except Exception: pass
    for b in (await pg.locator(".tlf button").all())[:3]:
        try:
            if await b.is_visible(): await b.click(timeout=1500)
        except Exception: pass
    for b in (await pg.locator(".maptools .lb[data-l]").all())[:4]:
        try:
            if await b.is_visible(): await b.click(timeout=1500)
        except Exception: pass
    sel=pg.locator(".imap-src").first
    try:
        if await sel.count() and await sel.is_visible():
            await sel.select_option("carto"); await pg.wait_for_timeout(400)
            await sel.select_option("offline"); await pg.wait_for_timeout(300)
    except Exception: pass
    for b in (await pg.locator(".rmodes button").all())[:3]:
        try:
            if await b.is_visible(): await b.click(timeout=1500)
        except Exception: pass
    try:
        if await pg.locator("#qznext").count() and await pg.locator("#qznext").is_visible():
            await pg.locator("#qznext").click(timeout=1500)
    except Exception: pass


async def toc_qa(pg, port, bad, rep):
    """TOC resize, collapse/expand every level, mobile drawer."""
    issues=[]
    # desktop
    await pg.set_viewport_size({"width":1440,"height":900})
    await pg.goto(f"http://127.0.0.1:{port}/paul-major.html",wait_until="domcontentloaded",timeout=60000)
    await pg.evaluate("document.documentElement.classList.remove('toc-off','toc-open')")
    await pg.wait_for_timeout(200)
    r=await pg.evaluate("""()=>{
      const w=document.getElementById('tocwrap'), toc=document.getElementById('toc'), h=document.getElementById('tocresizer');
      const links=[...document.querySelectorAll('#toc-page a')];
      const wrap=links.filter(a=>a.scrollWidth>a.clientWidth+2).slice(0,3).map(a=>a.textContent.slice(0,24));
      const lv={2:document.querySelectorAll('#toc-page .lv2').length,3:document.querySelectorAll('#toc-page .lv3').length,4:document.querySelectorAll('#toc-page .lv4').length};
      const tw=[...document.querySelectorAll('#toc-page .toc-tw')].filter(b=>!b.hidden).length;
      const vis=w&&getComputedStyle(w).transform==='none'||(w&&w.getBoundingClientRect().left>=-2);
      return {hasWrap:!!w,hasResizer:!!h,width:w?Math.round(w.getBoundingClientRect().width):0,lv,tw,wrap,vis,g:!!document.getElementById('toc-global'),p:!!document.getElementById('toc-page')};
    }""")
    if not (r["hasWrap"] and r["hasResizer"] and r["g"] and r["p"] and int((r.get("lv") or {}).get("2") or (r.get("lv") or {}).get(2) or 0) and int((r.get("lv") or {}).get("3") or (r.get("lv") or {}).get(3) or 0) and int((r.get("lv") or {}).get("4") or (r.get("lv") or {}).get(4) or 0) and r["tw"]>=3):
        issues.append("desktop-chrome "+str(r))
    if r["wrap"]:
        issues.append("desktop-trunc "+str(r["wrap"]))
    start_w=r["width"]
    box=await pg.locator("#tocresizer").bounding_box()
    if not box:
        issues.append("no-resizer-box")
    else:
        await pg.mouse.move(box["x"]+box["width"]/2, box["y"]+80)
        await pg.mouse.down()
        await pg.mouse.move(box["x"]+140, box["y"]+80, steps=8)
        await pg.mouse.up()
        await pg.wait_for_timeout(80)
        w2=await pg.evaluate("()=>Math.round(document.getElementById('tocwrap').getBoundingClientRect().width)")
        stored=await pg.evaluate("()=>localStorage.getItem('nt-tocw')")
        if w2 < start_w+40:
            issues.append(f"drag-widen {start_w}->{w2}")
        if not stored or int(stored)<start_w+20:
            issues.append(f"persist-widen {stored}")
        # drag narrow toward min
        box=await pg.locator("#tocresizer").bounding_box()
        await pg.mouse.move(box["x"]+1, box["y"]+80)
        await pg.mouse.down()
        await pg.mouse.move(box["x"]-500, box["y"]+80, steps=8)
        await pg.mouse.up()
        w3,css=await pg.evaluate("()=>[Math.round(document.getElementById('tocwrap').getBoundingClientRect().width), getComputedStyle(document.documentElement).getPropertyValue('--tocw')]")
        if w3<200-2:
            issues.append(f"below-min {w3}")
        # restore mid width for later
        box=await pg.locator("#tocresizer").bounding_box()
        await pg.mouse.move(box["x"]+1, box["y"]+80)
        await pg.mouse.down()
        await pg.mouse.move(box["x"]+180, box["y"]+80, steps=6)
        await pg.mouse.up()
    # collapse / expand all levels
    await pg.locator("#toc-col").click()
    c=await pg.evaluate("""()=>{
      const vis=[...document.querySelectorAll('#toc-page .toc-tw')].filter(b=>!b.hidden);
      const closed=vis.filter(b=>b.getAttribute('aria-expanded')==='false').length;
      const kids=document.querySelectorAll('#toc-page .toc-n.collapsed > ol > .toc-n');
      let shown=0; kids.forEach(n=>{if(n.getBoundingClientRect().height>1)shown++});
      return {vis:vis.length,closed,shown};
    }""")
    if c["vis"]==0 or c["closed"]<c["vis"] or c["shown"]>0:
        issues.append("collapse-all "+str(c))
    await pg.locator("#toc-ex").click()
    e=await pg.evaluate("""()=>{
      const vis=[...document.querySelectorAll('#toc-page .toc-tw')].filter(b=>!b.hidden);
      const open=vis.filter(b=>b.getAttribute('aria-expanded')==='true').length;
      return {vis:vis.length,open};
    }""")
    if e["open"]<e["vis"]:
        issues.append("expand-all "+str(e))
    # per-level toggle (inspect the clicked row)
    for lv in (2,3,4):
        tw=pg.locator(f"#toc-page .lv{lv} > .toc-row > .toc-tw:not([hidden])").first
        if await tw.count():
            await tw.click()
            st=await tw.evaluate("""el=>{const li=el.closest('.toc-n');const ol=li.querySelector(':scope > ol');
              return {exp:el.getAttribute('aria-expanded'),hid:li.classList.contains('collapsed')||(ol&&getComputedStyle(ol).display==='none')};}""")
            if st["exp"]!="false" or not st["hid"]:
                issues.append(f"lv{lv}-collapse {st}")
            await tw.click()
            st2=await tw.evaluate("el=>el.getAttribute('aria-expanded')")
            if st2!="true":
                issues.append(f"lv{lv}-expand {st2}")
    # scrollspy auto-expand
    await pg.locator("#toc-col").click()
    await pg.evaluate("""()=>{document.documentElement.style.scrollBehavior='auto';
      const el=document.getElementById('rom-hard'); if(el) el.scrollIntoView({block:'start',behavior:'instant'});}""")
    await pg.wait_for_timeout(300)
    spy=await pg.evaluate("""()=>{
      const act=document.querySelector('#toc-page a.act');
      const href=act&&act.getAttribute('href');
      const target=document.querySelector('#toc-page a[href="#rom-hard"]');
      let n=target&&target.closest('.toc-n'), collapsed=0;
      while(n){if(n.classList.contains('collapsed'))collapsed++;n=n.parentElement&&n.parentElement.closest('.toc-n')}
      const top=document.getElementById('rom-hard').getBoundingClientRect().top;
      return {href,collapsed,txt:act&&act.textContent.trim().slice(0,40),top:Math.round(top)};
    }""")
    if not spy["href"] or spy["collapsed"] or spy["top"]>220:
        issues.append("scrollspy "+str(spy))
    # hideable
    if await pg.locator("#tocx").is_visible():
        await pg.locator("#tocx").click()
        off=await pg.evaluate("()=>document.documentElement.classList.contains('toc-off')")
        if not off: issues.append("hide-failed")
        await pg.locator("#tocbtn").click()
        on=await pg.evaluate("()=>!document.documentElement.classList.contains('toc-off')")
        if not on: issues.append("show-failed")

    # mobile drawer
    await pg.set_viewport_size({"width":390,"height":844})
    await pg.goto(f"http://127.0.0.1:{port}/maps.html",wait_until="domcontentloaded",timeout=60000)
    await pg.evaluate("document.documentElement.classList.remove('toc-open');document.documentElement.classList.add('toc-off')")
    await pg.wait_for_timeout(80)
    closed=await pg.evaluate("()=>{const r=document.getElementById('tocwrap').getBoundingClientRect();return r.right<8}")
    if not closed: issues.append("mobile-starts-open")
    await pg.locator("#tocbtn").click()
    await pg.wait_for_timeout(400)
    opened=await pg.evaluate("()=>{const r=document.getElementById('tocwrap').getBoundingClientRect();return {open:document.documentElement.classList.contains('toc-open'),left:Math.round(r.left),w:Math.round(r.width),vw:innerWidth}}")
    if not opened["open"] or opened["left"]>4:
        issues.append("drawer-open "+str(opened))
    # resize drawer
    box=await pg.locator("#tocresizer").bounding_box()
    if box:
        w0=opened["w"]
        await pg.mouse.move(box["x"]+1, box["y"]+120)
        await pg.mouse.down()
        await pg.mouse.move(max(box["x"]-100, 8), box["y"]+120, steps=6)
        await pg.mouse.up()
        w1,vw=await pg.evaluate("()=>[Math.round(document.getElementById('tocwrap').getBoundingClientRect().width), innerWidth]")
        if w1>vw*0.96+2:
            issues.append(f"drawer-overwide {w1}>{vw}")
        if not (w1+8 < w0):
            issues.append(f"drawer-no-resize {w0}->{w1}")
    wrap=await pg.evaluate("""()=>[...document.querySelectorAll('#toc-page a')].filter(a=>a.scrollWidth>a.clientWidth+3).slice(0,3).map(a=>a.textContent.slice(0,20))""")
    if wrap: issues.append("mobile-trunc "+str(wrap))
    await pg.locator("#toc-col").click(); await pg.locator("#toc-ex").click()
    # close via scrim
    scr=pg.locator("#scrim")
    if await scr.is_visible():
        await pg.mouse.click(385, 400)
        await pg.wait_for_timeout(300)
        if await pg.evaluate("()=>document.documentElement.classList.contains('toc-open')"):
            issues.append("scrim-close-fail")
    else:
        # try tocx if drawer still open
        if await pg.evaluate("()=>document.documentElement.classList.contains('toc-open')"):
            await pg.locator("#tocx").click()

    print("TOC_QA", "OK" if not issues else "BAD", issues[:8])
    rep["toc-qa"]={"ok":not issues,"issues":issues}
    if issues:
        return bad+1
    return bad

async def main():

    so=socket.socket(); so.bind(("127.0.0.1",0)); PORT=so.getsockname()[1]; so.close()
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1","-d",D],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(.5)
    rep={}; bad=0; jserrs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--disable-dev-shm-usage"])
        for w,h in VIEWS:
            ctx=await b.new_context(viewport={"width":w,"height":h})
            pg=await ctx.new_page()
            errors=[]
            pg.on("pageerror", lambda e: errors.append(str(e)))
            for f in PAGES:
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}",wait_until="domcontentloaded",timeout=45000)
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                await pg.wait_for_timeout(80)
                await interact(pg, f)
                await pg.wait_for_timeout(80)
                r=await pg.evaluate(JS)
                r["errs"]=errors[:]; errors.clear()
                ok = r["sw"]<=r["vw"]+1 and not r["off"] and not r["clip"] and not r["hdr"] and not r["errs"]
                bad += (not ok); rep[f"{w}/{f}"]=r
                print(("OK " if ok else "BAD"),w,f,"sw",r["sw"], r["off"][:2], r["clip"][:2], r["hdr"], r["errs"][:1])
                if w in (390,1440) and f in ("index.html","maps.html","paul-major.html","creeds.html","memory.html"):
                    await pg.screenshot(path=os.path.join(OUT,f"{w}-{f[:-5]}.png"))
            await ctx.close()
        # second pass on 390 & 1440 (interaction again)
        for w,h in ((390,844),(1440,900)):
            ctx=await b.new_context(viewport={"width":w,"height":h})
            pg=await ctx.new_page(); errs=[]
            pg.on("pageerror", lambda e: errs.append(str(e)))
            for f in PAGES:
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}",wait_until="domcontentloaded",timeout=60000)
                await interact(pg,f)
                r=await pg.evaluate(JS); r["errs"]=errs[:]; errs.clear()
                ok=r["sw"]<=r["vw"]+1 and not r["off"] and not r["clip"] and not r["hdr"] and not r["errs"]
                bad += (not ok); rep[f"pass2-{w}/{f}"]=r
                print(("OK2" if ok else "BAD2"),w,f,r["off"][:1],r["errs"][:1])
            await ctx.close()
        # TOC v3 behaviour
        ctx=await b.new_context(viewport={"width":1440,"height":900})
        pg=await ctx.new_page()
        bad=await toc_qa(pg, PORT, bad, rep)
        await ctx.close()
        # tile failure fallback
        ctx=await b.new_context(viewport={"width":1440,"height":900})
        pg=await ctx.new_page()
        async def abort_tiles(route):
            await route.abort()
        for host in ["tile.openstreetmap.org","basemaps.cartocdn.com","server.arcgisonline.com","tile.opentopomap.org","dh.gu.se","tile.openstreetmap.fr","tile.openstreetmap.de","tile-cyclosm.openstreetmap.fr"]:
            await pg.route(f"**/{host}/**", abort_tiles)
            await pg.route(f"**/*{host}*/*", abort_tiles)
        await pg.goto(f"http://127.0.0.1:{PORT}/maps.html#map-empire-t",wait_until="domcontentloaded",timeout=45000)
        await pg.wait_for_timeout(8000)
        fb=await pg.evaluate("""()=>({
          st: (document.querySelector('#imap-map-empire .imap-st')||{}).textContent||'',
          src: (document.querySelector('#imap-map-empire .imap-src')||{}).value||'',
          paths: document.querySelectorAll('#imap-map-empire .leaflet-overlay-pane path, #imap-map-empire svg path').length,
          ready: !!(document.querySelector('#imap-map-empire')||{})._ready,
          tiles: document.querySelectorAll('#imap-map-empire .leaflet-tile').length
        })""")
        print("FALLBACK", fb)
        await pg.screenshot(path=os.path.join(OUT,"fallback-empire.png"))
        rep["tile-fallback"]=fb
        # must end on offline or have vector paths and not be blank
        okfb = fb["paths"]>0 and ("离线" in fb["st"] or fb["src"]=="offline" or fb["paths"]>=5)
        if not okfb: bad += 1; print("BAD FALLBACK")
        else: print("OK FALLBACK")
        await ctx.close(); await b.close()
    srv.terminate()
    json.dump(rep, open(os.path.join(OUT,"qa.json"),"w"), ensure_ascii=False, indent=1)
    print("BAD COUNT", bad)
    return bad
asyncio.run(main())
