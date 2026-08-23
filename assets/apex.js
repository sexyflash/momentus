
(function(){
  var $=function(id){return document.getElementById(id);};

  /* ── 다크모드 ── */
  var tb=$('kbthemebtn');
  if(tb) tb.addEventListener('click',function(){
    var d=document.documentElement, next=d.dataset.theme==='dark'?'light':'dark';
    d.dataset.theme=next;
    try{localStorage.setItem('mmt-theme',next);}catch(e){}
    tb.setAttribute('aria-label', next==='dark'?'라이트모드로 전환':'다크모드로 전환');
  });

  /* ── 모바일 시트 ── */
  var bg=$('kbburger'), sh=$('kbsheet');
  if(bg&&sh) bg.addEventListener('click',function(){
    if(sh.hasAttribute('data-open')) sh.removeAttribute('data-open'); else sh.setAttribute('data-open','');
  });

  /* ── 검색 오버레이 (페이지 안 인덱스를 훑는다 — 서버 없음) ── */
  var IDX=[{"t": "헤이레시", "k": "제품", "g": "AI 상품사진 · 쇼핑몰 셀러", "u": "/products/heyreci/", "im": "https://heyreci.com/og-default.png", "ic": "◆"}, {"t": "마크", "k": "제품", "g": "로고 디자인 · 자영업 사장님", "u": "/products/mark/", "im": "https://mark.the-moment.us/og-default.png", "ic": "✕"}, {"t": "더플랜", "k": "제품", "g": "디지털 플래너 · 굿노트 · 아이패드", "u": "/products/theplan/", "im": "https://notes.the-moment.us/img/wizard/wz_9abd2186-233/draft_user_cover.png", "ic": "▤"}, {"t": "큐", "k": "제품", "g": "AI 모의면접 · 경력직 이직", "u": "/products/cue/", "im": "https://cue.the-moment.us/og.png", "ic": "◎"}, {"t": "빈방", "k": "제품", "g": "펜션·글램핑 빈방 알림", "u": "/products/binbang/", "im": "https://bb.the-moment.us/assets/hero.jpg", "ic": "◇"}, {"t": "컨텍스트", "k": "제품", "g": "노드로 잇는 AI 작업 공간", "u": "/products/kontext/", "im": "https://the-moment.us/assets/home/kontext.jpg", "ic": "◈"}, {"t": "퀵팡", "k": "무료 도구", "g": "커머스 · 북마크릿 · 1만+ 사용", "u": "/tools/quickpang/", "im": "", "ic": "⚡"}, {"t": "인스타 인기순 정렬", "k": "무료 도구", "g": "리서치 · 북마크릿", "u": "/tools/insta-rank/", "im": "", "ic": "◲"}, {"t": "유튜브 인기순 정렬", "k": "무료 도구", "g": "리서치 · 북마크릿", "u": "/tools/youtube-rank/", "im": "", "ic": "▶"}, {"t": "핀터레스트 원본 추출", "k": "무료 도구", "g": "리서치 · 북마크릿", "u": "/tools/pinterest-grab/", "im": "", "ic": "⚲"}, {"t": "ChatPage", "k": "무료 도구", "g": "생산성 · 크롬 확장 · 사용자 4,000명", "u": "/tools/chatpage/", "im": "", "ic": "✎"}, {"t": "her", "k": "무료 도구", "g": "생산성 · 크롬 확장 · NEW", "u": "/tools/her/", "im": "", "ic": "◉"}, {"t": "AI로 로고 공모에 524번 나가봤습니다", "k": "이야기", "g": "2026-07-13", "u": "/stories/loud-ai-contest/", "im": "", "ic": "✎"}, {"t": "AI 에이전트를 만들며 세 번 버린 것", "k": "이야기", "g": "2026-07-11", "u": "/stories/ai-agent-lessons/", "im": "", "ic": "✎"}, {"t": "왜 공짜로 푸는가", "k": "이야기", "g": "2026-07-05", "u": "/stories/why-free/", "im": "", "ic": "✎"}];
  var sr=$('kbsr'), q=$('kbsrq'), hits=$('kbsrhits');
  function openSr(){ sr.setAttribute('data-open',''); q.value=''; render(''); setTimeout(function(){q.focus();},30); }
  function closeSr(){ sr.removeAttribute('data-open'); }
  function render(v){
    v=v.trim().toLowerCase();
    var list = v ? IDX.filter(function(x){return (x.t+' '+x.k+' '+(x.g||'')).toLowerCase().indexOf(v)>=0;}) : IDX.slice(0,8);
    if(!list.length){ hits.innerHTML='<p class="kb-sr-none">찾는 것이 없어요. 다른 말로 해보시겠어요?</p>'; return; }
    hits.innerHTML=list.slice(0,10).map(function(x){
      var ext=/^https?:/.test(x.u)?' target="_blank" rel="noopener"':'';
      var th=x.im?'<span class="th"><img src="'+x.im+'" alt="" loading="lazy"></span>'
                 :'<span class="th">'+(x.ic||'·')+'</span>';
      return '<a href="'+x.u+'"'+ext+'>'+th+'<span class="tx"><b></b><i></i></span></a>';
    }).join('');
    [].forEach.call(hits.children,function(a,i){
      a.querySelector('b').textContent=list[i].t;
      a.querySelector('i').textContent=(list[i].k||'')+(list[i].g?' · '+list[i].g:'');
    });
  }
  if($('kbsearchbtn')) $('kbsearchbtn').addEventListener('click',openSr);
  if($('kbsrclose')) $('kbsrclose').addEventListener('click',closeSr);
  if(q) q.addEventListener('input',function(){render(q.value);});
  addEventListener('keydown',function(e){
    if(e.key==='Escape'&&sr&&sr.hasAttribute('data-open')) closeSr();
    if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault();openSr();}
  });
  if(sr) sr.addEventListener('click',function(e){ if(e.target===sr) closeSr(); });

  /* ── 히어로 슬라이드 ── */
  var hz=$('kbhero');
  if(hz){
    var ss=[].slice.call(hz.querySelectorAll('.kb-slide')),
        ds=[].slice.call(hz.querySelectorAll('.kb-dots button')), i=0, t=null;
    function go(n){ i=(n+ss.length)%ss.length;
      ss.forEach(function(s,k){s.classList.toggle('on',k===i);});
      ds.forEach(function(d,k){ if(k===i) d.setAttribute('aria-current','true'); else d.removeAttribute('aria-current'); }); }
    function play(){ if(ss.length<2) return;
      if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      stop(); t=setInterval(function(){go(i+1);},7000); }
    function stop(){ if(t) clearInterval(t); t=null; }
    ds.forEach(function(d){ d.addEventListener('click',function(){ go(+d.dataset.i); play(); }); });
    hz.addEventListener('mouseenter',stop); hz.addEventListener('mouseleave',play);
    play();
  }

  /* ── 가로 레일 화살표 ── */
  [].forEach.call(document.querySelectorAll('.kb-arrows[data-rail]'),function(box){
    var rail=$(box.dataset.rail); if(!rail) return;
    var btns=[].slice.call(box.querySelectorAll('button'));
    function step(){ var c=rail.firstElementChild; return c?c.getBoundingClientRect().width+20:320; }
    function sync(){
      var max=rail.scrollWidth-rail.clientWidth-2;
      btns[0].disabled = rail.scrollLeft<=2;
      btns[1].disabled = rail.scrollLeft>=max;
    }
    btns.forEach(function(b){ b.addEventListener('click',function(){
      rail.scrollBy({left:step()*(+b.dataset.dir),behavior:'smooth'}); }); });
    rail.addEventListener('scroll',sync,{passive:true});
    addEventListener('resize',sync); sync();
  });

  /* ── 카테고리 스크롤러 ── */
  var CATS=[{"slug": "heyreci", "url": "/products/heyreci/", "name": "헤이레시", "tagline": "폰으로 찍어도 판매용 컷이 됩니다.", "shot": "https://heyreci.com/og-default.png", "icon": "◆", "color": "#3182f6"}, {"slug": "mark", "url": "/products/mark/", "name": "마크", "tagline": "내 업종 로고를 먼저 보고 고릅니다.", "shot": "https://mark.the-moment.us/og-default.png", "icon": "✕", "color": "#0E1013"}, {"slug": "theplan", "url": "/products/theplan/", "name": "더플랜", "tagline": "내 손에 맞는 플래너를 골라서 씁니다.", "shot": "https://notes.the-moment.us/img/wizard/wz_9abd2186-233/draft_user_cover.png", "icon": "▤", "color": "#5A5A5A"}, {"slug": "cue", "url": "/products/cue/", "name": "큐", "tagline": "면접장에서 얼어붙지 않게 잡아 줍니다.", "shot": "https://cue.the-moment.us/og.png", "icon": "◎", "color": "#0E1013"}, {"slug": "binbang", "url": "/products/binbang/", "name": "빈방", "tagline": "다 찬 숙소도 취소는 나옵니다.", "shot": "https://bb.the-moment.us/assets/hero.jpg", "icon": "◇", "color": "#191f28"}, {"slug": "kontext", "url": "/products/kontext/", "name": "컨텍스트", "tagline": "생각을 정리하고, 그 상태로 AI에게 넘깁니다.", "shot": "https://the-moment.us/assets/home/kontext.jpg", "icon": "◈", "color": "#5b5bd6"}, {"slug": "quickpang", "url": "/tools/quickpang/", "name": "퀵팡", "tagline": "클릭 없이 옵션·재고 확인.", "shot": "", "icon": "⚡", "color": "var(--coup)"}, {"slug": "insta-rank", "url": "/tools/insta-rank/", "name": "인스타 인기순 정렬", "tagline": "이 계정, 뭐가 제일 잘 됐나?", "shot": "", "icon": "◲", "color": "var(--ig)"}, {"slug": "youtube-rank", "url": "/tools/youtube-rank/", "name": "유튜브 인기순 정렬", "tagline": "가장 많이 재생된 순서로.", "shot": "", "icon": "▶", "color": "var(--yt)"}, {"slug": "pinterest-grab", "url": "/tools/pinterest-grab/", "name": "핀터레스트 원본 추출", "tagline": "저해상 썸네일 말고, 원본을.", "shot": "", "icon": "⚲", "color": "var(--pin)"}, {"slug": "chatpage", "url": "/tools/chatpage/", "name": "ChatPage", "tagline": "아무리 긴 유튜브도, 3초 요약.", "shot": "", "icon": "✎", "color": "#111"}, {"slug": "her", "url": "/tools/her/", "name": "her", "tagline": "타이핑 대신, 말로.", "shot": "", "icon": "◉", "color": "var(--ok)"}], list=$('kbcatlist'), card=$('kbcatcard');
  if(list&&card&&CATS.length){
    var lis=[].slice.call(list.children), ci=0, ct=null, paused=false,
        art=card.querySelector('.kb-cat-art'), h3=card.querySelector('h3'), p=card.querySelector('p');
    function paint(n){
      ci=(n+CATS.length)%CATS.length;
      var c=CATS[ci], h=lis[0]?lis[0].offsetHeight:56;
      list.style.transform='translateY('+(-(ci*h)-h/2)+'px)';
      lis.forEach(function(li,k){ if(k===ci) li.setAttribute('aria-current','true'); else li.removeAttribute('aria-current'); });
      card.href=c.url;
      card.style.setProperty('--cc','color-mix(in srgb,'+c.color+' 16%,#fff)');
      art.style.background=c.color;
      art.innerHTML = c.shot ? '<img src="'+c.shot+'" alt="" loading="lazy">' : c.icon;
      h3.textContent=c.name; p.textContent=c.tagline;
    }
    function tick(){ if(!paused) paint(ci+1); }
    function start(){ if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      if(ct) clearInterval(ct); ct=setInterval(tick,3200); }
    lis.forEach(function(li,k){ li.querySelector('button').addEventListener('click',function(){ paint(k); start(); }); });
    [].forEach.call(document.querySelectorAll('.kb-cat-ctl button[data-dir]'),function(b){
      b.addEventListener('click',function(){ paint(ci+(+b.dataset.dir)); start(); }); });
    var pb=$('kbcatpause');
    if(pb) pb.addEventListener('click',function(){
      paused=!paused;
      if(paused) pb.setAttribute('data-paused',''); else pb.removeAttribute('data-paused');
      pb.setAttribute('aria-label', paused?'자동 넘김 재생':'자동 넘김 멈춤');
    });
    paint(0); start();
  }

  /* ── 맨 위로 ── */
  var top=$('kbtop');
  if(top){
    top.addEventListener('click',function(){ scrollTo({top:0,behavior:'smooth'}); });
    addEventListener('scroll',function(){
      if(scrollY>600) top.setAttribute('data-on',''); else top.removeAttribute('data-on');
    },{passive:true});
  }
})();

