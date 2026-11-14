/* 新约书信深读 GROKstudy v1.0.0 */
(function(){
"use strict";
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var html=document.documentElement,wide=function(){return innerWidth>1100};
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
/* TOC */
var toc=$('#toc');
function tocToggle(force){
  if(wide()){var off=force!==undefined?!force:!html.classList.contains('toc-off');html.classList.toggle('toc-off',off);store('nt-toc',off?'0':'1')}
  else{html.classList.toggle('toc-open',force!==undefined?force:!html.classList.contains('toc-open'))}
}
$('#tocbtn').addEventListener('click',function(){tocToggle()});
$('#tocx').addEventListener('click',function(){tocToggle(false)});
$('#scrim').addEventListener('click',function(){html.classList.remove('toc-open')});
$$('#toc a').forEach(function(a){a.addEventListener('click',function(){if(!wide())html.classList.remove('toc-open')})});
document.addEventListener('keydown',function(e){
  if(/INPUT|TEXTAREA/.test(e.target.tagName))return;
  if(e.key==='t'||e.key==='T'){tocToggle()}
  if(e.key==='Escape'){html.classList.remove('toc-open');hidePop();$('#navdrop').classList.remove('open')}
});
$('#tocq').addEventListener('input',function(){
  var q=this.value.trim().toLowerCase();
  $$('#toc li').forEach(function(li){li.classList.toggle('hid',!!q&&li.textContent.toLowerCase().indexOf(q)<0)});
});
/* nav dropdown + theme */
$('#navbtn').addEventListener('click',function(e){e.stopPropagation();$('#navdrop').classList.toggle('open')});
document.addEventListener('click',function(e){if(!e.target.closest('#navdrop'))$('#navdrop').classList.remove('open')});
$('#themebtn').addEventListener('click',function(){var t=html.dataset.theme==='light'?'night':'light';html.dataset.theme=t;store('nt-theme',t);document.dispatchEvent(new CustomEvent('nt-theme'))});
/* progress, scrollspy, totop */
var links=$$('#toc a'),heads=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}),prog=$('#prog'),top=$('#totop'),ticking=false;
function onScroll(){
  var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,max=h.scrollHeight-h.clientHeight;
  prog.style.width=(max>0?sc/max*100:0)+'%';top.classList.toggle('show',sc>600);
  var cur=-1;for(var i=0;i<heads.length;i++){if(heads[i]&&heads[i].getBoundingClientRect().top<120)cur=i;else if(heads[i])break}
  links.forEach(function(a,i){a.classList.toggle('act',i===cur)});
  if(cur>=0&&wide()){var a=links[cur],tr=toc.getBoundingClientRect(),ar=a.getBoundingClientRect();if(ar.top<tr.top+60||ar.bottom>tr.bottom-20)toc.scrollTop+=ar.top-tr.top-tr.height/3}
  ticking=false;
}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();
top.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});
/* reveal */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
  $$('.reveal').forEach(function(el){io.observe(el)});
}else $$('.reveal').forEach(function(el){el.classList.add('in')});
/* verse popover */
var pop=null;
function hidePop(){if(pop){pop.remove();pop=null}}
document.addEventListener('click',function(e){
  var b=e.target.closest('.vs');
  if(!b){if(!e.target.closest('#pop'))hidePop();return}
  e.preventDefault();var same=pop&&pop._src===b;hidePop();if(same)return;
  pop=document.createElement('div');pop.id='pop';pop._src=b;pop.setAttribute('role','dialog');
  pop.textContent=b.dataset.t;var sm=document.createElement('small');sm.textContent='— '+b.textContent+'（和合本）';pop.appendChild(sm);
  document.body.appendChild(pop);
  var r=b.getBoundingClientRect(),pw=pop.offsetWidth,x=Math.min(Math.max(8,r.left+scrollX),scrollX+document.documentElement.clientWidth-pw-8),y=r.bottom+scrollY+8;
  if(r.bottom+pop.offsetHeight+16>innerHeight&&r.top>pop.offsetHeight+16)y=r.top+scrollY-pop.offsetHeight-8;
  pop.style.left=x+'px';pop.style.top=y+'px';
});
addEventListener('resize',hidePop);
/* flip cards */
document.addEventListener('click',function(e){var f=e.target.closest('.flip');if(f&&!e.target.closest('.vs'))f.classList.toggle('on')});
document.addEventListener('keydown',function(e){var f=e.target.closest&&e.target.closest('.flip');if(f&&(e.key==='Enter'||e.key===' ')){e.preventDefault();f.classList.toggle('on')}});
/* timeline filter */
$$('.tlf button').forEach(function(b){b.addEventListener('click',function(){
  $$('.tlf button').forEach(function(x){x.classList.toggle('on',x===b)});var f=b.dataset.f;
  $$('.tli').forEach(function(li){var show=f==='all'||(f==='ep'?li.classList.contains('ep'):li.classList.contains('c-'+f));li.classList.toggle('hid',!show);if(show)li.classList.add('in')});
})});
/* map */
var gm=$('.gmap');
if(gm){
  $$('.maptools .lb[data-l]').forEach(function(b){b.addEventListener('click',function(){b.classList.toggle('on');$$('.lyr[data-l="'+b.dataset.l+'"]',gm).forEach(function(g){g.classList.toggle('off',!b.classList.contains('on'))})})});
  var pl=$('#playroutes');if(pl)pl.addEventListener('click',function(){gm.classList.remove('playing');void gm.getBoundingClientRect();gm.classList.add('playing')});
  var info=$('#cityinfo');
  $$('.city[data-n]',gm).forEach(function(c){
    function sel(){$$('.city.sel',gm).forEach(function(x){x.classList.remove('sel')});c.classList.add('sel');var i=c.dataset.i;info.innerHTML='';var b=document.createElement('b');b.textContent='📍 '+c.dataset.n+'：';info.appendChild(b);info.appendChild(document.createTextNode(i?i:'与书信写作/收信无直接关系，是行程中的城市。'))}
    c.addEventListener('click',sel);c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sel()}});
  });
}
/* creed recite modes */
$$('.recite').forEach(function(r){
  var body=$('.rbody',r);
  $$('.rmodes button',r).forEach(function(b){b.addEventListener('click',function(){
    var m=b.dataset.m;
    if(m==='big'){b.classList.toggle('on');body.classList.toggle('big');return}
    $$('.rmodes button:not([data-m=big])',r).forEach(function(x){x.classList.toggle('on',x===b)});
    body.classList.remove('hint','hide');$$('.rt.show',body).forEach(function(x){x.classList.remove('show')});
    $$('.rt',body).forEach(function(x){if(x.dataset.o){x.textContent=x.dataset.o;delete x.dataset.o}});
    if(m==='hint'){body.classList.add('hint');$$('.rt',body).forEach(function(x){var t=x.textContent;x.dataset.o=t;var k=t.replace(/^\d+\)\s*/,'');var pre=t.slice(0,t.length-k.length);x.innerHTML='';x.appendChild(document.createTextNode(pre));var s=document.createElement('b');s.className='hint1';s.textContent=k.charAt(0);x.appendChild(s);x.appendChild(document.createTextNode(k.slice(1)))})}
    if(m==='hide')body.classList.add('hide');
  })});
  body.addEventListener('click',function(e){var t=e.target.closest('.rt');if(t&&(body.classList.contains('hint')||body.classList.contains('hide')))t.classList.toggle('show')});
});
/* memory page */
var dEl=$('#epdata');
if(dEl){
  var D=JSON.parse(dEl.textContent);
  var shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a};
  var fc=$('#fcards');
  $('#fcshuf').addEventListener('click',function(){shuffle($$('.flip',fc)).forEach(function(c){fc.appendChild(c)})});
  $('#fcall').addEventListener('click',function(){$$('.flip.on',fc).forEach(function(c){c.classList.remove('on')})});
  /* cloze */
  var cz=$('#cloze');
  shuffle(D).slice(0,6).forEach(function(d){
    var t=d.kvt,cands=['神','基督','信心','恩典','义','爱','盼望','圣灵','福音','真理','生命','律法','喜乐','平安','救恩','智慧','荣耀','十字架','行为','圣洁'].filter(function(w){return t.indexOf(w)>=0});
    var w=cands.length?cands[Math.floor(Math.random()*cands.length)]:t.slice(2,4),i=t.indexOf(w);
    var row=document.createElement('div');row.className='cz2';var p=document.createElement('p');
    p.appendChild(document.createTextNode(t.slice(0,i)));var g=document.createElement('span');g.className='gap';g.textContent=w;p.appendChild(g);p.appendChild(document.createTextNode(t.slice(i+w.length)));
    var s=document.createElement('small');s.textContent='— '+d.kv;var b=document.createElement('button');b.className='btn';b.textContent='显示';b.addEventListener('click',function(){row.classList.toggle('rev')});
    row.appendChild(p);row.appendChild(s);row.appendChild(b);cz.appendChild(row);
  });
  /* quiz */
  var kinds=[
    function(d){return{q:'《'+d.n+'》的钥字是？',a:d.kw,o:D.map(function(x){return x.kw})}},
    function(d){return{q:'“'+d.kvt.slice(0,40)+(d.kvt.length>40?'……':'')+'” 出自哪卷书？',a:d.n,o:D.map(function(x){return x.n})}},
    function(d){return{q:'《'+d.n+'》大约写于哪里？',a:d.place,o:D.map(function(x){return x.place}),p:1}},
    function(d){return{q:'记忆钩“'+d.mn.slice(0,34)+(d.mn.length>34?'……':'')+'”对应哪卷书？',a:d.n,o:D.map(function(x){return x.n})}}
  ];
  var qi=0,sc=0,cur=null,done=false,ord=[];
  function newQ(){
    if(!ord.length)ord=shuffle(D);var d=ord.pop();var k=kinds[Math.floor(Math.random()*kinds.length)](d);
    var opts=shuffle(k.o.filter(function(x,i,a){return x!==k.a&&a.indexOf(x)===i&&!(k.p&&x.slice(0,2)===k.a.slice(0,2))})).slice(0,3);opts.push(k.a);cur=k;done=false;
    $('#qzn').textContent='第 '+(++qi)+' 题';$('#qzq').textContent=k.q;$('#qzf').textContent='';var o=$('#qzo');o.innerHTML='';
    shuffle(opts).forEach(function(t){var b=document.createElement('button');b.textContent=t;b.addEventListener('click',function(){if(done)return;done=true;var ok=t===k.a;if(ok)sc++;b.classList.add(ok?'ok':'no');$$('button',o).forEach(function(x){if(x.textContent===k.a)x.classList.add('ok')});$('#qzs').textContent='得分 '+sc+' / '+qi;$('#qzf').textContent=ok?'✅ 正确！':'❌ 正确答案：'+k.a});o.appendChild(b)});
  }
  $('#qznext').addEventListener('click',newQ);$('#qzre').addEventListener('click',function(){qi=0;sc=0;ord=[];$('#qzs').textContent='得分 0';newQ()});newQ();
  /* plan */
  var saved={};try{saved=JSON.parse(store('nt-plan')||'{}')}catch(e){}
  $$('#plan input').forEach(function(c){c.checked=!!saved[c.dataset.d];c.addEventListener('change',function(){saved[c.dataset.d]=c.checked;store('nt-plan',JSON.stringify(saved))})});
}
/* draw svg in twoage */
$$('.twoage').forEach(function(f){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){$$('.draw',f).forEach(function(d){d.classList.add('in')});o.disconnect()}})});o.observe(f)});
})();

