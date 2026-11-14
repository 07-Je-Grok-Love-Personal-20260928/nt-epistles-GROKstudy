/* 新约书信深读 v2 — 本地 Leaflet 互动地图：多底图 + 自动回退 + 离线矢量 */
(function(){
"use strict";
var TILES=[
  {id:"dare",name:"DARE 罗马帝国（古代）",url:"https://dh.gu.se/tiles/imperium/{z}/{x}/{y}.png",attr:"© DARE / University of Gothenburg",max:11},
  {id:"carto",name:"CARTO Positron",url:"https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",attr:"© OSM © CARTO",max:20},
  {id:"voyager",name:"CARTO Voyager",url:"https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",attr:"© OSM © CARTO",max:20},
  {id:"dark",name:"CARTO Dark",url:"https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",attr:"© OSM © CARTO",max:20},
  {id:"osm",name:"OpenStreetMap",url:"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",attr:"© OpenStreetMap",max:19},
  {id:"hot",name:"OSM Humanitarian",url:"https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",attr:"© OSM / HOT",max:19},
  {id:"osmde",name:"OpenStreetMap DE",url:"https://tile.openstreetmap.de/{z}/{x}/{y}.png",attr:"© OSM",max:18},
  {id:"esri",name:"Esri 卫星影像",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",attr:"© Esri, Maxar",max:19},
  {id:"topo",name:"Esri 地形图",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",attr:"© Esri",max:19},
  {id:"natgeo",name:"Esri National Geographic",url:"https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",attr:"© Esri",max:16},
  {id:"otm",name:"OpenTopoMap",url:"https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",attr:"© OSM © OpenTopoMap (CC-BY-SA)",max:17},
  {id:"offline",name:"离线矢量（Natural Earth）",url:null,attr:"Natural Earth 公有领域",max:8}
];
var failedSrc={}; var FALLBACK=["carto","osm","hot","osmde","voyager","esri","topo","natgeo","otm","dare","offline"];
var geoCache=null, leafletReady=null;
function byId(id){for(var i=0;i<TILES.length;i++) if(TILES[i].id===id) return TILES[i]; return TILES[0]}
function loadLeaflet(){
  if(window.L) return Promise.resolve();
  if(leafletReady) return leafletReady;
  leafletReady=new Promise(function(res,rej){
    var c=document.createElement("link"); c.rel="stylesheet"; c.href="assets/vendor/leaflet/leaflet.css"; document.head.appendChild(c);
    var s=document.createElement("script"); s.src="assets/vendor/leaflet/leaflet.js"; s.onload=res; s.onerror=rej; document.head.appendChild(s);
  });
  return leafletReady;
}
function loadGeo(){
  if(geoCache) return Promise.resolve(geoCache);
  return fetch("assets/geo/med.geojson").then(function(r){return r.json()}).then(function(j){geoCache=j;return j});
}
function themeDark(){return document.documentElement.dataset.theme!=="light"}
function vectorStyle(k){
  var d=themeDark();
  if(k==="land") return {color:d?"#8fb38a":"#5a7a4a", weight:1, fillColor:d?"#2a3b2c":"#d5e0c8", fillOpacity:.92};
  if(k==="lake") return {color:d?"#6fb6ff":"#7aa0c4", weight:.6, fillColor:d?"#0c2a4a":"#c5d8ea", fillOpacity:.95};
  return {color:d?"#6fb6ff":"#3d7ea6", weight:1.2, fill:false};
}
function addVector(map){
  if(map._neLayer){map.removeLayer(map._neLayer); map._neLayer=null}
  if(!geoCache) return;
  var sea=themeDark()?"#0a2540":"#cfe4f5";
  if(map._container) map._container.style.background=sea;
  map._neLayer=L.geoJSON(geoCache,{style:function(f){return vectorStyle(f.properties.k)}}).addTo(map);
}
function overlay(map,cfg){
  if(map._ov){map.removeLayer(map._ov); map._ov=null}
  var g=L.layerGroup();
  (cfg.areas||[]).forEach(function(a){
    var latlngs=a.ring.map(function(p){return [p[1],p[0]]});
    L.polygon(latlngs,{color:a.color,weight:1.5,fillColor:a.color,fillOpacity:.22}).bindPopup("<b>"+a.n+"</b>").addTo(g);
  });
  map._routes=[];
  (cfg.routes||[]).forEach(function(r){
    var ll=r.pts.map(function(p){return [p.lat,p.lon]});
    var line=L.polyline(ll,{color:r.color||"#ffc44d",weight:3,opacity:.92,dashArray:"8 6"}).bindPopup(r.name).addTo(g);
    map._routes.push(line);
  });
  (cfg.places||[]).forEach(function(p){
    var col=p.role==="from"?"#ffc44d":p.role==="to"?"#ff8fa3":p.role==="church"?"#ffe08a":"#ffffff";
    var mk=L.circleMarker([p.lat,p.lon],{radius:p.role==="from"||p.role==="to"?8:6,color:"#111",weight:1.4,fillColor:col,fillOpacity:1})
      .bindPopup("<b>"+p.n+"</b>"+(p.role?" · "+p.role:""))
      .bindTooltip(p.n,{direction:"top",className:"imap-lab",offset:[0,-8]});
    mk.addTo(g);
  });
  map._ov=g.addTo(map);
}
function playRoutes(map){
  (map._routes||[]).forEach(function(line){
    var el=line.getElement&&line.getElement();
    if(!el) return;
    var len=0; try{len=el.getTotalLength()}catch(e){return}
    el.style.strokeDasharray=len; el.style.strokeDashoffset=len;
    el.getBoundingClientRect();
    el.style.transition="stroke-dashoffset 3.2s ease";
    el.style.strokeDashoffset="0";
  });
}
function setStatus(root,msg,ok){
  var s=root.querySelector(".imap-st"); if(!s) return;
  s.textContent=msg; s.className="imap-st"+(ok===false?" bad":ok?" ok":"");
}
function applyTile(root,map,cfg,id,reason){
  var t=byId(id), prev=map._tile;
  if(prev){map.removeLayer(prev); map._tile=null}
  map._srcId=id;
  var sel=root.querySelector(".imap-src"); if(sel&&sel.value!==id) sel.value=id;
  try{localStorage.setItem("nt-tiles",id)}catch(e){}
  if(!t.url){
    addVector(map);
    setStatus(root,"离线矢量底图（Natural Earth）",true);
    return;
  }
  if(!map._neLayer) addVector(map); // keep land under tiles as instant fallback
  var layer=L.tileLayer(t.url,{maxZoom:t.max||18,attribution:t.attr,timeout:8000});
  var loaded=0, errors=0, done=false;
  var timer=setTimeout(function(){ if(loaded<1) fail("timeout")}, 2200);
  function fail(why){
    if(done) return; done=true; clearTimeout(timer);
    failedSrc[id]=1;
    if(layer) try{map.removeLayer(layer)}catch(e){}
    var order=FALLBACK.slice();
    if(cfg.prefer&&order[0]!==cfg.prefer) order.unshift(cfg.prefer);
    var next="offline";
    for(var i=0;i<order.length;i++){ if(order[i]!==id && !failedSrc[order[i]]){next=order[i];break} }
    setStatus(root,(t.name)+" 失败（"+why+"），切换至下一来源…",false);
    applyTile(root,map,cfg,next,"fallback");
  }
  layer.on("tileload",function(){loaded++; if(!done&&loaded>=1){done=true;clearTimeout(timer); setStatus(root,"底图："+t.name+(reason==="fallback"?"（已自动切换）":""),true)}});
  layer.on("tileerror",function(){errors++; if(loaded===0&&errors>=2) fail("error")});
  layer.addTo(map); map._tile=layer;
  // lift overlays above tiles
  if(map._ov&&map._ov.eachLayer) map._ov.eachLayer(function(l){if(l.bringToFront)l.bringToFront()});
}
function initOne(root){
  if(root._ready||!window.L) return;
  var cfg={}; try{cfg=JSON.parse(root.getAttribute("data-cfg")||"{}")}catch(e){cfg={}}
  var canvas=root.querySelector(".imap-canvas"); if(!canvas) return;
  root._ready=true;
  var map=L.map(canvas,{scrollWheelZoom:false,zoomControl:true,attributionControl:true,worldCopyJump:false});
  root._map=map;
  var c=cfg.center||[36.5,26]; map.setView(c, cfg.zoom||5);
  addVector(map);
  overlay(map,cfg);
  var sel=root.querySelector(".imap-src");
  TILES.forEach(function(t){var o=document.createElement("option");o.value=t.id;o.textContent=t.name;sel.appendChild(o)});
  var saved=null; try{saved=localStorage.getItem("nt-tiles")}catch(e){}
  var start=cfg.prefer||saved||"carto";
  if(saved&&saved!=="offline") start=saved;
  if(cfg.prefer==="dare") start="dare"; // historical maps prefer ancient tiles first
  sel.value=start;
  sel.addEventListener("change",function(){applyTile(root,map,cfg,sel.value,"user")});
  applyTile(root,map,cfg,start);
  var pb=root.querySelector(".imap-play"); if(pb) pb.addEventListener("click",function(){playRoutes(map)});
  // invalidate size after open / theme
  setTimeout(function(){map.invalidateSize()}, 200);
  root._resize=function(){map.invalidateSize()};
}
function boot(root){
  Promise.all([loadLeaflet(), loadGeo().catch(function(){return null})]).then(function(){initOne(root)}).catch(function(e){
    setStatus(root,"Leaflet 未能加载，已显示离线概念图。",false);
  });
}
function inView(el){var r=el.getBoundingClientRect();return r.bottom>0&&r.top<(window.innerHeight||800)+240&&r.height>0}
function watch(root){
  if(inView(root)||!("IntersectionObserver" in window)){boot(root);return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();boot(root)}})},{rootMargin:"240px 0px"});
  io.observe(root);
  addEventListener("scroll",function sc(){if(inView(root)){removeEventListener("scroll",sc);io.disconnect();boot(root)}},{passive:true});
  addEventListener("hashchange",function(){if(inView(root)){io.disconnect();boot(root)}});
}
function scan(ctx){
  (ctx||document).querySelectorAll(".imap:not([data-watched])").forEach(function(el){
    el.setAttribute("data-watched","1");
    var det=el.closest("details");
    if(det&&!det.open){
      det.addEventListener("toggle",function on(){if(det.open){boot(el); /* keep listener for resize */ setTimeout(function(){el._resize&&el._resize()},250)}});
    } else watch(el);
  });
}
document.addEventListener("DOMContentLoaded",function(){scan(document)});
document.addEventListener("nt-theme",function(){
  document.querySelectorAll(".imap").forEach(function(el){if(el._map){addVector(el._map); if(el._map._ov&&el._map._ov.eachLayer) el._map._ov.eachLayer(function(l){if(l.bringToFront)l.bringToFront()})}});
});
window.NTMaps={scan:scan,TILES:TILES,boot:boot};
})();