/* 홈 하단 레일 — 좌우 버튼으로 한 화면씩 민다. */
(function(){
  document.querySelectorAll('.rl-nav[data-rail]').forEach(function(box){
    var rail=document.getElementById(box.dataset.rail); if(!rail) return;
    var btns=[].slice.call(box.querySelectorAll('button'));
    function step(){ var c=rail.firstElementChild;
      return c?(c.getBoundingClientRect().width+16)*Math.max(1,Math.floor(rail.clientWidth/(c.getBoundingClientRect().width+16))):320; }
    function sync(){ btns[0].disabled=rail.scrollLeft<=2;
      btns[1].disabled=rail.scrollLeft+rail.clientWidth>=rail.scrollWidth-2; }
    btns.forEach(function(b){ b.addEventListener('click',function(){
      rail.scrollBy({left:step()*(+b.dataset.d),behavior:'smooth'}); }); });
    rail.addEventListener('scroll',sync); addEventListener('resize',sync); sync();
  });
})();

/* 홈 제품 무대 — 스크롤을 따라 한 장씩 올라온다. 첫 장은 기다리지 않는다. */
(function(){
  var els=[].slice.call(document.querySelectorAll('.stg'));
  if(!els.length) return;
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){
    els.forEach(function(e){e.classList.add('in');}); return; }
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('in'); io.unobserve(e.target);}});},
    {rootMargin:'0px 0px -10% 0px'});
  els.forEach(function(e){io.observe(e);});
  els[0].classList.add('in');
})();