/* Lenis inertial scroll — skipped when user prefers reduced motion or if load fails */
(function(){
  try{ if(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches) return; }catch(e){return}
  var s=document.createElement("script"); s.src="assets/vendor/lenis.min.js"; s.defer=true;
  s.onload=function(){
    if(!window.Lenis) return;
    var opts={duration:1.05,lerp:.09,smoothWheel:true,syncTouch:false,anchors:true,autoRaf:true,prevent:function(n){return n.closest&&(n.closest("#toc")||n.closest(".imap")||n.closest(".mapscroll")||n.closest(".navdrop"))}};
    var lenis; try{lenis=new Lenis(opts)}catch(e){try{delete opts.autoRaf;delete opts.anchors;lenis=new Lenis(opts);(function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(0)}catch(e2){return}}
    document.documentElement.classList.add("lenis");
    window.NTLenis=lenis;
    document.querySelectorAll('a[href^="#"]').forEach(function(a){
      a.addEventListener("click",function(ev){
        var id=a.getAttribute("href"); if(!id||id==="#")return;
        var el=document.getElementById(id.slice(1)); if(!el||!lenis)return;
        ev.preventDefault(); lenis.scrollTo(el,{offset:-70}); history.pushState(null,"",id);
      });
    });
  };
  document.head.appendChild(s);
})();
