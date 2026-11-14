# Playwright QA v2: overflow, clip, header overlap, JS errors, interactions, tile fallback
import asyncio, json, os, sys, subprocess, time, socket
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,"docs"); OUT=os.path.join(ROOT,"build","qa"); os.makedirs(OUT,exist_ok=True)
PAGES=[f for f in sorted(os.listdir(D)) if f.endswith(".html")]
VIEWS=((360,800),(390,844),(768,1024),(1024,768),(1440,900),(1920,1080))
JS=r"""()=>{const de=document.documentElement,vw=de.clientWidth,res={sw:de.scrollWidth,vw:vw,off:[],clip:[],hdr:[],js:0};
const skip=n=>{for(let p=n;p;p=p.parentElement){const s=getComputedStyle(p);if(p===document.body||p===de)break;if(/(auto|scroll|hidden)/.test(s.overflowX+' '+s.overflowY+' '+s.overflow)||p.id==='toc'||p.id==='navdrop'||p.classList.contains('leaflet-container')||p.classList.contains('imap-canvas')||p.classList.contains('mapscroll')||p.classList.contains('mainnav'))return true}return false};
document.querySelectorAll('main *, header.top *').forEach(n=>{
  if(n.closest&& (n.closest('.leaflet-container')||n.closest('#toc')||n.closest('.navdrop'))) return;
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
                await d.locator("summary").first.click(timeout=2000); opened+=1; await pg.wait_for_timeout(200)
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
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}",wait_until="networkidle",timeout=60000)
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                await pg.wait_for_timeout(250)
                await interact(pg, f)
                await pg.wait_for_timeout(200)
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
        # tile failure fallback
        ctx=await b.new_context(viewport={"width":1440,"height":900})
        pg=await ctx.new_page()
        async def abort_tiles(route):
            await route.abort()
        for host in ["tile.openstreetmap.org","basemaps.cartocdn.com","server.arcgisonline.com","tile.opentopomap.org","dh.gu.se","tile.openstreetmap.fr","tile.openstreetmap.de","tile-cyclosm.openstreetmap.fr"]:
            await pg.route(f"**/{host}/**", abort_tiles)
            await pg.route(f"**/*{host}*/*", abort_tiles)
        await pg.goto(f"http://127.0.0.1:{PORT}/maps.html#map-empire-t",wait_until="networkidle",timeout=60000)
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
