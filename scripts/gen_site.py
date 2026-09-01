# -*- coding: utf-8 -*-
"""MOMENTUS 정적 사이트 생성기 v1 — 루트(the-moment.us) 본 사이트.
   assets/bookmarklets/*.txt(원본 소스)를 드래그 버튼 href에 실제 주입한다.
   실행: python3 scripts/gen_site.py (repo 루트에서)"""
import os
import json
import hashlib
import re

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

BM = {}
for k in ["insta-rank", "youtube-rank", "pinterest-grab", "quickpang"]:
    with open(f"assets/bookmarklets/{k}.txt", encoding="utf-8") as f:
        raw = f.read().strip()
    BM[k] = raw.replace("&", "&amp;").replace('"', "&quot;")

# 제품 진실의 원천 = data/products.json (지그 매니페스트). 새 제품 = 거기 한 줄 추가.
#   ⚠️ 바·푸터가 이걸 읽으므로 CSS/gnb 정의보다 먼저 로드해야 한다.
with open("data/products.json", encoding="utf-8") as _mf:
    _MANIFEST = json.load(_mf)
ORDER = _MANIFEST["order"]
P = _MANIFEST["products"]
BAR = _MANIFEST["bar"]
# 무료 도구 = 매니페스트에서 파생(free + 북마크릿/확장). 하드코딩 목록을 두지 않는다.
TOOLS = [s for s in ORDER if P[s].get("free") and P[s].get("type") in ("bookmarklet", "extension")]
SPOKES = [s for s in ORDER if s not in TOOLS]
# 네이티브 앱(/apps/<slug>/) + 영구 링크 층(/l/<키>). 둘 다 없으면 빈 값으로 넘어간다.
APPS = {k: v for k, v in _MANIFEST.get("apps", {}).items() if not k.startswith("_")}
LINKS = _MANIFEST.get("links", {})

CSS = """/* MOMENTUS site.css — v1 */
/* /products/ 제품 허브 — /tools/(.tls-*) 와 같은 골격의 형제 페이지.
   ⚠️ 클래스 접두사를 prh- 로 못박은 이유: 처음엔 .pcard/.pgrid 로 지었다가
   아래쪽 레거시 .pcard/.pgrid 규칙과 정면 충돌해 레이아웃이 깨졌다(2026-08-23).
   같은 파일 안에서 뒤에 오는 규칙이 이겨 카드가 flex 컬럼으로 뒤집히고 그리드가
   3분할 + 자체 패딩을 먹었다. 새 컴포넌트는 반드시 안 쓰는 접두사로 시작해라. */
.prh{padding:0 var(--gut)}
.prh-g{margin-top:52px}
.prh-gh{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;
padding-bottom:12px;border-bottom:1.5px solid var(--ink)}
.prh-gh h2{font-size:19px;font-weight:800;letter-spacing:-.035em}
.prh-gh .s{font-size:13.5px;color:var(--faint)}
.prh-list{display:flex;flex-direction:column}
.prh-row{display:flex;align-items:center;gap:24px;padding:20px 4px;
border-bottom:1px solid var(--line);transition:background .14s}
.prh-row:hover{background:var(--soft)}
.prh-row .th{width:172px;aspect-ratio:16/10;flex:0 0 auto;border-radius:12px;
overflow:hidden;background:var(--soft2)}
/* 로고 썸네일은 자르지 않는다 — cover 로 자르면 로고가 잘려 무슨 서비스인지 안 읽힌다. */
.prh-row .th.logo{background:var(--paper);box-shadow:inset 0 0 0 1px var(--line)}
.prh-row .th.logo img{object-fit:contain;padding:14px}
.prh-row .th img{width:100%;height:100%;object-fit:cover;display:block;
transition:transform .45s var(--ease)}
.prh-row:hover .th img{transform:scale(1.04)}
/* 무료 도구는 우리 스크린샷이 없다 — 아이콘 타일로 그린다(제품 색 그대로). */
.prh-row .th.ic{display:flex;align-items:center;justify-content:center;
background:var(--soft);background:color-mix(in srgb,var(--c,#888) 9%,var(--soft));
color:var(--c,var(--ink));font-size:40px;line-height:1}
.prh-row .bd{flex:1 1 auto;min-width:0}
.prh-row .nm{font-size:17px;font-weight:700;letter-spacing:-.03em}
.prh-row .tg{font-size:12.5px;color:var(--faint);margin-top:3px}
.prh-row .ds{font-size:14.5px;color:var(--gray);margin-top:8px;line-height:1.5}
/* 과금 표기 — 옅은 mono 회색이라 안 보였다(2026-08-23). 알약 + 굵기로 올린다. */
.prh-row .mt{flex:0 0 auto;font-size:12px;font-weight:700;letter-spacing:-.01em;
padding:6px 12px;border-radius:99px;background:var(--soft2);color:var(--ink2);white-space:nowrap}
.prh-row:hover .mt{background:var(--paper)}
.prh-row .mt.free{background:rgba(18,183,106,.12);color:#0b8f52}
.prh-foot{margin:44px 0 110px;font-size:14px;color:var(--gray)}
.prh-foot a{text-decoration:underline;text-underline-offset:3px}
@media(max-width:640px){
  .prh-row{gap:14px;padding:15px 2px}
  .prh-row .th{width:112px;border-radius:9px}
  .prh-row .th.ic{font-size:23px}
  .prh-row .ds{font-size:13.5px;margin-top:5px}
  .prh-row .mt{padding:4px 9px;font-size:11px}
}

:root{--ink:#0b0c0e;--ink2:#3a4150;--paper:#fff;--soft:#f4f5f7;--soft2:#e9ebee;--gray:#5b6270;--faint:#9aa0a8;--line:#e6e8ec;
--pt:#ff4b26;--ok:#12b76a;--ig:#e1306c;--yt:#ff0033;--pin:#e60023;--coup:#346aff;
--gut:max(20px,calc((100% - 1200px)/2));
--sans:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Helvetica Neue","Segoe UI",sans-serif;
--mono:"SF Mono",ui-monospace,Menlo,monospace;--ease:cubic-bezier(.16,1,.3,1)}
*{box-sizing:border-box}
body{margin:0;word-break:keep-all;overflow-wrap:break-word;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}h1,h2,h3,h4,p{margin:0;font-weight:400}img{display:block;max-width:100%}
/* .gnb 의 gap·padding 은 아래 '브랜드 바' 절이 정한다(크롬 층 전용 여백) — 여기 적지 마라 */
.gnb{position:fixed;inset:0 0 auto;z-index:100;height:56px;display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.85);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.gnb .wm{font-size:20px;font-weight:800;letter-spacing:-.02em}
.gnb .lk{display:flex;align-items:center;gap:26px;height:56px}
.gnb .lk>a,.gnb .hasdrop>a{font-size:14px;color:var(--gray);font-weight:500}
.gnb .lk>a:hover,.gnb .hasdrop>a:hover{color:var(--ink)}.gnb .lk .on{color:var(--ink);font-weight:700}
.gnb .hasdrop{position:relative;display:flex;align-items:center;height:56px}
.gnb .drop{position:absolute;top:56px;left:50%;transform:translateX(-50%) translateY(4px);background:#fff;border:1px solid var(--line);border-radius:10px;padding:6px 0;min-width:160px;opacity:0;visibility:hidden;transition:opacity .16s,transform .16s;box-shadow:0 12px 32px -12px rgba(0,0,0,.18)}
.gnb .hasdrop:hover .drop{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
.gnb .drop a{display:block;padding:9px 18px;font-size:13px;color:var(--gray);white-space:nowrap}.gnb .drop a:hover{color:var(--ink);background:var(--soft)}
@media(max-width:820px){.gnb .lk{gap:15px}.gnb .lk .hidem{display:none}}
/* 1단 바(브랜드 바) — products.json 의 bar 를 그린다. shell.js 가 스포크에 그리는 것과 같은 문법. */
/* 브랜드 바는 콘텐츠 그리드에 맞추지 않는다 — '크롬(chrome) 층'이라 자기 여백을 쓴다.
   실측 근거: apple.com/kr/mac 1280px 에서 글로벌 바 142px vs 페이지 콘텐츠 80px = 62px 어긋남.
   제품마다 그리드(최대폭·거터)가 다르므로 맞추려 들면 어느 하나엔 반드시 어긋나고,
   '살짝 어긋남'은 실수로 읽힌다. 그래서 전 사이트 공통 고정 여백으로 확실히 분리한다. */
.gnb{gap:14px;padding:0 20px}
@media(max-width:640px){.gnb{padding:0 16px}}
.gnb .wm{flex:0 0 auto}
.gnb .lk{flex-wrap:nowrap;min-width:0}
.gnb .lk>a{white-space:nowrap;flex:0 0 auto}
.gnb .lk .sep{width:1px;height:13px;background:var(--line);flex:0 0 auto}
.gnb .lk a[aria-current="page"]{color:var(--ink);font-weight:700}
.gnb .lk .ext i{font-style:normal;font-size:9px;opacity:.5;margin-left:3px;vertical-align:super}
.gnb .lk a[data-sub]{position:relative}
.gnb .lk a[data-sub]::after{content:attr(data-sub);position:absolute;top:calc(100% + 8px);left:50%;
transform:translateX(-50%) translateY(-3px);white-space:nowrap;background:var(--ink);color:#fff;font-size:12px;
font-weight:500;letter-spacing:-.01em;padding:6px 11px;border-radius:8px;opacity:0;visibility:hidden;
pointer-events:none;transition:opacity .14s,transform .14s;box-shadow:0 10px 26px -12px rgba(0,0,0,.35);z-index:5}
.gnb .lk a[data-sub]:hover::after,.gnb .lk a[data-sub]:focus-visible::after{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
@media(max-width:820px){.gnb .lk{gap:11px;font-size:13px;overflow-x:auto;scrollbar-width:none}
.gnb .lk::-webkit-scrollbar{display:none}.gnb .lk .sep{display:none}
.gnb .lk a[data-sub]::after{display:none}}
/* /tools/ 허브 — 무료 도구 목록 */
/* 랜딩 히어로 — 한 번에 하나만 크게. 레퍼런스: samsung.com/sec · awwwards.com
   공통 문법 = 텍스트 최소·초대형 / 압도적 여백 / CTA 한 개 / 큰 비주얼이 주인공. */
.hz{position:relative;background:#fff}
.hz-s{display:none;max-width:1245px;margin:0 auto;padding:clamp(44px,5.5vw,78px) 24px clamp(36px,4vw,60px)}
.hz-s.on{display:block;animation:hzIn .6s var(--ease) both}
@keyframes hzIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.hz-cap{text-align:center;max-width:900px;margin:0 auto}
.hz-k{font-family:var(--mono);font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint)}
.hz-cap h1{margin-top:16px;font-size:clamp(38px,6.2vw,86px);font-weight:800;letter-spacing:-.055em;
line-height:1.02;color:var(--ink);word-break:keep-all;text-wrap:balance}
.hz-cap p{margin:22px auto 0;font-size:clamp(15px,1.5vw,19px);line-height:1.66;color:var(--gray);max-width:44ch}
.hz-cta{display:inline-flex;align-items:center;margin-top:30px;background:var(--ink);color:#fff;
font-size:15px;font-weight:700;padding:14px 30px;border-radius:99px;transition:transform .15s}
.hz-cta:hover{transform:translateY(-2px)}
.hz-art{margin-top:clamp(40px,5vw,68px);border-radius:20px;overflow:hidden;aspect-ratio:16/9;
box-shadow:0 40px 80px -40px rgba(16,24,40,.34)}
.hz-art img{width:100%;height:100%;display:block}
.hz-dots{display:flex;justify-content:center;gap:9px;padding:26px 0 0}
.hz-dots button{width:7px;height:7px;border-radius:50%;border:0;padding:0;cursor:pointer;
background:var(--soft2);transition:.18s}
.hz-dots button[aria-current]{background:var(--ink);width:22px;border-radius:99px}
@media(max-width:640px){.hz-art{aspect-ratio:4/3}.hz-cap{max-width:none}}
/* 랜딩 — 지금 새로 나온 것 */
.nw{padding:54px 24px 8px;max-width:1245px;margin:0 auto}
.nw-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;padding-bottom:18px}
.nw-head h2{font-size:20px;font-weight:800;letter-spacing:-.035em}
.nw-more{font-size:13.5px;font-weight:700;color:var(--gray);white-space:nowrap}
.nw-more:hover{color:var(--ink)}
.nw-list{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.nw-row{display:flex;align-items:center;gap:14px;padding:14px 2px;border-bottom:1px solid var(--line);transition:background .14s}
.nw-row:hover{background:var(--soft)}
.nw-k{flex:0 0 auto;font-size:11.5px;font-weight:700;color:var(--pt);background:#fff5f2;padding:3px 9px;border-radius:99px}
.nw-t{flex:1 1 auto;font-size:15px;font-weight:650;letter-spacing:-.02em;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nw-s{flex:0 0 auto;font-size:12.5px;color:var(--gray)}
.nw-d{flex:0 0 auto;font-family:var(--mono);font-size:11.5px;color:var(--faint);font-variant-numeric:tabular-nums}
@media(max-width:640px){.nw{padding-top:48px}.nw-s{display:none}}
/* 글 하단 태그 */
.an-tags{display:flex;gap:8px;flex-wrap:wrap;margin:26px 0 0}
.an-tag{font-size:13px;font-weight:600;color:var(--gray);background:var(--soft);padding:7px 13px;border-radius:99px}
.an-tag:hover{background:var(--soft2);color:var(--ink)}
.tls{padding:0 var(--gut)}
.tls-head{padding:var(--pg-top) 0 var(--pg-head-gap);display:flex;flex-direction:column;gap:10px}
.tls-head .k{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;color:var(--faint)}
.tls-head h1{font-size:clamp(28px,4vw,40px);font-weight:800;letter-spacing:-.045em;line-height:1.15}
.tls-head p{color:var(--gray);font-size:16px;max-width:56ch}
.tls-list{display:flex;flex-direction:column;border-top:1px solid var(--line);margin-bottom:110px}
.tls-row{display:flex;align-items:center;gap:18px;padding:20px 4px;border-bottom:1px solid var(--line);transition:background .14s}
.tls-row:hover{background:var(--soft)}
.tls-row .ic{width:38px;height:38px;flex:0 0 auto;display:flex;align-items:center;justify-content:center;
border-radius:10px;background:var(--soft2);font-size:17px}
.tls-row .bd{flex:1 1 auto;min-width:0}
.tls-row .nm{font-size:16px;font-weight:700;letter-spacing:-.025em}
.tls-row .ds{color:var(--gray);font-size:14px;margin-top:2px}
.tls-row .mt{flex:0 0 auto;font-family:var(--mono);font-size:11.5px;color:var(--faint);white-space:nowrap}
@media(max-width:640px){.tls-row .mt{display:none}.tls-head{padding-top:64px}}
main{padding-top:0}
.vd-qa{max-width:760px;margin:64px auto 0;padding:0 20px}.vd-qa>h2{font-size:26px;font-weight:800;letter-spacing:-.02em;margin:0 0 24px;color:var(--ink)}.vd-qa-i{padding:20px 0;border-top:1px solid var(--line)}.vd-qa-i h3{font-size:17px;font-weight:700;margin:0 0 8px;color:var(--ink);letter-spacing:-.01em}.vd-qa-i p{margin:0;font-size:15px;line-height:1.7;color:var(--gray)}.btn{display:inline-flex;align-items:center;gap:var(--mmt-ctrl-gap,8px);background:var(--ink);color:#fff;font-size:var(--mmt-fs-ctrl,15px);font-weight:var(--mmt-fw-ctrl,700);padding:var(--mmt-ctrl-pad,14px 28px);border-radius:var(--mmt-r-ctrl,999px);border:none;cursor:pointer}
.btn:hover{opacity:.87}.btn.lg{font-size:15px;padding:14px 26px}
.btn.ghost{background:none;color:var(--ink);border:1px solid var(--line)}
.btn.drag{border:2px dashed var(--pt);color:var(--pt);background:#fff5f2;cursor:grab;font-weight:800}
/* 드래그 안내 — 글 대신 그림. 버튼 글자는 북마크 이름이 되므로 안내문을 넣을 수 없다(2026-09-01).
   버튼 위에 작은 브라우저 그림이 떠서 "끌어다 놓으면 북마크바에 꽂힌다"를 보여준다.
   꽂히는 순간이 제일 중요한 장면이라 그때 북마크바 쪽으로 줌인한다(창업자 지시). */
.dragwrap{position:relative;display:inline-flex}
.dragdemo{position:absolute;left:50%;bottom:calc(100% + 13px);width:232px;padding:9px 9px 7px;
  background:#111;border-radius:14px;box-shadow:0 16px 36px rgba(0,0,0,.3);
  transform:translateX(-50%) translateY(6px);opacity:0;pointer-events:none;
  transition:opacity .16s ease,transform .16s ease;z-index:120}
.dragdemo::after{content:"";position:absolute;left:50%;top:100%;transform:translateX(-50%);
  border:7px solid transparent;border-top-color:#111}
.dragdemo svg{display:block;width:100%;height:auto;border-radius:8px}
.dd-cap{display:block;margin-top:7px;text-align:center;color:#c9ccd1;
  font-size:11.5px;font-weight:600;letter-spacing:-.01em;line-height:1.3}
.dd-win{fill:#fff}
.dd-bar{fill:#eceef1}
.dd-chip{fill:#c7ced6}
.dd-slot{fill:none;stroke:#aab2bc;stroke-width:1.4;stroke-dasharray:3.5 3}
.dd-land{fill:var(--dd,var(--pt));opacity:0}
.dd-spark{fill:#ffd24d;opacity:0}
.dd-fly rect{fill:var(--dd,var(--pt))}
.dd-fly circle{fill:#fff}
.dd-cur{fill:#111;stroke:#fff;stroke-width:1.2}
.dd-scene,.dd-fly,.dd-cur,.dd-land,.dd-spark{animation-duration:5s;animation-iteration-count:infinite;
  animation-timing-function:ease-in-out;animation-play-state:paused;
  transform-box:fill-box;transform-origin:center}
.dd-fly{animation-name:dd-fly}
.dd-cur{animation-name:dd-cur;transform-box:view-box;transform-origin:0 0}
.dd-land{animation-name:dd-land}
.dd-spark{animation-name:dd-spark}
.dd-scene{animation-name:dd-zoom;transform-box:view-box;transform-origin:91px 20.5px}
.dragwrap:hover .dragdemo,.dragwrap:focus-within .dragdemo{opacity:1;transform:translateX(-50%) translateY(0)}
.dragwrap:hover .dd-scene,.dragwrap:hover .dd-fly,.dragwrap:hover .dd-cur,
.dragwrap:hover .dd-land,.dragwrap:hover .dd-spark,
.dragwrap:focus-within .dd-scene,.dragwrap:focus-within .dd-fly,.dragwrap:focus-within .dd-cur,
.dragwrap:focus-within .dd-land,.dragwrap:focus-within .dd-spark{animation-play-state:running}
/* 5s 한 바퀴 — 잡고(0~14%) 천천히 올라가(14~52%) 꽂히고(52~60%) 줌으로 보여준 뒤(60~88%) 되돌아간다 */
@keyframes dd-fly{
  0%{transform:translate(110px,96px);opacity:0}
  5%{transform:translate(110px,96px);opacity:1}
  14%{transform:translate(110px,92px);opacity:1}
  52%{transform:translate(91px,20.5px);opacity:1}
  57%{transform:translate(91px,20.5px) scale(.66);opacity:.35}
  60%{transform:translate(91px,20.5px) scale(.62);opacity:0}
  100%{transform:translate(110px,96px);opacity:0}}
@keyframes dd-cur{
  0%,5%{transform:translate(124px,101px);opacity:1}
  14%{transform:translate(124px,97px);opacity:1}
  52%,72%{transform:translate(105px,25px);opacity:1}
  86%{transform:translate(124px,101px);opacity:0}
  100%{transform:translate(124px,101px);opacity:0}}
@keyframes dd-land{
  0%,56%{opacity:0;transform:scale(.55)}
  61%{opacity:1;transform:scale(1.12)}
  65%{opacity:1;transform:scale(1)}
  92%{opacity:1;transform:scale(1)}
  100%{opacity:0;transform:scale(1)}}
@keyframes dd-spark{
  0%,58%{opacity:0;transform:scale(.4)}
  66%{opacity:1;transform:scale(1)}
  80%{opacity:0;transform:scale(1.35)}
  100%{opacity:0;transform:scale(1.35)}}
@keyframes dd-zoom{
  0%,50%{transform:scale(1)}
  62%{transform:scale(1.75)}
  88%{transform:scale(1.75)}
  97%,100%{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.dd-scene,.dd-fly,.dd-cur,.dd-land,.dd-spark{animation:none}
  .dd-land{opacity:1}.dd-fly{opacity:0}}
@media (max-width:560px){.dragdemo{width:min(232px,82vw)}}
.btn.drag:active{cursor:grabbing}
.free{font-family:var(--mono);font-size:11px;font-weight:700;color:#fff;background:var(--ink);padding:3px 9px;border-radius:6px}
.kick{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--gray)}
.kick.pt{color:var(--pt);font-weight:700}
/* ⚠️ margin-top 을 주면 회색 섹션과 푸터 사이에 **흰 띠**가 남는다(2026-08-24 대표 지적).
   푸터는 흰 바탕으로 바로 이어붙이고, 경계는 헤어라인 하나로만 낸다. */
footer.site{background:var(--paper);border-top:1px solid var(--line);margin-top:0;padding:56px var(--gut) 44px;display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:24px;font-size:13px}
@media(max-width:760px){footer.site{grid-template-columns:1fr 1fr}}
footer.site h4{margin:0 0 12px;font-size:11px;color:var(--faint);font-weight:600;text-transform:uppercase;letter-spacing:.06em}
footer.site a{display:block;padding:4px 0;color:var(--gray)}footer.site a:hover{color:var(--ink)}
footer.site .brand .wm{font-family:var(--mmt-wm-font,var(--sans));font-size:var(--mmt-wm-md,19px);font-weight:var(--mmt-wm-fw,800);letter-spacing:var(--mmt-wm-ls,-.035em)}footer.site .brand p{margin-top:10px;color:var(--faint);font-size:12px;line-height:1.6}
footer.site .legal{grid-column:1/-1;margin-top:16px;padding-top:16px;border-top:1px solid var(--line);color:var(--faint);font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
.hero{padding:clamp(48px,9vh,100px) var(--gut) 0;text-align:center;display:flex;flex-direction:column;align-items:center}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--gray);display:inline-flex;gap:8px;align-items:center}
.eyebrow .dot{width:6px;height:6px;border-radius:99px;background:var(--ok)}
.hero h1{margin-top:20px;font-size:clamp(38px,6.5vw,84px);font-weight:700;letter-spacing:-.04em;line-height:1;max-width:15ch}
.hero .sub{margin-top:20px;font-size:clamp(16px,1.7vw,20px);color:var(--gray);max-width:48ch;line-height:1.6}
.hero .btns{margin-top:28px;display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.hero .micro{margin-top:14px;font-size:13px;color:var(--faint)}
/* ---- full-bleed rolling visual hero (placeholder) ---- */
.vhero{position:relative;width:100vw;margin-left:calc(50% - 50vw);height:min(84vh,780px);min-height:520px;overflow:hidden;background:#0b0c0e;color:#fff;display:flex}
.vslides{position:absolute;inset:0;z-index:0}
.vslide{position:absolute;inset:0;opacity:0;transition:opacity 1.2s var(--ease)}
.vslide.on{opacity:1}
.vslide img{width:100%;height:100%;object-fit:cover;transform:scale(1.05);transition:transform 8s linear}
.vslide.on img{transform:scale(1.12)}
.vover{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(180deg,rgba(11,12,14,.55),rgba(11,12,14,.12) 34%,rgba(11,12,14,.2) 56%,rgba(11,12,14,.86))}
.vph{position:absolute;top:16px;right:max(20px,calc((100vw - 1200px)/2));z-index:5;display:flex;align-items:center;gap:7px;font-family:var(--mono);font-size:11px;letter-spacing:.03em;color:#e2e6ee;background:rgba(11,12,14,.5);border:1px dashed rgba(255,255,255,.3);border-radius:20px;padding:6px 12px}
.vph i{width:7px;height:7px;border-radius:2px;background:#7fb0ff}
.vcontent{position:relative;z-index:3;align-self:center;width:100%;max-width:1200px;margin:0 auto;padding:0 var(--gut)}
.vcontent .eyebrow{color:rgba(255,255,255,.82)}
.vhero h1{margin-top:16px;font-size:clamp(40px,6.4vw,84px);font-weight:800;letter-spacing:-.04em;line-height:1;max-width:15ch;text-shadow:0 2px 40px rgba(0,0,0,.4)}
.vhero .vsub{margin-top:18px;font-size:clamp(16px,1.7vw,20px);color:rgba(255,255,255,.86);max-width:40ch;line-height:1.6}
.vhero .btns{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}
.btn.light{background:#fff;color:var(--ink)}
.btn.glass{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.28)}
.vfoot{position:absolute;left:50%;transform:translateX(-50%);bottom:0;width:100%;max-width:1200px;z-index:4;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;padding:0 var(--gut) clamp(18px,4vh,38px)}
.vcap{position:relative;height:50px;flex:1}
.vcap .c{position:absolute;left:0;bottom:0;opacity:0;transform:translateY(6px);transition:opacity .6s,transform .6s}
.vcap .c.on{opacity:1;transform:none}
.vcap .tool{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:700}
.vcap .tool::before{content:"";width:8px;height:8px;border-radius:99px;background:#7fb0ff;box-shadow:0 0 12px #7fb0ff}
.vcap .line{margin-top:5px;color:rgba(255,255,255,.72);font-size:13.5px}
.vdots{display:flex;gap:8px;flex:none}
.vdots button{width:26px;height:4px;border-radius:3px;border:none;padding:0;cursor:pointer;background:rgba(255,255,255,.3);overflow:hidden;position:relative}
.vdots button .f{position:absolute;inset:0;width:0;background:#fff}
.vdots button.on .f{animation:vprog var(--vd,5500ms) linear forwards}
@keyframes vprog{to{width:100%}}
@media(max-width:640px){.vfoot{flex-direction:column;align-items:flex-start;gap:10px}.vcap{width:100%;height:46px}}
.demo-wrap{width:100%;max-width:980px;margin:52px auto 0;padding:0 20px}
.frame{border:1px solid var(--line);border-radius:16px 16px 0 0;overflow:hidden;background:#fff;box-shadow:0 40px 90px -40px rgba(11,12,20,.3);border-bottom:none}
.frame .bar{display:flex;align-items:center;gap:8px;padding:11px 15px;background:var(--soft);border-bottom:1px solid var(--line)}
.frame .bar i{width:11px;height:11px;border-radius:99px;background:var(--soft2)}
.frame .bar .url{flex:1;margin-left:8px;height:22px;border-radius:6px;background:#fff;border:1px solid var(--line);font-family:var(--mono);font-size:11px;color:var(--faint);display:flex;align-items:center;padding:0 10px}
.frame .bar .pill{font-family:var(--mono);font-size:10px;color:#fff;background:var(--ink);padding:3px 9px;border-radius:99px}
.frame .stage{background:#fff;padding:26px;min-height:320px;display:flex;align-items:center;justify-content:center}
.ig{position:relative;width:min(100%,400px);aspect-ratio:1}
.ig .tile{position:absolute;width:31.5%;aspect-ratio:1;border-radius:12px;overflow:hidden;transition:left .95s var(--ease),top .95s var(--ease);box-shadow:0 8px 22px -12px rgba(0,0,0,.3)}
.ig .tile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ig .tile .lk{position:absolute;left:7px;bottom:7px;z-index:2;font-family:var(--mono);font-size:11px;font-weight:700;color:#fff;background:rgba(0,0,0,.55);backdrop-filter:blur(4px);padding:3px 8px;border-radius:99px}
.ig .tile .rk{position:absolute;right:7px;top:7px;z-index:2;width:22px;height:22px;border-radius:99px;background:var(--ig);color:#fff;font-family:var(--mono);font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.5);transition:.4s}
.ig.sorted .tile .rk{opacity:1;transform:scale(1)}
.cat-head{max-width:1200px;margin:0 auto clamp(22px,3.5vw,40px);display:flex;align-items:baseline;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line);padding-bottom:16px}
.cat-head .l{display:flex;align-items:baseline;gap:14px}
.cat-head h2{font-size:clamp(22px,2.6vw,32px);font-weight:700;letter-spacing:-.02em}
.cat-head .en{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.cat-head .cnt{font-family:var(--mono);font-size:12px;color:var(--gray)}
.cat-head .new{font-family:var(--mono);font-size:11px;font-weight:700;color:#fff;background:var(--ok);padding:3px 9px;border-radius:99px}
.banners{max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:clamp(16px,2.2vw,26px)}
.banner{position:relative;border-radius:26px;overflow:hidden;padding:clamp(28px,4.2vw,60px);min-height:clamp(340px,40vw,480px);display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center;background:var(--soft)}
.banner.dark{background:#0b0c0e;color:#fff}
.banner.tint{background:linear-gradient(135deg,#eef3ff,#f6f8fc)}
.banner.rev .b-txt{order:2}
@media(max-width:820px){.banner{grid-template-columns:1fr;min-height:0;gap:22px}.banner.rev .b-txt{order:0}}
.b-txt .tag{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;opacity:.6;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.banner.dark .free{background:#fff;color:#0b0c0e}
.b-txt h3{margin-top:16px;font-size:clamp(28px,4.2vw,58px);font-weight:700;letter-spacing:-.035em;line-height:1.02}
.b-txt .d{margin-top:16px;font-size:clamp(15px,1.5vw,18px);line-height:1.55;opacity:.72;max-width:36ch}
.b-txt .act{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}
.banner.dark .btn:not(.ghost):not(.drag){background:#fff;color:#0b0c0e}
.banner.dark .btn.ghost{color:#fff;border-color:rgba(255,255,255,.3)}
.b-vis{position:relative;height:100%;min-height:220px;border-radius:16px;overflow:hidden;display:flex;align-items:center;justify-content:center;background:#fff;box-shadow:0 30px 60px -34px rgba(11,12,20,.35)}
.banner.dark .b-vis{background:#131418}
.b-vis>img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.reveal{opacity:0;transform:translateY(28px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.reveal.in{opacity:1;transform:none}
.kbd{font-family:var(--mono);font-size:12px;background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:2px 7px}
.banner.dark .kbd{background:#1a1c20;border-color:#2a2c31}
.herm{width:100%;padding:24px;display:flex;flex-direction:column;align-items:center;gap:18px}
.herm .field{width:100%;max-width:320px;border:1px solid var(--line);border-radius:12px;padding:14px 16px;font-size:15px;min-height:74px;background:#fff}
.banner.dark .herm .field{background:#0b0c0e;border-color:#2a2c31;color:#fff}
.herm .cur{display:inline-block;width:2px;height:1em;background:currentColor;vertical-align:-2px;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.herm .mic{width:52px;height:52px;border-radius:99px;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px;position:relative}
.banner.dark .herm .mic{background:#fff;color:#0b0c0e}
.herm .mic::after{content:"";position:absolute;inset:-7px;border-radius:99px;border:2px solid currentColor;opacity:.4;animation:ring 1.6s var(--ease) infinite}
@keyframes ring{0%{transform:scale(1);opacity:.5}100%{transform:scale(1.5);opacity:0}}
.ytm{width:100%;padding:20px;display:flex;flex-direction:column;gap:8px}
.ytrow{display:flex;gap:11px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px}
.ytrow .rk{font-family:var(--mono);font-weight:800;font-size:13px;color:var(--yt);width:26px;text-align:center}
.ytrow .th{width:74px;height:44px;border-radius:6px;overflow:hidden;flex:0 0 74px}
.ytrow .th img{width:100%;height:100%;object-fit:cover;position:static}
.ytrow .mt b{font-size:12.5px;font-weight:600;display:block}.ytrow .mt span{font-size:11px;color:var(--gray);font-family:var(--mono)}
.qpm{width:100%;padding:22px}
.qpm .card{display:flex;gap:12px}.qpm .card .im{width:80px;height:80px;border-radius:10px;overflow:hidden;flex:0 0 80px}
.qpm .card .im img{width:100%;height:100%;object-fit:cover;position:static}
.qpm .nm{font-size:13px;font-weight:600;line-height:1.4}.qpm .pr{font-size:15px;font-weight:800;margin-top:4px}
.qpm .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.qpm .chip2{font-size:12px;font-weight:600;padding:5px 10px;border-radius:6px}
.qpm .chip2.ok{background:#eafaf1;color:#0b8f4e;border:1px solid #c7efd8}
.qpm .chip2.out{background:var(--soft);color:var(--faint);text-decoration:line-through;border:1px solid var(--line)}
.phead{padding:clamp(40px,7vh,76px) var(--gut) 0}
.phead h1{margin-top:14px;font-size:clamp(32px,5vw,56px);font-weight:700;letter-spacing:-.03em}
.phead p{margin-top:16px;font-size:clamp(15px,1.5vw,18px);color:var(--gray);max-width:52ch;line-height:1.55}
.filters{position:sticky;top:56px;z-index:30;background:rgba(255,255,255,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);margin-top:clamp(26px,3.5vw,44px)}
.filters .row{padding:14px var(--gut);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.chip{font-size:14px;font-weight:600;color:var(--gray);background:var(--soft);border:1px solid transparent;border-radius:99px;padding:8px 15px;cursor:pointer;display:inline-flex;gap:7px;align-items:center;transition:all .18s;font-family:inherit}
.chip:hover{color:var(--ink)}.chip.on{background:var(--ink);color:#fff}
.chip .n{font-family:var(--mono);font-size:11px;opacity:.6}
.pgrid{padding:clamp(26px,4vw,44px) var(--gut) 0;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.6vw,22px);max-width:calc(1200px + 2*var(--gut));margin:0 auto}
@media(max-width:900px){.pgrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.pgrid{grid-template-columns:1fr}}
.pcard{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:#fff;display:flex;flex-direction:column;transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.pcard:hover{transform:translateY(-4px);box-shadow:0 24px 50px -30px rgba(11,12,20,.3)}
.pcard .thumb{aspect-ratio:16/10;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;background:var(--soft)}
.pcard .thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pcard .thumb .ic{position:relative;z-index:2;width:56px;height:56px;border-radius:15px;color:#fff;font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px -8px rgba(0,0,0,.4)}
.pcard .thumb .badge{position:absolute;z-index:3;left:12px;top:12px;font-family:var(--mono);font-size:10px;font-weight:700;color:#fff;background:rgba(0,0,0,.55);backdrop-filter:blur(4px);padding:4px 9px;border-radius:99px}
.pcard .thumb .newb{position:absolute;z-index:3;right:12px;top:12px;font-family:var(--mono);font-size:10px;font-weight:700;color:#fff;background:var(--ok);padding:4px 9px;border-radius:99px}
.pcard .bd{padding:18px 18px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.pcard .top{display:flex;align-items:center;gap:8px}
.pcard .med{font-family:var(--mono);font-size:11px;color:var(--faint)}
.pcard h3{font-size:18px;font-weight:700;letter-spacing:-.01em}
.pcard .d{font-size:13.5px;color:var(--gray);line-height:1.5}
.pcard .foot{margin-top:auto;padding-top:12px;display:flex;align-items:center;justify-content:space-between}
.pcard .tags{display:flex;gap:6px;flex-wrap:wrap}
.pcard .tagx{font-size:11px;color:var(--gray);background:var(--soft);border-radius:6px;padding:3px 8px}
.pcard .go{font-size:13px;font-weight:700}
.dwrap{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,40px)}
.dhead{padding:clamp(36px,6vh,72px) 0 clamp(24px,4vh,42px);display:grid;grid-template-columns:1.1fr 1fr;gap:36px;align-items:end}
.dhead .back{grid-column:1/-1;font-size:13px;color:var(--gray);margin-bottom:22px;width:max-content}
.dhead .back:hover{color:var(--ink)}
.dhead h1{margin-top:14px;font-size:clamp(38px,6vw,74px);font-weight:800;letter-spacing:-.03em;line-height:1}
.dhead .lead{font-size:clamp(16px,1.5vw,19px);color:var(--gray);line-height:1.65;padding-bottom:6px}
.dhead .lead b{color:var(--ink)}
@media(max-width:860px){.dhead{grid-template-columns:1fr;gap:16px;align-items:start}}
.dbody{display:grid;grid-template-columns:1fr 350px;gap:clamp(36px,5vw,72px);padding:clamp(30px,5vh,56px) 0 0;align-items:start}
@media(max-width:960px){.dbody{grid-template-columns:1fr}}
.feature{padding-bottom:clamp(44px,7vh,80px)}
.feature .fk{font-family:var(--mono);font-size:12px;color:var(--gray);letter-spacing:.06em;text-transform:uppercase}
.feature h2{margin-top:12px;font-size:clamp(24px,3vw,36px);font-weight:700;letter-spacing:-.02em;line-height:1.12}
.feature p{margin-top:12px;font-size:16px;color:var(--gray);line-height:1.65;max-width:48ch}
.howto{border-top:1px solid var(--line);padding-top:30px}
.howto h2{font-size:20px;font-weight:700}
.steps{margin-top:20px;display:flex;flex-direction:column;gap:16px}
.step{display:flex;gap:14px}
.step .n{font-family:var(--mono);font-weight:700;font-size:14px;flex:0 0 26px}
.step b{font-size:15px;font-weight:600}.step p{margin-top:3px;font-size:14px;color:var(--gray)}
.buy{position:sticky;top:84px;border:1px solid var(--line);border-radius:16px;padding:24px;background:#fff;box-shadow:0 20px 50px -30px rgba(12,14,20,.22)}
.buy .price{margin-top:12px;font-size:30px;font-weight:800;letter-spacing:-.02em}
.buy .price small{font-size:13px;font-weight:500;color:var(--gray)}
.buy .cta-main{width:100%;margin-top:16px;justify-content:center;font-size:15px;padding:14px;text-align:center}
.buy .risk{margin-top:10px;font-size:12px;color:var(--faint);text-align:center;line-height:1.5}
.buy .spec{margin-top:18px;border-top:1px solid var(--line)}
.buy .spec .r{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);font-size:13px}
.buy .spec .r span:first-child{color:var(--gray)}
.buy .spec .r span:last-child{text-align:right;font-weight:500}
.buy .also{margin-top:18px}
.buy .also .lbl{font-family:var(--mono);font-size:11px;color:var(--gray);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}
.buy .also a{display:flex;align-items:center;gap:10px;padding:8px 0;font-size:13px}
.buy .also a:hover{color:var(--gray)}
.buy .also .ic{width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:13px;flex:0 0 28px}
.related{padding:clamp(50px,8vh,90px) 0 0}
.related h2{font-size:20px;font-weight:700;margin-bottom:20px}
.rgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:760px){.rgrid{grid-template-columns:1fr}}
.rcard{border:1px solid var(--line);border-radius:14px;padding:18px;transition:box-shadow .2s,transform .2s;display:block}
.rcard:hover{box-shadow:0 16px 40px -24px rgba(12,14,20,.25);transform:translateY(-2px)}
.rcard .ic{width:36px;height:36px;border-radius:10px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800}
.rcard h3{margin-top:12px;font-size:16px;font-weight:700}
.rcard p{margin-top:6px;font-size:13px;color:var(--gray)}
.jhead{padding:clamp(40px,7vh,76px) var(--gut) 0}
.jhead h1{margin-top:14px;font-size:clamp(32px,5vw,56px);font-weight:700;letter-spacing:-.03em}
.jhead p{margin-top:14px;font-size:clamp(15px,1.5vw,18px);color:var(--gray);max-width:52ch;line-height:1.55}
.jfeat{padding:clamp(30px,5vw,50px) var(--gut) 0;max-width:calc(1200px + 2*var(--gut));margin:0 auto}
.jfeat a{display:grid;grid-template-columns:1.15fr 1fr;gap:clamp(24px,4vw,52px);align-items:center}
@media(max-width:820px){.jfeat a{grid-template-columns:1fr}}
.jfeat .im{aspect-ratio:16/11;border-radius:16px;overflow:hidden;background:var(--soft)}
.jfeat .im img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.jfeat a:hover .im img{transform:scale(1.03)}
.jfeat h2{margin-top:14px;font-size:clamp(24px,3vw,38px);font-weight:700;letter-spacing:-.025em;line-height:1.18}
.jfeat .ex{margin-top:14px;font-size:16px;color:var(--gray);line-height:1.6;max-width:40ch}
.jfeat .meta{margin-top:16px;font-size:13px;color:var(--faint);font-family:var(--mono)}
.jlist{padding:clamp(40px,6vw,64px) var(--gut) 0;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(20px,2.4vw,32px);max-width:calc(1200px + 2*var(--gut));margin:0 auto}
@media(max-width:900px){.jlist{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.jlist{grid-template-columns:1fr}}
.jpost .im{aspect-ratio:16/11;border-radius:12px;overflow:hidden;background:var(--soft);position:relative}
.jpost .im img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.jpost:hover .im img{transform:scale(1.04)}
.jpost .catb{position:absolute;left:12px;top:12px;z-index:2;font-family:var(--mono);font-size:10px;font-weight:700;color:#fff;background:var(--pt);padding:4px 9px;border-radius:99px}
.jpost h3{margin-top:14px;font-size:18px;font-weight:700;line-height:1.35}
.jpost .ex{margin-top:8px;font-size:14px;color:var(--gray);line-height:1.5}
.jpost .meta{margin-top:10px;font-size:12px;color:var(--faint);font-family:var(--mono)}
.post-top{max-width:calc(760px + 2*clamp(18px,4vw,40px));margin-inline:auto;padding:clamp(30px,5vh,56px) clamp(18px,4vw,40px) 0}
.post-top h1{margin-top:16px;font-size:clamp(28px,4vw,46px);font-weight:800;letter-spacing:-.03em;line-height:1.22;text-wrap:balance}
.post-top .sub{margin-top:16px;font-size:clamp(16px,1.4vw,18px);color:var(--gray);line-height:1.6}
.post-grid{display:grid;grid-template-columns:1fr min(760px,100%) 1fr;column-gap:clamp(20px,3vw,52px);max-width:1480px;margin:clamp(22px,3vw,32px) auto 0;padding-inline:clamp(18px,4vw,40px);align-items:start}
.post-toc{grid-column:1;justify-self:start}
.post-main{grid-column:2;min-width:0}
.post-aside{grid-column:3;justify-self:end}
@media(max-width:1080px){.post-grid{grid-template-columns:min(760px,100%);justify-content:center}.post-toc,.post-aside{display:none}.post-main{grid-column:1}}
.post-toc nav{position:sticky;top:80px;width:190px}
.rail-title{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--faint);letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px}
.post-toc ul{list-style:none;padding:0;margin:0;display:grid;gap:9px;border-left:1px solid var(--line)}
.post-toc li a{display:block;padding-left:14px;color:var(--gray);font-size:13px;line-height:1.5;border-left:2px solid transparent;margin-left:-1px}
.post-toc li a:hover,.post-toc li a.on{color:var(--ink);border-color:var(--pt)}
.post-aside .rail{position:sticky;top:80px;width:240px}
.rail-posts{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px}
.rail-posts a{display:flex;gap:11px;align-items:center}
.rail-posts .th{width:62px;height:44px;border-radius:8px;overflow:hidden;flex:0 0 62px;background:var(--soft)}
.rail-posts .th img{width:100%;height:100%;object-fit:cover}
.rail-posts .t{font-size:13px;font-weight:600;line-height:1.35}
.rail-posts a:hover .t{color:var(--pt)}
.post-meta{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:22px}
.byline{display:flex;align-items:center;gap:11px}
.byline .av{width:40px;height:40px;border-radius:99px;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800}
.byline b{font-size:14px;display:block}.byline time{font-size:12px;color:var(--faint);font-family:var(--mono)}
.share{display:flex;gap:8px}
.share a,.share button{width:38px;height:38px;border-radius:99px;border:1px solid var(--line);display:grid;place-items:center;color:var(--gray);background:#fff;cursor:pointer;transition:all .14s;font-size:13px;font-weight:700}
.share a:hover,.share button:hover{background:var(--ink);color:#fff;border-color:var(--ink)}
.post-cover{margin:0 0 clamp(22px,3vw,32px)}
.post-cover img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:16px;border:1px solid var(--line)}
.prose{font-size:17px;line-height:1.9;color:var(--ink2)}
.prose h2{font-size:clamp(21px,2.3vw,27px);font-weight:800;letter-spacing:-.02em;margin:38px 0 14px;line-height:1.3;color:var(--ink);scroll-margin-top:80px}
.prose p{margin:16px 0}.prose b{color:var(--ink)}
.prose a{color:var(--pt);text-decoration:underline;text-underline-offset:2px}
.prose img{width:100%;border-radius:12px;border:1px solid var(--line);margin:24px 0}
.prose blockquote{margin:28px 0;padding:6px 0 6px 22px;border-left:3px solid var(--pt);font-size:20px;font-weight:600;line-height:1.5;color:var(--ink)}
.prose ul{margin:16px 0;padding-left:22px}.prose li{margin:8px 0}
.inline-cta{margin:32px 0;border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:flex;align-items:center;gap:14px;background:var(--soft)}
.inline-cta .ic{width:42px;height:42px;border-radius:11px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;flex:0 0 42px}
.inline-cta .t b{display:block;font-size:15px;color:var(--ink)}.inline-cta .t span{font-size:13px;color:var(--gray)}
.inline-cta .btn{margin-left:auto;font-size:13px;padding:9px 15px;white-space:nowrap}
.comments{margin-top:52px;padding-top:26px;border-top:1px solid var(--line)}
.comments h3{font-size:16px;font-weight:700;margin-bottom:14px}
.cbox{border:1px solid var(--line);border-radius:12px;padding:14px 14px 10px;background:#fff}
.cbox textarea{width:100%;border:none;outline:none;resize:vertical;font:inherit;font-size:14px;line-height:1.6;min-height:48px;background:transparent}
.cbox .crow{display:flex;gap:8px;justify-content:flex-end;align-items:center;margin-top:8px;border-top:1px solid var(--line);padding-top:10px}
.cbox .crow input{margin-right:auto;border:1px solid var(--line);border-radius:8px;padding:7px 11px;font:inherit;font-size:13px;width:150px;outline:none}
.cbox .crow button{background:var(--ink);color:#fff;border:none;font-size:13px;font-weight:600;padding:8px 18px;border-radius:8px;cursor:pointer}
.cdone{border:1px solid var(--line);border-radius:12px;padding:15px 18px;background:var(--soft);font-size:13.5px;color:var(--gray);line-height:1.6;display:flex;gap:10px;align-items:flex-start}
.cdone b{color:var(--ink)}
.lab-hero{padding:clamp(48px,8vh,90px) var(--gut) clamp(20px,3vh,34px);text-align:center}
.lab-hero h1{margin-top:16px;font-size:clamp(30px,4.6vw,52px);font-weight:800;letter-spacing:-.03em;line-height:1.12}
.lab-hero .lead{margin-top:16px;font-size:clamp(15px,1.6vw,18px);color:var(--gray);line-height:1.65;max-width:46ch;margin-left:auto;margin-right:auto}
.lab-wrap{max-width:820px;margin:0 auto;padding:0 clamp(20px,4vw,40px)}
.submitb{border:1px solid var(--line);border-radius:16px;padding:16px;background:#fff;box-shadow:0 20px 50px -34px rgba(11,12,20,.22)}
.submitb textarea{width:100%;border:none;outline:none;resize:vertical;font:inherit;font-size:15px;line-height:1.6;min-height:58px;background:transparent}
.submitb .row{display:flex;justify-content:space-between;align-items:center;gap:8px;border-top:1px solid var(--line);padding-top:12px;margin-top:8px}
.submitb .hint{font-size:12px;color:var(--faint)}
.ldone{border:1px solid var(--ok);background:#eafaf1;border-radius:16px;padding:16px 18px;font-size:14px;color:#0b8f4e;display:none;gap:10px;align-items:flex-start}
.ldone.show{display:flex}.ldone b{color:#076b3a}
.board{margin-top:clamp(40px,6vw,60px)}
.board-head{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:12px}
.board-head h2{font-size:17px;font-weight:700}
.board-head span{font-size:12px;color:var(--faint);font-family:var(--mono)}
.litem{display:flex;gap:15px;padding:16px 2px;border-bottom:1px solid var(--line);align-items:flex-start}
.vote{flex:0 0 54px;display:flex;flex-direction:column;align-items:center;gap:2px;border:1px solid var(--line);border-radius:12px;padding:8px 0;cursor:pointer;user-select:none;transition:.15s;background:#fff;font-family:inherit}
.vote:hover{border-color:var(--ink)}.vote.on{border-color:var(--pt);background:#fff4f1}
.vote .ar{font-size:13px;color:var(--gray)}.vote.on .ar{color:var(--pt)}
.vote .n{font-size:15px;font-weight:800}
.litem h3{font-size:15.5px;font-weight:600;line-height:1.4}
.litem p{font-size:13px;color:var(--gray);margin-top:4px}
.litem .tags{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap}
.litem .tagx{font-size:11px;color:var(--gray);background:var(--soft);border-radius:99px;padding:3px 10px}
.litem .tagx.building{color:#fff;background:var(--ok)}
.hsteps{margin:clamp(46px,7vw,70px) 0 0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:720px){.hsteps{grid-template-columns:1fr 1fr}}
.hstep{border-top:2px solid var(--ink);padding-top:14px}
.hstep .n{font-family:var(--mono);font-size:12px;font-weight:700}
.hstep b{display:block;margin-top:8px;font-size:14px}.hstep p{font-size:12.5px;color:var(--gray);margin-top:5px;line-height:1.5}
.note-c{font-size:13px;color:var(--faint);text-align:center;margin-top:clamp(40px,6vw,56px);line-height:1.6}
.awrap{max-width:880px;margin:0 auto;padding:0 clamp(20px,5vw,40px)}
.ahero{padding:clamp(48px,9vh,100px) 0 clamp(26px,4vh,50px)}
.ahero h1{margin-top:16px;font-size:clamp(32px,5.4vw,60px);font-weight:800;letter-spacing:-.03em;line-height:1.06}
.ahero .lead{margin-top:20px;font-size:clamp(16px,1.7vw,20px);color:var(--gray);line-height:1.7;max-width:44ch}
.avat{display:flex;align-items:center;gap:14px;margin-top:30px}
.avat .a{width:54px;height:54px;border-radius:99px;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;font-size:21px;font-weight:800}
.avat b{font-size:15px;display:block}.avat span{font-size:13px;color:var(--faint);font-family:var(--mono)}
.split3{text-align:center;color:var(--faint);letter-spacing:.5em;margin:clamp(36px,5vw,56px) 0}
.say{max-width:620px;margin:0 auto;font-size:clamp(17px,1.9vw,22px);line-height:1.7;color:#26303f}
.say b{color:var(--ink)}
.stats3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:clamp(44px,7vw,76px) 0}
@media(max-width:640px){.stats3{grid-template-columns:1fr}}
.stat3{border:1px solid var(--line);border-radius:16px;padding:22px;text-align:center}
.stat3 b{font-size:30px;font-weight:800;letter-spacing:-.03em;color:var(--pt);display:block}
.stat3 span{font-size:13px;color:var(--gray);margin-top:6px;display:block}
.tl{border-top:1px solid var(--line);padding-top:32px}
.tl h2{font-size:19px;font-weight:700;margin-bottom:18px}
.trow{display:flex;gap:22px;padding:16px 0;border-bottom:1px solid var(--line)}
.trow .yr{font-family:var(--mono);font-size:13px;color:var(--faint);flex:0 0 56px}
.trow b{font-size:15.5px;font-weight:700;display:block}.trow p{font-size:14px;color:var(--gray);margin-top:4px}
.cta-dark{margin:clamp(44px,7vw,76px) 0 0;background:var(--ink);color:#fff;border-radius:20px;padding:clamp(32px,4.5vw,54px);text-align:center}
.cta-dark h2{font-size:clamp(22px,3.2vw,36px);font-weight:700;letter-spacing:-.02em}
.cta-dark p{margin-top:12px;color:#aeb4bd;font-size:15px}
.cta-dark .btns{margin-top:24px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.cta-dark a{background:#fff;color:var(--ink);font-size:14px;font-weight:600;padding:12px 22px;border-radius:99px}
.cta-dark a.ghost{background:none;color:#fff;border:1px solid rgba(255,255,255,.3)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.reveal{opacity:1;transform:none}}

/* ============================================================
   리뉴얼 2026-07 — 파는 것이 주인공, 무료 도구는 유입 깔때기
   팔레트: 흰 + 블루(#3182f6) + 잉크
   ============================================================ */
:root{--rn-blue:#3182f6}
/* ============================================================
   랜딩 = vinylc.com/ko/goods 구조 그대로 (실측)
   컨테이너 1245px · 3열 345px gap 105 · 대형 풀폭 1245
   제목 24px w700 ls-1px #202020 · 라벨 19px w700 #909090
   ============================================================ */
.vc{--vc-w:1245px;--vc-col:345px;--vc-gap:105px}
.vc-head{max-width:var(--vc-w);margin:0 auto;padding:calc(56px + 120px) 24px 0}
.vc-head h1{font-size:clamp(28px,3.2vw,44px);font-weight:700;letter-spacing:-.03em;line-height:1.35;color:#202020}
.vc-head p{margin-top:18px;font-size:17px;color:#909090;line-height:1.75;max-width:52ch}

/* 소팅 */
.vc-sort{max-width:var(--vc-w);margin:56px auto 0;padding:0 24px;display:flex;gap:26px;flex-wrap:wrap;
  border-bottom:1px solid #EAEAEA;padding-bottom:16px}
.vc-sort button{background:none;border:0;padding:0 0 16px;margin-bottom:-17px;cursor:pointer;
  font-family:inherit;font-size:16px;font-weight:700;color:#B4B4B4;letter-spacing:-.02em;
  border-bottom:2px solid transparent;transition:color .2s}
.vc-sort button:hover{color:#5A5A5A}
.vc-sort button[aria-pressed="true"]{color:#202020;border-bottom-color:#202020}

/* 그리드 */
.vc-grid{max-width:var(--vc-w);margin:0 auto;padding:100px 24px 0;
  display:grid;grid-template-columns:repeat(3,1fr);gap:117px var(--vc-gap)}
.vc-item{grid-column:span 1}
.vc-item.big{grid-column:1 / -1}
.vc-item[hidden]{display:none}


.vc-item a{display:block}
.vc-thumb{width:100%;aspect-ratio:1;overflow:hidden;background:#F4F4F4}
.vc-item.big .vc-thumb{aspect-ratio:1245/795}
.vc-thumb img{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .7s cubic-bezier(.16,1,.3,1)}
.vc-item a:hover .vc-thumb img{transform:scale(1.03)}

.vc-item h3{margin-top:34px;font-size:24px;font-weight:700;letter-spacing:-1px;line-height:1.5;color:#202020}
.vc-item.big h3{font-size:30px;max-width:22ch}
.vc-item .cat{margin-top:14px;font-size:19px;font-weight:700;color:#909090;letter-spacing:normal}
.vc-item a:hover h3{color:#5A5A5A}

.vc-empty{max-width:var(--vc-w);margin:80px auto;padding:0 24px;color:#909090;font-size:17px}

@media(max-width:1100px){
  .vc-grid{grid-template-columns:repeat(2,1fr);gap:80px 40px}
  .vc-item.big{grid-column:1 / -1}
}
@media(max-width:680px){
  .vc-grid{grid-template-columns:1fr;gap:64px;padding-top:56px}
  .vc-item h3,.vc-item.big h3{font-size:21px}
  .vc-item .cat{font-size:16px}
}

/* ============================================================
   제품 상세 = vinylc.com/ko/goods/{id} 구조 그대로 (실측)
   풀블리드 히어로(제목 54px 흰색) → 이미지 리듬 → CTA → Next
   ============================================================ */
.vd{--vd-w:1245px}
.vd-hero{position:relative;width:100vw;margin-left:calc(50% - 50vw);height:600px;overflow:hidden}
.vd-hero img{width:100%;height:100%;object-fit:cover;display:block}
.vd-hero::after{content:"";position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(0,0,0,.35) 0 30%,rgba(0,0,0,.1) 60%,rgba(0,0,0,.45) 100%)}
.vd-hero .cap{position:absolute;left:50%;transform:translateX(-50%);bottom:64px;z-index:2;
  width:100%;max-width:var(--vd-w);padding:0 24px}
.vd-hero .kick{font-size:19px;font-weight:500;color:rgba(255,255,255,.75);letter-spacing:normal}
.vd-hero h1{margin-top:14px;font-size:54px;font-weight:700;letter-spacing:-1px;line-height:1.25;color:#fff;max-width:20ch}

.vd-flow{max-width:var(--vd-w);margin:0 auto;padding:0 24px}
.vd-note{max-width:var(--vd-w);margin:0 auto;padding:96px 24px;text-align:center}
.vd-note p{font-size:16px;line-height:2;color:#5A5A5A;max-width:60ch;margin:0 auto}
.vd-note p+p{margin-top:0}

.vd-full{width:100vw;margin-left:calc(50% - 50vw);margin-top:100px}
.vd-full img{width:100%;height:auto;display:block}
.vd-wide{margin-top:100px}
.vd-wide img{width:100%;aspect-ratio:1245/779;object-fit:cover;display:block}
.vd-duo{margin-top:100px;display:grid;grid-template-columns:345px 795px;gap:105px;align-items:center}
.vd-duo.rev{grid-template-columns:795px 345px}
.vd-duo img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.vd-pair{margin-top:100px;display:grid;grid-template-columns:1fr 1fr;gap:105px}
/* 실제 도구 캡처(.sh)는 정사각 크롭을 하면 화면이 잘려 못 읽는다 — 가로형으로 둔다 */
.vd-duo.sh{grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.vd-duo.sh img{aspect-ratio:1500/1080;object-fit:contain;background:#0b0c0e;border-radius:14px}
.vd-wide.sh img{aspect-ratio:2560/900;object-fit:contain;background:#0b0c0e;border-radius:14px}
.vd-pair img{width:100%;aspect-ratio:1;object-fit:cover;display:block}

.vd-cta{max-width:var(--vd-w);margin:0 auto;padding:120px 24px;text-align:center}
.vd-cta .btn-buy{display:inline-flex;align-items:center;justify-content:center;
  min-width:280px;height:64px;padding:0 40px;background:#202020;color:#fff;
  font-size:21px;font-weight:700;letter-spacing:-.02em;border-radius:0;transition:background .2s}
.vd-cta .btn-buy:hover{background:#5A5A5A}
.vd-cta .hint{margin-top:20px;font-size:15px;color:#909090;line-height:1.7}
/* 도구 CTA — 그냥 흰 바닥에 점선 버튼 하나라 힘이 없었다(2026-09-01 대표 지적).
   따뜻한 띠 위에 카드를 올리고, 버튼을 키우고, 설치 조건을 칩으로 못박는다. */
.vd-cta.tool{max-width:none;width:100vw;margin-left:calc(50% - 50vw);padding:0}
.vd-cta.tool .wrap{max-width:var(--vd-w);margin:0 auto;padding:96px 24px 104px;text-align:center;
  background:linear-gradient(180deg,#fbf6f0 0%,#fdfbf8 62%,#fff 100%);
  border-top:1px solid rgba(0,0,0,.05)}
.vd-cta.tool .kick{font-size:13px;font-weight:700;letter-spacing:.04em;color:#b08968;text-transform:uppercase}
.vd-cta.tool h3{margin:14px 0 0;font-size:clamp(26px,3.4vw,38px);font-weight:700;letter-spacing:-.03em;color:#1b1b1d}
.vd-cta.tool .sub{margin:14px auto 0;max-width:44ch;font-size:16px;line-height:1.8;color:#6b6b70}
.vd-cta.tool .go{margin-top:34px;display:inline-flex}
.vd-cta.tool .btn.drag{padding:18px 34px;font-size:17px;border-radius:999px;border-width:2px;
  background:#fff;box-shadow:0 10px 30px -12px rgba(200,90,60,.45)}
.vd-cta.tool .btn.drag:hover{background:#fff8f4;opacity:1}
.vd-cta.tool .chips{margin-top:26px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.vd-cta.tool .chips span{font-size:13px;color:#7a7a80;background:rgba(0,0,0,.045);
  padding:7px 14px;border-radius:999px}
.vd-cta.tool .hint{margin-top:18px;font-size:14px;color:#9a9aa0}
@media(max-width:760px){.vd-cta.tool .wrap{padding:64px 20px 72px}}

.vd-next{position:relative;width:100vw;margin-left:calc(50% - 50vw);height:271px;overflow:hidden;display:block}
.vd-next img{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .8s cubic-bezier(.16,1,.3,1)}
.vd-next:hover img{transform:scale(1.04)}
.vd-next::after{content:"";position:absolute;inset:0;background:rgba(0,0,0,.42)}
.vd-next .cap{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;
  width:100%;max-width:var(--vd-w);padding:0 24px;text-align:center}
.vd-next .lbl{font-size:19px;font-weight:500;color:rgba(255,255,255,.72)}
.vd-next .ttl{margin-top:10px;font-size:24px;font-weight:500;color:#fff;letter-spacing:-.02em}

@media(max-width:1100px){
  .vd-duo,.vd-duo.rev{grid-template-columns:1fr;gap:40px}
  .vd-pair{gap:40px}
  .vd-hero{height:420px}
  .vd-hero h1{font-size:34px}
  .vd-full,.vd-wide,.vd-duo,.vd-pair{margin-top:64px}
  .vd-note{padding:64px 24px}
}

/* ---- 항시 떠 있는 설치 독 (풀스크린 이미지는 그대로 두고 아래에 고정) ---- */
body:has(.vd){padding-bottom:88px}
.vd-dock{position:fixed;left:0;right:0;bottom:0;z-index:90;
  background:rgba(255,255,255,.82);backdrop-filter:saturate(180%) blur(24px);
  -webkit-backdrop-filter:saturate(180%) blur(24px);
  border-top:1px solid rgba(0,0,0,.07)}
.vd-dock .bar{max-width:1245px;margin:0 auto;padding:15px 24px;
  display:flex;align-items:center;justify-content:space-between;gap:24px}
.vd-dock .id{min-width:0}
.vd-dock .id .n{font-size:16px;font-weight:700;letter-spacing:-.02em;color:#202020;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vd-dock .id .s{margin-top:3px;font-size:13.5px;color:#909090;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vd-dock .acts{display:flex;align-items:center;gap:10px;flex:none}
.vd-dock .how{background:none;border:0;cursor:pointer;font-family:inherit;
  font-size:14px;font-weight:600;color:#5A5A5A;letter-spacing:-.02em;
  display:inline-flex;align-items:center;gap:6px;padding:10px 4px;transition:color .2s}
.vd-dock .how:hover{color:#202020}
.vd-dock .how .car{display:inline-block;transition:transform .3s;font-size:11px}
.vd-dock .how[aria-expanded="true"] .car{transform:rotate(180deg)}
.vd-dock .go{display:inline-flex;align-items:center;justify-content:center;height:48px;padding:0 26px;
  background:#202020;color:#fff;font-size:15px;font-weight:700;letter-spacing:-.02em;
  white-space:nowrap;transition:background .2s}
.vd-dock .go:hover{background:#5A5A5A}

/* 설명서 — 열면 위로 펼쳐짐 */
.vd-guide{max-height:0;overflow:hidden;transition:max-height .42s cubic-bezier(.16,1,.3,1);
  border-bottom:1px solid rgba(0,0,0,.06)}
.vd-guide.open{max-height:280px}
.vd-guide .inner{max-width:1245px;margin:0 auto;padding:34px 24px 30px;
  display:grid;grid-template-columns:repeat(3,1fr);gap:44px}
.vd-guide .st .k{font-size:12px;font-weight:700;color:#C4C4C4;letter-spacing:.06em}
.vd-guide .st b{display:block;margin-top:9px;font-size:15.5px;font-weight:700;color:#202020;letter-spacing:-.02em}
.vd-guide .st p{margin-top:7px;font-size:13.5px;color:#909090;line-height:1.75}

@media(max-width:820px){
  body:has(.vd){padding-bottom:132px}
  .vd-dock .bar{flex-wrap:wrap;gap:12px;padding:13px 20px}
  .vd-dock .id{width:100%}
  .vd-dock .acts{width:100%;justify-content:space-between}
  .vd-dock .go{flex:1;justify-content:center}
  .vd-dock .dragwrap{flex:1}
  .vd-dock .dragwrap .go{width:100%}
  .vd-guide.open{max-height:520px}
  .vd-guide .inner{grid-template-columns:1fr;gap:22px;padding:26px 20px 24px}
}

/* ---- 소개 (vinylc 톤: 넉넉한 여백, 담백한 타이포) ---- */
.ab{max-width:1245px;margin:0 auto;padding:0 24px}
.ab-hero{padding:calc(56px + 140px) 0 0}
.ab-hero h1{font-size:clamp(30px,3.8vw,54px);font-weight:700;letter-spacing:-1px;line-height:1.35;color:#202020}
.ab-hero .lead{margin-top:26px;font-size:19px;line-height:1.9;color:#909090}
.ab-body{max-width:660px;padding:100px 0 0}
.ab-body p{font-size:17px;line-height:2.05;color:#5A5A5A}
.ab-body p+p{margin-top:38px}
.ab-body b{color:#202020;font-weight:700}
.ab-now{padding:130px 0 0}
.ab-kick{font-size:19px;font-weight:700;color:#909090}
.ab-now h2{margin-top:16px;font-size:clamp(24px,2.8vw,36px);font-weight:700;letter-spacing:-1px;line-height:1.5;color:#202020;max-width:24ch}
.ab-cards{margin-top:64px;display:grid;grid-template-columns:repeat(3,1fr);gap:60px}
.ab-card b{display:block;font-size:19px;font-weight:700;letter-spacing:-.02em;line-height:1.5;color:#202020}
.ab-card p{margin-top:16px;font-size:15.5px;line-height:1.9;color:#909090}
.ab-end{padding:150px 0 40px;border-top:1px solid #EAEAEA;margin-top:130px}
.ab-end p{font-size:clamp(21px,2.4vw,30px);font-weight:700;letter-spacing:-.03em;line-height:1.6;color:#202020}
.ab-btns{margin-top:44px;display:flex;gap:14px;flex-wrap:wrap}
.ab-go{display:inline-flex;align-items:center;height:60px;padding:0 34px;background:#202020;color:#fff;font-size:17px;font-weight:700;letter-spacing:-.02em;transition:background .2s}
.ab-go:hover{background:#5A5A5A}
.ab-ghost{display:inline-flex;align-items:center;height:60px;padding:0 30px;border:1px solid #DADADA;color:#5A5A5A;font-size:17px;font-weight:700;letter-spacing:-.02em;transition:border-color .2s,color .2s}
.ab-ghost:hover{border-color:#202020;color:#202020}
@media(max-width:900px){
  .ab-cards{grid-template-columns:1fr;gap:44px}
  .ab-body{padding-top:64px}
  .ab-now{padding-top:90px}
  .ab-end{padding-top:90px;margin-top:90px}
}

/* ============================================================
   블로그 + 소개 = anthropic.com 구조 (실측)
   글: 중앙 컬럼 640px · h1 52px w700 중앙 · 본문 17px/26px
   목록: 카테고리 · 날짜 · 제목 · 요약
   소개: 좌측 섹션 라벨 + 우측 2열 콘텐츠
   ============================================================ */
.an{max-width:1140px;margin:0 auto;padding:0 24px}

/* --- 블로그 목록 = openai.com/news 구조: 큰 제목 + 필터탭 + 3열 큰 썸네일 --- */
.an-lhead{padding:calc(56px + 90px) 0 0}
.an-lhead h1{font-size:clamp(38px,5vw,64px);font-weight:400;letter-spacing:-.02em;line-height:1.1;color:#191919}
.an-tabs{margin-top:34px;padding-bottom:22px;display:flex;gap:26px;flex-wrap:wrap;align-items:center;
  border-bottom:1px solid #E5E1D8}
.an-tabs button{background:none;border:0;padding:0;cursor:pointer;font-family:inherit;
  font-size:16px;color:#6B6862;letter-spacing:-.01em;transition:color .2s}
.an-tabs button:hover{color:#191919}
.an-tabs button[aria-pressed="true"]{color:#191919;font-weight:600}

.an-grid{margin-top:48px;padding-bottom:120px;display:grid;grid-template-columns:repeat(3,1fr);gap:52px 32px}
.an-card[hidden]{display:none}
.an-card a{display:block}
.an-card .th{position:relative;width:100%;aspect-ratio:1;border-radius:14px;overflow:hidden;
  transition:transform .6s cubic-bezier(.16,1,.3,1)}
.an-card a:hover .th{transform:scale(1.02)}
/* 추상 그라디언트 썸네일 — 글마다 다른 결. 스톡 사진보다 정직하다. */
.an-card .th::before{content:"";position:absolute;inset:-20%;filter:blur(28px)}
.an-card .th.vid{background:#0E0E0E}
.an-card .th.vid::before{display:none}
.an-card .th.vid img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.an-card .th.vid .play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;
  width:56px;height:56px;border-radius:50%;background:rgba(0,0,0,.62);backdrop-filter:blur(6px)}
.an-card .th.vid .play::after{content:"";position:absolute;left:52%;top:50%;transform:translate(-50%,-50%);
  border-left:15px solid #fff;border-top:9px solid transparent;border-bottom:9px solid transparent}
.an-lsub{margin-top:18px;font-size:16px;line-height:1.7;color:#6B6862;max-width:56ch}
.an-lsub a{color:#191919;text-decoration:underline;text-underline-offset:3px}
.th.g1{background:#DDE7F5}
.th.g1::before{background:
  radial-gradient(closest-side,#7BA7E8 0 40%,transparent 70%) 12% 22%/62% 62% no-repeat,
  radial-gradient(closest-side,#B9CFF0 0 45%,transparent 72%) 78% 30%/58% 58% no-repeat,
  radial-gradient(closest-side,#5C86C9 0 38%,transparent 68%) 55% 88%/70% 62% no-repeat}
.th.g2{background:#DCEDE4}
.th.g2::before{background:
  radial-gradient(closest-side,#6FC49B 0 40%,transparent 70%) 18% 78%/64% 62% no-repeat,
  radial-gradient(closest-side,#AFDCC6 0 45%,transparent 72%) 72% 24%/60% 60% no-repeat,
  radial-gradient(closest-side,#3E9E77 0 36%,transparent 66%) 88% 82%/56% 56% no-repeat}
.th.g3{background:#F1E6DC}
.th.g3::before{background:
  radial-gradient(closest-side,#E0A87A 0 40%,transparent 70%) 24% 26%/62% 62% no-repeat,
  radial-gradient(closest-side,#EFD2B8 0 46%,transparent 74%) 76% 70%/64% 64% no-repeat,
  radial-gradient(closest-side,#C8804F 0 34%,transparent 64%) 60% 14%/52% 52% no-repeat}
.an-card h3{margin-top:22px;font-size:21px;font-weight:600;letter-spacing:-.015em;line-height:1.35;color:#191919}
.an-card .m{margin-top:12px;display:flex;gap:12px;align-items:center;font-size:13.5px;color:#6B6862}
.an-card .cat{color:#191919}
.an-card p{margin-top:12px;font-size:15px;line-height:1.6;color:#6B6862}
.an-card a:hover h3{color:#C15F3C}
.an-empty{padding:80px 0 120px;color:#6B6862;font-size:16px}

/* --- 글 상세 --- */
.an-post{max-width:1140px;margin:0 auto;padding:calc(56px + 80px) 24px 0}
.an-post .top{text-align:center}
.an-post .cat{font-size:14px;font-weight:600;color:#191919}
.an-post h1{margin-top:16px;font-size:clamp(30px,3.8vw,52px);font-weight:700;letter-spacing:-.01em;
  line-height:1.1;color:#191919;max-width:20ch;margin-left:auto;margin-right:auto}
.an-post .date{margin-top:18px;font-size:14px;color:#6B6862}
.an-post .cover{position:relative;margin:44px auto 0;max-width:752px;aspect-ratio:752/367;
  border-radius:16px;overflow:hidden}
.an-body{max-width:640px;margin:0 auto;padding:56px 0 0}
.an-body p{font-size:17px;line-height:1.55;color:#2B2926}
.an-body p+p{margin-top:22px}
.an-body h2{margin:44px 0 14px;font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.4;color:#191919}
.an-body h3{margin:36px 0 12px;font-size:17px;font-weight:700;color:#191919}
.an-body ul{margin:18px 0;padding-left:22px}
.an-body li{font-size:17px;line-height:1.55;color:#2B2926;margin-bottom:12px}
.an-body li b{color:#191919}
.an-body blockquote{margin:28px 0;padding-left:20px;border-left:2px solid #E5E1D8;color:#4A4741;font-style:normal}
.an-body a{color:#C15F3C;text-decoration:underline;text-underline-offset:3px}
.an-body b{font-weight:700;color:#191919}
.an-share{max-width:640px;margin:64px auto 0;padding-top:28px;border-top:1px solid #E5E1D8;
  display:flex;gap:14px;font-size:14px;color:#6B6862}
.an-share a{color:#6B6862}
.an-share a:hover{color:#191919}

/* --- Related content --- */
.an-rel{max-width:1140px;margin:96px auto 0;padding:56px 24px 120px;border-top:1px solid #E5E1D8}
.an-rel h2{font-size:32px;font-weight:600;letter-spacing:-.01em;color:#191919}
.an-rel .g{margin-top:36px;display:grid;grid-template-columns:repeat(3,1fr);gap:36px}
.an-rel b{display:block;font-size:17px;font-weight:700;line-height:1.4;color:#191919}
.an-rel p{margin-top:10px;font-size:14.5px;line-height:1.6;color:#6B6862}
.an-rel .more{margin-top:12px;font-size:14px;font-weight:600;color:#191919}
.an-rel a:hover b{color:#C15F3C}

/* --- 소개 (anthropic /company: 좌 라벨 + 우 콘텐츠) --- */
.an-ahero{padding:calc(56px + 90px) 24px 0;text-align:center;max-width:900px;margin:0 auto}
.an-ahero h1{font-size:clamp(30px,3.9vw,52px);font-weight:700;letter-spacing:-.015em;line-height:1.18;color:#191919}
.an-ahero p{margin-top:20px;font-size:16px;line-height:1.65;color:#6B6862;max-width:52ch;margin-left:auto;margin-right:auto}
.an-ahero .btn{display:inline-flex;align-items:center;height:44px;padding:0 26px;margin-top:30px;
  border-radius:99px;background:#F2EDE4;color:#191919;font-size:15px;font-weight:600;transition:background .2s}
.an-ahero .btn:hover{background:#E5DED1}

.an-sec{max-width:1140px;margin:0 auto;padding:80px 24px 0}
.an-sec+.an-sec{border-top:1px solid #E5E1D8;margin-top:80px}
.an-row{display:grid;grid-template-columns:300px 1fr;gap:60px}
.an-lbl h2{font-size:26px;font-weight:700;letter-spacing:-.01em;line-height:1.3;color:#191919}
.an-lbl p{margin-top:14px;font-size:15px;line-height:1.65;color:#6B6862}
.an-two{display:grid;grid-template-columns:1fr 1fr;gap:36px 44px}
.an-two h3{font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.35;color:#191919}
.an-two p{margin-top:10px;font-size:15px;line-height:1.65;color:#6B6862}
.an-num{display:grid;grid-template-columns:1fr 1fr;gap:36px 44px}
.an-num .n{font-size:12.5px;font-weight:600;color:#A8A398}
.an-num h3{margin-top:8px;font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.35;color:#191919}
.an-num p{margin-top:10px;font-size:15px;line-height:1.65;color:#6B6862}
.an-cta{margin-top:100px;background:#191919;color:#fff;padding:96px 24px;text-align:center}
.an-cta h2{font-size:clamp(26px,3.2vw,40px);font-weight:700;letter-spacing:-.015em;line-height:1.3;color:#fff;
  max-width:20ch;margin:0 auto}
.an-cta .sub{margin:20px auto 0;font-size:16px;line-height:1.7;color:rgba(255,255,255,.72);max-width:46ch}
.an-cta-btns{margin-top:32px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.an-cta .btn{display:inline-flex;align-items:center;height:46px;padding:0 28px;
  border-radius:99px;background:#fff;color:#191919;font-size:15px;font-weight:600}
.an-cta .btn.ghost{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.35)}
.an-cta .btn.ghost:hover{border-color:#fff}
.an-cta .note{margin-top:26px;font-size:14px;color:rgba(255,255,255,.5)}
.an-cta .btn:hover{background:#E5DED1}

@media(max-width:900px){
  .an-grid,.an-rel .g,.an-two,.an-num{grid-template-columns:1fr}
  .an-row{grid-template-columns:1fr;gap:32px}
  .an-post h1{font-size:30px}
}

/* ---- 법적 페이지 (약관·개인정보·환불) + 푸터 사업자 표기 ---- */
.lg{max-width:760px;margin:0 auto;padding:0 24px}
.lg-head{padding:calc(56px + 90px) 0 0;border-bottom:1px solid #EAEAEA;padding-bottom:32px}
.lg-head h1{font-size:var(--mmt-fs-page-title,clamp(28px,3.4vw,40px));font-weight:var(--mmt-fw-page-title,700);letter-spacing:var(--mmt-ls-page-title,-.03em);color:#202020}
.lg-head .upd{margin-top:12px;font-size:14px;color:#909090}
.lg-body{padding:48px 0 120px}
.lg-body p{font-size:16px;line-height:1.85;color:#5A5A5A}
.lg-body p+p{margin-top:16px}
.lg-body b{color:#202020;font-weight:700}
.lg-body h2{margin:44px 0 14px;font-size:20px;font-weight:700;letter-spacing:-.02em;color:#202020}
.lg-body h3{margin:28px 0 10px;font-size:16.5px;font-weight:700;color:#202020}
.lg-body ul{margin:14px 0;padding-left:20px}
.lg-body li{font-size:16px;line-height:1.85;color:#5A5A5A;margin-bottom:10px}
.lg-body a{color:#202020;text-decoration:underline;text-underline-offset:3px}
.lg-biz{width:100%;border-collapse:collapse;margin-top:16px;font-size:15px}
.lg-biz th{text-align:left;padding:12px 16px 12px 0;color:#909090;font-weight:400;white-space:nowrap;
  border-bottom:1px solid #F0F0F0;vertical-align:top;width:150px}
.lg-biz td{padding:12px 0;color:#202020;border-bottom:1px solid #F0F0F0}

footer.site .biz{grid-column:1/-1;margin-top:36px;padding-top:24px;border-top:1px solid #EAEAEA;
  display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12.5px;color:#A8A8A8;line-height:1.8}


.vc-ic{display:grid;place-items:center;background:linear-gradient(150deg,color-mix(in srgb,var(--ic) 16%,#fff),color-mix(in srgb,var(--ic) 5%,#fff))}
.vc-ic span{font-size:clamp(52px,7vw,86px);color:var(--ic);line-height:1}
/* ── 카드 오버레이(맨 뒤에 둔다 — 위쪽 기존 .vc-item 규칙을 이겨야 한다) ── */
/* 카드 — 이미지 위 캡션 오버레이(레퍼런스: marieclairepicknview.com).
   이미지가 주인공이고 글자는 그 위에 얹는다. 아래로 흐르던 캡션보다 밀도·시원함이 산다. */
.vc-item>a{position:relative;display:block;border-radius:14px;overflow:hidden;background:var(--soft)}
.vc-item .vc-thumb{aspect-ratio:4/3;margin:0;overflow:hidden}
.vc-item .vc-thumb img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.vc-item>a:hover .vc-thumb img{transform:scale(1.045)}
.vc-item>a::after{content:"";position:absolute;inset:auto 0 0 0;height:78%;pointer-events:none;z-index:1;
background:linear-gradient(to top,rgba(10,12,16,.94) 0%,rgba(10,12,16,.78) 24%,rgba(10,12,16,.34) 56%,transparent 100%)}
.vc-item h3{position:absolute;left:18px;right:18px;bottom:42px;z-index:2;color:#fff;
font-size:17px;font-weight:750;letter-spacing:-.025em;line-height:1.35;margin:0;
text-shadow:0 1px 12px rgba(0,0,0,.35)}
.vc-item .cat{position:absolute;left:18px;right:18px;bottom:17px;z-index:2;
color:rgba(255,255,255,.88);font-size:12.5px;font-weight:600;text-shadow:0 1px 10px rgba(0,0,0,.35)}
.vc-thumb--g{background:linear-gradient(135deg,#dfe7fb,#eef1f8)}
.vc-thumb--g.g2{background:linear-gradient(135deg,#dcf0e4,#eef7f1)}
.vc-thumb--g.g3{background:linear-gradient(135deg,#fbe3d6,#f9efe9)}
/* 섹션 헤더 — 큰 타이틀 + 한 줄 + 우측 더보기 */
.vc-head--tight{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap}
.vc-head--tight .more{font-size:14px;font-weight:700;color:var(--gray)}
.vc-head--tight .more:hover{color:var(--ink)}
"""

# ---------- 네이티브 앱 페이지(/apps/<slug>/) 전용 ----------
#   기존 제품 상세(.vd)는 실물 사진 10여 장을 전제로 짜여 있다. 앱은 그 자산이 없고
#   'setup(권한 켜는 법)'이라는 다른 목적의 화면이 필요해 별도 컴포넌트로 둔다.
CSS += """
/* 앱 하위 페이지(setup·support) — **인사이트 목록과 같은 골격**(2026-08-24 대표 지적).
   컨테이너 1224 + 히어로는 .nws-head 규격(제목 --pg-h1, 그 아래 한 줄).
   본문 단락만 읽기 폭(780)으로 잡는다 — 글이라 그 이상 넓히면 안 읽힌다. */
.ap{max-width:1224px;margin:0 auto;padding:0 24px 110px}
.ap-head{padding:var(--pg-top) 0 var(--pg-head-gap)}
.ap-head h1{font-size:var(--pg-h1);font-weight:800;letter-spacing:-.045em;line-height:1.08;
color:var(--ink)}
.ap-head .lead{margin-top:var(--pg-sub-gap);font-size:16px;line-height:1.72;color:var(--gray);
max-width:56ch}
/* 본문도 컨테이너를 따라 넓어진다 — 폭만 넓히고 안쪽을 780 에 묶으면 아무것도 안 바뀐다
   (2026-08-24 대표 지적). 순수 텍스트 단락만 읽기 폭으로 잡고, 표·탭·단계·그림은 다 쓴다. */
.ap-body{max-width:none}
.ap-body > .hint,.ap-body > p{max-width:70ch}
.ap-steps li{max-width:none}
.ap-steps .d{max-width:76ch}
.ap-pane{max-width:none}
.ap-qa{max-width:none}
/* 단계 그림은 넓어진 폭을 실제로 쓴다 */
.ap-steps img,.ap-pane img{max-width:100%}
.ap-kick{font-size:13.5px;font-weight:700;letter-spacing:-.01em;color:var(--brand-cta);text-transform:none}
/* 설정·지원 같은 **곁가지 페이지**는 돌아갈 길이 바닥에만 있으면 없는 것과 같다
   (2026-08-24 대표 지적: "네비가 없는데 이거 어떻게 할꺼야?").
   GNB 는 제품 이름을 안 들고 있어서 Flipper 로 돌아갈 수 없다 — 여기가 유일한 길이다. */
.ap-crumb{display:flex;flex-wrap:wrap;align-items:center;gap:7px;
font-size:13.5px;font-weight:600;letter-spacing:-.01em;color:var(--gray)}
.ap-crumb a{color:var(--gray);text-decoration:none;border-radius:6px}
.ap-crumb a:hover{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.ap-crumb .sep{color:var(--line2,#c8c8cc);font-weight:400}
.ap-crumb .now{color:var(--brand-cta);font-weight:700}
/* 뒤로 가는 링크를 본문 끝에도 한 번 더 — 다 읽고 나서 위로 올릴 필요가 없게. */
.ap-back{margin-top:34px;display:inline-flex;align-items:center;gap:8px;
font-size:14.5px;font-weight:700;color:var(--ink);text-decoration:none;
border:1px solid var(--line);border-radius:999px;padding:11px 18px}
.ap-back:hover{border-color:var(--ink2);background:var(--soft)}
.ap h1{font-size:var(--pg-h1,clamp(28px,5vw,42px));font-weight:800;letter-spacing:-.045em;
line-height:1.12;margin:10px 0 0}
.ap .sub{font-size:17px;color:var(--gray);margin-top:14px;line-height:1.65}
.ap .lead{font-size:16px;color:var(--ink2);line-height:1.75;margin-top:26px}
.ap .lead b{font-weight:700;color:var(--ink)}
.ap-badge{display:inline-flex;align-items:center;gap:7px;margin-top:20px;padding:7px 13px;border-radius:999px;
background:var(--soft);font-size:13px;font-weight:600;color:var(--ink2)}
.ap-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--pt)}
.ap-cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.ap-cta a{display:inline-flex;align-items:center;justify-content:center;padding:14px 22px;border-radius:12px;
font-size:15px;font-weight:700;border:1px solid var(--line);transition:.16s var(--ease)}
.ap-cta .go{background:var(--ink);color:#fff;border-color:var(--ink)}
.ap-cta .go:hover{transform:translateY(-1px);box-shadow:0 12px 26px -12px rgba(0,0,0,.4)}
.ap-cta .sec:hover{background:var(--soft)}
.ap h2{font-size:22px;font-weight:800;letter-spacing:-.02em;margin:64px 0 0}
.ap h2+.hint{font-size:14px;color:var(--gray);margin-top:8px;line-height:1.6}
/* 문의 때 적어 달라고 할 항목. 기본 list-style 은 들여쓰기가 튀어 글머리표를 직접 그린다. */
.ap .ask{list-style:none;margin:10px 0 0;padding:0}
.ap .ask li{position:relative;padding-left:13px;margin-top:5px}
.ap .ask li::before{content:"·";position:absolute;left:2px;color:var(--faint)}
.ap-feats{display:grid;gap:2px;margin-top:24px;background:var(--line);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.ap-feats>div{background:var(--paper);padding:22px}
.ap-feats .t{font-size:16px;font-weight:700;letter-spacing:-.01em}
.ap-feats .d{font-size:14px;color:var(--gray);margin-top:7px;line-height:1.65}
.ap-spec{width:100%;border-collapse:collapse;margin-top:24px;font-size:14px}
.ap-spec th,.ap-spec td{text-align:left;padding:13px 0;border-bottom:1px solid var(--line);vertical-align:top}
.ap-spec th{width:34%;color:var(--gray);font-weight:600}
.ap-spec td{font-family:var(--mono);font-size:13px}
/* 기기 선택 탭 */
.ap-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.ap-tabs button{padding:10px 16px;border-radius:999px;border:1px solid var(--line);background:var(--paper);
font-family:inherit;font-size:14px;font-weight:600;color:var(--gray);cursor:pointer;transition:.14s var(--ease)}
.ap-tabs button:hover{border-color:var(--ink2);color:var(--ink)}
.ap-tabs button[aria-selected="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}
.ap-dev[hidden]{display:none}
/* setup 의 기기별 경고 + support 의 자가진단 머리말이 같이 쓴다(.ap 안이면 어디서든). */
.ap .note{margin-top:22px;padding:15px 17px;border-radius:12px;background:#fff8f4;border:1px solid #ffd9c9;
font-size:14px;line-height:1.65;color:var(--ink2)}
/* ── 설정 단계 = **3열 카드 그리드** ────────────────────────────────────
   세로 한 줄로 쌓으니 스크린샷 하나에 화면 한 판을 쓰고 오른쪽이 통째로 비었다
   (2026-08-24 대표 지적). 단계는 "훑고 따라 하는" 것이라 나란히 보이는 게 맞다.
   ⚠️ 숫자는 CSS counter 로 매긴다 — 그리드로 바꿔도 순서가 안 깨진다. */
/* ⚠️ 카드 안(뱃지·제목·설명·그림)의 행을 **바깥 그리드와 공유**한다(subgrid).
   설명이 2줄인 카드가 하나 섞이면 그 카드만 그림이 아래로 밀려 나란한 줄이 깨진다
   (2026-08-24 대표 지적: "이게 2줄되고 나머지 1줄이니깐 이상하잖아").
   설명 높이를 '2줄'로 못 박는 방법도 있지만, 다음에 문구가 3줄이 되는 순간 같은 사고가
   그대로 재발한다. 행을 공유시키면 줄 수가 몇이든 스스로 맞는다.
   ⚠️ row-gap 은 0 이어야 한다 — 카드 *안쪽* 행 사이까지 벌어진다. 줄 간격은 li 의
   margin-bottom 이 만든다. 카드 padding 은 전부 같아야 정렬이 유지된다(subgrid 특성). */
.ap-steps{--g:clamp(14px,1.8vw,24px);--min:320px;list-style:none;margin:26px 0 0;padding:0;
counter-reset:s;display:grid;column-gap:var(--g);row-gap:0;
grid-template-columns:repeat(auto-fit,minmax(min(var(--min),100%),1fr))}
.ap-steps li{counter-increment:s;grid-row:span 4;display:grid;grid-template-rows:subgrid;
border:0;background:var(--soft);border-radius:16px;padding:clamp(16px,1.8vw,22px);
margin-bottom:var(--g);min-width:0}
.ap-steps li>div{grid-row:span 3;display:grid;grid-template-rows:subgrid;min-width:0}
.ap-steps li::before{content:counter(s);justify-self:start;width:26px;height:26px;border-radius:50%;
background:var(--ink);color:#fff;font-size:12.5px;font-weight:700;
display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.ap-steps .t{align-self:start;font-size:15.5px;font-weight:700;letter-spacing:-.03em;color:var(--ink)}
.ap-steps .d{align-self:start;font-size:14px;color:var(--gray);margin-top:6px;line-height:1.65}
/* ⚠️ 열 수를 숫자로 박지 마라(3열·2열). 화면이 넓어지면 그림이 쓸데없이 커지고
   좁아지면 글씨가 안 읽힌다. 대신 **읽히는 최소 폭**만 정하고 열 수는 브라우저가 센다
   (2026-08-24 대표 지적: "적절히 크기에 맞춰서 하면 되지 반응형으로").
   그래서 데스크톱·태블릿·모바일에 따로 규칙을 둘 필요가 없다 — min() 이 폭을 넘지
   않게 잡아 주므로 320px 화면에서도 가로 스크롤이 안 생긴다.
   눕혀 찍은 화면(교보 SAM 1600×1200)은 세로 폰과 같은 260px 로 두면 메뉴 글씨가
   안 보인다 — 가로가 긴 만큼 최소 폭을 키운다. 판정은 PNG 헤더(가로>세로). */
.ap-steps.landscape{--min:440px}
/* 단계·경고 안의 링크는 본문과 같은 회색이라 링크인 줄 모른다. 밑줄과 굵기로 분리한다. */
.ap-steps .d a,.ap .note a,.ap .ask a{font-weight:700;color:var(--ink);text-decoration:underline;
text-underline-offset:3px}
/* 실기기 폰 스크린샷 — 세로로 매우 길다(840×2326 등).
   ⚠️ **자르지 마라.** max-height + object-fit:cover 로 위쪽만 남겼더니 각 단계가 보여줘야 할
   바로 그 부분이 잘렸다(2026-08-24 실사고: 2번의 '접근성 설정 열기' 안내창이 화면 아래쪽에
   뜨는데 위만 남아 1번과 똑같아 보였고, 3번은 목록이 중간에서 끊겼다).
   세로로 긴 게 문제였던 건 1열이던 시절 얘기다 — 3열이면 폭이 이미 1/3 이라 통째로 깔아도 된다.
   설정 안내 그림은 '무엇을 눌러야 하는지'가 전부라, 짧게 만드는 것보다 다 보이는 게 우선이다. */
.ap-steps .shot{margin-top:14px;width:100%;height:auto;align-self:start;
border-radius:12px;border:1px solid var(--line);background:var(--paper)}
/* 가로로 찍힌 태블릿·리더기 화면(교보 SAM 1600×1200 등)은 세로 폰 기준 220px 로 묶으면
   220×165 로 쪼그라들어 메뉴 글씨가 안 읽힌다. 생성기가 PNG 헤더를 읽어 가로가 길면 .wide 를 붙인다. */
/* .wide 는 이제 '이 탭을 2열로 벌려라' 는 신호로만 쓴다 — 폭 제한은 카드가 한다. */
.ap-qa{margin-top:24px;border-top:1px solid var(--line)}
.ap-qa details{border-bottom:1px solid var(--line)}
.ap-qa summary{padding:18px 0;font-size:15px;font-weight:700;cursor:pointer;list-style:none;display:flex;
align-items:center;justify-content:space-between;gap:14px}
.ap-qa summary::-webkit-details-marker{display:none}
.ap-qa summary::after{content:"+";font-size:19px;font-weight:400;color:var(--faint);flex:0 0 auto}
.ap-qa details[open] summary::after{content:"−"}
.ap-qa .a{font-size:14px;color:var(--ink2);line-height:1.75;padding:0 0 20px}
.ap-help{margin-top:56px;padding:24px;border-radius:14px;background:var(--soft);font-size:14px;line-height:1.7;color:var(--ink2)}
.ap-help a{font-weight:700;text-decoration:underline;text-underline-offset:3px}
@media(max-width:640px){.ap{padding:0 18px 80px}.ap-cta a{width:100%}}
"""

# ─────────────────────────────────────────────────────────────────────────────
# KB 랜딩 — 구성 클론(레퍼런스: blog.kakaobank.com/home)
#   왜: 기존 랜딩(hz 히어로 + vc 그리드)은 "제품 카탈로그" 문법이라 콘텐츠가 쌓일 자리가 없었다.
#   무엇을: 레퍼런스의 '구성'만 가져온다 — 섹션 순서(히어로 → 최신 레일 → 인기 그리드 →
#           시리즈 레일 → 카테고리 스크롤러), 알약 GNB, 다크모드 토글, 검색 오버레이.
#   무엇을 안 가져오나: 남의 카피·일러스트·로고. 내용물은 전부 우리 자산(products.json·스트림·이야기).
#   이 층은 `body.kbp` 안에서만 산다 — 다른 페이지(제품·이야기·법적)는 손대지 않는다.
# ─────────────────────────────────────────────────────────────────────────────
KB_CSS = """
/* ═══ KB 랜딩 (body.kbp 에서만 적용) ═══ */
html[data-theme="dark"]{--ink:#f1f3f6;--ink2:#c4cad4;--paper:#0e1013;--soft:#181b20;--soft2:#22262d;
--gray:#a0a7b3;--faint:#737b88;--line:#242931}
html[data-theme="dark"] body{background:var(--paper);color:var(--ink)}
html[data-theme="dark"] footer.site .biz{border-top-color:var(--line)}
html[data-theme="dark"] .kb-th,html[data-theme="dark"] .kb-rail-th{background:var(--soft2)}

/* ── 랜딩 색 토큰 — 브랜드 색은 여기서만 바꾼다 ──────────────────────────────
   팔레트 = 흰 + 블루 #3182f6 + 잉크. '미니멀'이라 파랑은 장식이 아니라
   **행동과 현재 위치**에만 쓴다(CTA·활성 내비·활성 표식). 나머지는 잉크/무채색.

   --brand      : 브랜드 정체성. 작은 면적 강조·표식용.
   --brand-cta  : 흰 글자를 얹는 '채운 면'용. #3182f6 은 흰 글자 대비가 3.71:1 이라
                  15px 굵은 글씨에서 WCAG AA(4.5:1) 에 못 미친다. 같은 계열을 한 단계
                  내린 #1b64da 는 5.41:1 로 통과한다 — 눈으로는 같은 파랑으로 읽힌다.
                  순정 #3182f6 을 고집하려면 이 줄만 --brand 와 같게 두면 된다.
   --brand-tint : 파랑 위에 얹는 아주 옅은 배경(배지 등).
   ────────────────────────────────────────────────────────────────────────── */
/* ── 타이포 척도 — 한글 기준 ────────────────────────────────────────────────
   전엔 12·13·14·15·16·17·19·20·22·26·30·40·42px 가 규칙 없이 섞여 있었다.
   "글자가 크다"는 증상이고 원인은 척도가 없던 것. 역할 이름으로 10단계만 둔다.

   한글에 맞춘 세 가지 규칙 (라틴 기준으로 짜면 한글이 답답해진다)
     · 자간 — 클수록 좁히고, 작을수록 0 에 가깝게. 본문 크기에 -.04em 을 주면
       한글은 획이 뭉쳐 읽기 어려워진다.
     · 행간 — 라틴보다 넉넉히. 본문 1.7, 두 줄짜리 제목 1.42.
     · 줄바꿈 — `text-wrap:balance` 로 제목의 마지막 줄이 한 어절만 남는 걸 막는다.
       (body 의 `word-break:keep-all` 과 함께 동작한다)
   ────────────────────────────────────────────────────────────────────────── */
.kbp{--kb-max:1310px;--kb-pad:max(20px,calc((100% - 1310px)/2));--kb-r:16px;
--brand:#3182f6;--brand-cta:#1b64da;--brand-hover:#154fae;--brand-tint:#eef4ff;--on-brand:#fff;
--f-micro:12px;--f-cap:13px;--f-ui:14px;--f-ui-lg:15px;--f-body:17px;
--f-title-s:clamp(16px,1.35vw,18px);
--f-title:clamp(19px,1.85vw,23px);
--f-title-l:clamp(22px,2.15vw,27px);
--f-display:clamp(25px,2.6vw,34px);
--f-mega:clamp(27px,3vw,38px);
--ls-display:-.04em;--ls-title:-.028em;--ls-body:-.008em;
--lh-tight:1.32;--lh-title:1.42;--lh-body:1.7}
.kbp h1,.kbp h2,.kbp h3{text-wrap:balance}
.kbp p{text-wrap:pretty}
html[data-theme="dark"] .kbp{--brand:#6aa5ff;--brand-tint:#15213a}
.kbp ::selection{background:var(--brand-tint);color:var(--brand-cta)}
html[data-theme="dark"] .kbp ::selection{background:var(--brand-tint);color:var(--brand)}
/* 키보드 이동 표시 — 브랜드 색으로 통일(기존엔 브라우저 기본값이라 제각각이었다). */
.kbp a:focus-visible,.kbp button:focus-visible,.kbp input:focus-visible{
outline:2px solid var(--brand);outline-offset:3px;border-radius:6px}
.kbp main{padding-top:0}
.kbp .gnb{display:none}                      /* 랜딩은 자체 헤더(kb-gnb)를 쓴다 */

/* ── 헤더: 워드마크(좌) · 알약 내비(중앙) · 액션(우) ── */
.kb-gnb{position:sticky;top:0;z-index:120;display:grid;grid-template-columns:1fr auto 1fr;
align-items:center;gap:16px;height:66px;padding:0 var(--kb-pad);
background:color-mix(in srgb,var(--paper) 86%,transparent);backdrop-filter:blur(16px)}
/* 워드마크는 본문 척도 밖이다(로고에 가깝다) — 토큰으로 바꾸지 마라. */
.kb-wm{justify-self:start;display:inline-flex;align-items:baseline;gap:7px;
font-size:19px;font-weight:800;letter-spacing:-.03em;color:var(--ink)}
.kb-wm span{font-size:var(--f-ui);font-weight:500;color:var(--gray);letter-spacing:var(--ls-body)}
.kb-nav{justify-self:center;display:flex;align-items:center;gap:2px;padding:4px;
background:var(--soft);border-radius:99px}
.kb-nav a{padding:7px 16px;border-radius:99px;font-size:var(--f-ui);font-weight:600;color:var(--gray);
transition:background .18s var(--ease),color .18s var(--ease)}
.kb-nav a:hover{color:var(--ink)}
.kb-nav a.on{background:var(--brand-cta);color:var(--on-brand)}
.kb-act{justify-self:end;display:flex;align-items:center;gap:2px}
.kb-ib{display:grid;place-items:center;width:38px;height:38px;padding:0;border:0;border-radius:50%;
background:none;color:var(--ink);cursor:pointer;transition:background .18s}
.kb-ib:hover{background:var(--soft)}
.kb-ib svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.7;
stroke-linecap:round;stroke-linejoin:round}
.kb-ib .moon{display:none}
html[data-theme="dark"] .kb-ib .moon{display:block}
html[data-theme="dark"] .kb-ib .sun{display:none}
.kb-burger{display:none}
@media(max-width:860px){
  .kb-gnb{grid-template-columns:1fr auto}
  .kb-nav{display:none}
  .kb-burger{display:grid}
}
/* 모바일 시트 */
.kb-sheet{position:fixed;inset:66px 0 auto;z-index:119;background:var(--paper);
border-bottom:1px solid var(--line);padding:14px var(--kb-pad) 22px;display:none}
.kb-sheet[data-open]{display:block}
.kb-sheet a{display:block;padding:12px 0;font-size:var(--f-body);font-weight:600;color:var(--ink)}

/* ── 검색 오버레이 ── */
.kb-sr{position:fixed;inset:0;z-index:200;background:color-mix(in srgb,var(--paper) 96%,transparent);
backdrop-filter:blur(10px);padding:14vh var(--kb-pad) 0;display:none}
.kb-sr[data-open]{display:block}
.kb-sr-in{max-width:640px;margin:0 auto}
.kb-sr-box{display:flex;align-items:center;gap:12px;padding:0 4px 16px;border-bottom:2px solid var(--ink)}
.kb-sr-box input{flex:1;min-width:0;border:0;background:none;outline:none;color:var(--ink);
font-family:inherit;font-size:var(--f-display);font-weight:700;letter-spacing:var(--ls-title)}
.kb-sr-box input::placeholder{color:var(--faint)}
.kb-sr-box input::-webkit-search-cancel-button{-webkit-appearance:none;display:none}
.kb-sr-hits{margin-top:18px;max-height:56vh;overflow:auto}
.kb-sr-hits a{display:flex;align-items:center;gap:13px;padding:9px 8px;border-radius:12px}
.kb-sr-hits a:hover{background:var(--soft)}
.kb-sr-hits .th{width:56px;height:36px;border-radius:8px;overflow:hidden;flex:0 0 auto;
background:var(--soft2);display:grid;place-items:center;font-size:16px;color:var(--gray)}
.kb-sr-hits .th img{width:100%;height:100%;object-fit:cover;display:block}
.kb-sr-hits .tx{min-width:0}
.kb-sr-hits b{display:block;font-size:15px;font-weight:700;color:var(--ink);
overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.kb-sr-hits i{display:block;font-style:normal;font-size:12px;font-weight:600;
color:var(--faint);margin-top:2px}
/* 입력칸은 테두리 하이라이트 대신 **커서만** 깜빡인다(2026-08-23 대표 지적).
   ⚠️ .kbp input:focus-visible 전역 규칙을 여기서 되돌린다 — 순서상 뒤에 와야 이긴다. */
.kb-sr-box input,.kbp .kb-sr-box input:focus,.kbp .kb-sr-box input:focus-visible{
outline:none;box-shadow:none;caret-color:var(--brand-cta)}
.kb-sr-none{padding:16px 4px;color:var(--faint);font-size:var(--f-ui)}

/* ── 공통 섹션 틀 ── */
.kb-sec{padding:0 var(--kb-pad)}
.kb-sec-head{display:flex;align-items:center;justify-content:space-between;gap:20px;
margin:0 0 26px;padding-top:clamp(64px,8vw,110px)}
.kb-sec-head h2{font-size:var(--f-title);font-weight:700;letter-spacing:var(--ls-title);
line-height:var(--lh-tight);color:var(--ink)}
.kb-arrows{display:flex;gap:6px}
.kb-arrows button{display:grid;place-items:center;width:38px;height:38px;padding:0;border:0;
border-radius:50%;background:none;color:var(--ink);cursor:pointer;transition:opacity .18s,background .18s}
.kb-arrows button:hover{background:var(--soft)}
.kb-arrows button[disabled]{opacity:.25;cursor:default;background:none}
.kb-arrows svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.8;
stroke-linecap:round;stroke-linejoin:round}

/* ── 히어로: 이미지(좌) + 메타(우) ── */
/*  subgrid 는 쓰지 않는다 — 구형 사파리에서 2단이 통째로 무너진다. 슬라이드가 각자 격자를 가진다. */
.kb-hero{padding:clamp(30px,4vw,56px) var(--kb-pad) 0}
.kb-slide{display:none;grid-template-columns:minmax(0,1.06fr) minmax(0,1fr);
gap:clamp(28px,5vw,72px);align-items:center}
.kb-slide.on{display:grid;animation:kbIn .55s var(--ease) both}
@keyframes kbIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.kb-hero-art{display:block;border-radius:var(--kb-r);overflow:hidden;aspect-ratio:16/11;background:var(--soft)}
.kb-hero-art img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease)}
.kb-hero-art:hover img{transform:scale(1.03)}
.kb-kick{font-size:var(--f-ui);font-weight:600;color:var(--faint);letter-spacing:.01em}
a.kb-kick{transition:color .18s var(--ease)}
a.kb-kick:hover{color:var(--brand-cta)}
html[data-theme="dark"] a.kb-kick:hover{color:var(--brand)}
.kb-hero-meta h1{margin-top:14px;font-size:var(--f-display);font-weight:700;
letter-spacing:var(--ls-display);line-height:var(--lh-tight);color:var(--ink)}
.kb-hero-meta p{margin-top:18px;font-size:var(--f-body);line-height:var(--lh-body);
letter-spacing:var(--ls-body);color:var(--gray);max-width:38ch}
.kb-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.kb-chips span{padding:7px 14px;border-radius:99px;background:var(--soft);
font-size:var(--f-cap);font-weight:600;color:var(--gray)}
.kb-cta{display:inline-flex;align-items:center;gap:8px;margin-top:30px;padding:13px 24px;
border-radius:99px;background:var(--brand-cta);color:var(--on-brand);font-size:var(--f-ui-lg);font-weight:700;
transition:background .18s var(--ease),transform .18s var(--ease)}
.kb-cta:hover{background:var(--brand-hover);transform:translateY(-1px)}
.kb-cta span{transition:transform .22s var(--ease)}
.kb-cta:hover span{transform:translateX(3px)}
.kb-dots{display:flex;gap:8px;justify-content:flex-end;padding-top:26px}
.kb-dots button{width:7px;height:7px;padding:0;border:0;border-radius:99px;background:var(--soft2);
cursor:pointer;transition:width .25s var(--ease),background .25s}
.kb-dots button[aria-current]{width:22px;background:var(--brand)}
@media(max-width:860px){
  .kb-slide.on{grid-template-columns:1fr}
  .kb-hero-art{aspect-ratio:16/10}
}

/* ── 최신 콘텐츠: 가로 레일(작은 카드) ── */
.kb-rail{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;
scroll-behavior:smooth;scrollbar-width:none;padding-bottom:4px}
.kb-rail::-webkit-scrollbar{display:none}
.kb-rail-card{flex:0 0 clamp(272px,29vw,400px);display:flex;gap:16px;align-items:center;
scroll-snap-align:start}
.kb-rail-th{flex:0 0 clamp(88px,9vw,110px);aspect-ratio:1;border-radius:12px;overflow:hidden;background:var(--soft)}
.kb-rail-th img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.kb-rail-th.ic{display:grid;place-items:center;
background:linear-gradient(150deg,color-mix(in srgb,var(--ic) 22%,var(--paper)),color-mix(in srgb,var(--ic) 6%,var(--paper)))}
.kb-rail-th.ic span{font-size:15px;font-weight:700;color:var(--ic);letter-spacing:-.02em}
.kb-rail-card:hover .kb-rail-th img{transform:scale(1.06)}
.kb-rail-tx h3{font-size:var(--f-ui-lg);font-weight:600;line-height:var(--lh-title);
letter-spacing:var(--ls-body);color:var(--ink);
display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.kb-rail-card:hover .kb-rail-tx h3{color:var(--brand-cta)}
html[data-theme="dark"] .kb-rail-card:hover .kb-rail-tx h3{color:var(--brand)}
.kb-rail-tx time{display:block;margin-top:10px;font-size:var(--f-cap);color:var(--faint);
font-variant-numeric:tabular-nums}

/* ── 인기 콘텐츠: 3열 그리드 ── */
.kb-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(40px,4.5vw,64px) clamp(20px,2.4vw,32px)}
.kb-card{display:block}
.kb-th{width:100%;aspect-ratio:16/10;border-radius:var(--kb-r);overflow:hidden;background:var(--soft)}
.kb-th img{width:100%;height:100%;object-fit:cover;transition:transform .55s var(--ease)}
.kb-card:hover .kb-th img{transform:scale(1.04)}
.kb-th.ic{display:grid;place-items:center;
background:linear-gradient(150deg,color-mix(in srgb,var(--ic) 18%,var(--paper)),color-mix(in srgb,var(--ic) 5%,var(--paper)))}
.kb-th.ic span{font-size:clamp(44px,5vw,68px);color:var(--ic);line-height:1}
.kb-card time{display:block;margin-top:20px;font-size:var(--f-ui);color:var(--faint);
font-variant-numeric:tabular-nums}
.kb-card h3{margin-top:8px;font-size:var(--f-title-s);font-weight:700;letter-spacing:var(--ls-title);
line-height:var(--lh-title);color:var(--ink)}
.kb-card:hover h3{color:var(--brand-cta)}
html[data-theme="dark"] .kb-card:hover h3{color:var(--brand)}
.kb-card .kb-chips{margin-top:16px}
.kb-card .kb-chips span{padding:6px 12px;font-size:var(--f-micro)}
@media(max-width:1000px){.kb-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.kb-grid{grid-template-columns:1fr}}

/* ── 시리즈 레일: [목록 패널][커버 패널] 짝 ── */
.kb-srail{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;
scroll-behavior:smooth;scrollbar-width:none}
.kb-srail::-webkit-scrollbar{display:none}
.kb-spair{flex:0 0 auto;display:flex;gap:20px;scroll-snap-align:start}
.kb-spanel{width:clamp(300px,34vw,486px);min-height:clamp(360px,32vw,486px);
display:flex;flex-direction:column;padding:28px;border-radius:var(--kb-r);
background:var(--paper);border:1px solid var(--line)}
.kb-badge{align-self:flex-start;padding:6px 14px;border-radius:99px;background:var(--brand-tint);
font-size:var(--f-micro);font-weight:700;color:var(--brand-cta);letter-spacing:.02em}
html[data-theme="dark"] .kb-badge{color:var(--brand)}
.kb-spanel h3{margin-top:18px;font-size:var(--f-title-l);font-weight:700;
letter-spacing:var(--ls-title);line-height:var(--lh-tight);color:var(--ink)}
.kb-slist{margin-top:auto;padding-top:32px;list-style:none}
.kb-slist li+li{border-top:1px solid var(--line)}
.kb-slist a{display:flex;align-items:center;gap:14px;padding:13px 0}
.kb-slist .n{flex:0 0 auto;font-size:var(--f-cap);font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums}
.kb-slist .t{font-size:var(--f-ui);font-weight:600;line-height:var(--lh-title);color:var(--ink);
letter-spacing:var(--ls-body);
display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.kb-slist a:hover .t{color:var(--brand-cta)}
html[data-theme="dark"] .kb-slist a:hover .t{color:var(--brand)}
.kb-slist .sq{flex:0 0 auto;width:36px;height:36px;border-radius:9px;overflow:hidden;
display:grid;place-items:center;font-size:15px;color:var(--ic,var(--gray));
background:linear-gradient(150deg,color-mix(in srgb,var(--ic,#9aa0a8) 22%,var(--paper)),color-mix(in srgb,var(--ic,#9aa0a8) 7%,var(--paper)))}
.kb-slist .sq img{width:100%;height:100%;object-fit:cover}
.kb-scover{width:clamp(300px,34vw,486px);border-radius:var(--kb-r);overflow:hidden;
display:grid;place-items:center;background:var(--sc,var(--soft))}
.kb-scover img{width:100%;height:100%;object-fit:cover}
.kb-srail-foot{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:28px}
.kb-pill{display:inline-flex;padding:12px 22px;border-radius:99px;background:var(--brand-cta);
color:var(--on-brand);font-size:var(--f-ui);font-weight:700;transition:background .18s var(--ease)}
.kb-pill:hover{background:var(--brand-hover)}
@media(max-width:620px){.kb-spair{flex-direction:column}.kb-scover{min-height:260px}}

/* ── 카테고리 스크롤러: 고정 카드(좌) + 큰 단어 목록(우) ── */
.kb-cats{position:relative;display:grid;grid-template-columns:clamp(240px,24vw,302px) 1fr;
gap:clamp(28px,6vw,96px);align-items:center}
.kb-cat-card{position:sticky;top:96px;align-self:center;display:block;padding:0 0 22px;
border-radius:var(--kb-r);overflow:hidden;background:var(--cc,var(--soft));
transition:background .5s var(--ease)}
.kb-cat-art{width:100%;aspect-ratio:1;display:grid;place-items:center;font-size:64px;color:#fff}
.kb-cat-art img{width:100%;height:100%;object-fit:cover}
.kb-cat-card h3{padding:0 20px;font-size:var(--f-title-s);font-weight:700;
line-height:var(--lh-title);letter-spacing:var(--ls-title);color:#111}
.kb-cat-card p{padding:0 20px;margin-top:9px;font-size:var(--f-cap);line-height:var(--lh-body);color:#3b3b3b}
.kb-cat-view{position:relative;height:min(62vh,520px);overflow:hidden;
-webkit-mask-image:linear-gradient(180deg,transparent,#000 26%,#000 74%,transparent);
mask-image:linear-gradient(180deg,transparent,#000 26%,#000 74%,transparent)}
.kb-cat-list{position:absolute;left:0;top:50%;width:100%;list-style:none;
transition:transform .6s var(--ease)}
.kb-cat-list li{height:56px;display:flex;align-items:center}
.kb-cat-list button{position:relative;border:0;background:none;padding:0;cursor:pointer;font-family:inherit;
font-size:var(--f-mega);font-weight:600;letter-spacing:var(--ls-display);color:var(--soft2);
transition:color .35s var(--ease),padding-left .35s var(--ease)}
.kb-cat-list button:hover{color:var(--gray)}
/* 지금 어디인지 = 잉크 글자 + 브랜드 표식. 큰 글자를 통째로 파랗게 칠하면 미니멀이 깨진다. */
.kb-cat-list li[aria-current] button{color:var(--ink);padding-left:30px}
.kb-cat-list li[aria-current] button::before{content:"";position:absolute;left:0;top:50%;
transform:translateY(-50%);width:18px;height:3px;border-radius:2px;background:var(--brand)}
.kb-cat-ctl{position:absolute;right:0;bottom:6px;display:flex;gap:8px}
.kb-cat-ctl button{display:grid;place-items:center;width:38px;height:38px;padding:0;border:0;
border-radius:50%;background:var(--soft);color:var(--ink);cursor:pointer}
.kb-cat-ctl button:hover{background:var(--soft2)}
.kb-cat-ctl svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:2;
stroke-linecap:round;stroke-linejoin:round}
.kb-cat-ctl .pauseoff{display:none}
.kb-cat-ctl [data-paused] .pauseoff{display:block}
.kb-cat-ctl [data-paused] .pauseon{display:none}
@media(max-width:860px){
  .kb-cats{grid-template-columns:1fr;gap:32px}
  .kb-cat-card{position:static;display:grid;grid-template-columns:120px 1fr;align-items:center;padding:0 20px 0 0}
  .kb-cat-art{aspect-ratio:1;font-size:40px}
  .kb-cat-card h3,.kb-cat-card p{padding:0}
  .kb-cat-view{height:340px}
}

/* ── 맨 위로 ── */
.kb-top{position:fixed;right:22px;bottom:22px;z-index:110;display:grid;place-items:center;
width:44px;height:44px;border:1px solid var(--line);border-radius:50%;background:var(--paper);
color:var(--ink);cursor:pointer;opacity:0;pointer-events:none;transition:opacity .25s}
.kb-top[data-on]{opacity:1;pointer-events:auto}
.kb-top:hover{border-color:var(--brand);color:var(--brand)}
.kb-top svg{width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:1.9;
stroke-linecap:round;stroke-linejoin:round}
.kbp /* ⚠️ 여기서 다시 회색+여백을 주면 위 회색 섹션과 사이에 흰 띠가 남는다(2026-08-24).
   푸터는 흰 바탕 + 헤어라인 하나. 위 규칙을 덮지 마라. */
footer.site{margin-top:0;background:var(--paper);border-top:1px solid var(--line)}
@media(prefers-reduced-motion:reduce){
  .kb-rail,.kb-srail{scroll-behavior:auto}
  .kb-cat-list{transition:none}
  .kb-slide.on{animation:none}
}
"""
CSS += KB_CSS

AP_CSS = """
/* ═══ 홈 — 제품이 차례로 무대에 선다 ═══════════════════════════════════════
   2026-08-23 개편. 그전 홈은 캐러셀·최신 콘텐츠·많이 찾는 것·묶어서 보면·
   무엇을 하려고 오셨나요 로 이어지는 '콘텐츠 허브'였다. 대표: "잡스러운 거 치우고
   이 업체 제대로 뭔가 제품 만드는 곳이구나 느끼게 해줘야." 목록을 쌓는 대신
   제품 하나에 화면 하나를 준다 — 이름 · 한 줄 · 행동 둘 · 큰 그림. 그게 전부다. */
/* 애플 타일 실측(apple.com/kr/airpods, 1440 뷰포트):
     카드 폭 1380 · 좌우 여백 30px · 모서리 18px · 높이 756(≈1.83:1)
     그림은 카드 안에서 꽉 참(object-fit:cover), 글은 그림 **위** 좌하단 x=48 y=539,
     제품명 80px/600, 한 줄 21px, 버튼 둘은 우하단 같은 줄.
   ⚠️ 종전엔 카드를 뷰포트에 거의 붙이고(12px) 글을 그림 아래 띠에 뒀다 — 둘 다 애플과 다르다. */
/* 배너·레일이 같은 좌변에서 시작하도록 여백을 한 변수로 묶는다. */
:root{--stack-pad:max(clamp(12px,2.1vw,30px),calc((100vw - 1520px)/2 + clamp(12px,2.1vw,30px)))}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.stg-stack{display:flex;flex-direction:column;gap:clamp(12px,2.1vw,30px);
max-width:1520px;margin:0 auto;padding:clamp(12px,2.1vw,30px) clamp(12px,2.1vw,30px) 0}
.stg-row{display:grid;grid-template-columns:1fr 1fr;gap:clamp(12px,2.1vw,30px)}
.stg{position:relative;display:flex;flex-direction:column;text-align:left;
border-radius:18px;overflow:hidden;background:var(--soft)}
.stg--paper{background:var(--paper);box-shadow:inset 0 0 0 1px var(--line)}
.stg--ink{background:#0b0c0e;color:#fff}
.stg--ink .stg-claim{color:#aeb5c0}
.stg--ink .stg-eyebrow{color:#79828f}

/* ── 전면 타일: 그림이 카드를 채우고 글이 그 위에 얹힌다 ── */
.stg--hero{width:100%;aspect-ratio:1380/756;min-height:340px}
.stg--hero .stg-art{position:absolute;inset:0;aspect-ratio:auto;z-index:0}
.stg--hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:62%;z-index:1;
pointer-events:none;background:linear-gradient(to top,rgba(0,0,0,.62),rgba(0,0,0,.28) 42%,transparent)}
.stg--hero .stg-bd{position:relative;z-index:2;padding:clamp(24px,3.3vw,48px)}
/* 배너 전면 클릭 판 — 글·버튼보다 아래(z1)에 깔려 버튼 클릭을 안 가로챈다. */
.stg-hit{position:absolute;inset:0;z-index:1}
.stg-bd,.stg-cta{position:relative;z-index:2}
.stg:hover{cursor:pointer}
.stg--hero .stg-name{color:#fff;font-size:clamp(34px,5.6vw,80px);letter-spacing:-.055em}
.stg--hero .stg-claim{color:rgba(255,255,255,.88);font-size:clamp(15px,1.5vw,21px);font-weight:600}
.stg--hero .stg-eyebrow{color:rgba(255,255,255,.72)}
.stg--hero .stg-pill--line{color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.75)}
/* 2단 칸도 같은 전면 타일 문법. 폭이 절반이라 글자만 한 단계 작아진다
   (2026-08-23 대표: "크기는 다 똑같이 하라고"). */
.stg-row .stg--hero{aspect-ratio:1380/900}
.stg-row .stg--hero .stg-name{font-size:clamp(26px,3vw,46px)}
.stg-row .stg--hero .stg-claim{font-size:clamp(14.5px,1.25vw,19px)}

/* ── 2단 타일: 그림 위, 글 아래(애플 '모델 비교하기' 배치). 우리 og 배너는
      글자가 박혀 있어 그림 위에 글을 얹으면 겹친다 — 그래서 이쪽만 아래 띠. ── */
.stg-art{width:100%;aspect-ratio:16/9;overflow:hidden;background:var(--paper)}
/* ⚠️ video 는 자기 고유 크기(1600x900)로 그려진다 — width/height 100% 를 명시하지 않으면
   창을 좁혀도 안 줄어들고 카드 밖으로 넘친다(2026-08-24 실측: 430px 화면에서 영상 폭 1600). */
.stg-art img,.stg-art video{width:100%;height:100%;object-fit:cover;object-position:center;
display:block;transition:transform .6s var(--ease)}
.stg-art video{transition:none}
.stg-art img{width:100%;height:100%;object-fit:contain;display:block;
transition:transform .6s var(--ease)}
.stg--hero .stg-art img,.stg--hero .stg-art video{object-fit:cover}
.stg:hover .stg-art img{transform:scale(1.02)}
.stg--paper .stg-art{background:var(--soft)}
.stg--ink .stg-art{background:none}
.stg-bd{margin-top:auto;display:grid;grid-template-columns:1fr auto;align-items:end;gap:18px 26px;
padding:clamp(20px,2.4vw,30px) clamp(20px,2.6vw,34px) clamp(24px,2.8vw,34px)}
.stg-eyebrow{font-size:12.5px;font-weight:600;letter-spacing:-.01em;color:var(--faint)}
/* 기기 배지 — 이름 앞에 띠로 두른다. */
.stg-eyebrow .dev{display:inline-block;margin-right:9px;padding:4px 10px;border-radius:99px;
font-size:11.5px;font-weight:800;letter-spacing:-.01em;background:rgba(255,255,255,.9);
color:#0b0c0e;vertical-align:1px}
.stg-eyebrow em{font-style:normal;margin-left:8px;padding:3px 8px;border-radius:99px;
font-size:10px;font-weight:800;letter-spacing:.07em;color:#fff;background:var(--brand-cta);
vertical-align:2px}
.stg-name{font-weight:800;letter-spacing:-.05em;line-height:1.04;margin-top:9px;
font-size:clamp(24px,2.3vw,32px)}
.stg-claim{margin-top:9px;font-size:clamp(14.5px,1.05vw,17px);color:var(--gray);letter-spacing:-.02em}
.stg-cta{display:flex;gap:9px;flex-wrap:wrap}
.stg-pill{display:inline-flex;align-items:center;height:40px;padding:0 20px;border-radius:99px;
font-size:14.5px;font-weight:600;background:var(--brand-cta);color:#fff;white-space:nowrap;
transition:opacity .18s var(--ease)}
.stg-pill:hover{opacity:.88}
.stg-pill--line{background:transparent;color:var(--brand-cta);box-shadow:inset 0 0 0 1px currentColor}
.stg--ink .stg-pill--line{color:#8fc0ff}
/* ── 철학 + 제품 색인(애플 서비스 번들 섹션 문법) ── */
.idx{background:var(--soft);margin-top:clamp(20px,2.6vw,40px)}
.idx-in{max-width:1520px;margin:0 auto;padding:clamp(52px,6.5vw,96px) clamp(16px,2.4vw,40px);
display:grid;grid-template-columns:1fr 1.1fr;gap:clamp(28px,5vw,80px)}
.idx .k{font-size:12.5px;font-weight:700;color:var(--brand-cta)}
.idx-l h2{margin-top:12px;font-size:clamp(26px,3.4vw,46px);font-weight:800;letter-spacing:-.055em;
line-height:1.1;color:var(--ink)}
.idx-l .s{margin-top:16px;font-size:16px;line-height:1.75;color:var(--gray);max-width:44ch}
.idx-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.idx-cta .b{display:inline-flex;align-items:center;height:44px;padding:0 22px;border-radius:99px;
font-size:15px;font-weight:600;background:var(--brand-cta);color:#fff}
.idx-cta .b.line{background:transparent;color:var(--brand-cta);box-shadow:inset 0 0 0 1px currentColor}
.idx-r{display:flex;flex-direction:column;gap:10px;align-self:center}
.idx-go{display:block;padding:18px 22px;border-radius:14px;background:var(--paper);
transition:transform .18s var(--ease),box-shadow .18s var(--ease)}
.idx-go:hover{transform:translateY(-2px);box-shadow:0 14px 30px -20px rgba(0,0,0,.35)}
.idx-go b{display:block;font-size:17px;font-weight:700;letter-spacing:-.035em;color:var(--ink)}
.idx-go i{display:block;font-style:normal;font-size:14px;color:var(--gray);margin-top:5px}
@media(max-width:900px){.idx-in{grid-template-columns:1fr}}

/* ── 무료 도구 = 애플 스토어 'The latest' 카드 레일 ── */
.tsec{padding:clamp(56px,7vw,104px) 0 clamp(20px,2.6vw,40px)}
.tsec-h{display:flex;align-items:baseline;justify-content:space-between;gap:20px;
padding:0 clamp(12px,2.1vw,30px) 0 var(--stack-pad)}
.tsec-h h2{font-size:clamp(22px,2.6vw,34px);font-weight:800;letter-spacing:-.05em;color:var(--ink)}
.tsec-h h2 span{color:var(--faint)}
/* 애플은 레일을 컨테이너 안에 가두지 않는다 — 카드가 화면 끝까지 흘러간다.
   왼쪽 시작점만 위 배너와 같은 그리드에 맞춘다(--stack-pad). */
.tcards{display:flex;gap:clamp(12px,1.4vw,20px);overflow-x:auto;scroll-snap-type:x mandatory;
scroll-behavior:smooth;scrollbar-width:none;scroll-padding-left:var(--stack-pad);
margin:clamp(20px,2.4vw,32px) 0 0;padding:0 clamp(12px,2.1vw,30px) 6px var(--stack-pad)}
.tcards::-webkit-scrollbar{display:none}
/* 카드는 전부 같은 밝은 판 — 검정↔흰색 교차는 눈이 튄다(2026-08-24 대표 지적). */
.tcard{flex:0 0 clamp(260px,27vw,400px);scroll-snap-align:start;position:relative;
display:flex;flex-direction:column;aspect-ratio:4/5;border-radius:18px;overflow:hidden;
background:var(--paper);box-shadow:inset 0 0 0 1px var(--line);
padding:clamp(20px,2vw,28px);transition:transform .2s var(--ease)}
.tcard:hover{transform:translateY(-3px)}
.tcard .k{font-size:12px;font-weight:800;letter-spacing:.04em;color:var(--brand-cta)}
.tcard b{margin-top:10px;font-size:clamp(20px,1.9vw,26px);font-weight:800;letter-spacing:-.045em;
color:var(--ink)}
.tcard i{margin-top:8px;font-style:normal;font-size:14.5px;line-height:1.6;color:var(--gray)}
.tcard .art{margin-top:auto;display:grid;place-items:center;padding-bottom:6px}
.tcard .gl{display:grid;place-items:center;width:clamp(84px,9.5vw,124px);aspect-ratio:1}
.tcard .gl img{width:100%;height:100%;object-fit:contain;display:block}
.tcard .gl--tx{border-radius:28px;font-size:clamp(36px,4vw,56px);color:var(--ink);background:var(--soft)}
.stg-icons{flex:1;display:flex;gap:10px;flex-wrap:wrap;align-items:center;align-content:center;
padding:clamp(30px,3.6vw,52px) clamp(20px,2.6vw,34px)}
/* 홈 하단 레일 — apple.com/airpods 아래쪽 '더 알아보기' 캐러셀과 같은 문법:
   가로로 흐르고 좌우 버튼으로 한 장씩 민다. 스냅으로 카드가 정확히 선다. */
.rl{max-width:1520px;margin:clamp(40px,5vw,72px) auto 0;padding:0 clamp(12px,2.1vw,30px)}
.rl-h{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:18px}
.rl-h h2{font-size:clamp(20px,2vw,28px);font-weight:800;letter-spacing:-.04em;color:var(--ink)}
.rl-nav{display:flex;gap:8px}
.rl-nav button{width:38px;height:38px;border:0;border-radius:50%;background:var(--soft);
color:var(--ink);cursor:pointer;display:grid;place-items:center;transition:background .18s}
.rl-nav button:hover{background:var(--soft2)}
.rl-nav button[disabled]{opacity:.35;cursor:default}
.rl-nav svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:2;
stroke-linecap:round;stroke-linejoin:round}
.rl-track{display:flex;gap:clamp(12px,1.6vw,20px);overflow-x:auto;scroll-snap-type:x mandatory;
scroll-behavior:smooth;scrollbar-width:none;padding-bottom:4px}
.rl-track::-webkit-scrollbar{display:none}
.rl-it{flex:0 0 clamp(240px,25vw,330px);scroll-snap-align:start;display:block}
.rl-it .th{display:block;width:100%;aspect-ratio:1200/630;border-radius:14px;
overflow:hidden;background:var(--soft)}
.rl-it .th img{width:100%;height:100%;object-fit:cover;display:block;
transition:transform .5s var(--ease)}
.rl-it:hover .th img{transform:scale(1.04)}
.rl-it h3{margin-top:13px;font-size:15.5px;font-weight:700;letter-spacing:-.03em;line-height:1.45;
color:var(--ink);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.rl-it .d{margin-top:8px;font-size:13px;color:var(--faint)}
@media(prefers-reduced-motion:reduce){.rl-track{scroll-behavior:auto}}
.stg-icons span{width:52px;height:52px;border-radius:15px;display:grid;place-items:center;
font-size:22px;background:var(--soft);color:var(--ink)}
.stg--paper .stg-icons span{background:var(--soft)}
@media(max-width:820px){.stg-row{grid-template-columns:1fr}.stg-bd{grid-template-columns:1fr}
.stg--hero{aspect-ratio:4/5}}
@media(prefers-reduced-motion:no-preference){
.stg{opacity:0;transform:translateY(16px);
transition:opacity .65s var(--ease),transform .65s var(--ease)}
.stg.in{opacity:1;transform:none}}

/* 홈 상단 바 = 스포크와 같은 공용 1단 바(패밀리룩). 검색·테마만 우측에 얹는다. */
#mmt-bar+.kb-sr{position:fixed}
"""
CSS += AP_CSS

ABOUT_CSS = """
/* ═══ /about/ — toss.im/company 구조 실측 이식(2026-08-23) ══════════════════
   토스 실측(1440): 컨테이너 x=108 w=1224 · h1 100px/700/ls-3px · 섹션 h2 40px/700
   · 좌측 라벨 레일(●) + 우측 본문 2단 · 큰 선언 문장 80px.
   그전 소개는 이미지 0장에 글만 빼곡했고(대표: "읽고 싶지 않은데?"),
   마지막이 '유튜브 지켜봐 주세요' 였다 — 소개하러 온 사람에게 할 말이 아니다. */
.abt{max-width:1224px;margin:0 auto;padding:0 24px}
.abt-hero{padding:var(--pg-top) 0 clamp(56px,7vw,96px);position:relative;overflow:hidden}
.abt-hero::before{content:"";position:absolute;right:-8%;top:-40%;width:78%;height:150%;
border-radius:50%;z-index:0;pointer-events:none;
background:radial-gradient(closest-side,rgba(49,130,246,.16),transparent 72%)}
.abt-hero>*{position:relative;z-index:1}
.abt-hero h1{font-size:clamp(38px,6.6vw,92px);font-weight:800;letter-spacing:-.055em;
line-height:1.02;color:var(--ink)}
.abt-hero .sub{margin-top:clamp(14px,1.8vw,26px);font-size:clamp(18px,2.3vw,32px);
font-weight:700;letter-spacing:-.04em;color:var(--ink2);line-height:1.34}
.abt-hero .lede{margin-top:20px;max-width:46ch;font-size:16px;line-height:1.75;color:var(--gray)}

.abt-sec{border-top:1px solid var(--line);padding:clamp(44px,5.5vw,80px) 0}
.abt-row{display:grid;grid-template-columns:1fr 1.55fr;gap:clamp(20px,4vw,56px)}
.abt-lbl{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:600;color:var(--ink);
align-self:start}
.abt-lbl::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--ink);flex:0 0 auto}
.abt-say{font-size:clamp(19px,1.7vw,23px);font-weight:700;letter-spacing:-.035em;
line-height:1.5;color:var(--ink)}
.abt-body{margin-top:14px;font-size:16px;line-height:1.78;color:var(--gray);max-width:60ch}
.abt-body+.abt-body{margin-top:12px}

/* 큰 선언 + 사진 */
.abt-band{margin:clamp(30px,4vw,56px) auto 0;max-width:1520px;padding:0 clamp(12px,2.1vw,30px)}
.abt-band-in{position:relative;width:100%;border-radius:18px;overflow:hidden;aspect-ratio:1380/756;
display:flex;flex-direction:column;justify-content:flex-end;min-height:320px}
.abt-band-in img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.abt-band-in::after{content:"";position:absolute;left:0;right:0;bottom:0;height:66%;z-index:1;
background:linear-gradient(to top,rgba(20,16,12,.6),rgba(20,16,12,.2) 45%,transparent)}
.abt-band-tx{position:relative;z-index:2;padding:clamp(24px,3.3vw,48px);color:#fff}
.abt-band-tx h2{font-size:clamp(26px,4.4vw,64px);font-weight:800;letter-spacing:-.055em;line-height:1.08}
.abt-band-tx p{margin-top:12px;font-size:clamp(14.5px,1.4vw,19px);font-weight:600;
color:rgba(255,255,255,.86);letter-spacing:-.02em}

/* 원칙 카드 */
.abt-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.8vw,24px);margin-top:8px}
.abt-card{background:var(--soft);border-radius:16px;padding:clamp(20px,2.2vw,28px)}
.abt-card .n{font-family:var(--mono);font-size:12px;color:var(--faint)}
.abt-card h3{margin-top:10px;font-size:18px;font-weight:800;letter-spacing:-.035em;color:var(--ink)}
.abt-card p{margin-top:9px;font-size:14.5px;line-height:1.7;color:var(--gray)}

/* 연혁 */
.abt-hist{display:flex;flex-direction:column}
.abt-hist-it{display:grid;grid-template-columns:96px 1fr;gap:18px;padding:16px 0;
border-bottom:1px solid var(--line)}
.abt-hist-it:first-child{border-top:1px solid var(--line)}
.abt-hist-it .y{font-family:var(--mono);font-size:14px;font-weight:700;color:var(--brand-cta)}
.abt-hist-it h4{font-size:16px;font-weight:700;letter-spacing:-.03em;color:var(--ink)}
.abt-hist-it p{margin-top:4px;font-size:14px;color:var(--gray)}

/* 숫자 */
.abt-nums{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(14px,1.8vw,24px)}
.abt-num b{display:block;font-size:clamp(26px,2.8vw,38px);font-weight:800;letter-spacing:-.05em;color:var(--ink)}
.abt-num span{display:block;margin-top:6px;font-size:13.5px;color:var(--gray)}

/* 마무리 */
.abt-fig{margin:clamp(30px,3.6vw,52px) 0 0}
.abt-fig img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:18px;display:block}
.abt-fig figcaption{margin-top:12px;font-size:13.5px;color:var(--faint)}
.abt-end{border-top:1px solid var(--line);padding:clamp(56px,7vw,104px) 0 clamp(72px,9vw,130px)}
.abt-end h2{font-size:clamp(24px,3.2vw,44px);font-weight:800;letter-spacing:-.05em;
line-height:1.2;color:var(--ink)}
.abt-end p{margin-top:14px;font-size:16px;line-height:1.75;color:var(--gray);max-width:52ch}
.abt-end .btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.abt-end .b{display:inline-flex;align-items:center;height:46px;padding:0 24px;border-radius:99px;
font-size:15px;font-weight:600;background:var(--brand-cta);color:#fff}
.abt-end .b.line{background:transparent;color:var(--brand-cta);box-shadow:inset 0 0 0 1px currentColor}
@media(max-width:860px){
  .abt-band-in{aspect-ratio:4/5}
  .abt-row{grid-template-columns:1fr;gap:14px}
  .abt-cards{grid-template-columns:1fr}
  .abt-nums{grid-template-columns:1fr 1fr}
  .abt-hist-it{grid-template-columns:72px 1fr;gap:12px}
}
"""
CSS += ABOUT_CSS

NEWS_CSS = """
/* ═══ /stories/ — toss.im/newsroom 구조 실측 이식(2026-08-23) ═════════════
   토스 실측(1440): 컨테이너 x=108 · h1 '뉴스룸' 56px/700/ls-1.12px
   · 상단 피처 카드 596x456(1.307:1) 라운드 큼 · 아래 목록은
     좌측 라벨 레일(● 보도자료·534건) + 우측 3단 그리드
   · **모든 카드 그림이 같은 비율** — 그전 우리 카드는 4:3·1:1·그라디언트가 섞여 있었다. */
.nws{max-width:1224px;margin:0 auto;padding:0 24px}
.nws-head{padding:var(--pg-top) 0 var(--pg-head-gap)}
.nws-head h1{font-size:var(--pg-h1);font-weight:800;letter-spacing:-.045em;
line-height:1.08;color:var(--ink)}
.nws-head p{margin-top:var(--pg-sub-gap);font-size:16px;line-height:1.7;color:var(--gray);max-width:52ch}

.nws-feat{display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,2.2vw,32px)}
.nws-fcard{position:relative;display:block;border-radius:28px;overflow:hidden;
aspect-ratio:1200/700;background:var(--soft)}
.nws-fcard img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
transition:transform .6s var(--ease)}
.nws-fcard:hover img{transform:scale(1.03)}
.nws-fcard::after{content:"";position:absolute;left:0;right:0;bottom:0;height:66%;
background:linear-gradient(to top,rgba(16,14,12,.88),rgba(16,14,12,.5) 40%,
rgba(16,14,12,.12) 72%,transparent)}
/* ⚠️ 스크림을 약하게 두지 마라 — 마크 표지는 큰 색글자가 박힌 배너라 .66 으로는
   제목이 안 읽혔다(2026-08-25 실측). 본진 표지처럼 차분한 그림엔 손해가 없다. */
.nws-fcard .tx{position:absolute;left:0;right:0;bottom:0;z-index:2;
padding:clamp(20px,2.6vw,34px);color:#fff}
.nws-fcard .m{font-size:13px;font-weight:600;color:rgba(255,255,255,.78)}
.nws-fcard h2{margin-top:9px;font-size:clamp(18px,1.9vw,25px);font-weight:800;
letter-spacing:-.04em;line-height:1.35}

.nws-sec{margin-top:clamp(56px,7vw,104px)}
.nws-sec-h{display:flex;align-items:baseline;justify-content:space-between;gap:16px;
padding-bottom:14px;border-bottom:1px solid var(--line)}
.nws-sec-h h2{font-size:clamp(20px,2vw,28px);font-weight:800;letter-spacing:-.04em;color:var(--ink)}
.nws-row{display:grid;grid-template-columns:1fr 2.6fr;gap:clamp(20px,3.4vw,48px);
padding-top:clamp(26px,3.4vw,44px)}
.nws-rail{display:flex;align-items:center;gap:9px;font-size:14.5px;font-weight:600;
color:var(--ink);align-self:start}
.nws-rail::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--ink);flex:0 0 auto}
.nws-grid{display:grid;grid-template-columns:repeat(3,1fr);
gap:clamp(34px,4.6vw,64px) clamp(18px,2.6vw,36px)}
.nws-card{display:block}
.nws-card .th{width:100%;aspect-ratio:1200/630;border-radius:16px;overflow:hidden;
background:var(--soft);display:block}
.nws-card .th img{width:100%;height:100%;object-fit:cover;display:block;
transition:transform .55s var(--ease)}
.nws-card:hover .th img{transform:scale(1.04)}
/* 제목 2줄 고정 — 줄 수가 들쭉날쭉하면 날짜 줄이 카드마다 다른 높이에 앉는다. */
.nws-card h3{margin-top:16px;font-size:17px;font-weight:700;letter-spacing:-.03em;
line-height:1.45;color:var(--ink);display:-webkit-box;-webkit-line-clamp:2;
-webkit-box-orient:vertical;overflow:hidden;min-height:calc(1.45em * 2)}
.nws-card .d{margin-top:12px;font-size:14px;color:var(--faint);font-variant-numeric:tabular-nums}
.nws-card:hover h3{color:var(--brand-cta)}
.nws-empty{padding:40px 0;color:var(--faint);font-size:15px}
.nws-tabs{display:flex;gap:7px;flex-wrap:wrap;margin-top:22px}
.nws-tabs button{border:0;cursor:pointer;font-family:inherit;font-size:13.5px;font-weight:600;
padding:8px 15px;border-radius:99px;background:var(--soft);color:var(--gray)}
.nws-tabs button[aria-pressed=true]{background:var(--ink);color:#fff}
@media(max-width:960px){
  .nws-grid{grid-template-columns:1fr 1fr}
  .nws-row{grid-template-columns:1fr;gap:16px}
}
@media(max-width:640px){
  .nws-feat{grid-template-columns:1fr}
  .nws-grid{grid-template-columns:1fr;gap:34px}
}
"""
CSS += NEWS_CSS

# 인사이트 목록 규칙 중 **스포크와 공유할 것**만 추린다. 값은 NEWS_CSS 하나가 원본이고
# 여기서는 고르기만 한다 — 복사본을 만들지 않는다(2026-08-25).
_NWS_SHARE = ('.nws', '.nws-head', '.nws-feat', '.nws-fcard',
              '.nws-sec', '.nws-sec-h', '.nws-row', '.nws-rail', '.nws-empty')


def _pick_rules(css, roots):
    out = []
    for m in re.finditer(r'(?m)^(\.[a-zA-Z][\w -]*(?:::?[a-zA-Z-]+)?(?:\s+[.a-zA-Z][\w-]*)?)\{([^}]*)\}', css):
        sel = m.group(1).strip()
        base = sel.split(':')[0].split(' ')[0]
        if base in roots:
            out.append(m.group(0))
    for m in re.finditer(r'@media[^{]*\{(?:[^{}]*\{[^}]*\})+[^{}]*\}', css):
        if any(r + '{' in m.group(0) or r + ',' in m.group(0) or r + ' ' in m.group(0) for r in roots):
            out.append(m.group(0))
    return "\n".join(out)


NEWS_SHARED = _pick_rules(NEWS_CSS, _NWS_SHARE)

POST_CSS = """
/* ═══ 글 상세 — mark.the-moment.us/insights/ 구조 실측 이식(2026-08-23) ══════
   실측(1440): .post-grid cols 1fr/780px/240px · gap 43.2px · max-width 1560 · padding 0 56px
   toc x=56 w=200 · main x=321 w=780 · aside x=1144 w=240
   h1 64px/800/lh78 · sub 23.2px/lh37 · prose 16px/lh25.6 · h2 23.2px/800/mt38
   그전 우리 글은 본문이 좁고 태그 줄이 밖으로 튀어나갔다(대표 지적). */
/* 폭은 목록(/stories/, .nws max-width 1224)과 **똑같이** 맞춘다 — 상세만 좁으면
   같은 페이지를 오간다는 느낌이 깨지고 양옆 레일 정렬이 어긋나 보인다(2026-08-23 대표 지적).
   1224 = 목차 180 + 32 + 본문 1fr + 32 + 이어서읽기 220. 제목은 본문 칸에 얹어 좌변을 맞춘다. */
/* 본문 칸은 **목록의 본문 폭(1176 = .nws 1224 − 좌우 24)** 과 항상 같다.
   레일(목차·이어서읽기)은 그 바깥에 두고, 바깥에 자리가 없으면 접는다.
   ⚠️ 레일을 본문과 같은 폭 안에 욱여넣으면 본문이 712 로 쪼그라든다(2026-08-23 대표 지적). */
.pst{max-width:none;margin:0;padding:0}
.pst-top{grid-column:2;padding:var(--pg-top) 0 0}
/* 태그 줄은 위에 두지 않는다 — 아래 '이야기 전체 보기' 자리에 이미 있고, 제목 위에서
   가장 먼저 읽히기엔 정보가 아니다(2026-08-23 대표 지적). 분류만 한 줄. */
.pst-kick{font-size:13.5px;font-weight:700;letter-spacing:-.01em;color:var(--brand-cta)}
.pst-h1{margin-top:var(--pg-sub-gap);font-size:var(--pg-h1-post);font-weight:800;letter-spacing:-.05em;
line-height:1.22;color:var(--ink);text-wrap:balance}
/* 부제는 제목 바로 밑이 아니라 **표지 아래**에 — 큰 글씨가 연달아 두 덩이면 안 읽힌다. */
.pst-sub{margin-top:22px;font-size:clamp(16px,1.35vw,19px);line-height:1.72;color:var(--gray);
letter-spacing:-.02em;padding-left:16px;border-left:3px solid var(--line)}
/* 🚫 그리드·목차·이어서읽기 규칙을 여기 다시 적지 마라 — 정본은 SHELL_POST_CSS 의
   '글 상세 레이아웃' 한 곳이고, shell.css 가 이 파일보다 뒤에 실린다(2026-08-27 통합). */
/* 지은이·날짜·공유는 글을 다 읽은 뒤에 온다. 읽기 전에 필요한 정보가 아니다. */
.pst-meta{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;
margin-top:clamp(34px,4vw,54px);padding-top:22px;border-top:1px solid var(--line)}
.pst-by{display:flex;align-items:center;gap:11px}
.pst-by .av{width:38px;height:38px;border-radius:50%;background:var(--ink);color:#fff;
display:grid;place-items:center;font-size:15px;font-weight:800}
.pst-by .nm{font-size:14.5px;font-weight:700;color:var(--ink)}
.pst-by .dt{font-size:13.5px;color:var(--faint)}
.pst-share{display:flex;gap:7px}
.pst-share a{width:34px;height:34px;border-radius:50%;background:var(--soft);
display:grid;place-items:center;font-size:13px;font-weight:700;color:var(--gray)}
.pst-share a:hover{background:var(--ink);color:#fff}
.pst-cover{width:100%;aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:var(--soft)}
.pst-cover img{width:100%;height:100%;object-fit:cover;display:block}
.pst-prose{margin-top:clamp(26px,3vw,40px);font-size:16.5px;line-height:1.78;color:var(--ink2)}
.pst-prose h2{margin:38px 0 0;font-size:clamp(20px,1.9vw,23px);font-weight:800;
letter-spacing:-.035em;color:var(--ink)}
.pst-prose h3{margin:28px 0 0;font-size:18px;font-weight:700;letter-spacing:-.03em;color:var(--ink)}
.pst-prose p{margin-top:14px}
.pst-prose ul,.pst-prose ol{margin-top:14px;padding-left:20px}
.pst-prose li{margin-top:7px}
.pst-prose b,.pst-prose strong{color:var(--ink);font-weight:700}
.pst-prose blockquote{margin:22px 0;padding:14px 18px;background:var(--soft);border-radius:12px;
color:var(--gray)}
.pst-prose img{max-width:100%;border-radius:12px;margin-top:18px}
.pst-prose table{width:100%;border-collapse:collapse;margin-top:18px;font-size:15px;display:block;
overflow-x:auto}
.pst-prose th,.pst-prose td{border-bottom:1px solid var(--line);padding:10px 12px;text-align:left}
.pst-end{grid-column:2;grid-row:3;margin:clamp(44px,5vw,72px) 0 clamp(64px,8vw,110px);
padding-top:26px;border-top:1px solid var(--line);text-align:center}
/* 태그는 버튼이 아니다 — 배경을 깔지 않고 선만 준다(2026-08-23 대표 지적). */
.pst-tags{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.pst-tags a{display:inline-flex;align-items:center;height:34px;padding:0 14px;border-radius:99px;
background:none;box-shadow:inset 0 0 0 1px var(--line);
font-size:13.5px;font-weight:600;color:var(--gray)}
.pst-tags a:hover{box-shadow:inset 0 0 0 1px var(--ink);color:var(--ink)}
.pst-backwrap{display:flex;justify-content:center;margin-top:30px}
.pst-back{display:inline-flex;align-items:center;height:50px;padding:0 30px;border-radius:99px;
background:var(--ink);color:#fff;font-size:15.5px;font-weight:700;letter-spacing:-.02em}
.pst-back:hover{opacity:.86}
@media(max-width:1120px){.pst-end{grid-column:1}}
"""
CSS += POST_CSS

INQP_CSS = """
/* ═══ /inquiry/ — 소개·이야기와 같은 골격(2026-08-23) ══════════════════════
   그전엔 760px 짜리 폼 한 덩이가 허공에 떠 있어 다른 페이지와 따로 놀았다.
   컨테이너·제목 크기를 abt/nws 와 맞추고, 왼쪽에 '무엇을 물어도 되는지'를 둔다.
   ⚠️ 폼 마크업과 스크립트(#f · #go · #err · #iqRoot)는 손대지 않는다 — 제출이 그걸로 돈다. */
.iqp{max-width:1224px;margin:0 auto;padding:0 24px}
.iqp-head{padding:var(--pg-top) 0 var(--pg-head-gap)}
.iqp-head h1{font-size:clamp(32px,4.4vw,54px);font-weight:800;letter-spacing:-.05em;
line-height:1.1;color:var(--ink)}
.iqp-head p{margin-top:16px;font-size:17px;line-height:1.72;color:var(--gray);max-width:46ch}
.iqp-grid{display:grid;grid-template-columns:1fr 1.35fr;gap:clamp(24px,4vw,64px);
padding-bottom:clamp(72px,9vw,130px)}
.iqp-side{align-self:start}
.iqp-fact{display:flex;align-items:baseline;gap:10px;padding:14px 0;border-top:1px solid var(--line)}
.iqp-fact b{font-size:20px;font-weight:800;letter-spacing:-.04em;color:var(--ink);white-space:nowrap}
.iqp-fact span{font-size:14.5px;color:var(--gray)}
.iqp-ex{margin-top:26px;list-style:none;padding:0;display:flex;flex-direction:column;gap:9px}
.iqp-ex li{position:relative;padding-left:16px;font-size:15px;line-height:1.6;color:var(--ink2)}
.iqp-ex li::before{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;
border-radius:50%;background:var(--faint)}
.iqp-mail{margin-top:26px;font-size:14px;color:var(--faint)}
.iqp-mail a{color:var(--ink);font-weight:600;text-decoration:underline;text-underline-offset:3px}
.iqp-form{background:var(--soft);border-radius:18px;padding:clamp(22px,2.8vw,36px)}
.iqp-form>p{margin-top:18px;font-size:13.5px;line-height:1.7;color:var(--faint)}
.iqp-form>p a{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
@media(max-width:860px){.iqp-grid{grid-template-columns:1fr;gap:26px}}
"""
CSS += INQP_CSS

FLIP_CSS = """
/* ═══ 제품 랜딩(앱형) — toss.im/service/teenagers 구조 실측 이식(2026-08-24) ═════
   실측(1440): 컨테이너 x108 w1224 · 히어로 = 작은 라벨 + 좌측 큰 제목 + 우측 문단 +
   전면 라운드 이미지 · 이후 번호 섹션(01,02..) 이 좌우 번갈아, 가운데 제목 + 카드 3장.
   ⚠️ 폭·간격은 공용 토큰(--pg-top 등)을 그대로 본다 — 다른 페이지와 리듬이 같아야 한다. */
.fl{max-width:1224px;margin:0 auto;padding:0 24px}
.fl-hero{padding:var(--pg-top) 0 0}
.fl-kick{font-size:14px;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.fl-hero-in{display:grid;grid-template-columns:1.25fr .75fr;gap:clamp(20px,4vw,64px);
align-items:end;margin-top:14px}
.fl-hero h1{font-size:clamp(32px,4.8vw,60px);font-weight:800;letter-spacing:-.055em;
line-height:1.14;color:var(--ink)}
.fl-hero .lede{font-size:16px;line-height:1.75;color:var(--gray)}
.fl-shot{margin-top:clamp(26px,3.4vw,44px);border-radius:24px;overflow:hidden;
background:var(--soft);aspect-ratio:16/9}
.fl-shot img,.fl-shot video{width:100%;height:100%;object-fit:cover;display:block}
.fl-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:clamp(20px,2.6vw,30px)}
.fl-btn{display:inline-flex;align-items:center;gap:9px;height:52px;padding:0 26px;
border-radius:99px;background:var(--ink);color:#fff;font-size:16px;font-weight:700;
letter-spacing:-.02em}
.fl-btn:hover{opacity:.86}
.fl-btn--line{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--line)}
.fl-btn--line:hover{background:var(--soft);opacity:1}
.fl-note{margin-top:12px;font-size:13.5px;color:var(--faint)}

/* 번호 섹션 — 좌우 번갈아 */
.fl-sec{padding:clamp(56px,8vw,120px) 0 0}
.fl-row{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,5vw,80px);align-items:center}
.fl-row--flip .fl-row-tx{order:2}
.fl-num{display:inline-flex;align-items:center;justify-content:center;min-width:38px;height:28px;
padding:0 11px;border-radius:99px;background:var(--soft);
font-family:var(--mono);font-size:12.5px;font-weight:700;color:var(--gray)}
.fl-row h2{margin-top:16px;font-size:clamp(24px,3vw,40px);font-weight:800;letter-spacing:-.05em;
line-height:1.16;color:var(--ink)}
.fl-row p{margin-top:16px;font-size:16.5px;line-height:1.75;color:var(--gray);max-width:44ch}
.fl-art{border-radius:20px;overflow:hidden;background:var(--soft);aspect-ratio:4/3}
.fl-art img{width:100%;height:100%;object-fit:cover;display:block}

/* 가운데 제목 + 카드 3장 */
.fl-mid{text-align:center;padding:clamp(56px,8vw,120px) 0 0}
.fl-mid h2{margin-top:14px;font-size:clamp(24px,3vw,40px);font-weight:800;letter-spacing:-.05em;
line-height:1.2;color:var(--ink)}
.fl-mid p{margin:14px auto 0;font-size:16.5px;line-height:1.75;color:var(--gray);max-width:46ch}
.fl-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(12px,1.6vw,20px);
margin-top:clamp(26px,3.4vw,44px)}

/* ── 연출 = 애플 macbook-air 식 **큰 장면 블록** ─────────────────────────
   실측(apple.com/macbook-air): 미디어 블록 696~980px · 라운드 28px · 한 화면에 하나,
   글은 그림 아래 넉넉한 여백. 작은 격자로 늘어놓지 않는다(2026-08-24 대표 지적).
   ⚠️ 8번째로 앱 화면을 끼워 두었다가 "덩그러니" 소리를 들었다 — 연출만 넣는다. */
.fl-scenes{display:flex;flex-direction:column;gap:clamp(40px,6vw,96px);
margin-top:clamp(30px,4vw,56px);text-align:left}
.fl-scene{display:grid;grid-template-columns:1fr;gap:0}
.fl-scene figure{margin:0;border-radius:28px;overflow:hidden;background:var(--soft)}
.fl-scene img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.fl-scene .tx{padding:clamp(18px,2.2vw,28px) 4px 0;max-width:52ch}
.fl-scene b{display:block;font-size:clamp(19px,1.9vw,25px);font-weight:800;letter-spacing:-.04em;
color:var(--ink)}
.fl-scene p{margin-top:10px;font-size:16px;line-height:1.72;color:var(--gray)}
/* 두 장씩 나란히 — 좁은 장면은 짝으로 묶어 리듬을 만든다(애플도 이 둘을 섞는다) */
.fl-duo{display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,1.8vw,24px)}
.fl-duo .fl-scene img{aspect-ratio:4/3}
@media(max-width:860px){.fl-duo{grid-template-columns:1fr;gap:clamp(28px,5vw,44px)}}

/* ── 볼륨키를 누르면 페이지가 올라간다 — 말로 설명하는 대신 보여준다 ──
   ⚠️ 2026-08-24: 갤러리 CSS 를 갈아 끼울 때 이 블록이 같이 지워졌다(마크업만 남아 무스타일).
      CSS 를 '어느 주석 앞'에 끼우고 나중에 그 주석까지 포함해 구간을 교체하면 이렇게 된다.
      블록을 지울 땐 지우는 구간에 남의 것이 섞여 있지 않은지 먼저 확인해라. */
.fl-demo{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,5vw,80px);align-items:center;
padding:clamp(56px,8vw,120px) 0 0}
.fl-phone{position:relative;width:min(280px,80%);margin:0 auto;aspect-ratio:9/19.5;
border-radius:34px;background:#0b0c0e;padding:9px;box-shadow:0 30px 60px -30px rgba(0,0,0,.5)}
.fl-phone .scr{position:relative;width:100%;height:100%;border-radius:26px;overflow:hidden;
background:var(--paper)}
.fl-phone .strip{position:absolute;inset:0;display:flex;flex-direction:column}
.fl-phone .strip span{flex:0 0 50%;display:grid;place-items:center;font-size:44px;font-weight:800;
letter-spacing:-.05em;color:var(--ink2);background:var(--soft)}
.fl-phone .strip span:nth-child(even){background:var(--soft2)}
.fl-phone .vk{position:absolute;right:-4px;top:24%;width:4px;height:64px;border-radius:3px;
background:#2b2f36}
.fl-phone .vk::after{content:"";position:absolute;inset:-9px -13px;border-radius:10px;
background:var(--brand-cta);opacity:0}
@media(prefers-reduced-motion:no-preference){
  .fl-phone .strip{animation:flstrip 3.2s cubic-bezier(.7,0,.2,1) infinite}
  .fl-phone .vk::after{animation:flkey 3.2s ease infinite}
}
@keyframes flstrip{
  0%,26%{transform:translateY(0)}
  34%,58%{transform:translateY(-50%)}
  66%,92%{transform:translateY(-100%)}
  100%{transform:translateY(-100%)}
}
@keyframes flkey{0%,22%{opacity:0}26%,30%{opacity:.55}34%,54%{opacity:0}
58%,62%{opacity:.55}66%,100%{opacity:0}}
.fl-demo-tx h2{font-size:clamp(24px,3vw,40px);font-weight:800;letter-spacing:-.05em;
line-height:1.16;color:var(--ink);margin-top:16px}
.fl-demo-tx p{margin-top:16px;font-size:16.5px;line-height:1.75;color:var(--gray);max-width:44ch}
@media(max-width:860px){.fl-demo{grid-template-columns:1fr;gap:26px}}

/* 설정 카드 — 스크린샷을 기기 틀에 끼운다(맨 이미지로 두면 화면인지 사진인지 모른다) */
.fl-card{background:var(--soft);border-radius:20px;overflow:hidden;text-align:left;
padding:clamp(22px,2.6vw,32px) clamp(18px,2vw,24px) 0}
.fl-card .fr{display:block;width:min(210px,84%);margin:0 auto;border-radius:26px;background:#0b0c0e;
padding:7px;box-shadow:0 22px 44px -24px rgba(0,0,0,.5)}
.fl-card .fr img{width:100%;aspect-ratio:1248/1972;object-fit:cover;object-position:top;
border-radius:20px;display:block}
.fl-card .cap{padding:20px 2px 22px}
.fl-card b{display:block;font-size:15.5px;font-weight:700;letter-spacing:-.03em;color:var(--ink)}
.fl-card i{display:block;font-style:normal;font-size:13.5px;color:var(--gray);margin-top:5px}

/* 사양표 */
.fl-spec{margin-top:clamp(26px,3.4vw,44px);width:100%;border-collapse:collapse;
max-width:760px;margin-left:auto;margin-right:auto;text-align:left}
.fl-spec th,.fl-spec td{border-bottom:1px solid var(--line);padding:15px 4px;font-size:15px;
vertical-align:top}
.fl-spec th{width:34%;font-weight:600;color:var(--gray)}
.fl-spec td{color:var(--ink);font-family:var(--mono);font-size:14px}
.fl-end{padding:clamp(56px,8vw,120px) 0 clamp(72px,9vw,130px);text-align:center}
.fl-end h2{font-size:clamp(26px,3.4vw,46px);font-weight:800;letter-spacing:-.055em;
line-height:1.14;color:var(--ink)}
.fl-end .fl-cta{justify-content:center}
@media(max-width:860px){
  .fl-hero-in{grid-template-columns:1fr;gap:16px;align-items:start}
  .fl-row{grid-template-columns:1fr;gap:20px}
  .fl-row--flip .fl-row-tx{order:0}
  .fl-cards{grid-template-columns:1fr}
}
"""
CSS += FLIP_CSS

# CSS 캐시 버스팅 — Cloudflare가 /assets/site.css를 max-age=14400(4시간) 캐시한다.
# 내용이 바뀌면 URL도 바뀌게 해서 즉시 반영시킨다.
# ── 클래스 충돌 감시 ───────────────────────────────────────────────────────
#   같은 클래스 이름을 서로 다른 곳에서 기본 규칙(.foo{...})으로 두 번 정의하면
#   뒤엣것이 앞엣것을 덮어 레이아웃이 조용히 깨진다. 2026-08-23 하루에만 네 번 겪었다
#   (.pcard → /products/ 폭 붕괴, .ap → 홈 폭 760px, .ab → 소개 문단에 100px 패딩,
#    .pgrid → 3분할 강제). 새 컴포넌트는 **안 쓰는 접두사**로 시작하고, 그래도 겹치면
#   여기서 잡는다. 비파괴 — 경고만 찍는다.
def _strip_at_blocks(css):
    """@media/@supports 안쪽은 의도된 재정의라 중복이 아니다 — 통째로 걷어낸다."""
    out, i = [], 0
    while i < len(css):
        a = css.find("@", i)
        if a < 0:
            out.append(css[i:]); break
        b = css.find("{", a)
        if b < 0:
            out.append(css[i:]); break
        out.append(css[i:a])
        depth, j = 1, b + 1
        while j < len(css) and depth:
            if css[j] == "{": depth += 1
            elif css[j] == "}": depth -= 1
            j += 1
        i = j
    return "".join(out)


def _decl_props(block):
    """선언 블록에서 프로퍼티 이름만 뽑는다. 괄호 안 세미콜론·콜론(url·gradient)은 건너뛴다."""
    props, buf, depth = [], [], 0
    for ch in block:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == ";" and depth == 0:
            props.append("".join(buf)); buf = []
        else:
            buf.append(ch)
    props.append("".join(buf))
    out = []
    for d in props:
        name = d.split(":", 1)[0].strip().lower()
        if name:
            out.append(name)
    return out


def _warn_dup_selectors(css):
    """같은 클래스가 두 번 나오는 것만으로는 경고하지 않는다 — **같은 프로퍼티가 겹칠 때만**.

    왜 좁혔나 (2026-08-25): 종전엔 '같은 선택자가 2곳'이면 전부 경고해서, 프로퍼티가 하나도
    안 겹치는 의도된 분할(.gnb 는 크롬 층 여백을 따로 두고, .ap-qa 는 max-width 만 따로 준다)까지
    매 빌드마다 울렸다. 경고가 상시로 켜져 있으면 그건 신호가 아니라 배경 소음이 되고,
    **진짜 충돌이 섞여 들어와도 안 보인다.**

    잡아야 할 것은 '앞엣것을 고쳐도 안 먹는' 상태다 = 같은 프로퍼티를 뒤에서 다시 선언한 경우.
    값이 같아도 경고한다 — 앞을 고치면 여전히 안 먹으므로 함정은 똑같다.
    순수 문자열 파싱이라 자연어 판단이 아니다(룰 #1 무관). 비파괴 — 경고만 찍는다.
    """
    import collections
    seen = collections.defaultdict(list)
    for m in re.finditer(r'(^|[}\n])\s*(\.[a-zA-Z][\w-]*)\s*\{([^}]*)\}', _strip_at_blocks(css)):
        seen[m.group(2)].append(m.group(3).strip())
    dups = {}
    for k, blocks in sorted(seen.items()):
        if len(blocks) < 2:
            continue
        counts = collections.Counter()
        for b in blocks:
            counts.update(set(_decl_props(b)))
        clash = sorted(p for p, n in counts.items() if n > 1)
        if not clash:
            continue                      # 프로퍼티가 안 겹친다 = 의도된 분할. 조용히 넘어간다
        dups[k] = blocks
        head = ", ".join(clash[:4]) + (" 외 %d개" % (len(clash) - 4) if len(clash) > 4 else "")
        print(f"  ⚠️ 클래스 중복 정의: {k} ({len(blocks)}곳) — 겹치는 프로퍼티: {head}. 앞엣것을 고쳐도 안 먹습니다")
    return dups


_warn_dup_selectors(CSS)

CSS_VER = hashlib.md5(CSS.encode("utf-8")).hexdigest()[:8]

# 본문 서체 = Pretendard(OFL-1.1) 자체 호스팅. assets/fonts/pretendard/ 는 정적 파일이라
# 이 생성기가 만들지 않는다 — npm 패키지 dist 를 그대로 커밋해 둔 것이다.
#   · 동적 서브셋(92청크)을 쓴다. 통짜 variable 은 2MB 라 모든 방문자가 다 받는다.
#     서브셋은 페이지에 실제 나온 글자 구간만 받아 한글 랜딩 기준 200~350KB 수준.
#   · 갱신 절차: npm pack pretendard → dist/web/variable/woff2-dynamic-subset/*.woff2 를
#     assets/fonts/pretendard/ 로, 같은 폴더 CSS 의 url() 을 /assets/fonts/pretendard/ 로
#     바꿔 assets/fonts/pretendard.css 로 저장 → 아래 FONT_VER 을 올린다.
FONT_VER = "1.3.9"

def purl(slug):
    """제품 페이지 주소 — 무료 도구는 /tools/, 유료 스포크는 /products/.
       무료 도구를 본 도메인 경로에 두는 이유는 PLATFORM_TOPOLOGY §5(미끼의 유입 권위)."""
    return f"/tools/{slug}/" if slug in TOOLS else f"/products/{slug}/"


def bar_items(active=""):
    """1단 바 **최상위** 항목 = (라벨, href, 트리거여부, 활성여부, 구분선앞).
       제품 이름들은 여기 없다 — '제품' 플라이아웃 안에 있다(2026-08-23).
       ⚠️ 활성 상태를 라벨로 하드코딩하지 않는다(nav-active-no-hardcode)."""
    active = {"j": "story", "a": "about", "p": "products"}.get(active, active)
    out = []
    for i, l in enumerate(BAR["links"]):
        out.append(dict(label=l["label"], href=l["href"], sub="", ext=False,
                        on=(active == l["key"]), sep=(l["key"] == "story"),
                        trg=(l["key"] == "products")))
    return out


def prod_shot(sl):
    """제품의 대표 그림 — 홈 배너·GNB 더보기·제품 목록이 **같은 것**을 쓴다.
       ⚠️ 세 곳이 각자 다른 소스를 보고 있어 목록만 옛 og 배너였다(2026-08-24 대표 지적).
          우선순위: 홈 배너용 컷 → 제품 shot. 여기 하나만 고치면 세 곳이 같이 바뀐다."""
    return HOME_SHOT.get(sl) or (P.get(sl, {}).get("shot") or "")


# ⚠️ 전부 **우리 자산으로 복사**해 둔다 — dev.heyreci.com 같은 주소는 언제 사라질지 모른다
#   (2026-08-23 대표: "그 주소 영상은 안 없어질 것 같거든, 복사든지 일단 넣고").
#   헤이레시 영상은 원본 28.5MB/1920px → 1600px·CRF30·무음으로 2.4MB. Workers 자산 상한이
#   한 파일 25MiB 라 원본 그대로는 배포조차 안 된다.
HOME_SHOT = {
    "mark": "/assets/home/mark.webp",
    "cue": "/assets/home/cue.png",
    "theplan": "/assets/home/theplan.png",
    "kontext": "/assets/home/kontext.jpg",
    # 홈 배너는 영상이지만 목록·더보기엔 정지컷이 필요하다(영상 5초 프레임).
    "heyreci": "/assets/home/heyreci.jpg",
    "flipper": "/assets/flipper/hero.png",
    "teamai": "/assets/home/teamai.jpg",
}
HOME_VIDEO = {"heyreci": "/assets/home/heyreci-hero.mp4"}


def bar_products():
    """플라이아웃·모바일 목록에 들어갈 제품.
       ⚠️ 스포크(자체 도메인)만 보면 **앱형 제품이 빠진다** — 플리퍼가 그래서 안 나왔다
          (2026-08-24). 자체 도메인이 없는 제품은 our 경로를 href 로 만들어 함께 싣는다."""
    out = [sp for sp in BAR["spokes"] if not sp.get("hidden")]
    have = {sp.get("slug") for sp in out}
    for sl, pr in P.items():
        if sl in have or pr.get("type") != "app":
            continue
        out.append({"slug": sl, "label": pr["short"],
                    "href": "https://the-moment.us" + purl(sl),
                    "sub": pr.get("tagline", "")})
    return out


def bar_html(active=""):
    parts = []
    for it in bar_items(active):
        if it["sep"]:
            parts.append('<span class="sep" aria-hidden="true"></span>')
        attrs = ""
        if it["sub"]:
            attrs += f' data-sub="{it["sub"]}"'
        if it["ext"]:
            attrs += ' target="_blank" rel="noopener" class="ext"'
        if it["on"]:
            attrs += ' aria-current="page"'
        tail = '<i aria-hidden="true">↗</i>' if it["ext"] else ""
        parts.append(f'<a href="{it["href"]}"{attrs}>{it["label"]}{tail}</a>')
    return "\n    ".join(parts)


def gnb(active=""):
    return f"""<header class="gnb">
  <a class="wm" href="/">MOMENTUS</a>
  <nav class="lk" aria-label="모멘터스">
    {bar_html(active)}
  </nav>
</header>"""

# ---------- 사업자 정보 (단일 소스) ----------
BIZ = dict(
    name="모멘터스 (MOMENTUS)",
    ceo="박진이",
    reg="113-34-00602",
    mail_order="2024-서울양천-1300호",
    addr="서울특별시 양천구 신월로 99",
    tel="010-7613-7327",  # 표기는 유지(통신판매업 표시사항) — 단, 상담 채널은 이메일 전용으로 안내
    email="hello.momentus@gmail.com",
    privacy_officer="강형모",
    updated="2026. 07. 28",
)
# 🔴 전화번호는 통신판매업 표시사항이라 **뺄 수 없다.** 대신 번호가 나오는 자리마다
#    "전화 상담은 안 한다"를 **번호와 한 덩어리로, 굵게** 붙인다(2026-08-26 대표 지시).
#    번호만 덩그러니 있으면 전화가 오고, 안 받으면 그게 더 나쁜 경험이 된다.
#    ⚠️ 번호가 보이는 모든 페이지에 적용한다 — 여기 한 곳만 고치면 생성물 전체가 따라온다.
# 굵게 제거(2026-08-27 대표 지시). pay(notes/web/src/pay_app.js BIZ.telHtml)와 같은 문장이어야
# 한다 — PG 심사에서 두 사이트 표시가 다르면 잡힌다. 바꿀 땐 반드시 양쪽 다.
BIZ["tel_html"] = f"전화 상담({BIZ['tel']})은 운영하지 않습니다"

# 푸터 제품·도구 목록도 매니페스트 파생 — 하드코딩 목록은 2026-07-27 폐기(새 제품 = 한 줄).
_FT_SPOKES = "".join(f'<a href="{purl(s)}">{P[s]["name"]}</a>' for s in SPOKES)
_FT_TOOLS = "".join(f'<a href="{purl(s)}">{P[s]["short"]}</a>' for s in TOOLS)

FOOTER = f"""<footer class="site">
  <div class="brand"><div class="wm">MOMENTUS</div><p>쓸모 있는 것만<br>만듭니다.</p></div>
  <div><h4>제품</h4>{_FT_SPOKES}</div>
  <div><h4>무료 도구</h4>{_FT_TOOLS}</div>
  <!-- 🚫 문의하기를 mailto 로 되돌리지 마라 — 2026-08-07. mailto 는 기록이 아무 데도 안 남아
       봇도 못 보고 이력도 없었다. 창구는 /inquiry/ 하나다(단일 원장 inquiries). -->
  <div><h4>모멘터스</h4><a href="/insights/">인사이트</a><a href="/about/">소개</a><a href="/inquiry/">문의하기</a><a href="/how-to-pay/">결제 안내</a><a href="/legal/terms/">이용약관</a><a href="/legal/privacy/">개인정보처리방침</a><a href="/legal/refund/">환불 규정</a></div>
  <div class="biz">
    <span>{BIZ['name']}</span><span>대표 {BIZ['ceo']}</span><span>사업자등록번호 {BIZ['reg']}</span><span>통신판매업신고 {BIZ['mail_order']}</span>
    <span>{BIZ['addr']}</span><span>{BIZ['tel_html']}</span><span>{BIZ['email']}</span><span>개인정보보호책임자 {BIZ['privacy_officer']}</span>
    <span>고객 문의는 이메일로만 받습니다. 이메일로 주시면 가장 빠르게 도와드릴 수 있습니다.</span>
  </div>
  <div class="legal"><span>© 2026 모멘터스</span><span>the-moment.us</span></div>
</footer>"""

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "모멘터스",
    "alternateName": "MOMENTUS",
    "url": "https://the-moment.us",
    "email": BIZ["email"],
    "telephone": BIZ["tel"],
    "description": "AI로 제품을 만드는 스튜디오. AI 상품사진(헤이레시), 로고 디자인(마크), 디지털 플래너(더플랜), AI 모의면접(큐)을 만들어 팔고, 브라우저 도구 6종을 무료로 제공합니다.",
    "address": {"@type": "PostalAddress", "addressLocality": "서울", "streetAddress": BIZ["addr"], "addressCountry": "KR"},
    "founder": {"@type": "Person", "name": "강형모"},
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@type": "SoftwareApplication", "name": "헤이레시 — AI 상품사진 생성", "applicationCategory": "DesignApplication", "url": "https://heyreci.com"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "마크 — 업종별 로고 디자인", "url": "https://mark.the-moment.us"}},
        {"@type": "Offer", "itemOffered": {"@type": "Product", "name": "더플랜 — 디지털 플래너", "url": "https://notes.the-moment.us"}},
        {"@type": "Offer", "itemOffered": {"@type": "SoftwareApplication", "name": "큐 — AI 모의면접", "applicationCategory": "EducationalApplication", "url": "https://cue.the-moment.us"}},
    ],
}, ensure_ascii=False)


def _toolfix(html):
    """무료 도구 주소가 /products/<slug>/ 로 하드코딩된 곳을 /tools/<slug>/ 로 정규화.
       (랜딩 그리드 등 f-string 이 아닌 리터럴 블록에 남은 링크를 놓치지 않기 위한 안전망)"""
    for t in TOOLS:
        html = html.replace(f'"/products/{t}/"', f'"/tools/{t}/"')
    return html


AGENTATION = """
<!-- Agentation(UI 주석 → AI 에이전트 컨텍스트) — notes·mark 와 같은 옵트인 블록.
     ?agent=1 로 켜면 유지, ?agent=0 로 끔. 옵트인 전에는 아무것도 로드하지 않아 방문자엔 무부담.
     apex 에만 빠져 있었다(2026-07-27 사장님 지적). -->
<script type="module">
(function(){
  try{
    var q=new URLSearchParams(location.search);
    if(q.has("agent")){var v=q.get("agent");localStorage.setItem("agentation",(v===""||v==="1"||v==="on")?"1":"0");}
  }catch(e){}
  if((localStorage.getItem("agentation")||"")!=="1")return;
  var root=document.getElementById("agentation-root");
  if(!root){root=document.createElement("div");root.id="agentation-root";document.body.appendChild(root);}
  var V="18.3.1";
  Promise.all([
    import("https://esm.sh/react@"+V),
    import("https://esm.sh/react-dom@"+V+"/client"),
    import("https://esm.sh/agentation@3?deps=react@"+V+",react-dom@"+V)
  ]).then(function(m){
    var React=m[0].default||m[0];
    var createRoot=(m[1].createRoot||(m[1].default&&m[1].default.createRoot));
    var Ag=m[2].Agentation||(m[2].default&&(m[2].default.Agentation||m[2].default));
    if(!createRoot||!Ag){console.warn("[agentation] API 형태 예상과 다름",m);return;}
    createRoot(root).render(React.createElement(Ag));
    console.log("[agentation] 설치됨(apex) — 끄려면 ?agent=0");
  }).catch(function(err){console.warn("[agentation] 로드 실패(네트워크/CDN):",err);});
})();
</script>"""




def _faq_html(p):
    """제품 FAQ 를 본문에 렌더한다. 소재는 data/products.json 의 faq.

       왜 본문에 넣나: GEO 는 '답이 페이지에 그대로 박혀 있는가'로 갈린다.
       질문형 헤딩 + 40~60단어 답이 AI 가 인용하는 단위다(docs/SEO_GEO.md §6).
       ⚠️ FAQPage 스키마만 넣고 화면에 안 보이면 구글 스팸 정책 위반이다 —
          그래서 스키마가 아니라 **본문이 먼저**다. 스키마는 이 HTML 에서 파생된다."""
    faq = p.get("faq") or []
    if not faq:
        return ""
    items = "".join(
        f'<div class="vd-qa-i"><h3>{q}</h3><p>{a}</p></div>' for q, a in faq)
    return f'<section class="vd-qa"><h2>자주 묻는 질문</h2>{items}</section>'


def _re_desc(t, lo=70, hi=120):
    """meta description 만들기 — 태그를 벗기고 문장 경계에서 자른다.
       hi 를 넘기면 검색결과에서 잘리고, lo 에 못 미치면 구글이 무시한다."""
    t = " ".join(re.sub(r"<[^>]+>", " ", t or "").split()).replace('"', "'")
    if len(t) <= hi:
        return t
    cut = t[:hi]
    for mark in (". ", "? ", "! ", "다. ", " "):     # 문장 끝 우선, 없으면 어절 경계
        i = cut.rfind(mark)
        if i >= lo:
            return cut[:i + len(mark)].strip()
    return cut.strip()


# 다크모드 — 그리기 전에 결정해서 흰 화면 번쩍임(FOUC)을 막는다. 반드시 blocking.
THEME_BOOT = """<script>
(function(){try{var t=localStorage.getItem('mmt-theme');
if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.dataset.theme=t;}catch(e){}})();
</script>"""

# ── 애널리틱스 ─────────────────────────────────────────────────────────
#   2026-08-24. apex 에만 없었다(마크 G-0MZD2HR8Y3 · 큐 G-QSHEQZ8V9C 는 이미 붙어 있음).
#   ⚠️ GA_ID 는 **apex 전용 속성**이어야 한다 — 다른 사이트 것을 재사용하면 데이터가 섞인다.
#      아직 못 받아서 빈 값이다. 값이 들어오면 그 줄 하나만 채우면 전부 켜진다.
#   바깥으로 나가는 클릭(제품 사이트·스토어)을 outbound 이벤트로 남긴다 —
#   "어느 배너에서 어디로 갔나"를 봐야 랜딩이 일을 하는지 알 수 있다.
# MOMENTUS 계정(405789423) · the-moment.us 속성(551281263) · apex 스트림(15491123505)
#   ⚠️ **apex 전용**이다. 마크(G-0MZD2HR8Y3)·큐(G-QSHEQZ8V9C) 것을 여기 넣지 마라 — 섞인다.
GA_ID = "G-1T66ZV28MB"

ANALYTICS = ("" if not GA_ID else f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());gtag('config','{GA_ID}');
</script>""") + """<script>
/* 바깥 클릭 추적 — GA 가 없어도 죽지 않는다(gtag 있을 때만 보낸다). */
(function(){
  addEventListener('click',function(e){
    var a=e.target.closest('a[href]'); if(!a) return;
    var h=a.getAttribute('href')||'';
    if(!/^https?:/.test(h)) return;
    var host=''; try{ host=new URL(h,location.href).hostname }catch(x){ return }
    if(host===location.hostname) return;
    var kind = /play[.]google[.]com/.test(h) ? 'store'
             : /the-moment[.]us|heyreci[.]com/.test(host) ? 'product' : 'external';
    // 어느 자리에서 눌렀는지 — 배너·더보기·목록을 구분해야 쓸모가 있다.
    var where = a.closest('.stg') ? 'banner'
              : a.closest('.mmt-fly') ? 'nav-more'
              : a.closest('.prh-row') ? 'product-list'
              : a.closest('#mmt-bar') ? 'nav' : 'body';
    if(window.gtag) gtag('event','outbound',{link_domain:host,link_url:h,
      link_kind:kind,link_where:where,link_text:(a.innerText||'').trim().slice(0,60)});
  },{capture:true});
})();

/* 북마크릿 "가져감" 추적 (2026-08-30, 2026-08-31 속성 분리).
   ★ 왜 필요한가 — 북마크릿은 **남의 사이트 안**에서 돈다. 인스타는 CSP 로
     script-src·connect-src·img-src 를 전부 막아서 도구 안에서는 어떤 방법으로도
     못 잰다(실측). 그래서 우리가 확실히 셀 수 있는 자리는 **여기, 우리 도메인**이다.
   드래그 = 실제 설치 몸짓. 클릭 = 설치 의도(안내 alert 로 끝난다).
   둘을 구분해 둬야 "안내를 못 읽어서 클릭만 하고 떠난" 손실이 보인다.

   ★ 어디로 보내나 — **무료 도구 (북마크릿)** 속성(G-T8Y89D206F) **한 곳**이다.
     창업자 지시(2026-08-31): 도구가 몇 개로 늘어도 속성은 하나, 안에서 `tool` 로 가른다.
     실행(tool_run, 픽셀→워커)도 같은 속성이라 **가져감→실행 전환율이 한 화면**에 있다.
     apex 로도 보내면 같은 사건이 두 속성에 이중 계상되므로 보내지 않는다.
   ⚠️ send_page_view:false — 이 설정은 오직 tool_install 을 실어 나르는 통로다.
     빼면 the-moment.us 전 페이지뷰가 도구 속성에도 쌓여 숫자가 못 쓰게 된다. */
(function(){
  var TOOLS_ID='G-T8Y89D206F';
  var configured=false;
  function ready(){
    if(configured || !window.gtag) return configured;
    gtag('config',TOOLS_ID,{send_page_view:false});
    configured=true; return true;
  }
  function send(a,how){
    if(!ready()) return;
    var t=a.getAttribute('data-bm')||'';
    /* 이벤트 이름에 도구를 박는다 — 실시간 보고서가 맞춤 측정기준을 안 받기 때문이다.
       (창업자 2026-08-31: "툴이 실행되었다가 아니라 그 툴이 뭐냐고")
       이름은 영문·숫자·밑줄만 되므로 하이픈을 바꾼다. tool 매개변수도 함께 보낸다. */
    gtag('event',t.replace(/-/g,'_')+'_install',{send_to:TOOLS_ID,
      tool:t,method:how,
      link_where:a.closest('.dock')?'dock':'body'});
  }
  function pick(e){ return e.target && e.target.closest ? e.target.closest('a[data-bm]') : null }
  addEventListener('dragstart',function(e){var a=pick(e); if(a) send(a,'drag')},{capture:true});
  addEventListener('click',   function(e){var a=pick(e); if(a) send(a,'click')},{capture:true});
})();
</script>"""


TOP_BTN = ('<button class="kb-top" id="kbtop" aria-label="맨 위로">'
           '<svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>')


def page(title, desc, body, active="", extra="", header=None, body_class="kbp", head_extra=""):
    """header/body_class/head_extra 는 랜딩(KB 구성 클론) 전용 훅 —
       기본값이면 지금까지와 완전히 동일한 출력이라 다른 페이지엔 영향이 없다."""
    body = _toolfix(body)
    _bc = f' class="{body_class}"' if body_class else ""
    _hd = APEX_HEADER if header is None else header
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MOMENTUS">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="stylesheet" href="/assets/fonts/pretendard.css?v={FONT_VER}">
<link rel="stylesheet" href="/assets/momentus.css">
<link rel="stylesheet" href="/assets/site.css?v={CSS_VER}">
<link rel="stylesheet" href="/shell.css">
<script type="application/ld+json">{JSONLD}</script>
{THEME_BOOT}
{ANALYTICS}
<script defer src="/assets/apex.js?v={CSS_VER}"></script>
{head_extra}</head>
<body{_bc}>
{_hd}
<main>
{body}
</main>
{FOOTER}
{TOP_BTN}
{AGENTATION}
{extra}</body>
</html>"""

YT_URL = "https://www.youtube.com/@momentus"   # TODO: 실제 채널 주소로 교체
YT_CHANNEL_ID = ""                            # UC... 를 넣으면 RSS 자동 연동 켜짐


def fetch_youtube(channel_id, limit=12):
    """유튜브 공개 RSS에서 최신 영상을 읽는다. API 키 불필요.
    채널 ID가 없거나 네트워크가 막히면 조용히 빈 목록 — 빌드는 절대 안 깨진다."""
    if not channel_id:
        return []
    import urllib.request, xml.etree.ElementTree as ET
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            root = ET.fromstring(r.read())
    except Exception as e:
        print(f"  ⚠️ 유튜브 RSS 실패({e}) — 영상 없이 빌드합니다")
        return []
    ns = {"a": "http://www.w3.org/2005/Atom", "m": "http://search.yahoo.com/mrss/",
          "yt": "http://www.youtube.com/xml/schemas/2015"}
    out = []
    for e in root.findall("a:entry", ns)[:limit]:
        vid = e.findtext("yt:videoId", "", ns)
        pub = e.findtext("a:published", "", ns)[:10].replace("-", ". ")
        out.append(dict(
            kind="video", id=vid,
            title=e.findtext("a:title", "", ns),
            date=pub,
            url=f"https://www.youtube.com/watch?v={vid}",
            thumb=f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            desc=(e.find("m:group/m:description", ns).text or "")[:110] if e.find("m:group/m:description", ns) is not None else "",
        ))
    return out


VIDEOS = fetch_youtube(YT_CHANNEL_ID)

DRAG_MSG = "클릭이 아니라 북마크바로 끌어놓으세요."
# ⚠️ 드래그하면 **버튼 글자가 그대로 북마크 이름**이 된다(2026-09-01 창업자 지적).
#    그래서 안내문("북마크바로 드래그")을 버튼 글자에 넣으면 안 된다 — 툴팁으로 뺀다.
#    버튼 글자 = data/products.json 의 bmname(북마크바에 남을 이름).
# 안내를 글로 쓰지 않는다 — 버튼 위에 뜨는 그림(DRAG_DEMO)이 "끌어놓으면 짠" 을 보여준다.
# 버튼 글자는 곧 북마크 이름이라 안내문을 넣을 수 없고(2026-09-01), 기본 title 툴팁은
# 1~2초 늦게 OS 스타일로 떠서 사실상 안 보였다. aria-label 로 스크린리더만 챙긴다.
DRAG_ATTR = f'aria-label="북마크바로 끌어놓아 설치" onclick="alert(\'{DRAG_MSG}\');return false"'

# 끌어놓는 동작을 그림 한 장으로. 글자 0. 버튼에 올리면 재생된다.
DRAG_DEMO = (
  '<span class="dragdemo" aria-hidden="true"><svg viewBox="0 0 220 132"><g class="dd-scene">'
  '<rect class="dd-win" x="10" y="8" width="200" height="116" rx="12"/>'
  '<path class="dd-bar" d="M10 20a12 12 0 0 1 12-12h176a12 12 0 0 1 12 12v14H10z"/>'
  '<rect class="dd-chip" x="22" y="15" width="24" height="11" rx="5.5"/>'
  '<rect class="dd-chip" x="51" y="15" width="18" height="11" rx="5.5"/>'
  '<rect class="dd-slot" x="74" y="15" width="34" height="11" rx="5.5"/>'
  '<rect class="dd-land" x="74" y="15" width="34" height="11" rx="5.5"/>'
  '<g class="dd-spark"><path d="M91 2l1.7 4.4 4.4 1.7-4.4 1.7L91 14.2l-1.7-4.4L84.9 8l4.4-1.7z"/>'
  '<circle cx="112" cy="9" r="1.8"/><circle cx="70" cy="7" r="1.4"/></g>'
  '<g class="dd-fly"><rect x="-27" y="-10" width="54" height="20" rx="10"/>'
  '<circle cx="-15" cy="0" r="3.2"/></g>'
  '<g class="dd-cur"><path d="M0 0l0 14 3.6-3.5 2.4 5.2 2.6-1.2-2.4-5.1 4.9-.2z"/></g>'
  '</g></svg><span class="dd-cap">북마크바로 끌어놓기</span></span>'
)

CATN = {"fast": "생산성", "sell": "커머스", "research": "리서치", "study": "스터디"}

def cta(slug, big=False):
    p = P[slug]
    cls = "btn lg cta-main drag" if (big and p["cta"] == "drag") else ("btn lg cta-main" if big else ("btn drag" if p["cta"] == "drag" else "btn"))
    if p["cta"] == "drag":
        return (f'<span class="dragwrap" style="--dd:{p["color"]}"><a class="{cls}" href="{BM[p["bm"]]}" '
                f'data-bm="{p["bm"]}" {DRAG_ATTR}>{p.get("bmname", p["short"])}</a>{DRAG_DEMO}</span>')
    if p["cta"] == "ext":
        return f'<a class="{cls}" href="{p["url"]}" target="_blank" rel="noopener">{p["ctatext"]}</a>'
    return f'<a class="{cls}" href="{p["store"]}" target="_blank" rel="noopener">크롬에 추가 →</a>'

# ---------- assets ----------
os.makedirs("assets", exist_ok=True)
with open("assets/site.css", "w", encoding="utf-8") as f:
    f.write(CSS)

# ---------- 공용 셸 정본 — 제품 소스에 '직접 박는' 블록을 생성한다 ----------
#   ⚠️ 2026-07-27 전환: 예전엔 shell.js 가 런타임에 바를 끼워 넣고 토큰을 덮어썼는데,
#      첫 페인트가 제품 원래 값으로 그려진 뒤 바뀌어 '깜빡'이 보였고 바 삽입이 페이지를 40px 밀었다.
#      → 이제 마크업·CSS 를 제품 소스에 박는다(런타임 보정 0). 정본은 여기, 반영은 sync_shell.py.
SHELL_TOKENS = {
    "--mmt-gut": "clamp(20px, 4vw, 56px)",
    "--mmt-maxw": "1224px",
    # 워드마크 — 자리마다 크기·자간이 달랐다(바 15/-.03em, 푸터 18/기본, apex 헤더 또 다름).
    # 로고가 없을수록 워드마크가 로고 역할을 하니 규격을 한 곳에서 정한다(2026-08-23).
    "--mmt-wm-font": '"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,'
                     '"Apple SD Gothic Neo","Helvetica Neue","Segoe UI",sans-serif',
    "--mmt-wm-fw": "800",
    "--mmt-wm-ls": "-.035em",
    "--mmt-wm-sm": "16px",
    "--mmt-wm-md": "19px",
    "--mmt-wm-lg": "24px",
    "--mmt-ink": "#0b0c0e",
    "--mmt-faint": "#9aa0a8",
    "--mmt-soft": "#f4f5f7",
    "--mmt-bar-h": "44px",
    "--mmt-bar2-h": "64px",
    "--mmt-fs-logo": "22px",
    "--mmt-fs-nav": "14px",
    "--mmt-fw-nav": "600",
    "--mmt-nav-gap": "26px",
    "--mmt-fs-cta": "14px",
    "--mmt-cta-pad": "9px 18px",
    "--mmt-cta-r": "999px",
    "--mmt-fs-base": "16px",
    "--mmt-lh-base": "1.6",
    "--mmt-ls-base": "-0.015em",
    "--mmt-fs-lead": "18px",
    "--mmt-lh-lead": "1.65",
    "--mmt-fs-sm": "14px",
    "--mmt-fs-h3": "19px",
    "--mmt-fs-h2": "clamp(26px, 2.6vw, 34px)",
    "--mmt-lh-head": "1.28",
    "--mmt-ls-head": "-0.035em",
}

SHELL_BAR_CSS = """/* 2026-08-23 재교정 — **검정으로 되돌린다.**
   밝게 바꿨더니 제품 사이트(마크·큐)의 흰 헤더와 위아래로 겹쳐 어느 게 무슨 메뉴인지
   구분이 안 됐다(대표: "색깔도 위아래가 비슷하니 이게 무슨 메뉴인지 모르겠고").
   패밀리 바는 뒤로 물러나고 제품 브랜드가 앞에 서야 한다 — 그게 검정이었던 이유다.
   정렬도 가운데가 아니라 **좌측**. 제품마다 본문 폭이 달라(마크 1208 / apex 1176)
   가운데 정렬로는 로고 기준선이 영원히 안 맞는다. 아예 다른 층으로 둔다. */
#mmt-bar{display:block;box-sizing:border-box;width:100%;height:var(--mmt-bar-h,44px);
background:#14161a;color:#cfd4dc;position:relative;z-index:2147483002;
font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Helvetica Neue','Segoe UI',sans-serif;
letter-spacing:normal;line-height:normal}
#mmt-bar *,#mmt-bar *::after{box-sizing:border-box}
/* 애플 글로벌 내비 실측(2026-08-23, 1440 뷰포트): .globalnav-content max-width 1024px,
   좌우 padding 22px, 바 높이 44px. 뷰포트 끝에 붙이면 넓은 화면에서 왼쪽만 붙고
   오른쪽이 휑해진다 — 가운데로 모으고 그 안에서 좌측 정렬한다. */
/* ⚠️ **폭·시작선은 apex 든 제품이든 같아야 한다**(2026-08-26 대표 지적:
   "일반과 결제 페이지 로고 위치가 떨어지니까 보기가 싫어").
   종전엔 max-width 가 [data-v=apex] 에만 걸려 있어서, 제품 사이트에서는 이 띠만
   전체폭 좌측 28px 에 붙고 그 아래 제품 헤더(1224px 가운데)와 248px 어긋났다.
   색(검정/밝음)은 계속 갈라도 되지만 **자리는 갈리면 안 된다.** */
#mmt-bar .mmt-in{display:flex;align-items:center;height:100%;gap:16px;
max-width:1224px;margin:0 auto;padding:0 24px}
/* 랜딩(apex)엔 아래에 제품 헤더가 없다 — 검정일 이유가 없고 가운데로 모은다.
   검정·좌측은 **제품 사이트**용이다: 그 아래 흰 제품 헤더가 오니 물러나 있어야 한다.
   (2026-08-23 대표: "검은색으로 하는 건 제품 페이지 들어갔을 때만") */
#mmt-bar[data-v=apex]{background:rgba(250,250,252,.86);color:rgba(0,0,0,.78);
backdrop-filter:saturate(1.8) blur(20px);-webkit-backdrop-filter:saturate(1.8) blur(20px);
border-bottom:1px solid rgba(0,0,0,.07)}
#mmt-bar[data-v=apex] .mmt-wm{color:#111}
#mmt-bar[data-v=apex] .mmt-nav{margin:0 auto}
#mmt-bar[data-v=apex] a.mmt-it{color:rgba(0,0,0,.78)}
#mmt-bar[data-v=apex] a.mmt-it:hover{background:rgba(0,0,0,.055);color:#000}
#mmt-bar[data-v=apex] a.mmt-it[aria-current=page]{background:#111;color:#fff}
#mmt-bar[data-v=apex] .mmt-sep{background:rgba(0,0,0,.14)}
#mmt-bar[data-v=apex] .mmt-cta{background:transparent;color:rgba(0,0,0,.78);
box-shadow:inset 0 0 0 1px rgba(0,0,0,.18);font-weight:600}
#mmt-bar[data-v=apex] .mmt-cta:hover{background:rgba(0,0,0,.05);color:#000}
#mmt-bar[data-v=apex] .mmt-ib{color:rgba(0,0,0,.7)}
#mmt-bar[data-v=apex] .mmt-ib:hover{background:rgba(0,0,0,.06);color:#000}
/* 본진(apex)에서는 이게 **주 내비**다 — 남의 사이트 위에 얹히는 게 아니니 작을 이유가 없다
   (2026-08-24 대표 지적). 패널을 넓히고 썸네일·글자를 한 단계 키운다.
   제품 사이트(spoke)는 그대로 작게 — 거긴 패밀리 메뉴다. */
#mmt-bar[data-v=apex] .mmt-fly{background:#fff;border:1px solid rgba(0,0,0,.09);
box-shadow:0 28px 56px -24px rgba(0,0,0,.26);width:min(880px,calc(100vw - 24px));border-radius:20px}
/* 오른쪽 '무료 도구' 칸이 0.85fr 이라 '인스타 인기순 정렬' 같은 긴 라벨이 항목 상자를
   13px 쯤 넘쳤다 -> 호버 배경이 글자보다 작아 보인다(2026-09-01 대표 지적).
   칸을 반반으로 넓히고, 그래도 넘치면 항목이 잘라내도록 overflow 를 건다. */
#mmt-bar[data-v=apex] .mmt-fly-in{grid-template-columns:1fr 1fr;gap:10px 26px;padding:22px 22px 8px}
#mmt-bar[data-v=apex] .mmt-fly-h{font-size:12px;margin:0 0 10px}
#mmt-bar[data-v=apex] .mmt-fly-it{gap:14px;padding:9px 10px;border-radius:13px}
#mmt-bar[data-v=apex] .mmt-fly-it .th{width:84px;height:53px;border-radius:10px}
#mmt-bar[data-v=apex] .mmt-fly-it b{font-size:16px;font-weight:700}
#mmt-bar[data-v=apex] .mmt-fly-it i{display:block;font-style:normal;font-size:12.5px;color:#6b7280;
margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#mmt-bar[data-v=apex] .mmt-fly-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 8px}
#mmt-bar[data-v=apex] .mmt-fly-grid .mmt-fly-it .th{width:38px;height:38px;border-radius:10px;padding:6px}
#mmt-bar[data-v=apex] .mmt-fly-grid .mmt-fly-it b{font-size:13.5px;font-weight:600}
#mmt-bar[data-v=apex] .mmt-fly-grid .mmt-fly-it i{display:none}
#mmt-bar[data-v=apex] .mmt-fly-foot{padding:8px 30px 18px}
#mmt-bar[data-v=apex] .mmt-fly-h{color:#86868b}
#mmt-bar[data-v=apex] .mmt-fly-it{color:#111}
#mmt-bar[data-v=apex] .mmt-fly-it:hover{background:rgba(0,0,0,.05)}
#mmt-bar[data-v=apex] .mmt-fly-it b{color:#111}
#mmt-bar[data-v=apex] .mmt-fly-it .th{background:rgba(0,0,0,.05);color:#333}
#mmt-bar[data-v=apex] .mmt-fly-grid .mmt-fly-it b{color:#3a4150}
#mmt-bar[data-v=apex] .mmt-fly-grid .mmt-fly-it .th{background:var(--soft,#f4f5f7)}
#mmt-bar[data-v=apex] .mmt-fly-foot a{color:#0071e3}
#mmt-bar .mmt-in::-webkit-scrollbar{display:none}
/* 워드마크는 바의 시스템 폰트를 상속하면 안 된다 — 본문(Pretendard)과 글자꼴이 갈린다. */
#mmt-bar .mmt-wm{flex:0 0 auto;
font-family:var(--mmt-wm-font,"Pretendard Variable",Pretendard,-apple-system,sans-serif);
font-size:var(--mmt-wm-sm,15px);font-weight:var(--mmt-wm-fw,800);
letter-spacing:var(--mmt-wm-ls,-.035em);color:#fff;text-decoration:none}
#mmt-bar .mmt-nav{display:flex;align-items:center;gap:2px;flex:0 0 auto}
#mmt-bar a.mmt-it{font-size:12.5px;font-weight:600;letter-spacing:-.02em;color:#cfd4dc;
text-decoration:none;padding:6px 11px;border-radius:99px;white-space:nowrap;position:relative}
#mmt-bar a.mmt-it:hover{background:rgba(255,255,255,.12);color:#fff}
#mmt-bar a.mmt-it .nb{font-style:normal;margin-left:5px;padding:1px 5px;border-radius:99px;
font-size:8.5px;font-weight:800;letter-spacing:.05em;background:#0071e3;color:#fff;vertical-align:1.5px}
#mmt-bar a.mmt-it[aria-current=page]{background:#fff;color:#14161a;font-weight:700}
#mmt-bar .mmt-sep{width:1px;height:14px;background:rgba(255,255,255,.2);flex:0 0 auto;margin:0 6px}
#mmt-bar i.mmt-ext{font-style:normal;font-size:9px;opacity:.55;margin-left:3px;vertical-align:super}
#mmt-bar a.mmt-it[data-sub]::after{content:none;position:absolute;top:calc(100% + 7px);left:50%;
transform:translateX(-50%) translateY(-3px);white-space:nowrap;background:#14161a;color:#fff;font-size:12px;
font-weight:500;padding:6px 11px;border-radius:8px;opacity:0;visibility:hidden;pointer-events:none;
transition:opacity .14s,transform .14s;box-shadow:0 10px 26px -12px rgba(0,0,0,.45)}
#mmt-bar a.mmt-it[data-sub]:hover::after,#mmt-bar a.mmt-it[data-sub]:focus-visible::after{
opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
@media(max-width:820px){#mmt-bar .mmt-in{gap:10px}#mmt-bar .mmt-sep{display:none}
#mmt-bar a.mmt-it{padding:5px 7px}#mmt-bar a.mmt-it[data-sub]::after{display:none}}
/* 모바일 셀렉션 — 좁은 화면에서 링크 7개를 가로로 흘리면 상단이 정신없고 잘린다.
   현재 제품 이름만 보이고 누르면 목록이 뜬다. <details> 라 **JS 없이도 동작**한다(바의 fail-open 규칙). */
#mmt-bar .mmt-pick{display:none;position:relative;margin-left:auto}
#mmt-bar .mmt-pick>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:5px;
font-size:13.5px;font-weight:700;color:#fff;padding:6px 13px;border-radius:999px;
background:rgba(255,255,255,.14);white-space:nowrap}
#mmt-bar .mmt-pick>summary::-webkit-details-marker{display:none}
#mmt-bar .mmt-pick>summary::after{content:"";width:0;height:0;border:4px solid transparent;
border-top-color:currentColor;margin-top:2px;opacity:.7}
#mmt-bar .mmt-menu{position:absolute;right:0;top:calc(100% + 9px);background:#14161a;border-radius:14px;
padding:6px;min-width:206px;box-shadow:0 18px 44px -14px rgba(0,0,0,.6);z-index:2147483001}
#mmt-bar .mmt-menu a{display:block;padding:10px 13px;border-radius:10px;color:#cfd4dc;
font-size:14.5px;font-weight:600;text-decoration:none;white-space:nowrap}
#mmt-bar .mmt-menu a[aria-current=page]{background:#fff;color:#14161a;font-weight:700}
#mmt-bar .mmt-menu hr{border:0;border-top:1px solid rgba(255,255,255,.12);margin:5px 8px}
@media(max-width:640px){#mmt-bar .mmt-in{gap:10px}
#mmt-bar .mmt-nav{display:none}#mmt-bar .mmt-pick{display:block}}
/* ⚠️ 액션(문의하기·검색·테마) 스타일은 **공용 셸**에 있어야 한다.
   apex 전용 CSS 에 두었더니 제품 사이트에서 문의하기가 스타일 없는 파란 밑줄 링크로
   나왔다(2026-08-24 빈방 실측). 마크업이 공용이면 스타일도 공용이다. */
#mmt-bar .mmt-act{margin-left:auto;display:flex;align-items:center;gap:4px;flex:0 0 auto}
/* 문의는 '메뉴'가 아니라 '행동'이다 — 토스 헤더가 앱 다운로드를 버튼으로 두는 자리.
   글자 수를 줄이려고 '문의'로 쓰던 것을 '문의하기'로 되돌린다(2026-08-23 대표 지적). */
/* 버튼도 내비와 같은 글자꼴·크기 — 하나만 튀면 메뉴가 아니라 광고로 읽힌다. */
/* 문의하기는 '있다'만 알리면 된다 — 꽉 채우면 광고처럼 튄다(2026-08-23 대표 지적). */
#mmt-bar .mmt-cta{display:inline-flex;align-items:center;height:28px;padding:0 13px;
border-radius:99px;background:transparent;color:#e6e9ee;
box-shadow:inset 0 0 0 1px rgba(255,255,255,.28);
font-size:12.5px;font-weight:600;letter-spacing:-.02em;
text-decoration:none;white-space:nowrap;margin-right:4px}
#mmt-bar .mmt-cta:hover{background:rgba(255,255,255,.12);color:#fff}
@media(max-width:640px){#mmt-bar .mmt-cta{display:none}}
#mmt-bar .mmt-ib{display:grid;place-items:center;width:30px;height:30px;padding:0;border:0;
border-radius:50%;background:none;color:#cfd4dc;cursor:pointer;transition:background .18s,color .18s}
#mmt-bar .mmt-ib:hover{background:rgba(255,255,255,.12);color:#fff}
#mmt-bar .mmt-ib svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.8;
stroke-linecap:round;stroke-linejoin:round}
#mmt-bar .mmt-ib .moon{display:none}
html[data-theme="dark"] #mmt-bar .mmt-ib .moon{display:block}
html[data-theme="dark"] #mmt-bar .mmt-ib .sun{display:none}
@media(prefers-reduced-motion:reduce){#mmt-bar a.mmt-it[data-sub]::after{transition:none}}
/* ── 제품 플라이아웃 ──────────────────────────────────────────────────────
   제품 이름을 바에 하나씩 늘어놓으면 제품이 늘 때마다 바가 길어지고 결국 잘린다
   (2026-08-23 대표: "제품이 늘어난다고 해서 이걸 다 올릴 순 없잖아").
   애플 글로벌 내비와 같은 방식 — 바에는 '제품' 하나, 목록은 호버 패널이 연다.
   ⚠️ JS 0. :has() 로만 연다. 지원 안 되는 브라우저에선 패널이 안 열리고 '제품'이
      그냥 /products/ 로 가는 평범한 링크가 된다(바의 fail-open 규칙). */
#mmt-bar .mmt-trg::after{content:"";display:inline-block;width:0;height:0;margin-left:5px;
border:3.5px solid transparent;border-top-color:currentColor;vertical-align:middle;opacity:.5}
/* 패널은 밝게, 썸네일은 크게, 설명 줄은 뺀다 — 목록은 고르라고 있는 것이지 읽으라고 있는 게 아니다
   (2026-08-23 대표: "심플하지만 썸네일도 큼직하게, 중요한 건 더 크게 간결하게"). */
/* ⚠️ 커튼(전체 화면 블러)은 걷어냈다. 이건 제품 사이트 위에 얹히는 **패밀리 메뉴**지
   그 사이트의 주 내비가 아니다 — 화면 전체를 덮으면 남의 집에서 주인 행세를 하는 꼴이다
   (2026-08-24 대표: "여전히 전체적으로 헤비한데"). 패널도 전체폭 → '더보기' 아래 작은 카드로. */
#mmt-bar .mmt-drop{position:relative;display:inline-flex}
#mmt-bar .mmt-fly{position:absolute;left:50%;top:calc(100% + 8px);transform:translateX(-50%) translateY(-4px);
width:min(620px,calc(100vw - 24px));background:#1a1d22;border:1px solid rgba(255,255,255,.1);
border-radius:16px;box-shadow:0 24px 48px -20px rgba(0,0,0,.65);
opacity:0;visibility:hidden;z-index:2147483003;
transition:opacity .15s ease,transform .15s ease,visibility .15s}
#mmt-bar:has(.mmt-trg:hover) .mmt-fly,
#mmt-bar:has(.mmt-fly:hover) .mmt-fly,
#mmt-bar:has(.mmt-trg:focus-visible) .mmt-fly,
#mmt-bar:has(.mmt-fly a:focus-visible) .mmt-fly{opacity:1;visibility:visible;
transform:translateX(-50%) translateY(0)}
#mmt-bar .mmt-fly-in{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;padding:14px 14px 4px}
#mmt-bar .mmt-fly-h{font-size:11px;font-weight:600;letter-spacing:.02em;color:#79828f;
margin:0 0 6px;padding:0 8px}
#mmt-bar .mmt-fly-it{display:flex;align-items:center;gap:10px;padding:6px 8px;border-radius:9px;
text-decoration:none;color:#cfd4dc}
#mmt-bar .mmt-fly-it:hover{background:rgba(255,255,255,.09)}
#mmt-bar .mmt-fly-it .th{width:44px;height:28px;border-radius:6px;overflow:hidden;flex:0 0 auto;
background:rgba(255,255,255,.08);display:grid;place-items:center;font-size:13px;color:#e6e9ee}
#mmt-bar .mmt-fly-it .th img{width:100%;height:100%;object-fit:cover;display:block}
#mmt-bar .mmt-fly-it .tx{min-width:0}
/* ⚠️ 그리드 칸은 기본이 min-width:auto 라 **내용보다 작아지지 않는다**. 판 폭을 아무리
   줄여도 안쪽이 그대로 삐져나온다(2026-08-24: 판을 좁혔더니 넘침이 12px→57px 로 늘었다).
   폭을 줄이려면 칸이 줄어들 수 있게 min-width:0 을 먼저 풀어 줘야 한다. */
#mmt-bar .mmt-fly-in>*,#mmt-bar .mmt-fly-grid>*,#mmt-bar .mmt-fly-it{min-width:0}
/* ⚠️ 항목 *안쪽*(제목 b, 설명 i, 텍스트 래퍼)도 풀어 줘야 한다. flex 자식은 기본이
   min-width:auto 라 글자가 안 줄어들고 항목 상자를 그대로 넘친다 → 호버 배경이 글자보다
   작아 보인다(2026-09-01 대표 지적). 위 줄은 항목 자신만 풀어 줘서 안쪽이 여전히 삐져나왔다. */
#mmt-bar .mmt-fly-it>*{min-width:0}
#mmt-bar .mmt-fly-it{overflow:hidden}
#mmt-bar .mmt-fly-it b,#mmt-bar .mmt-fly-it i{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#mmt-bar .mmt-fly-it b{font-size:13.5px;font-weight:600;letter-spacing:-.02em;color:#fff;
white-space:nowrap}
#mmt-bar .mmt-fly-it b .nb{font-style:normal;margin-left:6px;padding:1px 6px;border-radius:99px;
font-size:9px;font-weight:800;letter-spacing:.05em;background:#0071e3;color:#fff;vertical-align:1px}
#mmt-bar .mmt-fly-it i{display:none}
#mmt-bar .mmt-fly-it[aria-current=page]{background:rgba(255,255,255,.1)}
#mmt-bar .mmt-fly-it[aria-current=page] b{color:#8fc0ff}
#mmt-bar .mmt-fly-grid{display:flex;flex-direction:column;gap:0}
#mmt-bar .mmt-fly-grid .mmt-fly-it .th{width:26px;height:26px;border-radius:7px;background:#fff;padding:4px}
#mmt-bar .mmt-fly-grid .mmt-fly-it .th img{object-fit:contain}
#mmt-bar .mmt-fly-grid .mmt-fly-it b{font-size:13px;font-weight:500;color:#cfd4dc}
/* 더보기는 호버로 열리지만 **눌러서도 갈 수 있다** — 그걸 모르는 사람을 위해 맨 위에 둔다. */
#mmt-bar .mmt-fly-all{margin-bottom:4px}
#mmt-bar .mmt-fly-all .th{background:rgba(255,255,255,.14);font-size:15px}
#mmt-bar[data-v=apex] .mmt-fly-all .th{background:rgba(0,0,0,.06)}
#mmt-bar .mmt-fly-all b{color:#8fc0ff}
#mmt-bar[data-v=apex] .mmt-fly-all b{color:#0071e3}
#mmt-bar .mmt-fly-foot{padding:6px 22px 14px}
#mmt-bar .mmt-fly-foot a{font-size:12.5px;font-weight:600;color:#8fc0ff;text-decoration:none}
#mmt-bar .mmt-fly-foot a:hover{text-decoration:underline}
/* ⚠️ 더보기 판은 *버튼*을 기준으로 가운데 정렬된다. 그 버튼이 바 오른쪽에 있어서
   calc(100vw - 24px) 만으로는 오른쪽이 화면 밖으로 나간다 — 821~905px 구간에서
   가로 스크롤이 1~12px 생겼다(2026-08-24 실측, 전 페이지 공통).
   버튼 오른쪽에 남는 공간이 판의 절반보다 좁아지는 구간에서 판을 좁힌다. */
@media(max-width:1000px){#mmt-bar .mmt-fly,#mmt-bar[data-v=apex] .mmt-fly{
width:min(600px,calc(100vw - 24px))}}
@media(max-width:820px){#mmt-bar .mmt-fly{display:none}}
@media(prefers-reduced-motion:reduce){#mmt-bar .mmt-fly{transition:none}}"""



# ── 글 목록·상세 공용 스타일 ───────────────────────────────────────────────
#   2026-08-23 대표: "Q 비비 노트 이런 거 있으면 똑같은 레이아웃으로 리스팅이랑
#   상세페이지를 하라니까 왜 말을 안 듣냐." 맞다 — 물어보고 안 했다.
#   정본은 여기 하나. 각 제품의 기존 클래스 이름은 **별칭으로 묶어** 마크업을 안 건드리고
#   같은 규격을 받게 한다(마크 .post-*, 큐 .dg-*). 이름 통일은 그다음 단계.
#   반영: sync_shell.py 가 제품 스타일시트의 MMT 블록에 함께 밀어 넣는다.
SHELL_POST_CSS = """
/* ── 인사이트 목록 = 전 사이트 한 벌 ────────────────────────────────
   같은 글이 본진과 마크에 둘 다 보이는데 카드가 서로 달랐다(2026-08-24 대표 지적).
   ⚠️ 여기에 값을 **복붙하지 마라**. 원본은 NEWS_CSS 하나다 — 사본을 두면
     한쪽만 고쳐져서 다시 두 벌이 된다(스크림 밝기가 그렇게 갈릴 뻔했다).
     아래 {NEWS_SHARED} 자리에 그 원본이 그대로 들어간다. */
{NEWS_SHARED}

/* ── 글 페이지 공통 간격·크기 (목록 = 상세) ─────────────────────────────
   2026-08-24 대표: "목록은 상단 여백이 있는데 상세로 가면 굉장히 좁다.
   목록에 있는 간격 규칙이 상세에도 적용됐으면 좋겠다."
   실측 차이: 목록 상단 129.6px vs 상세 84px. 값을 각자 적어 두니 갈렸다 → 토큰 하나로.
   제목만 상세가 한 단계 크다(글의 주인공이라) — 그것도 여기서 정한다. */
:root{
--pg-top:clamp(64px,9vw,132px);      /* 바 아래 첫 요소까지 */
--pg-head-gap:clamp(26px,3.4vw,44px);/* 제목 블록 → 본문/목록 */
--pg-sub-gap:14px;                   /* 제목 → 부제 */
--pg-h1:clamp(34px,4.6vw,56px);      /* 목록 제목 */
--pg-h1-post:clamp(30px,4.4vw,64px); /* 글 제목 */
}
/* 카드 그림은 제품 og(1200x630) 비율 그대로 — 다른 비율로 자르면 글자가 잘린다 */
.nws-card .th,.dg-card .th{display:block;width:100%;aspect-ratio:1200/630;border-radius:16px;overflow:hidden;
background:var(--mmt-soft,#f4f5f7);display:block;margin:0}
.nws-card .th img,.dg-card .th img{width:100%;height:100%;object-fit:cover;display:block;
transition:transform .55s cubic-bezier(.2,.7,.3,1)}
.nws-card:hover .th img,.dg-card:hover .th img{transform:scale(1.04)}
.nws-card h3,.dg-card h3{margin-top:16px;font-size:17px;font-weight:700;letter-spacing:-.03em;
line-height:1.45;color:var(--mmt-ink,#0b0c0e);display:-webkit-box;-webkit-line-clamp:2;
-webkit-box-orient:vertical;overflow:hidden}
.nws-card .d,.dg-card .cat{margin-top:12px;font-size:14px;color:var(--mmt-faint,#9aa0a8);
font-variant-numeric:tabular-nums}
.dg-card .cat{margin-top:12px;order:2}
.dg-card p{display:none}                     /* 카드엔 제목·날짜만 — 요약은 목록을 무겁게 한다 */
/* ── 글 본문(상세) 공통 타이포 ─────────────────────────────────────────
   모멘터스 .pst-prose / 마크 .prose / 큐 .dg-post 가 각자 다른 크기·행간을 쓰고 있었다
   (실측 16.5/1.78 · 16/1.6 · 18.5/1.75). 읽는 글은 같은 리듬이어야 한다 → 토큰 하나로.
   ⚠️ 큐는 페이지 CSS 가 공용 블록보다 뒤에 실려서 !important 가 필요하다. */
:root{--art-fs:17px;--art-lh:1.75;--art-h2:clamp(20px,1.9vw,24px);--art-h2-mt:40px;
--art-p-mt:16px;--art-r:16px}
.pst-prose,.prose,.dg-post p,.dg-post li{font-size:var(--art-fs);line-height:var(--art-lh)}
.dg-post p{font-size:var(--art-fs) !important;line-height:var(--art-lh) !important;
margin:0 0 var(--art-p-mt) !important}
.pst-prose h2,.prose h2,.dg-post h2{font-size:var(--art-h2);font-weight:800;
letter-spacing:-.035em;margin-top:var(--art-h2-mt)}
.dg-post h2{font-size:var(--art-h2) !important;margin:var(--art-h2-mt) 0 14px !important}
.pst-prose p,.prose p{margin-top:var(--art-p-mt)}
.pst-cover,.post-cover,.dg-post .cover{border-radius:var(--art-r)}
.dg-post .cover{border-radius:var(--art-r) !important}

/* 제품 사이트의 글 목록·상세도 같은 간격을 본다(큐 .dg-hero, 마크 .post-top). */
.dg-hero{padding:var(--pg-top) 0 var(--pg-head-gap) !important}
.dg-hero h1{font-size:var(--pg-h1) !important;line-height:1.08}
.dg-hero p{margin-top:var(--pg-sub-gap) !important}
.post-top{padding-top:var(--pg-top) !important}
.post-h1{font-size:var(--pg-h1-post) !important}
.post-sub{margin-top:var(--pg-sub-gap) !important}
.nws-grid,.dg-grid{display:grid;grid-template-columns:repeat(3,1fr);
gap:clamp(34px,4.6vw,64px) clamp(18px,2.6vw,36px)}
@media(max-width:960px){.nws-grid,.dg-grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.nws-grid,.dg-grid{grid-template-columns:1fr;gap:34px}}

/* ── 글 상세 레이아웃 = 전 사이트 한 벌 (2026-08-27 대표 지시) ──────────────────
   왼쪽에 목차, 가운데 본문, **오른쪽 레일은 폐기**. 다 읽은 사람에게 주는
   '이어서 읽기'는 글 끝 카드로 내린다(토스 /business/tosspay 의 '더 읽어보기' 자리).
   왜 여기냐 — 실측(2026-08-27) 세 제품이 다 달랐다:
     큐 200/712/gap32 · 본진 200/1176/gap32 · 마크 240/maxw/gap56.
     같은 인사이트 목록에서 들어갔는데 글마다 화면이 달랐다.
   ⚠️ 제품 저장소에 이 값을 다시 적지 마라 — 적는 순간 또 세 벌이 된다.
     제품 CSS 가 이 블록보다 **뒤에** 실리므로, 제품 쪽 같은 규칙은 지워야 이게 이긴다.
   ⚠️ 목차↔본문 간격은 고정값이 아니라 화면에 따라 벌어진다(32px 고정이 붙어 보인 원인). */
:root{--art-rail:200px;--art-gap:clamp(40px,5vw,88px);--art-col:760px;--art-shell:1560px;--art-toc-top:80px}
.art-grid,.pst-grid,.post-grid{display:grid;
grid-template-columns:minmax(180px,1fr) minmax(0,var(--art-col)) minmax(180px,1fr);
column-gap:var(--art-gap);align-items:start;max-width:var(--art-shell);margin:0 auto;
padding-inline:24px;justify-content:center}
.art-top,.pst-top,.post-top{grid-column:2;grid-row:1;padding:var(--pg-top) 0 0}
.art-main,.pst-main,.post-main{grid-column:2;grid-row:2;min-width:0;margin-top:var(--pg-head-gap)}
/* 오른쪽 레일은 안 쓴다 — 마크업이 남아 있어도 화면에서 사라지게 둔다(제품별 철거 시차 흡수). */
.art-aside,.pst-aside,.post-aside{display:none}
.art-toc,.pst-toc,.post-toc{grid-column:1;grid-row:2;width:var(--art-rail);justify-self:end;
align-self:start;position:sticky;top:var(--art-toc-top);margin-top:var(--pg-head-gap)}
.art-toc .rail-title,.pst-toc .rt,.post-toc .rail-title{font-size:12px;font-weight:800;
letter-spacing:.04em;color:var(--dim,var(--mmt-faint,#9aa0a8));margin:0 0 12px}
.art-toc ul,.pst-toc ul,.post-toc ul{list-style:none;margin:0;padding:0;border:0}
/* 두 줄까지만 — 긴 제목이 세 줄씩 감기면 본문 옆에 회색 문단이 하나 더 붙은 꼴이 된다. */
.art-toc li a,.pst-toc a,.post-toc li a{display:-webkit-box;-webkit-line-clamp:2;
-webkit-box-orient:vertical;overflow:hidden;padding:7px 0 7px 14px;
border-left:2px solid var(--line,#e7e8ec);font-size:13.5px;line-height:1.5;
color:var(--gray,var(--ink-2,#4e5968));text-decoration:none;margin:0}
.art-toc li a:hover,.pst-toc a:hover,.post-toc li a:hover{color:var(--ink,var(--mmt-ink,#0b0c0e));
border-left-color:var(--ink,var(--mmt-ink,#0b0c0e))}
.art-toc li a.on,.pst-toc a.on,.post-toc li a.on{color:var(--ink,var(--mmt-ink,#0b0c0e));
font-weight:700;border-left-color:var(--acc,var(--brand-cta,var(--pt,#3182f6)))}
/* 좁은 화면에선 레일이 사라진다 — 예전엔 그대로 없어져 모바일은 목차를 아예 못 봤다. 접힘으로 산다. */
.art-toc-m{display:none;margin:22px 0 0;border:1px solid var(--line,#e7e8ec);
border-radius:14px;background:var(--soft,var(--mmt-soft,#f4f5f7))}
.art-toc-m>summary{list-style:none;cursor:pointer;padding:13px 16px;font-size:14px;
font-weight:800;color:var(--ink,var(--mmt-ink,#0b0c0e))}
.art-toc-m>summary::-webkit-details-marker{display:none}
.art-toc-m>summary::after{content:"+";float:right;color:var(--dim,var(--mmt-faint,#9aa0a8));font-weight:700}
.art-toc-m[open]>summary::after{content:"-"}
.art-toc-m ul{list-style:none;margin:0;padding:0 16px 14px}
.art-toc-m li a{display:block;padding:8px 0;font-size:14.5px;line-height:1.5;
color:var(--gray,var(--ink-2,#4e5968));text-decoration:none}
/* 이어서 읽기 — 글 끝 카드 3장. 카드 규격은 목록 카드와 같은 자를 쓴다.
   ⚠️ 카드 안 요소의 margin 은 **네 방향을 다 적는다**. 한쪽만 적으면 제품이 이미 쓰는 같은 이름
     (마크의 .cat = margin-bottom clamp(40,6vw,76))이 새어 들어와 카드가 세로로 벌어진다(2026-08-27 실측). */
.art-next{margin:44px 0 0;padding-top:28px;border-top:1px solid var(--line,#e7e8ec)}
.art-next-t{font-size:15px;font-weight:800;letter-spacing:-.02em;
color:var(--ink,var(--mmt-ink,#0b0c0e));margin:0 0 20px}
.art-next-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0 clamp(18px,2.4vw,36px)}
.art-next-card{display:block;text-decoration:none}
.art-next-card .th{display:block;width:100%;aspect-ratio:1200/630;border-radius:16px;
overflow:hidden;background:var(--soft,var(--mmt-soft,#f4f5f7));margin:0}
.art-next-card .th img{width:100%;height:100%;object-fit:cover;display:block;
transition:transform .55s cubic-bezier(.2,.7,.3,1)}
.art-next-card:hover .th img{transform:scale(1.04)}
.art-next-card .cat{margin:12px 0 0;font-size:13px;color:var(--dim,var(--mmt-faint,#9aa0a8))}
.art-next-card h3{margin:8px 0 0;font-size:16px;font-weight:700;letter-spacing:-.03em;
line-height:1.45;color:var(--ink,var(--mmt-ink,#0b0c0e));display:-webkit-box;
-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
@media(max-width:1120px){
.art-grid,.pst-grid,.post-grid{grid-template-columns:minmax(0,var(--art-col))}
.art-top,.pst-top,.post-top,.art-main,.pst-main,.post-main{grid-column:1}
.art-toc,.pst-toc,.post-toc{display:none}
.art-main>.art-toc-m,.pst-main>.art-toc-m,.post-main>.art-toc-m{display:block}}
@media(max-width:860px){.art-next-grid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.art-next-grid{grid-template-columns:1fr;gap:26px}}
"""

def shell_css_block():
    """제품 스타일시트에 그대로 박는 블록 — 토큰(실값) + 바 스타일. 런타임 덮어쓰기 없음."""
    toks = "".join(f"{k}:{v};" for k, v in SHELL_TOKENS.items())
    return ("/* MMT:BEGIN — 모멘터스 공용 셸(생성물). 손으로 고치지 말 것.\n"
            "   정본: momentus/scripts/gen_site.py · 반영: momentus/scripts/sync_shell.py */\n"
            f":root{{{toks}}}\n{SHELL_BAR_CSS}\n"
            + SHELL_POST_CSS.replace("{NEWS_SHARED}", NEWS_SHARED)
            + "\n/* MMT:END */")


# ── 법적 표기(전자상거래 6종) — **여기가 정본이다.** ────────────────────────────
# 종전엔 제품 저장소가 이 문장을 손으로 베꼈다(notes 2곳·cue 4곳·mark 1곳). 값이 지금 맞는 건
# 우연이고, 한 곳만 고치는 순간 갈린다 — 패밀리 바에서 이미 겪은 그 사고다(그래서 sync_shell 이 있다).
# 법적 표기는 **틀리면 심사에서 잡히는** 문장이라 더더욱 손복사로 두면 안 된다.
#   반영: sync_shell.py 가 제품 저장소의 MMT:LEGAL 마커 사이를 갈아 끼운다.
#   🚫 제품 저장소에서 이 문장을 고치지 마라 — 다음 동기화 때 덮어쓴다. 여기(BIZ)를 고쳐라.
def shell_legal_html(sep="<br>"):
    """제품 사이트 푸터에 들어가는 한 덩어리(마커 없음).

    ★ **내용만 준다. 스타일은 제품이 갖는다.** 인라인 style 을 여기서 박으면 제품마다 다른
      푸터 조판을 정본이 떠안게 되고, 결국 제품별 분기가 생겨 단일 소스가 아니게 된다.
    sep — 줄 구분. notes·mark 는 `<br>`, cue 는 한 줄이라 ` · `.
    """
    lines = [
        f"{BIZ['name']} · 대표 {BIZ['ceo']} · 사업자등록번호 {BIZ['reg']} · 통신판매업신고 {BIZ['mail_order']}",
        # ⚠️ Cloudflare 이메일 난독화 우회 — Pages 로 나가는 사이트(mark)에서 이메일이
        #    [email protected] 로 바뀌어 **로봇이 못 읽었다**(2026-08-08 실측). 법적 고지의
        #    연락처이고 GEO(AI 답변) 대상이라 읽혀야 한다. 대시보드를 끄지 않고 이 주석으로 푼다
        #    — 설정에 기대면 나중에 누가 켜도 모른다. 코드가 스스로 보장하게 둔다.
        f"{BIZ['addr']} · {BIZ['tel_html']} · <!--email_off-->{BIZ['email']}<!--/email_off-->",
        "고객 문의는 이메일로만 받습니다. 이메일로 주시면 가장 빠르게 도와드릴 수 있습니다.",
        ('<a href="https://the-moment.us/legal/terms/" target="_blank" rel="noopener">이용약관</a> · '
         '<a href="https://the-moment.us/legal/privacy/" target="_blank" rel="noopener">개인정보처리방침</a> · '
         '<a href="https://the-moment.us/legal/refund/" target="_blank" rel="noopener">환불 및 청약철회</a>'),
    ]
    return sep.join(lines)


def shell_legal_markup(sep="<br>"):
    """마커로 감싼 형태 — sync_shell 이 이 사이를 통째로 갈아 끼운다."""
    return ("<!-- MMT:LEGAL:BEGIN — 전자상거래 표기(생성물). 손으로 고치지 말 것.\n"
            "     정본: momentus/scripts/gen_site.py BIZ · 반영: momentus/scripts/sync_shell.py -->\n"
            + shell_legal_html(sep)
            + "\n<!-- MMT:LEGAL:END -->")


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


_FLY_SHOT = {          # 랜딩 배너와 같은 그림(정본은 HOME_SHOT — 여기선 경로만 재기재)
    "mark": "/assets/home/mark.webp",
    "cue": "/assets/home/cue.png",
    "theplan": "/assets/home/theplan.png",
    "kontext": "/assets/home/kontext.jpg",
    "heyreci": "/assets/home/heyreci.jpg",
    "binbang": "https://bb.the-moment.us/assets/hero.jpg",
    "flipper": "/assets/flipper/hero.png",
    "teamai": "/assets/home/teamai.jpg",
}
_NEWB = {"binbang": '<em class="nb">NEW</em>',
         "flipper": '<em class="nb">NEW</em>',
         "teamai": '<em class="nb">NEW</em>'}   # 바·플라이아웃에서 새 제품 표시
def shell_bar_markup(host="", act_extra=""):
    """제품 HTML의 <body> 바로 뒤에 박는 공용 1단 바. host 를 주면 그 제품에 활성 표시.

    구조 = 애플 글로벌 내비: [MOMENTUS] [제품 ▾] [이야기] [소개] [문의]
    제품 목록은 '제품'에 호버할 때 열리는 패널(.mmt-fly)에 들어간다 — 바는 안 길어진다.
    """
    def _abs(h):
        return h if "//" in h else ("https://the-moment.us" + h)

    def _host_of(h):
        return h.split("//")[1].split("/")[0] if "//" in h else ""

    # 제품 전체를 플라이아웃에만 두니 자주 가는 곳이 한 번 더 걸렸다(2026-08-23 대표 지적).
    # 앞의 3개는 바에 꺼내고, 나머지는 '더보기'가 연다.
    parts = []
    # 규칙: 바에 이름을 꺼내는 건 **이 패밀리 바를 달고 있는 사이트**(플래너·로고·모의면접·빈방).
    #   헤이레시·컨텍스트처럼 따로 개발돼 그냥 점프하는 서비스는 '더보기' 안에 둔다
    #   — 눌렀을 때 돌아올 길(패밀리 바)이 있느냐로 가른다(2026-08-24 대표 정리).
    #   ⚠️ 앱형(자체 사이트 없음)도 바에서 뺀다 — 눌러도 돌아올 패밀리 바가 없는 건 마찬가지다.
    _app = {sl for sl, pr in P.items() if pr.get("type") == "app"}
    tops = [sp for sp in bar_products()
            if not sp.get("external") and sp.get("slug") not in _app]
    for sp in tops:
        cur = ' aria-current="page"' if host and _host_of(sp["href"]) == host else ""
        ext = ' target="_blank" rel="noopener"' if sp.get("external") else ""
        parts.append(f'<a class="mmt-it" href="{sp["href"]}"{ext}{cur}>'
                     f'{sp["label"]}{_NEWB.get(sp.get("slug"), "")}</a>')
    # 트리거 = **목록으로 가는 링크**다(호버하면 패널, 누르면 /products/).
    #   '더보기'라고 쓰니 어디로 가는지 안 보였다(2026-08-24 대표 지적).
    _plabel = next((l["label"] for l in BAR["links"] if l["key"] == "products"), "제품 전체")
    parts.append("__DROP__")
    parts.append('<span class="mmt-sep" aria-hidden="true"></span>')
    for it in bar_items():
        if it.get("trg"):
            continue                      # '제품'은 위 '더보기'가 대신한다
        parts.append(f'<a class="mmt-it" href="{_abs(it["href"])}">{it["label"]}</a>')

    # ── 플라이아웃: 제품(썸네일+한 줄) + 무료 도구(아이콘 격자) ──
    prods = []
    for sp in bar_products():
        sl = sp.get("slug", "")
        pr = P.get(sl, {})
        cur = ' aria-current="page"' if host and _host_of(sp["href"]) == host else ""
        # 랜딩 배너와 **같은 그림**을 쓴다 — 메뉴와 본문이 다른 그림이면 다른 것으로 읽힌다
        # (2026-08-24 대표 지적). 헤이레시는 배너가 영상이라 첫 프레임을 떠서 넣었다.
        shot = prod_shot(sl)
        th = (f'<span class="th"><img src="https://the-moment.us{shot}" alt="" loading="lazy"></span>'
              if shot.startswith("/") else
              (f'<span class="th"><img src="{shot}" alt="" loading="lazy"></span>'
               if shot else f'<span class="th">{pr.get("icon", "")}</span>'))
        line = esc(pr.get("tagline", "")) or esc(sp.get("sub", ""))
        ext = ' target="_blank" rel="noopener"' if sp.get("external") else ""
        prods.append(f'<a class="mmt-fly-it" href="{sp["href"]}"{ext}{cur}>{th}'
                     f'<span class="tx"><b>{sp["label"]}{_NEWB.get(sl, "")}</b><i>{line}</i></span></a>')
    # 무료 도구도 로고로 — 랜딩 카드와 같은 그림을 써야 같은 것으로 읽힌다(2026-08-24 대표 지적).
    def _tth(t):
        lg = P[t].get("logo")
        return (f'<span class="th"><img src="https://the-moment.us{lg}" alt="" loading="lazy"></span>'
                if lg else f'<span class="th">{P[t]["icon"]}</span>')

    tools = "".join(
        f'<a class="mmt-fly-it" href="https://the-moment.us/tools/{t}/">{_tth(t)}'
        f'<span class="tx"><b>{P[t]["short"]}</b></span></a>' for t in TOOLS)
    fly = ('<div class="mmt-fly"><div class="mmt-fly-in">'
           f'<div><p class="mmt-fly-h">제품</p>{"".join(prods)}</div>'
           f'<div><p class="mmt-fly-h">무료 도구</p><div class="mmt-fly-grid">{tools}</div></div>'
           '</div><div class="mmt-fly-foot">'
           '<a href="https://the-moment.us/products/">전체 제품 보기 →</a></div></div>')

    # ── 모바일 셀렉션 — 좁은 화면엔 플라이아웃이 없으니 여기에 전부 담는다 ──
    here, mparts = "모멘터스", []
    for sp in bar_products():
        cur = bool(host and _host_of(sp["href"]) == host)
        if cur:
            here = sp["label"]
        ext = ' target="_blank" rel="noopener"' if sp.get("external") else ""
        act = ' aria-current="page"' if cur else ""
        mparts.append(f'<a href="{sp["href"]}"{act}{ext}>{sp["label"]}</a>')
    mparts.append("<hr>")
    for it in bar_items():
        mparts.append(f'<a href="{_abs(it["href"])}">{it["label"]}</a>')
    mparts.append('<a href="https://the-moment.us/inquiry/">문의하기</a>')
    pick = ('<details class="mmt-pick"><summary aria-label="모멘터스 제품 고르기">'
            f'{here}</summary><div class="mmt-menu">{"".join(mparts)}</div></details>')
    act = ('<div class="mmt-act">'
           '<a class="mmt-cta" href="https://the-moment.us/inquiry/">문의하기</a>'
           f'{act_extra}</div>')

    return ('<!-- MMT:BEGIN — 모멘터스 공용 1단 바(생성물). 손으로 고치지 말 것. -->\n'
            '<div id="mmt-bar"><div class="mmt-in">'
            '<a class="mmt-wm" href="https://the-moment.us">MOMENTUS</a>'
            f'<nav class="mmt-nav" aria-label="모멘터스">'
            + "".join(parts).replace("__DROP__",
                '<span class="mmt-drop">'
                f'<a class="mmt-it mmt-trg" href="https://the-moment.us/products/">{_plabel}</a>'
                + fly + '</span>')
            + '</nav>'
            f'{act}{pick}'
            '</div></div>\n<!-- MMT:END -->')


# ── apex 헤더 = 스포크와 **같은** 공용 1단 바 + 검색·다크모드 ────────────────
#   2026-08-23. 그전엔 apex 만 별도 헤더(.gnb 흰 바 / 홈은 영문 kb-gnb)를 써서
#   제품 페이지와 말도 간격도 달랐다(대표: "각각 간격과 방식 모두 맞춰야지").
#   이제 the-moment.us 의 모든 페이지가 제품 사이트와 같은 바를 쓴다.
_MMT_ICONS = (
            '<button class="mmt-ib" id="kbsearchbtn" aria-label="검색 열기">'
            '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg></button>'
            '<button class="mmt-ib" id="kbthemebtn" aria-label="다크모드로 전환">'
            '<svg viewBox="0 0 24 24" class="sun"><circle cx="12" cy="12" r="4"/>'
            '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2'
            'M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
            '<svg viewBox="0 0 24 24" class="moon"><path d="M20 14.6A8.6 8.6 0 019.4 4 8.6 8.6 0 1020 14.6z"/>'
            '</svg></button>')

SEARCH_OVERLAY = """<div class="kb-sr" id="kbsr" role="dialog" aria-modal="true" aria-label="검색">
  <div class="kb-sr-in">
    <div class="kb-sr-box">
      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
      <input id="kbsrq" type="search" placeholder="무엇을 찾으세요?" autocomplete="off" spellcheck="false">
      <button class="kb-ib" id="kbsrclose" aria-label="검색 닫기">
        <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="kb-sr-hits" id="kbsrhits"></div>
  </div>
</div>"""

APEX_HEADER = (shell_bar_markup(act_extra=_MMT_ICONS)
               .replace('<div id="mmt-bar">', '<div id="mmt-bar" data-v="apex">', 1)
               + SEARCH_OVERLAY)


with open("shell.css", "w", encoding="utf-8") as f:
    f.write(shell_css_block() + "\n")

# ---------- shell.js — (레거시) 아직 소스에 박지 않은 곳을 위한 폴백 ----------
#   제품이 부담하는 것: <script src="https://the-moment.us/shell.js" defer></script> 한 줄.
#   규칙 3개(PLATFORM_TOPOLOGY §3):
#     ① fail-open — 이 파일이 죽거나 못 뜨면 바만 없고 제품 사이트는 정상 작동해야 한다.
#     ② 활성 표시는 현재 도메인으로 도출한다(하드코딩 금지).
#     ③ 스타일은 #mmt-bar 로 스코프 — 제품 CSS를 오염시키지 않는다.
#   제품의 고정 헤더가 바를 덮으면 그 제품에서 한 줄만 오프셋: top: var(--mmt-bar-h)
SHELL_ITEMS = json.dumps(
    [dict(label=i["label"], href=i["href"], sub=i["sub"], ext=i["ext"], sep=i["sep"]) for i in bar_items()],
    ensure_ascii=False, separators=(",", ":"))

SHELL_JS = """/* MOMENTUS shell.js — 1단 브랜드 바. 생성물(scripts/gen_site.py). 손으로 고치지 말 것. */
(function () {
  "use strict";
  try {
    if (document.getElementById("mmt-bar")) return;
    var H = 40, ITEMS = __ITEMS__;
    var css = ""
      + "#mmt-bar{--mmt-bg:#14161a;--mmt-fg:#cfd4dc;--mmt-fg2:#8b93a1;"
      +   "all:initial;display:block;box-sizing:border-box;width:100%;height:" + H + "px;"
      +   "background:var(--mmt-bg);color:var(--mmt-fg);position:relative;z-index:2147483000;"
      +   "font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Helvetica Neue','Segoe UI',sans-serif}"
      + "#mmt-bar *,#mmt-bar *::after{box-sizing:border-box}"
      // 크롬 층이므로 제품 그리드에 맞추지 않고 고정 여백을 쓴다(애플 글로벌 바와 같은 원칙).
      + "#mmt-bar .mmt-in{display:flex;align-items:center;gap:16px;height:100%;"
      +   "padding:0 20px;overflow-x:auto;scrollbar-width:none}"
      + "@media(max-width:640px){#mmt-bar .mmt-in{padding:0 16px}}"
      + "#mmt-bar .mmt-in::-webkit-scrollbar{display:none}"
      + "#mmt-bar .mmt-wm{font-family:var(--mmt-wm-font,inherit);font-size:var(--mmt-wm-sm,15px);"
      + "font-weight:var(--mmt-wm-fw,800);letter-spacing:var(--mmt-wm-ls,-.035em);color:#111;text-decoration:none}"
      + "#mmt-bar .mmt-nav{display:flex;align-items:center;gap:4px;flex:0 0 auto}"
      + "#mmt-bar a.mmt-it{font-size:13px;font-weight:500;letter-spacing:-.01em;color:var(--mmt-fg);"
      +   "text-decoration:none;padding:5px 9px;border-radius:7px;white-space:nowrap;position:relative}"
      + "#mmt-bar a.mmt-it:hover{background:rgba(255,255,255,.1);color:#fff}"
      + "#mmt-bar a.mmt-it[aria-current=page]{background:#fff;color:#14161a;font-weight:700}"
      + "#mmt-bar .mmt-sep{width:1px;height:13px;background:rgba(255,255,255,.18);flex:0 0 auto;margin:0 5px}"
      + "#mmt-bar i.mmt-ext{font-style:normal;font-size:9px;opacity:.55;margin-left:3px;vertical-align:super}"
      + "#mmt-bar a.mmt-it[data-sub]::after{content:none;position:absolute;top:calc(100% + 7px);left:50%;"
      +   "transform:translateX(-50%) translateY(-3px);white-space:nowrap;background:#14161a;color:#fff;"
      +   "font-size:12px;font-weight:500;padding:6px 11px;border-radius:8px;opacity:0;visibility:hidden;"
      +   "pointer-events:none;transition:opacity .14s,transform .14s;box-shadow:0 10px 26px -12px rgba(0,0,0,.45)}"
      + "#mmt-bar a.mmt-it[data-sub]:hover::after,#mmt-bar a.mmt-it[data-sub]:focus-visible::after{"
      +   "opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}"
      + "@media(max-width:820px){#mmt-bar .mmt-in{gap:10px}#mmt-bar .mmt-sep{display:none}"
      +   "#mmt-bar a.mmt-it{padding:5px 7px}#mmt-bar a.mmt-it[data-sub]::after{display:none}}"
      + "@media(prefers-reduced-motion:reduce){#mmt-bar a.mmt-it[data-sub]::after{transition:none}}";

    var st = document.createElement("style");
    st.setAttribute("data-mmt", "shell");
    st.textContent = css;
    document.head.appendChild(st);

    var host = (location.hostname || "").replace(/^www\\./, "");
    var html = '<div class="mmt-in"><a class="mmt-wm" href="https://the-moment.us">MOMENTUS</a><nav class=\"mmt-nav\" aria-label="모멘터스">';
    for (var i = 0; i < ITEMS.length; i++) {
      var it = ITEMS[i], a = "";
      if (it.sep) html += '<span class="mmt-sep" aria-hidden="true"></span>';
      // ② 활성 표시 = 현재 도메인이 그 항목의 도메인과 같을 때만. 라벨 하드코딩 없음.
      var h = it.href.indexOf("//") > -1 ? it.href.split("//")[1].split("/")[0].replace(/^www\\./, "") : "";
      if (h && h === host) a += ' aria-current="page"';
      if (it.sub) a += ' data-sub="' + it.sub.replace(/"/g, "&quot;") + '"';
      if (it.ext) a += ' target="_blank" rel="noopener"';
      var href = it.href.indexOf("//") > -1 ? it.href : ("https://the-moment.us" + it.href);
      html += '<a class="mmt-it" href="' + href + '"' + a + '>' + it.label + (it.ext ? '<i class="mmt-ext" aria-hidden="true">↗</i>' : "") + '</a>';
    }
    html += "</nav></div>";

    var bar = document.createElement("div");
    bar.id = "mmt-bar";
    bar.innerHTML = html;
    // 제품이 고정 헤더를 내릴 때 쓸 값 — ⚠️ 바를 실제로 붙인 뒤에만 세운다.
    //   먼저 세우면 바가 실패했을 때 제품 헤더만 40px 내려가 빈 띠가 남는다(2026-07-27 실측).
    //
    // 스크롤: 바는 흐름 안에 있어 위로 밀려 나간다(애플 글로벌 바와 같은 거동).
    //   그때 제품의 고정 헤더도 같이 올라와 상단에 붙어야 한다 — 안 그러면 헤더가
    //   40px 아래 떠서 내용 위에 겹친다(2026-07-27 사장님 지적).
    //   → --mmt-bar-h 를 max(0, H - 스크롤) 로 갱신하면 제품은 CSS 한 줄 그대로 따라온다.
    // ── 패밀리 공용 디자인 토큰 ──
    //   여기 숫자 하나를 고치면 notes·mark·cue 의 2단 바가 동시에 따라온다("중앙에서 통제").
    //   제품은 반드시 var(--mmt-*, 자기값) 폴백 형태로 쓴다 → 이 파일이 못 떠도 원래 모습 유지(fail-open).
    var TOKENS = {
      "--mmt-gut": "clamp(20px, 4vw, 56px)",   // 로고 좌표(거터) — 세 사이트 동일해야 로고가 한 줄에 선다
      "--mmt-maxw": "1224px",                  // 2단 바 컨테이너 최대폭 — 공용 바(.mmt-in)와 **같은 값**이어야 한다
      "--mmt-bar2-h": "64px",                  // 2단 제품 바 높이
      "--mmt-fs-logo": "22px",
      "--mmt-fs-nav": "14px",
      "--mmt-fw-nav": "600",
      "--mmt-nav-gap": "26px",
      "--mmt-fs-cta": "14px",
      "--mmt-cta-pad": "9px 18px",
      "--mmt-cta-r": "999px",
      // ── 본문 타이포 ── 폰트는 셋 다 이미 Pretendard. 갈렸던 건 크기·행간·자간이었다
      //   (notes 16/1.65/-0.02 · cue 16/1.5/-0.01 · mark 15~17/1.6/-0.011).
      //   히어로·디스플레이 크기는 제품 브랜드 목소리라 건드리지 않는다.
      "--mmt-fs-base": "16px",
      "--mmt-lh-base": "1.6",
      "--mmt-ls-base": "-0.015em",
      "--mmt-fs-lead": "18px",         // 섹션 설명문
      "--mmt-lh-lead": "1.65",
      "--mmt-fs-sm": "14px",           // 캡션·보조
      "--mmt-fs-h3": "19px",
      "--mmt-fs-h2": "clamp(26px, 2.6vw, 34px)",   // 섹션 제목
      "--mmt-lh-head": "1.28",
      "--mmt-ls-head": "-0.035em"
    };
    var setH = function (v) { document.documentElement.style.setProperty("--mmt-bar-h", v + "px"); };
    var tick = 0;
    var onScroll = function () {
      if (tick) return;
      tick = requestAnimationFrame(function () {
        tick = 0;
        var y = window.pageYOffset || document.documentElement.scrollTop || 0;
        setH(Math.max(0, H - y));
      });
    };
    var put = function () {
      document.body.insertBefore(bar, document.body.firstChild);
      for (var k in TOKENS) document.documentElement.style.setProperty(k, TOKENS[k]);
      setH(H);
      onScroll();                                            // 새로고침이 중간 위치에서 일어난 경우
      window.addEventListener("scroll", onScroll, { passive: true });
    };
    if (document.body) put();
    else document.addEventListener("DOMContentLoaded", put);
  } catch (e) {
    // ① fail-open — 바를 못 그려도 제품 사이트는 그대로 산다.
    if (window.console) console.warn("[momentus shell] 바를 건너뜁니다:", e);
  }
})();
""".replace("__ITEMS__", SHELL_ITEMS)

with open("shell.js", "w", encoding="utf-8") as f:
    f.write(SHELL_JS)

# ---------- product detail pages ----------
DOCK_JS = """<script>
(function(){
  var btn=document.getElementById('vdhow'), g=document.getElementById('vdguide');
  if(!btn||!g) return;
  btn.addEventListener('click', function(){
    var open = g.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
})();
</script>"""

# ── 앱형 제품 랜딩(toss.im/service/teenagers 구조) ────────────────────────
#   가격은 쓰지 않는다 — 설치 하나에만 집중하고 가격은 스토어가 보여준다(2026-08-24 대표 지시).
FLIP_SCENES = [
    ("scene-webtoon", "누워서 웹툰을 볼 때",
     "손을 뻗지 않아도 다음 화면이 옵니다. 엄지가 볼륨키에 닿아 있으면 그걸로 끝입니다."),
    ("scene-instagram", "카페에서 피드를 넘길 때",
     "한 손엔 잔, 한 손엔 폰. 화면을 문지르지 않아도 됩니다."),
    ("scene-news", "출근길 지하철에서",
     "손잡이를 잡은 채로 기사를 끝까지 읽습니다."),
    ("scene-ebook", "비 오는 오후, 소파에서",
     "담요 밖으로 손을 내밀 필요가 없습니다. 전자책 한 권이 볼륨키 두 개로 넘어갑니다."),
    ("scene-recipe", "젖은 손으로 레시피를 볼 때",
     "화면을 만지면 자국이 남습니다. 볼륨키는 물기와 상관없습니다."),
    ("scene-pdf", "책상에서 문서를 훑을 때",
     "노트북 옆에 세워 두고 볼륨키로 페이지를 넘깁니다."),
    ("scene-article", "공원 벤치에서 긴 글을",
     "스크롤이 긴 글일수록 물리 버튼이 편합니다."),
]


def app_landing(slug, p):
    a = f"/assets/{slug}"
    store = p.get("store") or ""
    btn = (f'<a class="fl-btn" href="{store}" target="_blank" rel="noopener">'
           f'Google Play에서 받기</a>' if store else
           f'<a class="fl-btn" href="{purl(slug)}setup/">권한 켜는 법 보기</a>')
    sub = (f'<a class="fl-btn fl-btn--line" href="{purl(slug)}setup/">권한 켜는 법</a>')
    feats = p.get("feats") or []
    rows = ""
    for i, (t, d) in enumerate(feats[:3]):
        # ⚠️ 갤러리와 **겹치지 않는** 전용 컷을 쓴다 — 같은 사진이 한 페이지에 두 번 나오면
        #    스크롤이 되감기는 느낌이 든다(2026-08-24 대표 지적).
        # 있는 자산만 쓴다 — 새로 만들지 않는다(2026-08-24 대표 지시).
        #   갤러리 7컷과 겹치지 않는 것: 볼륨키 접사 + 원본 목업 2장.
        img = [f"{a}/feat-thumb.png", f"{a}/fold8ultra.jpg", f"{a}/fold8.jpg"][i]
        flip = " fl-row--flip" if i % 2 else ""
        rows += (f'<section class="fl-sec"><div class="fl-row{flip}">'
                 f'<div class="fl-row-tx"><span class="fl-num">{i + 1:02d}</span>'
                 f'<h2>{t}</h2><p>{d}</p></div>'
                 f'<div class="fl-art"><img src="{img}" alt="" loading="lazy"></div>'
                 f'</div></section>')
    def _scene(f, t, d):
        return (f'<div class="fl-scene"><figure><img src="{a}/{f}.png" '
                f'alt="{esc(t)}" loading="lazy"></figure>'
                f'<div class="tx"><b>{esc(t)}</b><p>{esc(d)}</p></div></div>')

    gal = ("".join(_scene(*x) for x in FLIP_SCENES[:1])
           + '<div class="fl-duo">' + "".join(_scene(*x) for x in FLIP_SCENES[1:3]) + '</div>'
           + "".join(_scene(*x) for x in FLIP_SCENES[3:4])
           + '<div class="fl-duo">' + "".join(_scene(*x) for x in FLIP_SCENES[4:6]) + '</div>'
           + "".join(_scene(*x) for x in FLIP_SCENES[6:7]))
    cards = "".join(
        f'<div class="fl-card"><span class="fr"><img src="{a}/{f}" alt="" loading="lazy"></span>'
        f'<div class="cap"><b>{t}</b><i>{d}</i></div></div>'
        for f, t, d in [
            ("screen-main.jpg", "어두운 화면", "밤에 누워 읽어도 눈이 부시지 않습니다."),
            ("screen-main-light.jpg", "밝은 화면", "낮에도 그대로 잘 보입니다."),
            ("screen-settings.jpg", "내 손에 맞게", "넘기는 거리와 느낌을 고를 수 있습니다."),
        ])
    spec = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in (p.get("spec") or []))
    extra = feats[3] if len(feats) > 3 else None
    return f"""<div class="fl">
  <header class="fl-hero">
    <p class="fl-kick">{esc(p["name"])}</p>
    <div class="fl-hero-in">
      <h1>{esc(p["tagline"])}</h1>
      <p class="lede">{p.get("lead", "")}</p>
    </div>
    <div class="fl-cta">{btn}{sub}</div>
    <p class="fl-note">{esc(p.get("ctasub") or p.get("platform", ""))}</p>
    <div class="fl-shot"><img src="{a}/hero.png" alt="{esc(p["name"])}" loading="eager"></div>
  </header>
  {rows}
  <section class="fl-demo">
    <div class="fl-phone" aria-hidden="true">
      <div class="scr"><div class="strip"><span>1</span><span>2</span><span>3</span></div></div>
      <span class="vk"></span>
    </div>
    <div class="fl-demo-tx"><span class="fl-num">04</span>
      <h2>누르면<br>다음 화면.</h2>
      <p>볼륨 아래 버튼을 누르면 한 화면씩 내려가고, 위 버튼을 누르면 되돌아옵니다.
        넘기는 거리는 화면 높이의 15~75%까지 다섯 단계로 고를 수 있습니다.</p></div>
  </section>
  <section class="fl-mid">
    <span class="fl-num">05</span>
    <h2>읽는 화면이면<br>어디서든 넘어갑니다.</h2>
    <p>웹툰도 릴스도 기사도, 스크롤로 읽는 화면이면 볼륨키만 누르면 됩니다.</p>
    <div class="fl-scenes">{gal}</div>
  </section>
  <section class="fl-mid">
    <span class="fl-num">06</span>
    <h2>내 손에 맞게 맞춥니다.</h2>
    <p>넘기는 거리는 5단계, 느낌도 고를 수 있습니다. 밝은 화면과 어두운 화면 모두 지원합니다.</p>
    <div class="fl-cards">{cards}</div>
  </section>
  {'<section class="fl-mid"><span class="fl-num">07</span><h2>' + esc(extra[0]) +
   '</h2><p>' + extra[1] + '</p></section>' if extra else ''}
  <section class="fl-mid">
    <span class="fl-num">08</span><h2>제품 사양</h2>
    <table class="fl-spec">{spec}</table>
  </section>
  <section class="fl-end">
    <h2>{esc(p.get("desire") or p["tagline"])}</h2>
    <div class="fl-cta">{btn}{sub}</div>
    <p class="fl-note">{esc(p.get("ctasub") or "")}</p>
  </section>
</div>"""


# ---------- 제품 상세 = vinylc 구조 (풀블리드 히어로 → 이미지 리듬 → CTA → Next) ----------
M = "https://www.vinylc.com/upload/module/"
G = "https://www.vinylc.com/upload/goods/"
# vinylc 상세 이미지 세트 (임시 — 추후 실제 제품 스크린샷으로 교체)
VIMG = [
    G + "GD00000066/vinylc_2021_calendar_diary_00.jpg",   # 0 히어로
    M + "MD00004413/vinylc_2021_calendar_diary_01.jpg",   # 1 풀블리드
    M + "MD00004415/vinylc_2021_calendar_diary_02.jpg",   # 2 소
    M + "MD00004416/vinylc_2021_calendar_diary_03.jpg",   # 3 대
    M + "MD00004417/vinylc_2021_calendar_diary_033.jpg",  # 4 짝
    M + "MD00004418/vinylc_2021_calendar_diary_04.jpg",   # 5 짝
    M + "MD00004420/vinylc_2021_calendar_diary_05.jpg",   # 6 와이드
    M + "MD00004421/vinylc_2021_calendar_diary_06.jpg",   # 7
    M + "MD00004422/vinylc_2021_calendar_diary_07.jpg",   # 8
    M + "MD00004425/vinylc_2021_calendar_diary_08.jpg",   # 9
    M + "MD00004426/vinylc_2021_calendar_diary_09.jpg",   # 10 와이드
    M + "MD00004428/vinylc_2021_calendar_diary_10.jpg",   # 11 풀블리드
]

for idx, slug in enumerate(ORDER):
    p = P[slug]
    nxt = ORDER[(idx + 1) % len(ORDER)]
    # 제품별로 이미지 순서를 돌려 서로 달라 보이게
    r = lambda n: VIMG[(n + idx * 3) % len(VIMG)]
    # 실제 도구 캡처 세트가 있으면 그걸 쓴다(hero/compare/d1/d2/wide/d3).
    # 없으면 옛 vinylc 사진으로 떨어진다 — 남의 사이트 이미지라 순차 교체 대상.
    SHOTS = p.get("shots") or []

    # feats 3개 → vinylc식 짧은 문단 3덩이
    f = p["feats"]
    note = lambda i: f'<div class="vd-note"><p><b>{f[i][0]}</b></p><p>{f[i][1]}</p></div>'

    # 설치 독 — 항시 노출. 설명서는 접혀 있다가 열림.
    guide = "".join(
        f'<div class="st"><div class="k">STEP {i+1}</div><b>{t}</b><p>{d}</p></div>'
        for i, (t, d) in enumerate(p["how"])
    )
    if p["cta"] == "drag":
        dock_sub = "설치 없음 · 끌어놓기만 하면 끝"
        dock_btn = (f'<span class="dragwrap" style="--dd:{p["color"]}"><a class="go" href="{BM[p["bm"]]}" '
                    f'data-bm="{p["bm"]}" {DRAG_ATTR}>{p.get("bmname", p["short"])}</a>{DRAG_DEMO}</span>')
    elif p["cta"] == "ext":
        dock_sub = p["ctasub"]
        dock_btn = f'<a class="go" href="{p["url"]}" target="_blank" rel="noopener">{p["ctatext"]}</a>'
    else:
        dock_sub = "크롬 웹스토어에서 1클릭 · 무료"
        dock_btn = f'<a class="go" href="{p["store"]}" target="_blank" rel="noopener">크롬에 추가 →</a>'

    hint_text = ("북마크바로 끌어놓으면 끝" if p["cta"] == "drag"
                 else p["ctasub"] if p["cta"] == "ext"
                 else "계정 없음 · 결제 없음 · 1클릭 제거")

    # ── 제품 안쪽으로 가는 문맥 링크(deeplinks) ─────────────────────────────
    # 왜 (2026-08-28, cue GSC 실측): 형제 사이트 약 860페이지가 이미 cue 를 링크하고 있었는데
    #   **전부 홈으로만** 갔다. 홈은 이미 크롤됐고, 깊은 페이지로 가는 경로가 없어
    #   609장이 "발견됨 - 크롤 안 됨"에 갇혀 있었다. 링크 수가 아니라 **어디로 가느냐**가 문제였다.
    # 🚫 링크를 남발하지 마라 — 제품이 실제로 제공하는 것만, 문맥에 맞게. 상호링크 스팸은 신호를 깎는다.
    _dl = p.get("deeplinks") or []
    deeplinks = ("" if not _dl else
        '<div class="vd-sec"><div class="vd-note"><p><b>안에 뭐가 있나</b></p><p>'
        + " · ".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in _dl)
        + '</p></div></div>')

    if SHOTS:
        rhythm = f"""<div class="vd-full"><img src="{SHOTS[1]}" alt="" loading="lazy"></div>

  {note(0)}

  <div class="vd-flow">
    <div class="vd-duo sh">
      <img src="{SHOTS[2]}" alt="" loading="lazy">
      <img src="{SHOTS[3]}" alt="" loading="lazy">
    </div>
  </div>

  {note(1)}

  <div class="vd-flow">
    <div class="vd-wide sh"><img src="{SHOTS[4]}" alt="" loading="lazy"></div>
  </div>

  {note(2)}

  <div class="vd-full"><img src="{SHOTS[5]}" alt="" loading="lazy"></div>"""
    else:
        rhythm = f"""<div class="vd-full"><img src="{r(1)}" alt="" loading="lazy"></div>

  {note(0)}

  <div class="vd-flow">
    <div class="vd-duo">
      <img src="{r(2)}" alt="" loading="lazy">
      <img src="{r(3)}" alt="" loading="lazy">
    </div>
  </div>

  {note(1)}

  <div class="vd-flow">
    <div class="vd-pair">
      <img src="{r(4)}" alt="" loading="lazy">
      <img src="{r(5)}" alt="" loading="lazy">
    </div>
    <div class="vd-wide"><img src="{r(6)}" alt="" loading="lazy"></div>
  </div>

  {note(2)}

  <div class="vd-flow">
    <div class="vd-duo rev">
      <img src="{r(9)}" alt="" loading="lazy">
      <img src="{r(7)}" alt="" loading="lazy">
    </div>
    <div class="vd-wide"><img src="{r(10)}" alt="" loading="lazy"></div>
  </div>

  <div class="vd-full"><img src="{r(11)}" alt="" loading="lazy"></div>"""

    if SHOTS or p.get("free"):
        _sp = "".join(f"<span>{esc(k)} · {esc(v)}</span>" for k, v in (p.get("spec") or [])[:3])
        cta_block = f"""<div class="vd-cta tool"><div class="wrap">
    <div class="kick">{esc((p.get('tag') or '무료 도구').split('·')[0].strip())}</div>
    <h3>{esc(p['tagline'])}</h3>
    <p class="sub">{esc(p.get('desire') or '')}</p>
    <div class="go">{cta(slug, big=True)}</div>
    <div class="chips">{_sp}</div>
    <div class="hint">{hint_text}</div>
  </div></div>"""
    else:
        cta_block = f"""<div class="vd-cta">
    {cta(slug, big=True)}
    <div class="hint">{hint_text}</div>
  </div>"""

    body = f"""<div class="vd">
  <div class="vd-hero">
    <img src="{SHOTS[0] if SHOTS else r(0)}" alt="{p['name']}">
    <div class="cap">
      <div class="kick">{p['tag']}</div>
      <h1>{p['tagline']}</h1>
    </div>
  </div>

  <div class="vd-note"><p>{p['lead']}</p></div>

  {rhythm}

  {cta_block}

  {_faq_html(p)}

  <a class="vd-next" href="{purl(nxt)}">
    <img src="{(P[nxt].get('shots') or [VIMG[(idx * 3 + 5) % len(VIMG)]])[0]}" alt="{P[nxt]['name']}" loading="lazy">
    <div class="cap">
      <div class="lbl">Next Product</div>
      <div class="ttl">{P[nxt]['tagline']}</div>
    </div>
  </a>
</div>

<div class="vd-dock">
  {deeplinks}
  <div class="vd-guide" id="vdguide">
    <div class="inner">{guide}</div>
  </div>
  <div class="bar">
    <div class="id">
      <div class="n">{p['name']}</div>
      <div class="s">{dock_sub}</div>
    </div>
    <div class="acts">
      <button class="how" type="button" id="vdhow" aria-expanded="false" aria-controls="vdguide">
        설치 방법 <span class="car">▾</span>
      </button>
      {dock_btn}
    </div>
  </div>
</div>"""
    # 무료 도구는 /tools/<slug>/ (본 도메인 경로 = 미끼의 유입 권위), 유료 스포크는 /products/<slug>/.
    _dir = purl(slug).strip("/")
    os.makedirs(_dir, exist_ok=True)
    # 앱형 제품(type=app)은 **자체 랜딩**을 쓴다 — 스토어로 보내는 게 목적이라 웹 제품과
    #   화면 구성이 다르다(2026-08-24). 본문만 갈아 끼우고 나머지 배선은 그대로.
    if p.get("type") == "app":
        body = app_landing(slug, p)
    with open(f"{_dir}/index.html", "w", encoding="utf-8") as fh:
        # description 은 70~120자여야 검색결과에서 제 몫을 한다(docs/SEO_GEO.md §3).
        # tagline 만 쓰면 10~29자라 구글이 무시하고 본문에서 임의 발췌한다(2026-08-07 실측).
        # 그래서 `desire`(방문자 욕망) + `lead`(무엇이 되는가)를 이어 붙여 만든다.
        _d = _re_desc(f"{p.get('desire') or p['tagline']} {p.get('lead') or ''}")
        fh.write(page(f"{p['name']} — MOMENTUS", _d, body,
                      active=("tools" if slug in TOOLS else ""), extra=DOCK_JS))

# (제품 인덱스 페이지 제거 — 홈이 곧 제품 목록이다. 중복 폐지)

# ---------- 이야기(공용 블로그) — 글은 content/stories/*.html 에 산다 ----------
#   ⚠️ 2026-07-27 전환: 전에는 본문이 이 파일 안 dict 에 박혀 있어 글 하나 쓰려면 1,800줄 코드를 고쳐야 했다.
#      이제 새 글 = content/stories/<slug>.html 파일 하나 추가. 생성기는 손대지 않는다.
#      형식 = frontmatter(--- 사이 key: value ---) + 본문 HTML. mark 저널의 콘텐츠 모델을 가져온 것.
def load_stories():
    out, d = {}, "content/stories"
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(d, fn), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            print(f"  ⚠️ frontmatter 없음: {fn} — 건너뜀")
            continue
        meta = {}
        for ln in m.group(1).split("\n"):
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip()] = v.strip()
        meta["slug"] = fn[:-5]
        meta["body"] = m.group(2).strip()
        meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        meta["mins"] = int(meta.get("mins", 5) or 5)
        out[meta["slug"]] = meta
    return out


POSTS = load_stories()
# 최신순. 날짜(ISO)는 문자열 정렬로 충분하다.
PORDER = sorted(POSTS, key=lambda s: POSTS[s].get("date", ""), reverse=True)
# 태그 축 = 매니페스트 파생(제품) + 사람. 새 제품이 생기면 태그도 자동으로 생긴다.
STORY_TAGS = [(s["slug"], s["tag"]) for s in BAR["spokes"] if s.get("tag")]
STORY_TAGS += [("tools", "무료 도구"), ("people", "사람")]
TAG_BY_LABEL = {lab: key for key, lab in STORY_TAGS}


# ---------- 랜딩 스트림 수집기 (PLATFORM_TOPOLOGY §10) ----------
#   허브가 스포크의 업데이트를 아는 법 = 푸시가 아니라 '풀'. 제품은 공개 피드 하나만 노출하면 되고,
#   apex 가 빌드할 때 읽어 온다. 실패해도 직전 캐시를 쓰고 조용히 넘어간다(빌드는 절대 안 깨진다).
#   자동화 상한은 2개 — 제품 피드 + 유튜브 RSS. 인스타·스레드는 손으로 한 줄(오버엔지니어링 방지선).
import datetime
import urllib.request
import xml.etree.ElementTree as ET

STREAM_CACHE = "data/stream_cache.json"


def _get(url, timeout=8):
    req = urllib.request.Request(url, headers={"user-agent": "momentus-site-generator"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# 제품이 발행한 글은 제품 사이트에 쌓인다(mark 만 172편). 허브의 '이야기'가 그걸 못 보면
# 우리가 쓴 글이 3편밖에 없는 것처럼 보인다(2026-08-23 대표 지적). 피드에서 **글만** 골라 온다.
# ⚠️ 채널 링크(<link>https://…/insights</link>)까지 글로 세면 목록에 껍데기가 섞인다.
#   경로에 슬러그가 붙은 항목만 글로 본다. 큐는 목록이 /insights 인데 **글은 /playbook/** 이다
#   (36편이 그 주소로 색인돼 있어 안 옮긴다) — 사이트마다 다르므로 여기서 각각 지정한다.
_FEED_ONLY = {"mark": "/insights/", "cue": "/playbook/"}


def _rss_items(raw, label, limit=4, only=None):
    root = ET.fromstring(raw)
    out = []
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        if only and only not in link:
            continue
        try:
            d = datetime.datetime.strptime(pub[:16], "%a, %d %b %Y").date().isoformat()
        except Exception:
            continue
        out.append(dict(kind="post", src=label, title=t, url=link, date=d,
                        desc=(it.findtext("description") or "").strip(),
                        cat=(it.findtext("category") or "").strip()))
        if len(out) >= limit:
            break
    return out


OG_CACHE = "data/og_cache.json"


def og_images(urls):
    """외부 글의 표지 = 그 페이지의 og:image. 한 번 읽으면 캐시에 남겨 다시 안 읽는다."""
    cache = {}
    if os.path.exists(OG_CACHE):
        try:
            cache = json.load(open(OG_CACHE, encoding="utf-8"))
        except Exception:
            cache = {}
    # ⚠️ 캐시를 영구로 믿으면 안 된다 — 마크가 재빌드될 때마다 Astro 해시가 바뀌어
    #   옛 og:image 주소가 404 가 된다(2026-08-24 홈 레일에서 깨진 그림 1장 실측).
    #   매 빌드에 다시 읽고, 네트워크가 실패했을 때만 캐시를 쓴다.
    miss = list(urls)
    for u in miss:
        try:
            html = _get(u, timeout=6).decode("utf-8", "ignore")
            m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html)
            cache[u] = m.group(1) if m else ""
        except Exception:
            cache.setdefault(u, "")        # 실패 시 옛 값 유지
    if miss:
        try:
            json.dump(cache, open(OG_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        except Exception:
            pass
        print(f"  · 외부 글 표지 조회: {len(miss)}건(신규)")
    return cache


def _shop_items(raw, label, base, limit=4):
    d = json.loads(raw)
    out = []
    for p0 in d.get("products", []):
        c = (p0.get("created_at") or "")[:10]
        if not c:
            continue
        _im = p0.get("hero") or p0.get("thumb")
        out.append(dict(kind="release", src=label,
                        title=(p0.get("name_kr") or p0.get("name_en") or p0.get("slug")),
                        url=f"{base}/p/{p0.get('slug')}", date=c,
                        img=(f"{base}/img/{_im}" if _im else "")))
    out.sort(key=lambda x: x["date"], reverse=True)
    return out[:limit]


def fetch_stream():
    """제품 피드를 긁어 단일 스트림으로. 소스별로 캐시하고, 실패한 소스만 캐시를 쓴다."""
    cache = {}
    if os.path.exists(STREAM_CACHE):
        try:
            cache = json.load(open(STREAM_CACHE, encoding="utf-8"))
        except Exception:
            cache = {}
    for sp in BAR["spokes"]:
        feed, key, label = sp.get("feed"), sp["slug"], sp["label"]
        # RSS 가 없는 사이트는 매니페스트에 글을 적어 둔다(컨텍스트). 대신 **조용히 낡지 않게**
        # 목록 페이지를 세어 개수가 다르면 시끄럽게 알린다. 손목록의 유일한 위험이 그거다.
        if sp.get("posts"):
            man = [dict(kind="post", src=label, title=x["title"], url=x["url"],
                        date=x["date"], desc=x.get("desc", ""), cat="")
                   for x in sp["posts"]]
            cache[key] = man
            print(f"  · 목록 {label}: {len(man)}건(매니페스트)")
            idx = sp.get("posts_index")
            if idx:
                try:
                    live = len(set(re.findall(rb'href="(/blog/[a-z0-9-]{5,})"', _get(idx))))
                    if live and live != len(man):
                        print(f"  ⚠️ {label} 글이 {live}편인데 매니페스트엔 {len(man)}편 — "
                              f"data/products.json 의 posts 를 갱신하라")
                except Exception as e:
                    print(f"  · {label} 신선도 확인 건너뜀({e})")
            continue
        if not feed:
            continue
        try:
            raw = _get(feed)
            base = feed.split("/")[0] + "//" + feed.split("/")[2]
            got = (_rss_items(raw, label, limit=40, only=_FEED_ONLY.get(key))
                   if feed.endswith(".xml") else _shop_items(raw, label, base))
            if got:
                cache[key] = got
                print(f"  · 피드 {label}: {len(got)}건")
            else:
                print(f"  ⚠️ 피드 {label}: 항목 0 — 캐시 사용")
        except Exception as e:
            print(f"  ⚠️ 피드 {label} 실패({e}) — 캐시 사용")
    try:
        json.dump(cache, open(STREAM_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception:
        pass
    return [x for v in cache.values() for x in v]


STREAM = fetch_stream()


def fmt_date(iso):
    p = (iso or "").split("-")
    return ". ".join(p) if len(p) == 3 else iso


COMMENT_HTML = """<section class="comments"><h3>댓글</h3>
<div class="cbox" id="cbox"><textarea id="ctext" placeholder="댓글을 남겨보세요…" rows="2"></textarea>
<div class="crow"><input id="cname" placeholder="이름 (선택)"><button id="cpost">등록</button></div></div>
<div class="cdone" id="cdone" hidden><span>🙌</span><div><b>고마워요, 잘 받았어요.</b> 댓글은 곧 열려요 — 준비되면 여기서 바로 알려드릴게요.</div></div></section>"""

def post_js(slug):
    return """<script>
var links=[].slice.call(document.querySelectorAll('.post-toc a')),secs=links.map(function(a){return document.querySelector(a.getAttribute('href'));});
addEventListener('scroll',function(){var y=scrollY+110,i=secs.length-1;while(i>0&&secs[i]&&secs[i].offsetTop>y)i--;links.forEach(function(a,j){a.classList.toggle('on',j===i);});},{passive:true});
var url=encodeURIComponent(location.href.split('?')[0]),ttl=encodeURIComponent(document.querySelector('.post-top h1').textContent);
document.getElementById('shX').href='https://twitter.com/intent/tweet?text='+ttl+'&url='+url;
document.getElementById('shF').href='https://www.facebook.com/sharer/sharer.php?u='+url;
document.getElementById('shL').href='https://www.linkedin.com/sharing/share-offsite/?url='+url;
document.getElementById('shC').addEventListener('click',function(){var b=this;navigator.clipboard.writeText(location.href.split('?')[0]).then(function(){b.textContent='✓';setTimeout(function(){b.textContent='↗';},1400);});});
var cp=document.getElementById('cpost');
if(cp){cp.addEventListener('click',function(){var t=document.getElementById('ctext').value.trim();if(!t)return;
try{var k='momentus_comment_interest';localStorage.setItem(k,(+localStorage.getItem(k)||0)+1);}catch(e){}
document.getElementById('cbox').hidden=true;document.getElementById('cdone').hidden=false;});}
</script>"""

# ---------- 이야기 렌더 — 글 페이지 · 인덱스 · 태그별 정적 페이지 · RSS ----------
#   URL 은 /insights/ — **전 사이트 공통**(2026-08-24 통일). 마크·큐·플래너가 다 이 주소다.
#   옛 /stories/ 는 _redirects 가 301 로 받는다(글 3편이 이미 색인됨).
#   ⚠️ 소스 폴더 content/stories/ 와 그림 /assets/stories/ 는 그대로 둔다 —
#     URL 이 아니라 내부 경로라 옮겨도 얻는 게 없고 링크만 깨진다.
STORY_BASE = "/insights"


def story_card(e, i=0):
    if e["kind"] == "video":
        th = f'<div class="th vid"><img src="{e["thumb"]}" alt="" loading="lazy"><span class="play"></span></div>'
        href, ext = e["url"], ' target="_blank" rel="noopener"'
    else:
        th = f'<div class="th g{(i % 3) + 1}"></div>'
        href, ext = f'{STORY_BASE}/{e["slug"]}/', ''
    tg = " ".join(e.get("tags", []))
    return (f'<div class="an-card" data-tags="{tg}"><a href="{href}"{ext}>{th}'
            f'<h3>{e["title"]}</h3>'
            f'<div class="m"><span class="cat">{e["cat"]}</span><span>{fmt_date(e["date"])}</span></div>'
            f'<p>{e["desc"]}</p></a></div>')


# 글 페이지
for i, slug in enumerate(PORDER):
    ps = POSTS[slug]
    rel = [x for x in PORDER if x != slug][:3]
    relh = "".join(
        f'<a href="{STORY_BASE}/{x}/"><b>{POSTS[x]["title"]}</b><p>{POSTS[x]["sub"]}</p>'
        f'<div class="more">더 읽기 →</div></a>' for x in rel)
    tagh = "".join(f'<a class="an-tag" href="{STORY_BASE}/tag/{TAG_BY_LABEL[t]}/">{t}</a>'
                   for t in ps["tags"] if t in TAG_BY_LABEL)
    # 목차 = 본문 h2 를 그대로 뽑는다(글마다 손으로 적지 않는다).
    _h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", ps["body"], re.S)
    _toc = _tocm = ""
    if len(_h2) >= 2:
        _bodyh = ps["body"]
        for n, t in enumerate(_h2):
            _bodyh = _bodyh.replace(f">{t}</h2>", f' id="s{n}">{t}</h2>', 1)
        ps = dict(ps, body=_bodyh)
        _items = [(n, re.sub(r"<[^>]+>", "", t)) for n, t in enumerate(_h2)]
        _toc = ('<nav class="pst-toc"><div class="rt">목차</div>'
                + "".join(f'<a href="#s{n}">{t}</a>' for n, t in _items) + '</nav>')
        # 좁은 화면에선 레일이 사라진다 — 그대로 없어지면 모바일은 목차를 아예 못 본다.
        _tocm = ('<details class="art-toc-m"><summary>목차</summary><ul>'
                 + "".join(f'<li><a href="#s{n}">{t}</a></li>' for n, t in _items)
                 + '</ul></details>')
    # '이어서 읽기'는 오른쪽 레일이 아니라 **글 끝**이다(2026-08-27 통합, 토스 '더 읽어보기' 자리).
    #   레일에선 썸네일이 56×42px 이라 사실상 안 보였고, 아직 읽는 중인 사람 옆구리에 붙어 있었다.
    _relcards = "".join(
        f'<a class="art-next-card" href="{STORY_BASE}/{x}/">'
        f'<span class="th"><img src="/assets/stories/{x}.png" alt="" loading="lazy"></span>'
        f'<div class="cat">{esc(POSTS[x]["cat"])}</div>'
        f'<h3>{esc(POSTS[x]["title"])}</h3></a>' for x in rel[:3])
    _next = (f'<section class="art-next"><h2 class="art-next-t">이어서 읽기</h2>'
             f'<div class="art-next-grid">{_relcards}</div></section>') if _relcards else ""
    _share = (f'<a href="https://twitter.com/intent/tweet?url=https://the-moment.us{STORY_BASE}/{slug}/"'
              f' target="_blank" rel="noopener" aria-label="X에 공유">X</a>'
              f'<a href="https://www.facebook.com/sharer/sharer.php?u=https://the-moment.us{STORY_BASE}/{slug}/"'
              f' target="_blank" rel="noopener" aria-label="페이스북에 공유">f</a>')
    # 목차 현재 위치 표시 — 전 사이트 같은 동작(큐 ART_SPY 와 같은 코드).
    _spy = ('<script>(function(){var ls=[].slice.call(document.querySelectorAll(".pst-toc a"));if(!ls.length||!window.IntersectionObserver)return;var secs=ls.map(function(a){return document.getElementById(a.getAttribute("href").slice(1))});var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var i=secs.indexOf(e.target);if(i<0)return;ls.forEach(function(a,j){a.classList.toggle("on",j===i)})})},{rootMargin:"-88px 0px -68% 0px"});secs.forEach(function(x){x&&io.observe(x)})})();</script>')
    body = f"""<div class="pst">
  <div class="pst-grid">
  <header class="pst-top">
    <p class="pst-kick">{esc(ps['cat'])}</p>
    <h1 class="pst-h1">{esc(ps['title'])}</h1>
  </header>
    {_toc}
    <article class="pst-main">
      <div class="pst-cover"><img src="/assets/stories/{slug}.png" alt="" loading="lazy"></div>
      <p class="pst-sub">{esc(ps['sub'])}</p>
      {_tocm}
      <div class="pst-prose">{ps['body']}</div>
      <div class="pst-meta">
        <div class="pst-by"><span class="av">M</span>
          <span><span class="nm">모멘터스</span><br><span class="dt">{fmt_date(ps['date'])} · {ps['mins']}분 읽기</span></span></div>
        <div class="pst-share">{_share}</div>
      </div>
      {_next}
    </article>
  <div class="pst-end">
    {'<div class="pst-tags">' + tagh + '</div>' if tagh else ''}
    <div class="pst-backwrap"><a class="pst-back" href="{STORY_BASE}/">인사이트 전체 보기</a></div>
  </div>
  </div>
</div>{_spy}"""
    os.makedirs(f"insights/{slug}", exist_ok=True)
    with open(f"insights/{slug}/index.html", "w", encoding="utf-8") as fh:
        # sub 가 짧으면(35자 미만) 제목을 앞세워 문맥을 보강한다 — 70자 미만이면 구글이 무시한다.
        _sd = ps["sub"] if len(ps["sub"]) >= 70 else _re_desc(f"{ps['sub']} {ps['title']} — 모멘터스가 제품을 만들며 알게 된 것을 실측과 함께 적은 글입니다.")
        fh.write(page(f"{ps['title']} — MOMENTUS 인사이트", _sd, body, active="story"))

# 스트림 = 글 + 영상(유튜브). 같은 시간축, 같은 카드. (PLATFORM_TOPOLOGY §10 '한 스트림')
entries = []
for i, x in enumerate(PORDER):
    p0 = POSTS[x]
    entries.append(dict(kind="post", slug=x, title=p0["title"], date=p0["date"],
                        cat=p0["cat"], desc=p0["sub"], tags=p0["tags"]))
for v in VIDEOS:
    entries.append(dict(kind="video", url=v["url"], title=v["title"], date=v["date"],
                        cat="영상", desc=v["desc"], thumb=v["thumb"], tags=[]))

# 제품 사이트에 쌓인 글을 같은 목록으로 끌어온다 — 우리가 쓴 글은 여기 다 모인다.
_TAG_BY_SRC = {sp["label"]: sp.get("tag", sp["label"]) for sp in BAR["spokes"]}
_ext = [x for x in STREAM if x.get("kind") == "post" and x.get("url")]
_ext.sort(key=lambda x: x["date"], reverse=True)
_covers = og_images([x["url"] for x in _ext[:60]])
for x in _ext:
    entries.append(dict(kind="ext", url=x["url"], title=x["title"], date=x["date"],
                        cat=x.get("cat") or x["src"], desc=x.get("desc", ""),
                        thumb=_covers.get(x["url"], ""), src=x["src"],
                        tags=[_TAG_BY_SRC.get(x["src"], x["src"])]))
entries.sort(key=lambda e: e["date"], reverse=True)

BLOG_JS = """<script>
(function(){
  var tabs=document.getElementById('bltabs'), grid=document.getElementById('blgrid'),
      empty=document.getElementById('blempty');
  if(!tabs||!grid) return;
  var items=[].slice.call(document.querySelectorAll('.nws-card,.nws-fcard'));
  tabs.addEventListener('click', function(e){
    var btn=e.target.closest('button[data-f]'); if(!btn) return;
    var f=btn.dataset.f, shown=0;
    [].slice.call(tabs.querySelectorAll('button')).forEach(function(b){
      b.setAttribute('aria-pressed', String(b===btn));
    });
    items.forEach(function(it){
      var ok=(f==='all')||(' '+(it.dataset.tags||'')+' ').indexOf(' '+f+' ')>-1;
      it.hidden=!ok; if(ok) shown++;
    });
    empty.hidden = shown>0;
  });
})();
</script>"""


def _story_cover(e):
    """표지 = 우리 글이면 /assets/stories/<slug>.png, 바깥 글이면 그 페이지의 og:image."""
    if e["kind"] in ("video", "ext"):
        return e.get("thumb", "")
    return f'/assets/stories/{e["slug"]}.png'


def _news_card(e):
    href = e["url"] if e["kind"] in ("video", "ext") else f'{STORY_BASE}/{e["slug"]}/'
    # 영상만 새 탭(유튜브). 제품 사이트 글은 같은 탭 — 거기에도 공용 바가 있어 바로 돌아온다.
    ext = ' target="_blank" rel="noopener"' if e["kind"] == "video" else ''
    cov = _story_cover(e)
    th = (f'<span class="th"><img src="{cov}" alt="" loading="lazy" decoding="async"></span>'
          if cov else '<span class="th"></span>')
    return (f'<a class="nws-card" href="{href}"{ext} data-tags="{" ".join(e.get("tags", []))}">'
            f'{th}<h3>{esc(e["title"])}</h3>'
            f'<div class="d">{esc(e["cat"])} · {fmt_date(e["date"])}</div></a>')


def _news_feature(e):
    href = e["url"] if e["kind"] in ("video", "ext") else f'{STORY_BASE}/{e["slug"]}/'
    ext = ' target="_blank" rel="noopener"' if e["kind"] == "video" else ''
    cov = _story_cover(e)
    img = f'<img src="{cov}" alt="" loading="lazy" decoding="async">' if cov else ''
    return (f'<a class="nws-fcard" href="{href}"{ext} data-tags="{" ".join(e.get("tags", []))}">{img}'
            f'<span class="tx"><span class="m">{esc(e["cat"])} · {fmt_date(e["date"])}</span>'
            f'<h2>{esc(e["title"])}</h2></span></a>')


def stories_page(title, sub, sel_label="", items=None, chips=True):
    its = items if items is not None else entries
    # 피처는 우리 글 우선 — 바깥 글 표지는 글자가 박힌 배너라 큰 화면에 깔면 잘린다.
    _own = [e for e in its if e.get("kind") == "post"][:2]
    feat = _own if len(_own) == 2 else its[:2]
    rest = [e for e in its if e not in feat]
    tabs = ""
    if chips:
        tabs = ('<div class="nws-tabs" id="bltabs">'
                '<button type="button" data-f="all" aria-pressed="true">전체</button>'
                + "".join(f'<button type="button" data-f="{lab}" aria-pressed="false">{lab}</button>'
                          for _, lab in STORY_TAGS) + '</div>')
    feath = ('<div class="nws-feat">' + "".join(_news_feature(e) for e in feat) + '</div>') if feat else ''
    listh = "".join(_news_card(e) for e in rest)
    sec = ''
    if rest:
        sec = (f'<section class="nws-sec"><div class="nws-sec-h"><h2>글</h2></div>'
               f'<div class="nws-row"><div class="nws-rail">전체 {len(its)}편</div>'
               f'<div class="nws-grid" id="blgrid">{listh}</div></div>'
               f'<p class="nws-empty" id="blempty" hidden>해당하는 글이 없어요.</p></section>')
    else:
        sec = ('<section class="nws-sec"><div class="nws-row">'
               f'<div class="nws-rail">전체 {len(its)}편</div>'
               f'<div class="nws-grid" id="blgrid"></div></div>'
               '<p class="nws-empty" id="blempty" hidden>해당하는 글이 없어요.</p></section>')
    return f"""<div class="nws">
  <header class="nws-head">
    <h1>{title}</h1>
    <p>{sub}</p>
    {tabs}
  </header>
  {feath}
  {sec}
</div>"""


LSUB = ("만든 것, 안 된 것, 배운 것을 그대로 적습니다. 자랑이 아니라 실측입니다.")
os.makedirs("insights", exist_ok=True)
with open("insights/index.html", "w", encoding="utf-8") as f:
    f.write(page("인사이트 — MOMENTUS", "AI로 제품을 만들며 알게 된 것들을 적습니다. 잘된 자랑이 아니라 실측 데이터와 실패 기록입니다. 로고 공모 524회 참가 결과, 에이전트를 만들며 세 번 버린 것 같은 이야기가 있습니다.",
                 stories_page("인사이트", LSUB), active="story", extra=BLOG_JS))

# 태그별 정적 페이지 — 제품 2단 바의 '이야기'가 여기로 온다. 매니페스트에서 자동 생성.
for key, lab in STORY_TAGS:
    sel = [e for e in entries if lab in e.get("tags", [])]
    os.makedirs(f"insights/tag/{key}", exist_ok=True)
    body = stories_page(f"{lab} 인사이트",
                        f"‘{lab}’ 태그가 붙은 글 {len(sel)}편. <a href=\"{STORY_BASE}/\">전체 보기 →</a>",
                        items=sel, chips=False)
    # 글이 0편인 태그는 색인시키지 않는다 — thin content 는 사이트 품질 신호를 깎는다.
    # 페이지 자체는 남긴다(링크가 죽으면 안 된다). 글이 붙으면 다음 빌드에 자동으로 색인 복귀.
    _nx = '<meta name="robots" content="noindex,follow">\n' if not sel else ""
    with open(f"insights/tag/{key}/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"{lab} 인사이트 — MOMENTUS",
                      _re_desc(f"‘{lab}’ 태그가 붙은 모멘터스 인사이트 {len(sel)}편. "
                               f"제품을 만들며 실제로 겪은 것과 실측 데이터를 적습니다.")
                      if sel else _re_desc(f"‘{lab}’ 태그의 모멘터스 인사이트입니다. 아직 이 태그로 발행한 글이 없습니다. "
                               f"전체 이야기에서 실측 데이터와 실패 기록을 보실 수 있습니다."),
                      body, active="story", head_extra=_nx))

# RSS — mark 저널과 같은 관행(구독 경로는 하나)
_items = "".join(
    f"<item><title>{POSTS[s]['title']}</title>"
    f"<link>https://the-moment.us{STORY_BASE}/{s}/</link>"
    f"<guid>https://the-moment.us{STORY_BASE}/{s}/</guid>"
    f"<description>{POSTS[s]['sub']}</description></item>" for s in PORDER)
with open("insights/rss.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            "<title>MOMENTUS 인사이트</title><link>https://the-moment.us/insights/</link>"
            "<description>AI로 제품을 만들며 알게 된 것들.</description>"
            f"{_items}</channel></rss>\n")


# (만들어드려요 폐기 — 요청은 유튜브 댓글에서 받는다)

# ---------- about ----------
about_body = """<div class="abt">
  <header class="abt-hero">
    <h1>나머지는<br>저희가 합니다.</h1>
    <p class="sub">사람이 안 해도 되는 일을 덜어냅니다.</p>
    <p class="lede">기다리고, 찾고, 정리하는 일. 그건 기계가 더 잘합니다.
      그 시간을 돌려드리는 게 저희가 만드는 이유입니다.</p>
  </header>

  <section class="abt-sec">
    <div class="abt-row">
      <div class="abt-lbl">우리가 믿는 것</div>
      <div>
        <p class="abt-say">사람이 할 일과 기계가 할 일은 다릅니다.</p>
        <p class="abt-body">취소표가 나올 때까지 새로고침하는 일, 로고 시안을 백 장 넘겨 보는 일,
          면접 예상 질문을 혼자 소리 내어 읽는 일. 하기 싫어서가 아니라, 사람이 하기엔 아까운 일입니다.</p>
        <p class="abt-body">저희는 그런 일부터 기계에 넘깁니다. 대단한 걸 하겠다는 게 아니라,
          저녁 시간을 일이 아니라 사람에게 쓰시게 하려는 겁니다.</p>
      </div>
    </div>
  </section>
</div>

<div class="abt-band"><div class="abt-band-in">
  <img src="/assets/about/moment.png" alt="저녁 거실에서 아이와 함께 책을 보는 모습" loading="lazy">
  <div class="abt-band-tx">
    <h2>저녁 7시엔<br>일이 아니라 사람이.</h2>
    <p>모멘터스라는 이름은 그 순간에서 왔습니다.</p>
  </div>
</div></div>

<div class="abt">
  <section class="abt-sec">
    <div class="abt-row">
      <div class="abt-lbl">만드는 방식</div>
      <div>
        <p class="abt-say">우리가 먼저 쓰다가, 남은 것만 팝니다.</p>
        <p class="abt-body">여기 있는 제품은 전부 저희가 쓰려고 만든 것입니다.
          매일 안 쓰게 되면 그대로 버립니다. 살아남은 것만 남아 있습니다.</p>
      </div>
    </div>
    <div class="abt-cards" style="margin-top:34px">
      <div class="abt-card"><div class="n">01</div>
        <h3>내가 안 쓰면 만들지 않습니다</h3>
        <p>남이 필요할 것 같아서 만든 건 전부 실패했습니다. 내 불편에서 시작한 것만 남았습니다.</p></div>
      <div class="abt-card"><div class="n">02</div>
        <h3>설명이 필요하면 진 겁니다</h3>
        <p>쓰는 법을 설명해야 하는 도구는 안 쓰게 됩니다. 눌러 보면 알아야 합니다.</p></div>
      <div class="abt-card"><div class="n">03</div>
        <h3>공짜로 풀 수 있으면 풉니다</h3>
        <p>돈을 받을 이유가 없는 건 그냥 드립니다. 브라우저 도구 6종이 그렇습니다.</p></div>
    </div>
  </section>

  <section class="abt-sec">
    <div class="abt-row">
      <div class="abt-lbl">만드는 사람</div>
      <div>
        <p class="abt-say">남의 제품을 20년 만들었고, 이제 우리 걸 만듭니다.</p>
        <p class="abt-body">이모션글로벌, NC소프트 재팬, 아이플래테아, 네오랩컨버전스, 엔카닷컴.
          이름을 다 아실 필요는 없습니다. 그 시간에 배운 걸로 지금 이걸 만듭니다.</p>
        <p class="abt-body">제품을 만드는 사람과, 그게 굴러가게 하는 사람. 둘이서 합니다.</p>
      </div>
    </div>
    <div class="abt-nums" style="margin-top:34px">
      <div class="abt-num"><b>20년</b><span>제품을 만든 시간</span></div>
      <div class="abt-num"><b>5종</b><span>파는 제품</span></div>
      <div class="abt-num"><b>6종</b><span>그냥 드리는 도구</span></div>
      <div class="abt-num"><b>2명</b><span>만드는 사람</span></div>
    </div>
    <figure class="abt-fig">
      <img src="/assets/about/desk.png" alt="1인 스튜디오의 아침 책상" loading="lazy">
      <figcaption>사무실은 없습니다. 책상 하나에서 기획부터 배포까지 합니다.</figcaption>
    </figure>
  </section>

  <section class="abt-sec">
    <div class="abt-row">
      <div class="abt-lbl">지나온 것</div>
      <div class="abt-hist">
        <div class="abt-hist-it"><span class="y">2024</span>
          <div><h4>모멘터스를 열었습니다</h4><p>남의 제품을 만들던 20년을 접고, 우리 것을 만들기 시작했습니다.</p></div></div>
        <div class="abt-hist-it"><span class="y">2025</span>
          <div><h4>무료 도구를 먼저 풀었습니다</h4><p>설치 없이 쓰는 브라우저 도구 6종. 회원가입도 결제도 없습니다.</p></div></div>
        <div class="abt-hist-it"><span class="y">2026</span>
          <div><h4>파는 제품이 5종이 됐습니다</h4><p>상품사진 · 로고 · 모의면접 · 플래너 · 빈방 알림.</p></div></div>
      </div>
    </div>
  </section>

  <section class="abt-end">
    <h2>덜어 드릴 게 있으신가요.</h2>
    <p>지금 없는 것도 괜찮습니다. 어떤 일이 번거로우신지 알려 주시면
      만들 수 있는 것인지 먼저 보고 답을 드립니다. 직접 읽고 직접 답합니다.</p>
    <div class="btns">
      <a class="b" href="/inquiry/">문의하기</a>
      <a class="b line" href="/products/">제품 보기</a>
    </div>
  </section>
</div>"""
os.makedirs("about", exist_ok=True)
with open("about/index.html", "w", encoding="utf-8") as f:
    f.write(page("소개 — MOMENTUS", "모멘터스는 사람이 안 해도 되는 일을 덜어내는 1인 AI 스튜디오입니다. 기다리고 찾고 정리하는 일을 기계에 넘기고, 그 시간을 돌려드립니다. 무엇을 어떻게 만드는지 적어 두었습니다.", about_body, active="about"))

# ---------- landing (root index.html) ----------
# ---------- 랜딩 카드 이미지 — 남의 사이트 핫링크 제거 ----------
#   2026-07-28: 랜딩 카드 10장이 vinylc.com(타사) 이미지를 핫링크하고 있었다.
#   제품은 우리 자산(products[].shot), 무료 도구는 아이콘 카드로 그린다.
def card_media(slug):
    p0 = P.get(slug, {})
    shot = p0.get("shot")
    if shot:
        return f'<div class="vc-thumb"><img src="{shot}" alt="{p0.get("tagline","")}" loading="lazy"></div>'
    return (f'<div class="vc-thumb vc-ic" style="--ic:{p0.get("color","#3182f6")}">'
            f'<span>{p0.get("icon","◆")}</span></div>')


def fix_card_media(html):
    """랜딩 리터럴 블록의 외부 이미지를 우리 자산/아이콘 카드로 치환."""
    import re as _re
    def _sub(m):
        return m.group(1) + card_media(m.group(2))
    return _re.sub(r'(<a href="/(?:tools|products)/([a-z-]+)/">\s*)<div class="vc-thumb"><img src="https://www\.vinylc[^>]*>\s*</div>',
                   lambda m: m.group(1) + card_media(m.group(2)), html)


# ---------- 랜딩 (KB 구성 클론) ----------
#   레퍼런스: blog.kakaobank.com/home — '구성'만 가져온다.
#   섹션 순서 = 히어로(이미지+메타) → 최신 콘텐츠 레일 → 인기 콘텐츠 3열 → 시리즈 레일
#              → 카테고리 스크롤러 → 푸터. 크롬 = 알약 GNB · 검색 오버레이 · 다크모드.
#   ⚠️ 남의 카피·일러스트·로고는 한 조각도 쓰지 않는다. 내용물은 전부 우리 자산
#      (products.json · 스트림 캐시 · content/stories). 스타일은 다음 단계에서 우리 색으로 갈아탄다.

# 제품 슬러그 → 카테고리 단어(스크롤러·칩에 쓰는 영문 라벨)
KB_WORD = {
    "heyreci": "Product Photo", "mark": "Logo", "theplan": "Planner", "cue": "Interview",
    "quickpang": "Coupang", "insta-rank": "Instagram", "youtube-rank": "YouTube",
    "pinterest-grab": "Pinterest", "chatpage": "Summary", "her": "Voice",
}

KINDN = {"release": "새 제품", "post": "글", "video": "영상", "tool": "새 도구"}
_all_new = STREAM + [dict(kind="post", src="모멘터스", title=POSTS[x]["title"],
                          url=f"{STORY_BASE}/{x}/", date=POSTS[x]["date"], img="") for x in PORDER]
_all_new = [x for x in _all_new if x.get("date")]
_all_new.sort(key=lambda x: x["date"], reverse=True)


def kb_media(slug, cls="kb-th"):
    """카드 비주얼 — 우리 자산(shot)이 있으면 사진, 없으면 아이콘 타일.
       (2026-07-28 사고: 랜딩 카드가 남의 사이트 이미지를 핫링크하고 있었다. 다시는.)"""
    p0 = P.get(slug, {})
    if p0.get("shot"):
        return f'<div class="{cls}"><img src="{p0["shot"]}" alt="{esc(p0.get("tagline",""))}" loading="lazy"></div>'
    return (f'<div class="{cls} ic" style="--ic:{p0.get("color","#3182f6")}">'
            f'<span>{p0.get("icon","◆")}</span></div>')


def _ext(url):
    return ' target="_blank" rel="noopener"' if str(url).startswith("http") else ""


# ── ① 히어로 ─────────────────────────────────────────────────────────────────
_hero = BAR.get("hero_shots", [])
_kb_slides = "".join(
    f'<article class="kb-slide{" on" if i == 0 else ""}" data-i="{i}">'
    f'<a class="kb-hero-art" href="{x.get("href","/")}"{_ext(x.get("href",""))}>'
    f'<img src="{x["src"]}" alt="{esc(x["alt"])}" loading="{"eager" if i == 0 else "lazy"}" '
    f'decoding="async" style="object-fit:{x.get("fit","cover")}"></a>'
    f'<div class="kb-hero-meta"><div class="kb-kick">{esc(x["label"])}</div>'
    f'<h1>{esc(x.get("title", x["label"]))}</h1>'
    f'<p>{esc(x.get("sub",""))}</p>'
    f'<a class="kb-cta" href="{x.get("href","/")}"{_ext(x.get("href",""))}>{esc(x.get("cta","보러 가기"))} <span aria-hidden="true">→</span></a>'
    f'</div></article>' for i, x in enumerate(_hero))
_kb_dots = "".join(
    f'<button type="button" data-i="{i}" aria-label="{esc(x["label"])}"'
    + (" aria-current=true" if i == 0 else "") + '></button>' for i, x in enumerate(_hero))
kb_hero = (f'<section class="kb-hero" id="kbhero" aria-label="주요 소식">{_kb_slides}'
           f'<div class="kb-dots">{_kb_dots}</div></section>') if _hero else ""


# ── ② 최신 콘텐츠 (가로 레일) ────────────────────────────────────────────────
_rail_items = _all_new[:10]
_rail_cards = "".join(
    f'<a class="kb-rail-card" href="{x["url"]}"{_ext(x["url"])}>'
    + (f'<div class="kb-rail-th"><img src="{x["img"]}" alt="" loading="lazy"></div>'
       if x.get("img") else
       f'<div class="kb-rail-th ic" style="--ic:#3182f6"><span>{KINDN.get(x["kind"],"소식")[:1]}</span></div>')
    + f'<div class="kb-rail-tx"><h3>{esc(x["title"])}</h3>'
      f'<time>{fmt_date(x["date"])}</time></div></a>' for x in _rail_items)
kb_latest = (f"""<section class="kb-sec" aria-labelledby="kb-latest-h">
  <div class="kb-sec-head"><h2 id="kb-latest-h">최신 콘텐츠</h2>
    <div class="kb-arrows" data-rail="kbrail">
      <button type="button" data-dir="-1" aria-label="이전 슬라이드"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
      <button type="button" data-dir="1" aria-label="다음 슬라이드"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </div></div>
  <div class="kb-rail" id="kbrail">{_rail_cards}</div>
</section>""") if _rail_cards else ""


# ── ③ 인기 콘텐츠 (3열 그리드) ───────────────────────────────────────────────
_grid_slugs = [s for s in ORDER if s in P][:6]
_grid_cards = "".join(
    f'<a class="kb-card" href="{purl(s)}">'
    + kb_media(s)
    + f'<time>{"무료 도구" if P[s].get("free") else "제품"} · {KB_WORD.get(s, P[s].get("short",""))}</time>'
      f'<h3>{esc(P[s].get("tagline", P[s]["name"]))}</h3>'
      f'<div class="kb-chips">'
    + "".join(f'<span>{esc(t.strip())}</span>' for t in P[s].get("tag", "").split("·") if t.strip())
    + '</div></a>' for s in _grid_slugs)
kb_popular = f"""<section class="kb-sec" aria-labelledby="kb-pop-h">
  <div class="kb-sec-head"><h2 id="kb-pop-h">많이 찾는 것</h2>
    <a class="kb-kick" href="/products/">제품 전체 →</a></div>
  <div class="kb-grid">{_grid_cards}</div>
</section>"""


# ── ④ 시리즈 레일 ────────────────────────────────────────────────────────────
def _stream_by(src, n=3):
    return [x for x in STREAM if x.get("src") == src][:n]


_series = []
_pl = _stream_by("플래너")
if _pl:
    _series.append(dict(title="새로 나온 플래너", href="https://notes.the-moment.us",
                        cover=P.get("theplan", {}).get("shot", ""), color="#f7f6f1", items=_pl))
_lg = _stream_by("로고")
if _lg:
    _series.append(dict(title="업종별 로고 이야기", href="https://mark.the-moment.us/insights/",
                        cover=P.get("mark", {}).get("shot", ""), color="#eef3ff", items=_lg))
if PORDER:
    _series.append(dict(title="스튜디오의 기록", href=f"{STORY_BASE}/", cover="", color="#f2f4f7",
                        items=[dict(title=POSTS[x]["title"], url=f"{STORY_BASE}/{x}/", img="")
                               for x in PORDER[:3]]))
_tl = [s for s in TOOLS if s in P][:3]
if _tl:
    _series.append(dict(title="브라우저에 붙이는 무료 도구", href="/products/", cover="", color="#eafaf1",
                        items=[dict(title=P[s].get("tagline", P[s]["name"]), url=purl(s),
                                    img=P[s].get("shot", ""), icon=P[s].get("icon", "◆"),
                                    color=P[s].get("color", "#3182f6")) for s in _tl]))


def _series_pair(sr):
    lis = "".join(
        f'<li><a href="{it["url"]}"{_ext(it["url"])}>'
        f'<span class="n">{i+1:02d}</span>'
        + (f'<span class="sq"><img src="{it["img"]}" alt="" loading="lazy"></span>'
           if it.get("img") else
           f'<span class="sq" style="--ic:{it.get("color","#9aa0a8")}">{it.get("icon","·")}</span>')
        + f'<span class="t">{esc(it["title"])}</span></a></li>' for i, it in enumerate(sr["items"]))
    cover = (f'<img src="{sr["cover"]}" alt="" loading="lazy">' if sr.get("cover")
             else f'<span class="kb-kick">{esc(sr["title"])}</span>')
    return (f'<div class="kb-spair">'
            f'<div class="kb-spanel"><span class="kb-badge">Series</span><h3>{esc(sr["title"])}</h3>'
            f'<ul class="kb-slist">{lis}</ul></div>'
            f'<a class="kb-scover" href="{sr["href"]}"{_ext(sr["href"])} '
            f'style="--sc:{sr["color"]}" aria-label="{esc(sr["title"])}">{cover}</a></div>')


kb_series = (f"""<section class="kb-sec" aria-labelledby="kb-ser-h">
  <div class="kb-sec-head"><h2 id="kb-ser-h">묶어서 보면 더 좋은 것</h2>
    <div class="kb-arrows" data-rail="kbsrail">
      <button type="button" data-dir="-1" aria-label="이전 슬라이드"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
      <button type="button" data-dir="1" aria-label="다음 슬라이드"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </div></div>
  <div class="kb-srail" id="kbsrail">{"".join(_series_pair(s) for s in _series)}</div>
  <div class="kb-srail-foot"><a class="kb-pill" href="/products/">전체 보기</a></div>
</section>""") if _series else ""


# ── ⑤ 카테고리 스크롤러 ──────────────────────────────────────────────────────
_cat_slugs = [s for s in ORDER if s in P]
_cat_words = "".join(
    '<li' + (" aria-current=true" if i == 0 else "") + '>'
    + f'<button type="button" data-i="{i}">{KB_WORD.get(s, P[s].get("short",""))}</button></li>'
    for i, s in enumerate(_cat_slugs))
_cat_data = json.dumps([dict(
    slug=s, url=purl(s), name=P[s].get("short", P[s]["name"]),
    tagline=P[s].get("tagline", ""), shot=P[s].get("shot", ""),
    icon=P[s].get("icon", "◆"), color=P[s].get("color", "#3182f6"),
) for s in _cat_slugs], ensure_ascii=False)

kb_cats = f"""<section class="kb-sec" aria-labelledby="kb-cat-h">
  <div class="kb-sec-head"><h2 id="kb-cat-h">무엇을 하려고 오셨나요</h2></div>
  <div class="kb-cats" id="kbcats">
    <a class="kb-cat-card" id="kbcatcard" href="/"><span class="kb-cat-art"></span><h3></h3><p></p></a>
    <div class="kb-cat-view">
      <ul class="kb-cat-list" id="kbcatlist">{_cat_words}</ul>
      <div class="kb-cat-ctl">
        <button type="button" id="kbcatpause" aria-label="자동 넘김 멈춤">
          <svg viewBox="0 0 24 24" class="pauseon"><path d="M9 5v14M15 5v14"/></svg>
          <svg viewBox="0 0 24 24" class="pauseoff"><path d="M7 4l12 8-12 8z"/></svg></button>
        <button type="button" data-dir="-1" aria-label="이전 카테고리"><svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
        <button type="button" data-dir="1" aria-label="다음 카테고리"><svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg></button>
      </div>
    </div>
  </div>
</section>"""


# ── 헤더 · 검색 인덱스 ───────────────────────────────────────────────────────
# 검색 결과는 **무엇인지 알아볼 수 있어야 한다** — 글자만 나열하면 뭐가 뭔지 모른다
# (2026-08-23 대표: "썸네일도 좀 나와 주면서 저게 나와야지"). 그림·종류·부제를 같이 싣는다.
def _kb_row(sl):
    pr = P[sl]
    return dict(t=pr.get("short") or pr.get("name", sl),
                k="무료 도구" if pr.get("free") else "제품",
                g=pr.get("tag", ""), u=purl(sl),
                im=pr.get("shot") or "", ic=pr.get("icon", ""))


KB_INDEX = json.dumps(
    [_kb_row(s) for s in ORDER if s in P]
    + [dict(t=POSTS[x]["title"], k="이야기", g=POSTS[x].get("date", ""),
            u=f"{STORY_BASE}/{x}/", im=POSTS[x].get("cover", "") or "", ic="✎") for x in PORDER],
    ensure_ascii=False)

KB_HEAD = """<script>
/* 다크모드 — 그리기 전에 결정해서 흰 화면 번쩍임(FOUC)을 막는다. */
(function(){try{var t=localStorage.getItem('mmt-theme');
if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.dataset.theme=t;}catch(e){}})();
</script>"""

KB_JS = """<button class="kb-top" id="kbtop" aria-label="맨 위로">
<svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
<script>
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
  var IDX=__INDEX__;
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
  var CATS=__CATS__, list=$('kbcatlist'), card=$('kbcatcard');
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
</script>"""

KB_JS = KB_JS.replace("__INDEX__", KB_INDEX).replace("__CATS__", _cat_data)

# ── 공용 스크립트 파일 — 37개 페이지에 같은 스크립트를 인라인으로 복사하지 않는다.
#    page() 가 <script defer src="/assets/apex.js?v=CSS_VER"> 로 건다.
def _strip_tags(js):
    out, i = [], 0
    while True:
        a = js.find("<script>", i)
        if a < 0:
            break
        b = js.index("</script>", a)
        out.append(js[a + len("<script>"):b])
        i = b + len("</script>")
    return "\n".join(out)


_apex_js = _strip_tags(KB_JS) + """
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
"""
with open("assets/apex.js", "w", encoding="utf-8") as f:
    f.write(_apex_js)

# ---------- 홈 — 제품 무대(Apple 문법) ----------
#   ⚠️ 옛 구성(kb_hero/kb_latest/kb_popular/kb_series/kb_cats)은 더 이상 홈에 싣지 않는다.
#      변수 자체는 남겨 둔다 — 다른 데서 참조하거나 되돌릴 때를 위해.
_SPOKE_HREF = {sp["slug"]: sp["href"] for sp in BAR["spokes"] if sp.get("slug")}
_SPOKE_HREF["flipper"] = P["flipper"]["store"]   # 앱은 스토어로 바로 보낸다
# 두 번째 버튼은 '알아보기'가 아니라 **그 제품에서 하는 일**을 말한다(애플의 '구입하기' 자리).
AP_GO = {"teamai": "팀AI 시작하기", "binbang": "빈방 알림 등록", "heyreci": "헤이레시 열기", "mark": "로고 만들어 보기",
         "cue": "모의면접 시작하기", "theplan": "플래너 보러 가기",
         "kontext": "컨텍스트 열기", "flipper": "Google Play에서 받기"}


# 홈 타일은 **글자가 없는 사진**을 쓴다. og 배너를 깔면 우리 제목과 겹친다.
#   더플랜은 notes 쇼룸(히어로 슬라이드) 이미지를 그대로 가져다 쓴다(2026-08-23 대표 지시).


def ap_stage(slug, tone="", badge=""):
    """제품 카드 = 그림(꽉 참) → 업종 한 줄 → 이름 → 한 줄 → 버튼 둘(우하단).
       애플 제품 카드(apple.com/airpods)의 배치 그대로."""
    pr = P[slug]
    p_type = pr.get("type")
    go = _SPOKE_HREF.get(slug, "")
    # 버튼은 하나다. '더 알아보기'와 '열기'는 결국 같은 말이라 둘을 나란히 두면 고민만 는다
    # (2026-08-23 대표: "여기는 메뉴가 두 개가 아니잖아"). 바로 그 제품에서 할 일 하나만 둔다.
    # 앱형은 '더 알아보기'(제품 페이지)와 '받기'(스토어) 둘 다 필요하다 — 설치 전에 볼 게 있다.
    if p_type == "app":
        cta = (f'<a class="stg-pill" href="{purl(slug)}">더 알아보기</a>'
               f'<a class="stg-pill stg-pill--line" href="{go}"{_ext(go)}>'
               f'{AP_GO.get(slug, "바로 가기")}</a>')
    else:
        cta = (f'<a class="stg-pill" href="{go}"{_ext(go)}>{AP_GO.get(slug, "바로 가기")}</a>'
               if go else f'<a class="stg-pill" href="{purl(slug)}">더 알아보기</a>')
    vid = HOME_VIDEO.get(slug)
    shot = HOME_SHOT.get(slug) or pr.get("shot") or ""
    if vid:
        art = (f'<div class="stg-art"><video src="{vid}" autoplay muted loop playsinline '
               f'preload="metadata" aria-hidden="true"></video></div>')
    elif shot:
        art = (f'<div class="stg-art"><img src="{shot}" alt="{esc(pr["short"])}" '
               f'loading="lazy" decoding="async"></div>')
    else:
        art = ""
    bdg = f'<em>{badge}</em>' if badge else ""
    # 기기 배지 — "내 폰 얘기구나"가 이름보다 먼저 읽혀야 한다(2026-08-24 대표 지시).
    dev = f'<b class="dev">{esc(pr["device"])}</b>' if pr.get("device") else ""
    cls = "".join(f" stg--{t}" for t in tone.split()) if tone else ""
    # 배너 전체를 누를 수 있게 — 카드처럼 보이는데 안 눌리면 손이 헛돈다(2026-08-24 대표 지적).
    #   버튼이 둘이면 제품 페이지로, 하나면 그 버튼과 같은 곳으로 보낸다.
    _whole = purl(slug) if p_type == "app" else (go or purl(slug))
    _wext = _ext(_whole) if "//" in _whole else ""
    hit = (f'<a class="stg-hit" href="{_whole}"{_wext} '
           f'aria-label="{esc(pr["short"])} 자세히 보기"></a>')
    return (f'<section class="stg{cls}">{art}{hit}<div class="stg-bd"><div>'

            f'<p class="stg-eyebrow">{dev}{esc(pr.get("tag", ""))}{bdg}</p>'
            f'<h2 class="stg-name">{esc(pr["short"])}</h2>'
            f'<p class="stg-claim">{esc(pr["tagline"])}</p></div>'
            f'<div class="stg-cta">{cta}</div></div></section>')


def ap_index_section():
    """왼쪽에 무엇을 하는 곳인지 한 문장, 오른쪽엔 다음에 갈 곳 셋.
       ⚠️ 제품 목록·결제 링크를 여기 다시 늘어놓지 마라 — 위 배너가 이미 그 일을 했고,
          결제는 이 자리에서 할 일이 아니다(2026-08-24 대표 지적)."""
    return ('<section class="idx"><div class="idx-in">'
            '<div class="idx-l"><p class="k">모멘터스</p>'
            '<h2>나머지는 저희가 합니다.</h2>'
            '<p class="s">기다리고, 찾고, 정리하는 일은 기계가 더 잘합니다. '
            '그 시간을 돌려드리려고 하나씩 만듭니다. 무엇을 왜 만드는지, '
            '무엇이 됐고 무엇이 안 됐는지 그대로 적어 둡니다.</p></div>'
            '<div class="idx-r">'
            '<a class="idx-go" href="/about/"><b>소개 보기</b>'
            '<i>어떤 기준으로 만들고 무엇을 안 만드는지</i></a>'
            '<a class="idx-go" href="/insights/"><b>인사이트 읽기</b>'
            '<i>만들며 알게 된 것을 실측과 함께</i></a>'
            '<a class="idx-go" href="/inquiry/"><b>문의하기</b>'
            '<i>덜어 드릴 게 있으면 직접 읽고 답합니다</i></a>'
            '</div></div></section>')


def ap_tools_section():
    """애플 스토어 'The latest' 실측(apple.com/store, 1440):
       카드 400x500(4:5) · 모서리 18px · 배경이 검정↔흰색 교차 · 가로 스크롤 · 좌우 여백은 그리드 정렬.
       구성 = 작은 머리말 → 굵은 제목 → 한 줄 → 아래쪽에 큰 그림.
       (2026-08-23 대표: "이미지 쓰지 말고 카드 형태로, 높이가 좀 있게, 애플 스토어처럼")"""
    cards = []
    for t in TOOLS:
        pr = P[t]
        # 그림은 그 도구가 **어느 서비스에서 도는지**를 바로 알려주는 게 낫다 — 우리 글리프보다
        # 쿠팡·유튜브 로고 한 장이 빠르다(2026-08-23 대표 지적). 지명적 사용.
        logo = pr.get("logo")
        art = (f'<span class="art"><span class="gl"><img src="{logo}" alt="" loading="lazy"></span></span>'
               if logo else f'<span class="art"><span class="gl gl--tx">{pr["icon"]}</span></span>')
        cards.append(
            f'<a class="tcard" href="/tools/{t}/">'
            f'<span class="k">무료</span>'
            f'<b>{esc(pr["short"])}</b>'
            f'<i>{esc(pr.get("tagline2") or pr["tagline"])}</i>'
            f'{art}</a>')
    return ('<section class="tsec"><div class="tsec-h">'
            '<h2>설치 없이. <span>지금 바로 쓰는 도구 여섯 개.</span></h2>'
            '<div class="rl-nav" data-rail="toolrail">'
            '<button type="button" data-d="-1" aria-label="이전"><svg viewBox="0 0 24 24">'
            '<path d="M15 6l-6 6 6 6"/></svg></button>'
            '<button type="button" data-d="1" aria-label="다음"><svg viewBox="0 0 24 24">'
            '<path d="M9 6l6 6-6 6"/></svg></button></div></div>'
            f'<div class="tcards" id="toolrail">{"".join(cards)}</div></section>')


def ap_tools_stage():
    icons = "".join(f'<span aria-hidden="true">{P[t]["icon"]}</span>' for t in TOOLS)
    return ('<section class="stg stg--paper">'
            f'<div class="stg-icons">{icons}</div>'
            '<div class="stg-bd"><div>'
            '<p class="stg-eyebrow">북마크릿 · 크롬 확장</p>'
            f'<h2 class="stg-name">무료 도구 {len(TOOLS)}종</h2>'
            '<p class="stg-claim">북마크바에 끌어놓거나 크롬에 추가하면 끝. '
            '회원가입도 결제도 없습니다.</p></div>'
            '<div class="stg-cta"><a class="stg-pill" href="/products/">전부 보기</a></div>'
            '</div></section>')


ap_body = (
    # h1 은 페이지당 정확히 1개다(SEO_GEO.md §3). 제품 카드는 h2 라 최상위 제목이 없었다.
    # 히어로 스택 디자인을 건드리지 않으려고 sr-only 로 둔다 — 화면에 안 보일 뿐
    # DOM 에 실재하는 우리 자신에 대한 설명이다(숨긴 키워드가 아니다).
    '<h1 class="sr-only">모멘터스 — 작게 만들어 빨리 내놓는 제품들</h1>'
    '<div class="stg-stack">'
    + ap_stage("teamai", "hero ink", "NEW")
    + ap_stage("binbang", "hero", "NEW")
    + ap_stage("flipper", "hero", "NEW")
    + ap_stage("heyreci", "hero ink")
    + ap_stage("mark", "hero")
    + ap_stage("cue", "hero")
    + ap_stage("theplan", "hero")
    + ap_stage("kontext", "hero ink")
    + '</div>'
    + ap_tools_section()
    + ap_index_section()
    )


_rail_items = _all_new[:10]
_rail_cards = "".join(
    f'<a class="kb-rail-card" href="{x["url"]}"{_ext(x["url"])}>'
    + (f'<div class="kb-rail-th"><img src="{x["img"]}" alt="" loading="lazy"></div>'
       if x.get("img") else
       f'<div class="kb-rail-th ic" style="--ic:#3182f6"><span>{KINDN.get(x["kind"],"소식")[:1]}</span></div>')
    + f'<div class="kb-rail-tx"><h3>{esc(x["title"])}</h3>'
      f'<time>{fmt_date(x["date"])}</time></div></a>' for x in _rail_items)
kb_latest = (f"""<section class="kb-sec" aria-labelledby="kb-latest-h">
  <div class="kb-sec-head"><h2 id="kb-latest-h">최신 콘텐츠</h2>
    <div class="kb-arrows" data-rail="kbrail">
      <button type="button" data-dir="-1" aria-label="이전 슬라이드"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
      <button type="button" data-dir="1" aria-label="다음 슬라이드"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </div></div>
  <div class="kb-rail" id="kbrail">{_rail_cards}</div>
</section>""") if _rail_cards else ""


# ── ③ 인기 콘텐츠 (3열 그리드) ───────────────────────────────────────────────
_grid_slugs = [s for s in ORDER if s in P][:6]
_grid_cards = "".join(
    f'<a class="kb-card" href="{purl(s)}">'
    + kb_media(s)
    + f'<time>{"무료 도구" if P[s].get("free") else "제품"} · {KB_WORD.get(s, P[s].get("short",""))}</time>'
      f'<h3>{esc(P[s].get("tagline", P[s]["name"]))}</h3>'
      f'<div class="kb-chips">'
    + "".join(f'<span>{esc(t.strip())}</span>' for t in P[s].get("tag", "").split("·") if t.strip())
    + '</div></a>' for s in _grid_slugs)
kb_popular = f"""<section class="kb-sec" aria-labelledby="kb-pop-h">
  <div class="kb-sec-head"><h2 id="kb-pop-h">많이 찾는 것</h2>
    <a class="kb-kick" href="/products/">제품 전체 →</a></div>
  <div class="kb-grid">{_grid_cards}</div>
</section>"""


# ── ④ 시리즈 레일 ────────────────────────────────────────────────────────────
def _stream_by(src, n=3):
    return [x for x in STREAM if x.get("src") == src][:n]


_series = []
_pl = _stream_by("플래너")
if _pl:
    _series.append(dict(title="새로 나온 플래너", href="https://notes.the-moment.us",
                        cover=P.get("theplan", {}).get("shot", ""), color="#f7f6f1", items=_pl))
_lg = _stream_by("로고")
if _lg:
    _series.append(dict(title="업종별 로고 이야기", href="https://mark.the-moment.us/insights/",
                        cover=P.get("mark", {}).get("shot", ""), color="#eef3ff", items=_lg))
if PORDER:
    _series.append(dict(title="스튜디오의 기록", href=f"{STORY_BASE}/", cover="", color="#f2f4f7",
                        items=[dict(title=POSTS[x]["title"], url=f"{STORY_BASE}/{x}/", img="")
                               for x in PORDER[:3]]))
_tl = [s for s in TOOLS if s in P][:3]
if _tl:
    _series.append(dict(title="브라우저에 붙이는 무료 도구", href="/products/", cover="", color="#eafaf1",
                        items=[dict(title=P[s].get("tagline", P[s]["name"]), url=purl(s),
                                    img=P[s].get("shot", ""), icon=P[s].get("icon", "◆"),
                                    color=P[s].get("color", "#3182f6")) for s in _tl]))


def _series_pair(sr):
    lis = "".join(
        f'<li><a href="{it["url"]}"{_ext(it["url"])}>'
        f'<span class="n">{i+1:02d}</span>'
        + (f'<span class="sq"><img src="{it["img"]}" alt="" loading="lazy"></span>'
           if it.get("img") else
           f'<span class="sq" style="--ic:{it.get("color","#9aa0a8")}">{it.get("icon","·")}</span>')
        + f'<span class="t">{esc(it["title"])}</span></a></li>' for i, it in enumerate(sr["items"]))
    cover = (f'<img src="{sr["cover"]}" alt="" loading="lazy">' if sr.get("cover")
             else f'<span class="kb-kick">{esc(sr["title"])}</span>')
    return (f'<div class="kb-spair">'
            f'<div class="kb-spanel"><span class="kb-badge">Series</span><h3>{esc(sr["title"])}</h3>'
            f'<ul class="kb-slist">{lis}</ul></div>'
            f'<a class="kb-scover" href="{sr["href"]}"{_ext(sr["href"])} '
            f'style="--sc:{sr["color"]}" aria-label="{esc(sr["title"])}">{cover}</a></div>')


kb_series = (f"""<section class="kb-sec" aria-labelledby="kb-ser-h">
  <div class="kb-sec-head"><h2 id="kb-ser-h">묶어서 보면 더 좋은 것</h2>
    <div class="kb-arrows" data-rail="kbsrail">
      <button type="button" data-dir="-1" aria-label="이전 슬라이드"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
      <button type="button" data-dir="1" aria-label="다음 슬라이드"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </div></div>
  <div class="kb-srail" id="kbsrail">{"".join(_series_pair(s) for s in _series)}</div>
  <div class="kb-srail-foot"><a class="kb-pill" href="/products/">전체 보기</a></div>
</section>""") if _series else ""


# ── ⑤ 카테고리 스크롤러 ──────────────────────────────────────────────────────
_cat_slugs = [s for s in ORDER if s in P]
_cat_words = "".join(
    '<li' + (" aria-current=true" if i == 0 else "") + '>'
    + f'<button type="button" data-i="{i}">{KB_WORD.get(s, P[s].get("short",""))}</button></li>'
    for i, s in enumerate(_cat_slugs))
_cat_data = json.dumps([dict(
    slug=s, url=purl(s), name=P[s].get("short", P[s]["name"]),
    tagline=P[s].get("tagline", ""), shot=P[s].get("shot", ""),
    icon=P[s].get("icon", "◆"), color=P[s].get("color", "#3182f6"),
) for s in _cat_slugs], ensure_ascii=False)

kb_cats = f"""<section class="kb-sec" aria-labelledby="kb-cat-h">
  <div class="kb-sec-head"><h2 id="kb-cat-h">무엇을 하려고 오셨나요</h2></div>
  <div class="kb-cats" id="kbcats">
    <a class="kb-cat-card" id="kbcatcard" href="/"><span class="kb-cat-art"></span><h3></h3><p></p></a>
    <div class="kb-cat-view">
      <ul class="kb-cat-list" id="kbcatlist">{_cat_words}</ul>
      <div class="kb-cat-ctl">
        <button type="button" id="kbcatpause" aria-label="자동 넘김 멈춤">
          <svg viewBox="0 0 24 24" class="pauseon"><path d="M9 5v14M15 5v14"/></svg>
          <svg viewBox="0 0 24 24" class="pauseoff"><path d="M7 4l12 8-12 8z"/></svg></button>
        <button type="button" data-dir="-1" aria-label="이전 카테고리"><svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
        <button type="button" data-dir="1" aria-label="다음 카테고리"><svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg></button>
      </div>
    </div>
  </div>
</section>"""


# ── 헤더 · 검색 인덱스 ───────────────────────────────────────────────────────
# 검색 결과는 **무엇인지 알아볼 수 있어야 한다** — 글자만 나열하면 뭐가 뭔지 모른다
# (2026-08-23 대표: "썸네일도 좀 나와 주면서 저게 나와야지"). 그림·종류·부제를 같이 싣는다.
def _kb_row(sl):
    pr = P[sl]
    return dict(t=pr.get("short") or pr.get("name", sl),
                k="무료 도구" if pr.get("free") else "제품",
                g=pr.get("tag", ""), u=purl(sl),
                im=pr.get("shot") or "", ic=pr.get("icon", ""))


KB_INDEX = json.dumps(
    [_kb_row(s) for s in ORDER if s in P]
    + [dict(t=POSTS[x]["title"], k="이야기", g=POSTS[x].get("date", ""),
            u=f"{STORY_BASE}/{x}/", im=POSTS[x].get("cover", "") or "", ic="✎") for x in PORDER],
    ensure_ascii=False)

KB_HEAD = """<script>
/* 다크모드 — 그리기 전에 결정해서 흰 화면 번쩍임(FOUC)을 막는다. */
(function(){try{var t=localStorage.getItem('mmt-theme');
if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.dataset.theme=t;}catch(e){}})();
</script>"""

KB_JS = """<button class="kb-top" id="kbtop" aria-label="맨 위로">
<svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
<script>
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
  var IDX=__INDEX__;
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
  var CATS=__CATS__, list=$('kbcatlist'), card=$('kbcatcard');
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
</script>"""

KB_JS = KB_JS.replace("__INDEX__", KB_INDEX).replace("__CATS__", _cat_data)

# ── 공용 스크립트 파일 — 37개 페이지에 같은 스크립트를 인라인으로 복사하지 않는다.
#    page() 가 <script defer src="/assets/apex.js?v=CSS_VER"> 로 건다.
def _strip_tags(js):
    out, i = [], 0
    while True:
        a = js.find("<script>", i)
        if a < 0:
            break
        b = js.index("</script>", a)
        out.append(js[a + len("<script>"):b])
        i = b + len("</script>")
    return "\n".join(out)


_apex_js = _strip_tags(KB_JS) + """
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
"""
with open("assets/apex.js", "w", encoding="utf-8") as f:
    f.write(_apex_js)

# ---------- 홈 — 제품 무대(Apple 문법) ----------
#   ⚠️ 옛 구성(kb_hero/kb_latest/kb_popular/kb_series/kb_cats)은 더 이상 홈에 싣지 않는다.
#      변수 자체는 남겨 둔다 — 다른 데서 참조하거나 되돌릴 때를 위해.
_SPOKE_HREF = {sp["slug"]: sp["href"] for sp in BAR["spokes"] if sp.get("slug")}
# 두 번째 버튼은 '알아보기'가 아니라 **그 제품에서 하는 일**을 말한다(애플의 '구입하기' 자리).
AP_GO = {"binbang": "빈방 알림 등록", "heyreci": "헤이레시 열기", "mark": "로고 만들어 보기",
         "cue": "모의면접 시작하기", "theplan": "플래너 보러 가기"}


land_body = ap_body

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page("MOMENTUS — 일하는 사람을 위한 도구를 만듭니다",
                 "모멘터스는 1인 AI 스튜디오입니다. 펜션 빈방 알림·AI 상품사진·로고 디자인·AI 모의면접·"
                 "디지털 플래너를 만들어 팔고, 설치 없이 쓰는 무료 브라우저 도구 6종을 함께 제공합니다.",
                 land_body, active=""))


# ---------- 법적 페이지 (약관·개인정보·환불) ----------
LEGAL_CSS_WRAP = '<div class="lg">'

BIZ_TABLE = f"""<table class="lg-biz">
<tr><th>상호</th><td>{BIZ['name']}</td></tr>
<tr><th>대표자</th><td>{BIZ['ceo']}</td></tr>
<tr><th>사업자등록번호</th><td>{BIZ['reg']}</td></tr>
<tr><th>통신판매업신고</th><td>{BIZ['mail_order']}</td></tr>
<tr><th>사업장 주소</th><td>{BIZ['addr']}</td></tr>
<tr><th>전화</th><td>{BIZ['tel']}</td></tr>
<tr><th>이메일</th><td><a href="mailto:{BIZ['email']}">{BIZ['email']}</a> (고객 문의는 이메일로만 받습니다)</td></tr>
<tr><th>개인정보보호책임자</th><td>{BIZ['privacy_officer']}</td></tr>
</table>"""

PRIVACY = f"""{LEGAL_CSS_WRAP}
  <div class="lg-head">
    <h1>개인정보처리방침</h1>
    <p class="upd">최종 업데이트: {BIZ['updated']}</p>
  </div>
  <div class="lg-body">
    <p><b>모멘터스는 개인정보를 수집하지 않는 것을 원칙으로 합니다.</b> 브라우저 도구(퀵팡·인스타 인기순 정렬·유튜브 인기순 정렬·핀터레스트 원본 추출·ChatPage·her)는 모든 처리를 이용자의 브라우저 안에서 수행하며, 어떠한 데이터도 모멘터스 서버로 전송하지 않습니다.</p>

    <h2>1. 수집하는 항목</h2>
    <h3>1.1 브라우저 도구 (무료)</h3>
    <ul>
      <li><b>수집하지 않습니다.</b> 회원가입, 로그인, 이메일 수집이 없습니다.</li>
      <li>도구가 다루는 데이터(예: 쿠팡 상품 정보, 인스타그램 게시물 좋아요 수, 음성 입력 내용)는 <b>이용자의 브라우저 안에서만</b> 처리되고 즉시 폐기됩니다.</li>
      <li><b>her(음성 입력)</b>: 음성 인식은 기기 내에서 처리되며, 녹음 파일이 외부로 전송되지 않습니다.</li>
      <li><b>ChatPage</b>: 이용자가 선택한 AI 서비스(ChatGPT·Claude·Gemini)의 탭으로 자막 텍스트를 전달합니다. 이때 해당 AI 서비스의 개인정보처리방침이 적용됩니다.</li>
    </ul>

    <h3>1.2 웹사이트 (the-moment.us)</h3>
    <ul>
      <li>방문 통계 확인을 위해 Google Analytics를 사용할 수 있으며, 이 경우 IP 주소·브라우저 종류·방문 페이지 등 <b>식별되지 않는 통계 정보</b>가 수집됩니다.</li>
      <li>쿠키는 통계 목적으로만 사용하며, 브라우저 설정에서 거부할 수 있습니다.</li>
    </ul>

    <h3>1.3 유료 제품</h3>
    <p>헤이레시(heyreci.com), 마크(mark.the-moment.us), 더플랜(notes.the-moment.us), 큐(cue.the-moment.us)는 <b>각 서비스에서 별도의 개인정보처리방침을 운영</b>합니다. 결제·회원 정보는 해당 서비스와 결제대행사가 처리하며, 모멘터스 웹사이트는 이를 수집·보관하지 않습니다.</p>

    <h3>1.4 모바일 앱 — Flipper (Android)</h3>
    <p>Flipper(<code>us.themoment.flipper</code>)는 볼륨키 등 물리 키로 전자책·웹페이지·문서의 페이지를 넘겨 주는 Android 접근성 유틸리티입니다. <b>개인정보를 수집·저장·전송하지 않습니다.</b></p>
    <ul>
      <li>계정 가입·로그인이 없으며, 이름·이메일·전화번호·위치·연락처·사진을 요구하거나 접근하지 않습니다.</li>
      <li>분석 SDK와 광고 SDK가 포함되어 있지 않습니다. 광고 식별자(AD_ID)를 사용하지 않습니다.</li>
      <li>설정값(스크롤 강도, 자동 시작 여부, 체험 시작 시각, 구매 상태)은 <b>기기 내부 저장소에만</b> 저장되며 앱을 삭제하면 함께 삭제됩니다.</li>
    </ul>

    <h4>접근성 서비스(AccessibilityService) 사용 고지</h4>
    <p>앱의 핵심 기능을 제공하기 위해 Android 접근성 서비스 권한을 사용하며, 그 목적은 다음 세 가지로 한정됩니다.</p>
    <ul>
      <li><b>물리 키 입력 감지</b> — 사용자가 누른 볼륨키 등을 페이지 넘김 신호로 인식</li>
      <li><b>화면 스크롤 수행</b> — 현재 보고 있는 앱의 화면을 대신 스크롤</li>
      <li><b>포그라운드 앱 확인</b> — 사용자가 앱별로 지정한 스크롤 설정을 적용</li>
    </ul>
    <p>접근성 서비스를 통해 접근 가능한 화면 내용은 <b>스크롤 동작을 수행하는 순간에만 메모리상에서 사용</b>되며 저장되거나 외부로 전송되지 않습니다. 화면의 텍스트를 읽어 기록하거나, 입력한 내용을 수집하거나, 스크린샷을 촬영하지 않습니다. 이 권한은 Android 시스템 설정 &gt; 접근성에서 언제든지 해제할 수 있으며, 해제 시 페이지 넘김 기능만 중단됩니다.</p>

    <h4>결제</h4>
    <p>프리미엄 구매는 Google Play 결제 시스템을 통해 처리됩니다. 카드번호를 포함한 결제 수단 정보는 Google이 처리하며 <b>개발자는 이에 접근할 수 없습니다.</b> 앱은 구매 성립 여부(프리미엄 활성/비활성)만 기기에 저장합니다. 결제 관련 개인정보는 <a href="https://policies.google.com/privacy">Google 개인정보처리방침</a>을 따릅니다.</p>

    <h4>사용하는 권한</h4>
    <ul>
      <li><code>BIND_ACCESSIBILITY_SERVICE</code> — 물리 키 감지 및 화면 스크롤 수행</li>
      <li><code>FOREGROUND_SERVICE</code> — 볼륨키가 ‘넘기기’인 동안 서비스 유지</li>
      <li><code>POST_NOTIFICATIONS</code> — 볼륨키 상태(넘기기/소리) 및 체험 기간 안내 표시</li>
      <li><code>RECEIVE_BOOT_COMPLETED</code> — 자동 시작 옵션 사용 시 재부팅 후 복원</li>
      <li><code>VIBRATE</code> — 모드 전환 시 진동 피드백</li>
      <li><code>MODIFY_AUDIO_SETTINGS</code> — 볼륨키를 스크롤로 사용할 때 시스템 볼륨 변화 억제</li>
      <li><code>INTERNET</code>, <code>BILLING</code> — Google Play 결제 및 구매 상태 확인</li>
    </ul>

    <h2>2. 이용 목적</h2>
    <p>수집된 통계 정보는 서비스 개선 목적으로만 사용하며, 제3자에게 판매하거나 제공하지 않습니다.</p>

    <h2>3. 보유 기간</h2>
    <p>브라우저 도구는 데이터를 보관하지 않습니다. 웹사이트 통계 정보는 수집일로부터 최대 26개월간 보관 후 파기합니다.</p>

    <h2>4. 이용자의 권리</h2>
    <p>개인정보를 수집하지 않으므로 열람·정정·삭제를 요청할 대상이 없습니다. 다만 문의사항이 있으시면 아래로 연락 주십시오.</p>

    <h2>5. 개인정보보호책임자</h2>
    <p>{BIZ['privacy_officer']} · <a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>

    <h2>6. 사업자 정보</h2>
    {BIZ_TABLE}

    <h2>7. 변경 고지</h2>
    <p>본 방침이 변경되는 경우 이 페이지에 게시합니다.</p>
  </div>
</div>"""

TERMS = f"""{LEGAL_CSS_WRAP}
  <div class="lg-head">
    <h1>이용약관</h1>
    <p class="upd">최종 업데이트: {BIZ['updated']}</p>
  </div>
  <div class="lg-body">
    <h2>1. 적용 범위</h2>
    <p>본 약관은 모멘터스가 the-moment.us에서 제공하는 <b>무료 브라우저 도구</b>와, 이 웹사이트를 통해 안내되는 <b>유료 제품</b>의 이용에 적용됩니다.</p>

    <h2>2. 무료 브라우저 도구</h2>
    <ul>
      <li>퀵팡, 인스타 인기순 정렬, 유튜브 인기순 정렬, 핀터레스트 원본 추출, ChatPage, her는 <b>무료로 제공</b>됩니다.</li>
      <li>회원가입·결제·이메일 등록이 필요하지 않습니다.</li>
      <li>개인적·상업적 용도로 자유롭게 사용할 수 있습니다.</li>
      <li>도구를 역공학하거나, 타인의 권리를 침해하는 목적으로 사용해서는 안 됩니다.</li>
      <li>각 도구는 대상 웹사이트(쿠팡·인스타그램·유튜브 등)의 화면 구성에 의존하므로, 해당 사이트의 변경으로 <b>예고 없이 동작하지 않을 수 있습니다.</b></li>
    </ul>

    <h2>3. 유료 제품</h2>
    <p>헤이레시·마크·더플랜·큐는 <b>각 서비스에서 별도의 약관과 결제 조건</b>을 운영합니다. 계약은 각 서비스와 이용자 사이에 성립하며, the-moment.us는 이를 안내하는 역할만 합니다.</p>

    <h2>4. 면책</h2>
    <ul>
      <li>무료 도구는 <b>있는 그대로(as-is)</b> 제공되며, 특정 목적에 대한 적합성을 보증하지 않습니다.</li>
      <li>도구 사용으로 발생한 직·간접적 손해에 대해 모멘터스는 책임을 지지 않습니다.</li>
      <li>도구가 다루는 제3자 사이트의 데이터에 대한 정확성은 보증하지 않습니다.</li>
    </ul>

    <h2>5. 서비스 변경·중단</h2>
    <p>모멘터스는 사전 고지 없이 도구를 수정하거나 중단할 수 있습니다. 무료 제공이므로 이에 따른 보상은 제공되지 않습니다.</p>

    <h2>6. 지식재산권</h2>
    <p>모멘터스가 제작한 도구·디자인·문서의 저작권은 모멘터스에 있습니다.</p>

    <h2>7. 문의</h2>
    <p><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>

    <h2>8. 사업자 정보</h2>
    {BIZ_TABLE}
  </div>
</div>"""

REFUND = f"""{LEGAL_CSS_WRAP}
  <div class="lg-head">
    <h1>환불 규정</h1>
    <p class="upd">최종 업데이트: {BIZ['updated']}</p>
  </div>
  <div class="lg-body">
    <h2>1. 무료 제품</h2>
    <p>브라우저 도구 6종은 <b>전액 무료</b>이므로 결제와 환불이 발생하지 않습니다.</p>

    <h2>2. 유료 제품</h2>
    <p>유료 제품은 각 서비스에서 결제가 이루어지며, 환불도 해당 서비스의 규정을 따릅니다.</p>
    <ul>
      <li><b>헤이레시</b> (AI 상품사진) — 크레딧 충전제. 미사용 크레딧은 결제일로부터 7일 이내 환불 가능. 이미 생성에 사용된 크레딧은 환불되지 않습니다.</li>
      <li><b>마크</b> (로고 디자인) — 제작 착수 전 전액 환불. 시안 전달 후에는 진행 단계에 따라 부분 환불.</li>
      <li><b>더플랜</b> (디지털 플래너) — 디지털 콘텐츠 특성상 <b>파일 다운로드 전까지</b> 환불 가능.</li>
      <li><b>큐</b> (AI 모의면접) — 구독 개시 후 7일 이내, 이용 이력이 없는 경우 전액 환불.</li>
    </ul>

    <h2>3. 청약철회</h2>
    <p>전자상거래법에 따라 결제일로부터 7일 이내 청약철회가 가능합니다. 다만 <b>디지털 콘텐츠의 제공이 개시된 경우</b>(플래너 파일 다운로드, 이미지 생성 완료 등) 청약철회가 제한될 수 있으며, 이는 결제 전에 고지됩니다.</p>

    <h2>4. 환불 절차</h2>
    <p>아래로 연락 주시면 3영업일 이내 회신하고, 승인 시 7영업일 이내 결제 수단으로 환불합니다.</p>
    <p><a href="mailto:{BIZ['email']}">{BIZ['email']}</a> (환불 문의는 이메일로만 받습니다)</p>

    <h2>5. 사업자 정보</h2>
    {BIZ_TABLE}
  </div>
</div>"""

# 설명 문구는 상수로 둔다 — apps/ 아래 별칭 페이지가 같은 값을 쓴다(두 벌이 갈라지면 안 된다).
LEGAL_DESC = {
    "privacy": "모멘터스는 개인정보를 수집하지 않습니다. 브라우저 도구 6종은 모든 처리를 사용자 기기 안에서 수행하며 서버로 데이터를 보내지 않습니다. 수집 항목과 보관 기간을 명시했습니다.",
    "terms": "모멘터스 무료 브라우저 도구 6종과 유료 제품의 이용약관입니다. 서비스 범위, 이용자의 권리와 의무, 책임의 한계를 정리했습니다.",
    "refund": "모멘터스 유료 제품의 환불 규정과 청약철회 안내입니다. 무료 브라우저 도구는 결제가 없어 환불이 발생하지 않습니다. 디지털 상품의 청약철회 조건을 확인하세요.",
}

for slug, title, body, desc in [
    ("privacy", "개인정보처리방침", PRIVACY, LEGAL_DESC["privacy"]),
    ("terms", "이용약관", TERMS, LEGAL_DESC["terms"]),
    ("refund", "환불 규정", REFUND, LEGAL_DESC["refund"]),
]:
    os.makedirs(f"legal/{slug}", exist_ok=True)
    with open(f"legal/{slug}/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"{title} — MOMENTUS", desc, body, active=""))

# ---------- 문의 단일 창구 /inquiry/ · 스레드 /i/ · 결제 안내 /how-to-pay/ ----------
# 사장님 2026-08-07: "각기 전투할 게 아니라 하나가 돼야 된다."
#   그전엔 mark=자체 폼, notes /business=mailto, apex 푸터=mailto 로 셋이 제각각이었고
#   mailto 둘은 **기록이 안 남아** 봇도 못 보고 이력도 없었다. 창구를 여기 하나로 모은다.
#
# 설계: 대화의 본체는 **웹 스레드**, 이메일은 "새 답변 왔어요" 봉투.
#   발송은 Resend(발신 전용)라 "이메일이 본체"인 설계는 반드시 반쪽이 된다 —
#   고객 회신이 원장 밖으로 흩어져 신청 내역과 끊긴다. 본체를 웹에 두면 그 약점이 사라진다.
# 🚫 여기(정적 페이지)에 가격을 박지 마라. 맞춤 제작은 상담에서 견적을 낸다(mark 룰과 같은 이유).
INQ_API = "https://pay.the-moment.us/api/inquiry"

INQ_CSS = """<style>
/* 폼 컨트롤만 정의한다. 페이지 골격(여백·제목·본문)은 apex 의 .lg/.lg-head/.lg-body 를
   그대로 쓴다 — 2026-08-07 사고: 자체 컨테이너를 만들었더니 고정 헤더(56px) 보정이 빠져
   제목이 헤더에 달라붙고 제목 크기도 다른 페이지와 어긋났다.
   🚫 여기에 컨테이너·h1 스타일을 다시 만들지 마라. 기존 패턴을 먼저 찾아 써라. */
.iq-f{display:grid;gap:20px;margin:0 0 8px}
.iq-f label{display:block;font-size:14px;font-weight:600;color:#202020}
.iq-f label>span{display:block;margin:0 0 8px}
.iq-f label em{font-weight:400;color:#909090;font-style:normal}
.iq-f input[type=text],.iq-f input[type=email],.iq-f textarea,.iq-f select{
  width:100%;padding:var(--mmt-field-pad,14px 16px);
  border:var(--mmt-field-bw,1px) solid var(--mmt-line,#e9e9e9);
  border-radius:var(--mmt-r-field,12px);font:inherit;
  font-size:var(--mmt-fs-field,15px);font-weight:400;background:#fff;color:#202020}
.iq-f textarea{min-height:150px;resize:vertical;line-height:1.7}
.iq-f input:focus,.iq-f textarea:focus,.iq-f select:focus{outline:none;border-color:#202020}
.iq-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.iq-go{display:inline-block;background:var(--brand-cta,#1b64da);color:#fff;border:0;
  border-radius:var(--mmt-r-ctrl,999px);padding:var(--mmt-ctrl-pad,14px 28px);
  font:inherit;font-size:var(--mmt-fs-ctrl,15px);font-weight:var(--mmt-fw-ctrl,700);
  cursor:pointer;text-decoration:none}
.iq-go[disabled]{opacity:.5;cursor:default}
.iq-err{color:#D33;font-size:14px;min-height:20px}
.iq-card{background:#F7F8F9;border-radius:14px;padding:26px}
.iq-card b{font-size:18px;display:block;margin:0 0 8px}
.iq-code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:700}
.iq-thr{display:grid;gap:14px;margin:0 0 34px}
.iq-msg{border-radius:14px;padding:16px 18px;white-space:pre-wrap;line-height:1.75;font-size:15px}
.iq-msg.me{background:#F7F8F9;color:#202020}
.iq-msg.us{background:#202020;color:#fff}
.iq-msg .who{font-size:12px;font-weight:700;opacity:.6;margin:0 0 6px}
html[data-theme="dark"] .iq-f label{color:#EAEAEA}
html[data-theme="dark"] .iq-f input,html[data-theme="dark"] .iq-f textarea,
html[data-theme="dark"] .iq-f select{background:#151515;color:#EAEAEA;border-color:#2A2A2A}
html[data-theme="dark"] .iq-card,html[data-theme="dark"] .iq-msg.me{background:#151515;color:#EAEAEA}
html[data-theme="dark"] .iq-go,html[data-theme="dark"] .iq-msg.us{background:#EAEAEA;color:#111}
</style>"""

INQUIRY = f"""<div class="iqp">
  <header class="iqp-head">
    <h1>무엇을 덜어 드릴까요.</h1>
    <p>제품에 대한 것도, 제휴나 협업도 여기로 오시면 됩니다.
      지금 없는 것을 만들어 달라는 이야기도 좋습니다.</p>
  </header>
  <div class="iqp-grid">
    <aside class="iqp-side">
      <div class="iqp-fact"><b>영업일 하루</b><span>안에 답을 드립니다</span></div>
      <div class="iqp-fact"><b>직접</b><span>읽고 직접 답합니다</span></div>
      <div class="iqp-fact"><b>기록</b><span>웹 스레드로 이어서 대화합니다</span></div>
      <ul class="iqp-ex">
        <li>로고·명함을 새로 만들고 싶어요</li>
        <li>기업·단체용 플래너를 맞추고 싶어요</li>
        <li>이런 걸 만들어 주실 수 있나요</li>
        <li>같이 해볼 만한 게 있을까요</li>
      </ul>
      <p class="iqp-mail">폼이 불편하시면 <a href="mailto:hello.momentus@gmail.com">hello.momentus@gmail.com</a> 으로 주셔도 됩니다.</p>
    </aside>
    <div class="iqp-form" id="iqRoot">
    <div class="iq-err" id="err"></div>
    <form class="iq-f" id="f">
      <label><span>무엇을 도와드릴까요?</span>
        <select name="topic" id="topic">
          <option>로고 제작 (마크)</option>
          <option>기업·단체 플래너 (노트)</option>
          <option>플래너 구매·다운로드</option>
          <option>그 외</option>
        </select></label>
      <label><span>회신받을 이메일</span>
        <input type="email" name="email" required placeholder="hello@example.com" autocomplete="email"></label>
      <label><span>회사·가게 이름 <em>(선택)</em></span>
        <input type="text" name="name" maxlength="60" autocomplete="organization"></label>
      <label><span>내용</span>
        <textarea name="body" required placeholder="어떤 걸 찾으시는지, 일정이나 예산이 있다면 함께 적어주세요."></textarea></label>
      <label class="iq-hp" aria-hidden="true" tabindex="-1"><span>이 칸은 비워두세요</span>
        <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
      <div><button class="iq-go" type="submit" id="go">문의 보내기</button></div>
    </form>
    <p>보내주신 이메일은 답변을 드리는 데에만 씁니다.
      결제가 어떻게 진행되는지는 <a href="/how-to-pay/">결제 안내</a>에서 미리 보실 수 있습니다.</p>
    </div>
  </div>
</div>
<script>
(function(){{
  var qs=new URLSearchParams(location.search);
  var pre=qs.get('topic'); if(pre){{ var o=[].find.call(document.getElementById('topic').options,
    function(x){{return x.text.indexOf(pre)>=0}}); if(o) o.selected=true; }}
  var ctx=null; try{{ ctx=qs.get('ctx')?JSON.parse(decodeURIComponent(qs.get('ctx'))):null }}catch(e){{}}
  // 유입 페이지에서 이미 적은 말이 있으면 옮겨 담는다 — 같은 걸 두 번 쓰게 하지 않는다.
  var pf=qs.get('prefill'); if(pf) document.querySelector('[name=body]').value=pf;
  // 무엇을 보고 왔는지 화면에도 보여준다. 안 보여주면 "내 선택이 전달됐나?" 불안해진다.
  if(ctx){{
    var rows=Object.keys(ctx).filter(function(k){{var v=ctx[k];return v&&v.length}})
      .map(function(k){{var v=ctx[k];return '<div style="display:flex;gap:10px"><span style="color:#909090;min-width:64px">'+k+'</span><span>'+
        (Array.isArray(v)?v.length+'개':String(v))+'</span></div>'}}).join('');
    if(rows) document.getElementById('f').insertAdjacentHTML('beforebegin',
      '<div class="iq-card" style="margin:0 0 24px;font-size:14px"><b style="font-size:14px">고르신 내용이 함께 전달됩니다</b>'+rows+'</div>');
  }}
  document.getElementById('f').addEventListener('submit',async function(e){{
    e.preventDefault();
    var f=e.target,b=document.getElementById('go'),err=document.getElementById('err');
    err.textContent=''; b.disabled=true; b.textContent='보내는 중…';
    var payload={{source:qs.get('from')||'apex',topic:f.topic.value,email:f.email.value,
      name:f.name.value,body:f.body.value,website:f.website.value,context:ctx,page:location.href}};
    try{{
      var r=await fetch('{INQ_API}',{{method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify(payload)}});
      var d=await r.json();
      if(!r.ok){{ throw new Error(d.error||'잠시 후 다시 시도해 주세요.') }}
      document.getElementById('iqRoot').innerHTML=
        '<div class="iq-card"><b>문의가 접수되었습니다 ✓</b>'+
        '<p style="margin:0 0 14px">접수번호 <span class="iq-code">'+d.id+'</span> · 영업일 기준 하루 안에 답변드립니다.</p>'+
        '<p style="margin:0 0 18px">접수 확인 메일을 보내드렸습니다. 아래에서 <b>진행 상황을 보고 이어서 대화</b>하실 수 있어요.</p>'+
        '<p style="margin:0"><a class="iq-go" href="'+d.url+'">문의 내용 보기 · 대화하기</a></p></div>'+
        '<p>결제 진행 방법은 <a href="/how-to-pay/">결제 안내</a>를 참고해 주세요.</p>';
      window.scrollTo({{top:0,behavior:'smooth'}});
    }}catch(ex){{
      err.textContent=ex.message; b.disabled=false; b.textContent='문의 보내기';
    }}
  }});
}})();
</script>"""

THREAD = f"""<div class="lg">
  <div class="lg-head">
    <h1 id="h">문의 내용</h1>
    <p class="upd" id="meta">불러오는 중…</p>
  </div>
  <div class="lg-body">
    <div class="iq-thr" id="thr"></div>
    <div id="box" hidden>
      <div class="iq-err" id="err"></div>
      <div class="iq-f">
        <label><span>이어서 말씀해 주세요</span>
          <textarea id="body" placeholder="추가로 알려주실 내용이 있으면 적어주세요."></textarea></label>
        <div><button class="iq-go" id="go" type="button">보내기</button></div>
      </div>
    </div>
    <p>이 페이지 주소가 곧 열쇠입니다. 회원가입 없이 언제든 다시 열어 확인하실 수 있어요.<br>
      <a href="/how-to-pay/">결제는 이렇게 진행됩니다 →</a></p>
  </div>
</div>
<script>
(function(){{
  var qs=new URLSearchParams(location.search),id=qs.get('id')||'',k=qs.get('k')||'';
  var thr=document.getElementById('thr'),meta=document.getElementById('meta');
  function esc(s){{var d=document.createElement('div');d.textContent=s;return d.innerHTML}}
  function when(ms){{var d=new Date(ms);return d.getFullYear()+'.'+(d.getMonth()+1)+'.'+d.getDate()+
    ' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')}}
  async function load(){{
    if(!id||!k){{ meta.textContent='주소가 올바르지 않습니다. 접수 확인 메일의 링크로 들어와 주세요.'; return }}
    var r=await fetch('{INQ_API}/thread?id='+encodeURIComponent(id)+'&k='+encodeURIComponent(k));
    if(!r.ok){{ meta.textContent='문의를 찾을 수 없습니다. 링크가 정확한지 확인해 주세요.'; return }}
    var d=await r.json();
    document.getElementById('h').textContent='문의 '+d.id;
    meta.innerHTML=esc(d.topic)+' · 접수 '+when(d.created_at)+
      (d.status==='replied'?' · <b>답변 완료</b>':' · 답변 준비 중');
    thr.innerHTML=d.messages.map(function(m){{
      return '<div class="iq-msg '+(m.author==='momentus'?'us':'me')+'">'+
        '<div class="who">'+(m.author==='momentus'?'모멘터스':'보내신 내용')+' · '+when(m.created_at)+'</div>'+
        esc(m.body)+'</div>' }}).join('');
    document.getElementById('box').hidden=false;
  }}
  document.getElementById('go').addEventListener('click',async function(){{
    var t=document.getElementById('body'),b=this,err=document.getElementById('err');
    if(!t.value.trim()) return t.focus();
    err.textContent=''; b.disabled=true; b.textContent='보내는 중…';
    try{{
      var r=await fetch('{INQ_API}/reply',{{method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{id:id,k:k,body:t.value}})}});
      var d=await r.json(); if(!r.ok) throw new Error(d.error||'잠시 후 다시 시도해 주세요.');
      t.value=''; await load();
    }}catch(ex){{ err.textContent=ex.message }}
    b.disabled=false; b.textContent='보내기';
  }});
  load();
}})();
</script>"""

HOW_TO_PAY = """<div class="lg">
  <div class="lg-head">
    <h1>결제는 이렇게 진행됩니다</h1>
    <p class="upd">상품 성격에 따라 두 갈래입니다.</p>
  </div>
  <div class="lg-body">
    <h2>1. 바로 살 수 있는 것 — 플래너 · 이용권</h2>
    <p>이미 만들어져 있어 <b>결제 즉시 받으시는</b> 상품입니다. 각 서비스에서 바로 구매하시면 됩니다.</p>
    <ul>
      <li><b>디지털 플래너</b> — <a href="https://notes.the-moment.us/shop">노트에서 보기</a>. 결제 후 다운로드 링크를 바로 보내드립니다.</li>
      <li><b>큐 이용권</b> — <a href="https://cue.the-moment.us/pricing">큐에서 보기</a>. 결제 후 이용권 코드를 메일로 보내드립니다.</li>
    </ul>

    <h2>2. 맞춤으로 만드는 것 — 로고 · 기업 플래너</h2>
    <p>사람이 직접 작업하는 상품이라 <b>가격을 미리 걸어두지 않습니다.</b> 무엇을 만드시는지에 따라 범위와 일정이 달라지기 때문입니다. 순서는 이렇습니다.</p>
    <ol>
      <li><b>문의</b> — <a href="/inquiry/">문의하기</a>에 원하시는 것을 남겨주세요.</li>
      <li><b>상담</b> — 영업일 하루 안에 답변드립니다. 범위·일정·견적을 함께 정리해 드립니다.
        대화는 문의 페이지에서 이어지고, 새 답변이 달리면 메일로 알려드립니다.</li>
      <li><b>확정</b> — 내용이 정해지면 <b>결제 링크를 보내드립니다.</b></li>
      <li><b>결제</b> — 보내드린 링크(네이버 스마트스토어)에서 결제하시면 됩니다.
        카드·계좌이체·네이버페이 모두 되고, 구매확정 전까지 네이버가 결제를 보관합니다.</li>
      <li><b>작업 시작</b> — 결제가 확인되면 바로 착수합니다.</li>
    </ol>
    <p>맞춤 제작을 문의 없이 바로 결제하시는 길은 따로 두지 않았습니다. 무엇을 받으실지 서로 합의되기 전에 돈이 오가지 않는 편이 안전하기 때문입니다.</p>

    <h2>3. 영수증 · 세금계산서</h2>
    <p>네이버 스마트스토어 결제는 구매 내역에서 영수증을 바로 받으실 수 있습니다.
      세금계산서가 필요하시면 사업자등록증을 <a href="/inquiry/">문의하기</a>로 보내주세요.</p>

    <h2>4. 환불</h2>
    <p>상품별 환불·청약철회 기준은 <a href="/legal/refund/">환불 규정</a>에 있습니다.</p>

    <h2>5. 사업자 정보</h2>
    """ + BIZ_TABLE + """
  </div>
</div>"""

for _slug, _title, _body, _desc, _noindex in [
    ("inquiry", "문의하기", INQUIRY,
     "로고 제작·기업용 플래너·그 밖의 문의를 남겨주세요. 영업일 기준 하루 안에 답변드립니다. 접수 후에는 진행 상황을 확인하고 이어서 대화하실 수 있습니다.", False),
    ("i", "문의 내용", THREAD,
     "접수하신 문의의 진행 상황을 확인하고 이어서 대화하실 수 있는 페이지입니다. 회원가입 없이 접수 시 받은 링크로 바로 들어옵니다.", True),
    ("how-to-pay", "결제 안내", HOW_TO_PAY,
     "모멘터스 상품의 결제 방법을 안내합니다. 바로 구매하는 상품과 맞춤 제작 상품의 진행 순서가 다릅니다. 결제는 pay.the-moment.us 한 곳에서만 이루어집니다.", False),
]:
    os.makedirs(_slug, exist_ok=True)
    # /i/ 는 개인 스레드라 색인 대상이 아니다. 링크 토큰이 검색에 노출되면 안 된다.
    _extra_head = INQ_CSS + ('<meta name="robots" content="noindex,nofollow">' if _noindex else "")
    with open(f"{_slug}/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"{_title} — MOMENTUS", _desc, _body, active="", head_extra=_extra_head))

# 크롬 웹스토어가 참조하는 기존 URL 유지 (내용만 교체)
os.makedirs("apps", exist_ok=True)
with open("apps/privacy-policy.html", "w", encoding="utf-8") as fh:
    fh.write(page("개인정보처리방침 — MOMENTUS", LEGAL_DESC["privacy"], PRIVACY, active=""))
with open("apps/legal.html", "w", encoding="utf-8") as fh:
    fh.write(page("이용약관 — MOMENTUS", LEGAL_DESC["terms"], TERMS, active=""))

# ---------- 네이티브 앱 /apps/<slug>/ · /setup/ · /support/ ----------
#   ⚠️ apps/ 에는 프로덕션 생명줄(크롬 확장 remote-config, 스토어가 참조하는 legal.html 등)이 산다.
#      apps/README.md 를 반드시 읽고 손대라. 여기서 만드는 건 <slug>/ 하위뿐이다.
APP_TAB_JS = """<script>
(function(){var ts=document.querySelectorAll('.ap-tabs button');if(!ts.length)return;
function sel(k){ts.forEach(function(b){var on=b.dataset.k===k;b.setAttribute('aria-selected',on?'true':'false');});
document.querySelectorAll('.ap-dev').forEach(function(d){d.hidden=d.dataset.k!==k;});
try{localStorage.setItem('ap-dev',k)}catch(e){}}
ts.forEach(function(b){b.addEventListener('click',function(){sel(b.dataset.k)})});
var saved=null;try{saved=localStorage.getItem('ap-dev')}catch(e){}
// 삼성이 국내 점유율이 가장 높아 기본값. 저장된 선택이 있으면 그걸 우선한다.
if(saved&&document.querySelector('.ap-dev[data-k="'+saved+'"]'))sel(saved);
})();
</script>"""

EMAIL = "hello.momentus@gmail.com"


def _shot_attrs(shot):
    """단계 스크린샷 <img> 의 class·width·height 를 만든다.

    가로가 세로보다 긴 그림(태블릿·리더기를 눕혀 찍은 것)은 `.wide` 를 붙여 크게 띄운다.
    세로 폰 기준 max-width:220px 에 묶이면 220×165 로 줄어 메뉴 글씨가 안 읽힌다
    (교보 SAM 10 Plus 1600×1200 실측, 2026-08-01).

    PNG 헤더(IHDR)만 읽는 결정론 판정이다. 파일을 못 읽으면 조용히 기본값으로 둔다 —
    스크린샷 하나 때문에 사이트 생성이 죽으면 안 된다.
    """
    cls, dim = "shot", ""
    try:
        with open(shot.lstrip("/"), "rb") as fh:
            head = fh.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
            w = int.from_bytes(head[16:20], "big")
            h = int.from_bytes(head[20:24], "big")
            if w and h:
                dim = f' width="{w}" height="{h}"'
                if w > h:
                    cls = "shot wide"
    except OSError:
        pass
    return f'class="{cls}"{dim}'


# ⚠️ 정본은 products 다(2026-08-24 승격). 여기서는 **setup/support 두 장만** 만든다 —
#   소개 1장은 제품 상세(/products/<slug>/)가 그린다. 경로도 /products/ 로 옮겼고
#   옛 /apps/<slug>/* 는 _redirects 가 301 로 넘긴다(앱 안에 박힌 링크 보호).
APP_PRODUCTS = {k: v for k, v in P.items() if v.get("type") == "app"}

for _slug, A in APP_PRODUCTS.items():
    _live = A.get("status") == "live" and A.get("store")
    _base = f"/products/{_slug}"

    # ── 1) 제품 소개 ────────────────────────────────────────────
    _feats = "".join(f'<div><div class="t">{t}</div><div class="d">{d}</div></div>'
                     for t, d in A["feats"])
    _spec = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in A["spec"])
    if _live:
        _cta = (f'<a class="go" href="{A["store"]}" target="_blank" rel="noopener">Google Play에서 받기 →</a>'
                f'<a class="sec" href="{_base}/setup/">권한 켜는 법</a>')
        _badge = ""
    else:
        # 아직 공개 스토어 링크가 없다. 없는 버튼을 만들지 않고 상태를 정직하게 쓴다.
        _cta = (f'<a class="go" href="{_base}/setup/">권한 켜는 법 보기</a>'
                f'<a class="sec" href="{_base}/support/">문의하기</a>')
        _badge = '<div class="ap-badge"><span class="dot"></span>비공개 테스트 중 · 정식 출시 준비 중입니다</div>'

    _body = f"""<div class="ap">
  <div class="ap-kick">{A['platform']}</div>
  <h1>{A['tagline']}</h1>
  <div class="sub">{A['desire']}</div>
  {_badge}
  <div class="ap-cta">{_cta}</div>
  <div class="lead">{A['lead']}</div>

  <h2>이런 점이 다릅니다</h2>
  <div class="ap-feats">{_feats}</div>

  <h2>제품 사양</h2>
  <table class="ap-spec">{_spec}</table>

  <h2>개인정보</h2>
  <div class="hint">이 앱은 아무것도 수집하지 않습니다. 접근성 권한이 무엇에 쓰이는지,
  화면 내용을 어떻게 다루는지 <a href="/legal/privacy/" style="text-decoration:underline">개인정보처리방침</a>에
  적어 두었습니다. <a href="/legal/terms/" style="text-decoration:underline">이용약관</a>도 함께 보실 수 있습니다.</div>

  <div class="ap-help">권한을 못 켜고 계신가요? <a href="{_base}/setup/">기기별 설정 방법</a>을 보세요.
  그래도 안 되면 <a href="mailto:{EMAIL}">{EMAIL}</a>로 알려주시면 답변드리겠습니다.</div>
</div>"""
    # (소개 1장은 제품 상세 /products/<slug>/ 가 그린다 — 여기선 안 쓴다)

    # ── 2) 접근성 권한 켜는 법 ──────────────────────────────────
    S = A["setup"]
    _tabs = "".join(f'<button type="button" data-k="{dv["key"]}" role="tab" '
                    f'aria-selected="{"true" if i == 0 else "false"}">{dv["label"]}</button>'
                    for i, dv in enumerate(S["devices"]))
    _panes = ""
    for i, dv in enumerate(S["devices"]):
        _steps, _land = "", False
        for t, d, shot in dv["steps"]:
            # shot 이 비어 있으면(실기기 촬영 대기) 그림 없이 글로만 안내한다.
            _at = _shot_attrs(shot) if shot else ""
            if "wide" in _at:
                _land = True          # 눕혀 찍은 화면이 섞인 탭 → 2열로 벌린다
            _img = f'<img {_at} src="{shot}" alt="{t} 화면" loading="lazy">' if shot else ""
            _steps += f'<li><div><div class="t">{t}</div><div class="d">{d}</div>{_img}</div></li>'
        _note = f'<div class="note">{dv["note"]}</div>' if dv.get("note") else ""
        _panes += (f'<div class="ap-dev" data-k="{dv["key"]}"{"" if i == 0 else " hidden"}>'
                   f'{_note}<ol class="ap-steps{" landscape" if _land else ""}">{_steps}</ol></div>')
    _qa = "".join(f"<details><summary>{q}</summary><div class=\"a\">{a}</div></details>"
                  for q, a in S["trouble"])

    _body = f"""<div class="ap">
  <header class="ap-head">
    <nav class="ap-crumb" aria-label="위치">
      <a href="/products/">제품</a><span class="sep">›</span>
      <a href="{_base}/">{A['name']}</a><span class="sep">›</span>
      <span class="now" aria-current="page">설정</span>
    </nav>
    <h1>접근성 권한 켜는 법</h1>
    <div class="lead">{S['lead']}</div>
  </header>
  <div class="ap-body">
  <div class="ap-tabs" role="tablist">{_tabs}</div>
  {_panes}

  <h2>잘 안 될 때</h2>
  <div class="ap-qa">{_qa}</div>

  <div class="ap-help">여기까지 해도 안 되면 <a href="mailto:{EMAIL}">{EMAIL}</a>로
  쓰시는 기기 이름과 안드로이드 버전을 알려주세요. 확인해서 답변드리겠습니다.</div>
  <a class="ap-back" href="{_base}/">← {A['name']} 제품 페이지</a>
  </div>
</div>"""
    os.makedirs(f"{_base.strip('/')}/setup", exist_ok=True)
    with open(f"{_base.strip('/')}/setup/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"접근성 권한 켜는 법 — {A['name']}",
                      # 실제 탭과 일치시킨다. '순정 안드로이드'는 실기기가 없어 확인 못 했으므로 쓰지 않는다.
                      f"{A['name']} 접근성 권한을 기기별로 켜는 방법입니다. 삼성 One UI·교보 SAM·하이센스 E-ink 리더기의 실제 화면을 단계별로 보여드립니다. 권한이 안 켜질 때 확인할 것도 함께 적었습니다.",
                      _body, active="", extra=APP_TAB_JS))

    # ── 3) 지원·문의 ────────────────────────────────────────────
    #   앱이 이 페이지를 '고장났을 때 누르는 곳'으로 쓰기 시작하면(Flipper v27 메인 화면 하단
    #   '도움받기'), 도착하는 사람은 결제 문의가 아니라 동작 불량 상태다. 그래서 자가진단이
    #   맨 위에 온다. 내용은 매니페스트 apps.<slug>.support 에 있고 없으면 이 절을 통째로 건너뛴다.
    SUP = A.get("support") or {}
    _sc = SUP.get("selfcheck") or {}
    if _sc:
        _sc_steps = "".join(
            f'<li><div><div class="t">{t}</div><div class="d">{d}</div></div></li>'
            for t, d in _sc["steps"])
        _selfcheck = (f'<h2>{_sc["title"]}</h2>'
                      f'<ol class="ap-steps">{_sc_steps}</ol>'
                      f'<div class="note">{_sc["fallback"]}</div>')
    else:
        _selfcheck = ""

    _ask = SUP.get("ask") or []
    _ask_html = (f"<br>메일에 아래 {len(_ask)}가지를 함께 적어 주시면 훨씬 빨리 답변드릴 수 있습니다."
                 f'<ul class="ask">{"".join(f"<li>{a}</li>" for a in _ask)}</ul>') if _ask else \
                "<br>기기 이름과 안드로이드 버전을 함께 적어 주시면 훨씬 빨리 답변드릴 수 있습니다."

    _lead = SUP.get("lead") or (f'가장 많은 문의는 <b>접근성 권한이 안 켜진다</b>는 것입니다. '
                                f'<a href="{_base}/setup/" style="text-decoration:underline">'
                                f'기기별 설정 방법</a>을 먼저 확인해 주세요.')

    _body = f"""<div class="ap">
  <header class="ap-head">
    <nav class="ap-crumb" aria-label="위치">
      <a href="/products/">제품</a><span class="sep">›</span>
      <a href="{_base}/">{A['name']}</a><span class="sep">›</span>
      <span class="now" aria-current="page">지원</span>
    </nav>
    <h1>도움이 필요하신가요</h1>
    <div class="lead">{_lead}</div>
  </header>
  <div class="ap-body">
  {_selfcheck}

  <h2>문의</h2>
  <div class="hint"><a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a>{_ask_html}</div>

  <h2>구독·결제</h2>
  <div class="hint">결제와 환불은 Google Play가 처리합니다. 구독 해지·환불은
  <b>Play 스토어 → 프로필 → 결제 및 구독</b>에서 하실 수 있습니다.
  자세한 내용은 <a href="/legal/refund/" style="text-decoration:underline">환불 규정</a>을 보세요.</div>

  <h2>문서</h2>
  <div class="hint"><a href="/legal/privacy/" style="text-decoration:underline">개인정보처리방침</a> ·
  <a href="/legal/terms/" style="text-decoration:underline">이용약관</a></div>

  <a class="ap-back" href="{_base}/">← {A['name']} 제품 페이지</a>
  <a class="ap-back" href="{_base}/setup/" style="margin-left:10px">권한 켜는 법 →</a>
</div>
</div>"""
    os.makedirs(f"{_base.strip('/')}/support", exist_ok=True)
    with open(f"{_base.strip('/')}/support/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"지원 — {A['name']} — MOMENTUS",
                      _re_desc(f"{A['name']} 지원 페이지입니다. 자가진단으로 흔한 문제를 먼저 "
                               f"확인하고, 해결되지 않으면 이메일로 문의하세요. 구독 해지와 환불 방법도 "
                               f"함께 안내합니다."), _body, active=""))

# ---------- /tools/ 허브는 폐지(2026-08-23) ----------
#   '제품'과 '무료 도구'를 나란히 놓으니 사용자에게 우리만 아는 구분을 강요하게 됐다
#   (대표: "전체 제품에는 도구는 전체 제품이 아니야, 이것도 웃기고").
#   목록은 /products/ 마지막 섹션으로 흡수하고 /tools/ 는 301 로 넘긴다.
#   ⚠️ 개별 도구 페이지 /tools/<slug>/ 는 그대로 — 무료 도구의 유입 권위(PLATFORM_TOPOLOGY §5).
_TYPEN = {"bookmarklet": "북마크릿", "extension": "크롬 확장"}
import shutil as _sh
if os.path.exists("tools/index.html"):
    os.remove("tools/index.html")

# ---------- /products/ 허브 (유료 제품 리스팅) ----------
#   무료 도구엔 /tools/ 허브가 있는데 유료 제품엔 모아 보는 자리가 없었다(2026-08-23 실측: /products/ 404).
#   그래서 GNB '전체 제품'이 갈 데가 없고, 제품이 늘어도 걸 자리가 없었다.
#   ⚠️ 그룹은 "무엇을 파느냐"가 아니라 "언제 쓰느냐"로 나눈다 — 제품이 늘어도 칸이 안 늘어난다.
# ⚠️ 무료/유료로 나누지 않는다 — 손님은 "지금 뭘 하려는가"를 먼저 찾지 "돈을 내나"를
#   먼저 찾지 않는다(2026-08-24). 과금은 카드 오른쪽 태그로만 표시한다.
PROD_GROUPS = [
    ("사업을 시작할 때", "가게를 열고 브랜드를 세울 때 필요한 것",
     ["heyreci", "mark"]),
    ("일과 성장", "일하는 나를 준비시키는 것",
     ["cue", "theplan", "kontext", "chatpage"]),
    ("곁에 두는 사람", "매일 이야기하고, 기억하고, 먼저 챙기는 것",
     ["teamai"]),
    ("일상을 편하게", "기다리고 챙기는 일을 대신 맡기는 것",
     ["binbang", "flipper", "quickpang", "insta-rank", "youtube-rank",
      "pinterest-grab", "her"]),
]

# ⚠️ '유료' 태그를 달지 않는다(2026-08-24 대표 지적). 그 말은 아무것도 안 알려준다 —
#   큐·더플랜은 구독이고 플리퍼도 구독이고 헤이레시는 사실상 쇼핑몰인데 전부 '유료'가 됐다.
#   게다가 경고처럼 읽힌다. **알릴 가치가 있는 건 공짜라는 사실뿐**이라 그것만 남긴다.
#   태그가 없으면 = 돈을 낸다. 얼마인지는 제품 페이지가 말한다.
_PRICE_TAG = {"teamai": "무료 시작", "binbang": "무료 있음", "flipper": "무료 체험", "kontext": "무료 체험"}


def _prod_card(s_):
    pr = P[s_]
    free = bool(pr.get("free"))
    price = _PRICE_TAG.get(s_) or ("무료" if free else "")
    shot = prod_shot(s_)
    _lg = " logo" if pr.get("logo") and shot and pr["logo"] in shot else ""
    th = (f'<div class="th{_lg}"><img src="{shot}" alt="" loading="lazy" decoding="async"></div>'
          if shot else
          f'<div class="th ic" style="--c:{pr.get("color", "#0b0c0e")}" aria-hidden="true">{pr["icon"]}</div>')
    # ⚠️ 태그를 조건부로 붙일 때 삼항을 **return 전체**에 걸면 안 된다 — 태그 없는 제품이
    #    통째로 사라진다(2026-08-24 실사고: 유료 4종이 목록에서 빠졌다). 조각만 조건부로.
    tag = f'<div class="mt{" free" if free else ""}">{esc(price)}</div>' if price else ""
    return (f'<a class="prh-row" href="{purl(s_)}">{th}'
            f'<div class="bd">'
            f'<div class="nm">{pr["short"]}</div>'
            f'<div class="tg">{pr["tag"]}</div>'
            f'<div class="ds">{pr["tagline"]}</div>'
            f'</div>{tag}</a>')

def _prod_group(t, sub, items):
    rows = "".join(_prod_card(x) for x in items if x in P)
    return (f'<section class="prh-g"><div class="prh-gh"><h2>{t}</h2><span class="s">{sub}</span></div>'
            f'<div class="prh-list">{rows}</div></section>')

_pg = "".join(_prod_group(t, sub, items) for t, sub, items in PROD_GROUPS)
# 무료 도구도 결국 우리가 만들어 내놓은 것이다 — 별도 페이지로 갈라 두니 사용자에게
# '제품 vs 도구'라는 우리만 아는 구분을 강요하게 됐다(2026-08-23 대표 지적). 같은 목록의 마지막 칸.

products_body = f"""<div class="prh">
  <header class="nws-head">
    <h1>제품</h1>
    <p>1인 AI 스튜디오가 직접 만들어 직접 팝니다. 결제하면 바로 시작되는 것부터,
      설치 없이 그냥 쓰는 것까지 여기 다 있습니다.</p>
  </header>
  {_pg}
  <p class="prh-foot">찾으시는 게 없거나 만들었으면 하는 게 있으면
    <a href="/inquiry/">문의해 주세요</a>. 직접 읽고 답합니다.</p>
</div>"""
os.makedirs("products", exist_ok=True)
with open("products/index.html", "w", encoding="utf-8") as f:
    f.write(page("제품 — MOMENTUS",
                 "모멘터스가 만든 제품 — AI 상품사진(헤이레시), 로고 디자인(마크), AI 모의면접(큐), 디지털 플래너(더플랜), 펜션 빈방 알림(빈방).",
                 products_body, active=""))

# ---------- 리다이렉트 — 옮긴 무료 도구 주소 회수 ----------
#   무료 도구가 /products/<slug>/ → /tools/<slug>/ 로 이동(2026-07-27). 기존 링크·검색 결과 보존.
with open("_redirects", "w", encoding="utf-8") as f:
    f.write("# 생성물(scripts/gen_site.py). 손으로 고치지 말 것.\n")
    for s in TOOLS:
        f.write(f"/products/{s}/* /tools/{s}/ 301\n")
        f.write(f"/products/{s} /tools/{s}/ 301\n")
    # /tools/ 허브 폐지(2026-08-23) — 목록은 /products/ 안으로 흡수. 개별 도구 페이지는 그대로.
    f.write("/tools/ /products/ 301\n")
    # 인사이트 주소 통일(2026-08-24). 옛 /stories/ 는 글 3편이 색인돼 있어 끊으면 안 된다.
    # ⚠️ 넓은 규칙 하나로 뭉치지 마라 — `/stories/*` 는 **빈 문자열을 안 잡아** 목록이 샌다.
    f.write("/stories/ /insights/ 301\n")
    f.write("/stories /insights/ 301\n")
    f.write("/stories/:slug/ /insights/:slug/ 301\n")
    f.write("/stories/:slug /insights/:slug/ 301\n")
    f.write("/stories/tag/:k/ /insights/tag/:k/ 301\n")
    f.write("/stories/tag/:k /insights/tag/:k/ 301\n")
    f.write("/tools /products/ 301\n")
    # /apps/ → /products/ (2026-08-24 승격). ⚠️ **설치된 앱 안에 /apps/flipper/setup/ 이
    #   박혀 있다** — 앱이 업데이트되기 전까지 이 301 이 유일한 연결이다. 지우지 마라.
    #   앱이 새 주소로 나가면 BACKLOG.md 의 항목을 지우고 이 줄도 뺄 수 있다.
    # ⚠️ 리다이렉트보다 **실제 파일이 먼저 이긴다**. 승격 뒤 apps/<slug>/ 산출물이 남아 있어
    #   301 이 통째로 무시됐다(2026-08-24 실측: /apps/flipper/setup/ → 제품 페이지로 감).
    #   생성기가 더 이상 안 만드니, 남아 있으면 지운다.
    import shutil as _sh2
    for _s in APP_PRODUCTS:
        if os.path.isdir(f"apps/{_s}"):
            _sh2.rmtree(f"apps/{_s}")
            print(f"  · 옛 apps/{_s}/ 제거 — 301 이 가려지고 있었다")
    # 인사이트로 옮긴 뒤 남은 옛 stories/ 산출물 — 같은 함정(파일이 301 을 이긴다).
    if os.path.isdir("stories"):
        _sh2.rmtree("stories")
        print("  · 옛 stories/ 제거 — 301 이 가려지고 있었다")
    for _s in APP_PRODUCTS:
        # ⚠️ `/x/*` 는 **빈 문자열을 안 잡는다** — `/apps/flipper/setup/` 가 이 규칙을 비켜가
        #   아래 `/apps/flipper/*` 에 걸려 제품 페이지로 갔다(2026-08-24 실측).
        #   앱이 여는 바로 그 주소라 치명적이었다. 슬래시로 끝나는 정확 경로를 따로 적는다.
        for _sub in ("setup", "support"):
            f.write(f"/apps/{_s}/{_sub}/ /products/{_s}/{_sub}/ 301\n")
            f.write(f"/apps/{_s}/{_sub} /products/{_s}/{_sub}/ 301\n")
            f.write(f"/apps/{_s}/{_sub}/* /products/{_s}/{_sub}/ 301\n")
        # ⚠️ 넓은 `/apps/<slug>/*` 을 두면 위의 setup·support 규칙을 삼킨다(2026-08-24 실측:
        #   순서를 앞세워도 CF 가 이걸 먼저 잡았다). 하위 경로는 각각 적고, 와일드카드는 안 쓴다.
        f.write(f"/apps/{_s}/ /products/{_s}/ 301\n")
        f.write(f"/apps/{_s} /products/{_s}/ 301\n")
    f.write("/apps/ /products/ 301\n")
    f.write("/apps /products/ 301\n")
    # 블로그가 /log/ → /stories/ 로 승격(2026-07-27). 기존 링크·검색 결과 보존.
    for s in PORDER:
        # 슬래시로 끝나는 정확 경로도 따로 적는다 — `/log/x/*` 는 뒤가 빈 `/log/x/` 를 안 잡는다(실측).
        f.write(f"/log/{s}/ /insights/{s}/ 301\n")
        f.write(f"/log/{s} /insights/{s}/ 301\n")
    # ⚠️ 와일드카드 /log/* 는 두지 않는다 — 실측에서 그게 개별 글 규칙을 덮어 전부 목록으로 보냈다.
    f.write("/log/ /insights/ 301\n")
    f.write("/log /insights/ 301\n")
    # 레거시 /apps/<슬러그>/ 회수(2026-08-01). 저장소를 비우고 외장 보관으로 옮긴 옛 앱 랜딩들.
    #   퀵팡이 이 중 유일하게 외부 유입이 살아 있다(1만+). 드래그 버튼 payload가
    #   /tools/quickpang/ 와 바이트 동일(14,796자)임을 실측 확인하고 넘긴다.
    #   ⚠️ 규칙을 슬러그별로만 쓴다. /apps/* 같은 광역 규칙 금지 — 아래 넷이 프로덕션 생명줄이라
    #      한 번에 죽는다: apps/chatpage/remote-config(확장이 실시간 조회) ·
    #      apps/legal.html · apps/privacy-policy.html(크롬 웹스토어 참조) ·
    #      apps/timer/support-page.html(맥 App Store 지원 URL).
    # ⚠️ /l/<키>(영구 링크 층) 규칙을 여기에 두지 마라. 별도 워커가 처리한다.
    #    2026-08-01 실측: 개별 규칙(/l/flipper …)을 catch-all(/l/*)보다 먼저 뒀는데도
    #    catch-all 이 전부 삼켰다 — _redirects 는 선매치 승리를 보장하지 않는다.
    #    앱은 배포 후 URL을 못 고치므로 그 층을 문서에 없는 동작에 걸 수 없다.
    #    → workers/link-redirect/ (라우트 the-moment.us/l/* 가 더 구체적이라 apex보다 먼저 매칭)
    f.write("/apps/quickpang/* /tools/quickpang/ 301\n")
    f.write("/apps/quickpang/ /tools/quickpang/ 301\n")
    f.write("/apps/quickpang /tools/quickpang/ 301\n")
    # 대체재가 없는 레거시는 홈으로 회수한다(방문자에게 404보다 낫다).
    for s in ("pion", "dokdo", "kidup", "openspot", "naver-talk-hub"):
        f.write(f"/apps/{s}/* / 301\n")
        f.write(f"/apps/{s}/ / 301\n")
        f.write(f"/apps/{s} / 301\n")

# ---------- 영구 링크 층 워커의 매핑 생성 ----------
#   data/products.json 의 links 가 원본. 워커는 이 파일을 import 해서 302를 쏜다.
#   이 파일을 손으로 고치지 마라 — 다음 생성에서 덮어쓴다.
if LINKS.get("map"):
    os.makedirs("workers/link-redirect", exist_ok=True)
    with open("workers/link-redirect/map.json", "w", encoding="utf-8") as f:
        json.dump({"_note": "생성물(scripts/gen_site.py). data/products.json 의 links 를 고쳐라.",
                   "map": LINKS["map"],
                   "catchall": LINKS.get("_catchall", "/")},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")

# ---------- sitemap ----------
# /i/ 는 개인 스레드라 뺀다(링크 토큰 노출 금지).
urls = ["", "about/", "tools/", "inquiry/", "how-to-pay/",
        "legal/privacy/", "legal/terms/", "legal/refund/"] \
    + [purl(s).lstrip("/") for s in ORDER] \
    + [f"products/{s}/{sub}" for s in APP_PRODUCTS for sub in ("setup/", "support/")] \
    + ["insights/"] + [f"insights/{s}/" for s in PORDER] \
    + [f"insights/tag/{k}/" for k, lab in STORY_TAGS
       if any(lab in e.get("tags", []) for e in entries)]   # 빈 태그는 sitemap 에서 뺀다
# ⚠️ /l/<키>는 sitemap 에 넣지 않는다 — 내용 없는 이정표(302)라 색인 대상이 아니다.
# lastmod — §16-3. **내용에서 나온 날짜만** 쓴다.
# 🚫 빌드 시각을 넣지 마라. 매일 05:45 재빌드가 32개 전부 "오늘 바뀜"으로 만들고,
#    그러면 크롤러가 이 사이트의 lastmod 를 통째로 믿지 않게 된다.
# 글은 POSTS 의 date 가 진짜 날짜다. 나머지(제품·법적 문서)는 날짜 출처가 없으므로 안 넣는다 —
# 없는 게 거짓말보다 낫다.
_lastmod = {}
for _s in PORDER:
    _d = POSTS[_s].get("updated") or POSTS[_s].get("date") or ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", str(_d)):
        _lastmod[f"insights/{_s}/"] = str(_d)
_newest = max(_lastmod.values(), default="")
if _newest:
    _lastmod["insights/"] = _newest      # 목록의 갱신일 = 가장 최근 글

# ── 제품 페이지의 lastmod — **원본 데이터가 바뀐 날**을 기록해서 쓴다 (2026-08-29)
#
# 왜 필요한가: apex 사이트맵이 2026-07-02 에 한 번 읽히고 58일간 방치됐다. 재제출로 풀었지만
#   재방문 신호가 없으면 또 방치된다. 그런데 32장 중 lastmod 가 붙은 건 글 4장뿐이었다.
#
# 🔴 왜 "생성된 HTML"이 아니라 "원본 데이터"를 해시하나:
#   셸(푸터·나브·CSS)은 여러 저장소가 공유하고 자주 바뀐다. 출력 HTML 을 해시하면
#   푸터 한 줄 고칠 때마다 **32장 전부가 "오늘 바뀜"**이 된다. 그게 §16-3 이 금지하는 거짓 신선도다.
#   제품 페이지의 내용은 products.json 의 그 제품 항목에서 나온다 — 그것만 본다.
#
# 🔴 첫 실행에 오늘 날짜를 박지 않는다:
#   기록이 없는 URL 은 **해시만 저장하고 lastmod 는 안 붙인다.** 없는 게 거짓말보다 낫다.
#   다음에 실제로 바뀌면 그때부터 진짜 날짜가 붙는다. 과거를 지어내지 않고 미래를 정확하게 만든다.
_LM_STATE = "data/page_lastmod.json"
try:
    with open(_LM_STATE, encoding="utf-8") as _f:
        _lm_state = json.load(_f)
except Exception:
    _lm_state = {}
_today = datetime.date.today().isoformat()
_lm_changed = 0
for _slug in ORDER:
    # ⚠️ URL 은 반드시 purl() 에서 가져온다 — 위 `urls` 도 같은 함수를 쓴다.
    #    여기서 문자열을 따로 조립하면 한 글자만 달라도 조용히 하나도 안 맞는다.
    _u = purl(_slug).lstrip("/")
    if _u not in urls:
        continue
    _h = hashlib.sha1(json.dumps(P[_slug], sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    _prev = _lm_state.get(_u)
    if _prev is None:
        _lm_state[_u] = {"h": _h}                       # 첫 관측 — 날짜는 안 붙인다
    elif _prev.get("h") != _h:
        _lm_state[_u] = {"h": _h, "d": _today}          # 실제로 바뀐 날
        _lm_changed += 1
    if _lm_state[_u].get("d"):
        _lastmod[_u] = _lm_state[_u]["d"]
try:
    with open(_LM_STATE, "w", encoding="utf-8") as _f:
        json.dump(_lm_state, _f, ensure_ascii=False, indent=1, sort_keys=True)
except Exception as _e:
    print(f"  🟠 page_lastmod 저장 실패: {_e}")
if _lm_changed:
    print(f"  lastmod: 제품 {_lm_changed}장이 오늘 바뀐 것으로 기록됨")

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    _lm = _lastmod.get(u)
    sm += f"  <url><loc>https://the-moment.us/{u}</loc>" + (f"<lastmod>{_lm}</lastmod>" if _lm else "") + "</url>\n"
sm += "</urlset>\n"
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sm)

# ── robots.txt ─────────────────────────────────────────────────────────────
# ⚠️ 이 파일이 없으면 **Cloudflare 가 자기 안내문을 자동 주입**한다(2026-08-04 실측):
#    설명 주석만 1248B, 실제 지시문 0줄, **Sitemap 선언 0줄**. 봇에게 "우리 페이지 여기 있다"를
#    못 알려주고 있었고 통제권도 우리에게 없었다. 파일을 두는 것만으로 회수된다.
# 🚫 AI 봇(GPTBot·ClaudeBot·PerplexityBot·OAI-SearchBot)을 막지 마라 — GEO 노출이 목적이다.
#    막고 싶어지면 그때 여기에 명시적으로 Disallow 를 적는다. 의도를 파일에 남긴다.
robots = """User-agent: *
Allow: /

# 결제 도메인은 색인 대상이 아니다(pay.the-moment.us 는 자체 robots 로 Disallow).
# apex 에는 비공개 경로가 없다.

# AI 검색·요약 봇을 의도적으로 허용한다(GEO). 우리 제품이 AI 답변에 인용되는 것이 목표다.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# 네이버·다음 — * 로도 통과하지만 명시한다.
# 2026-08-29 실측: cue 검색 유입의 47%가 네이버였고 구글은 0이었다. 국내 서비스의 주력이다.
User-agent: Yeti
Allow: /

User-agent: Daum
Allow: /

Sitemap: https://the-moment.us/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots)

# ── llms.txt ───────────────────────────────────────────────────────────────
# AI 가 "모멘터스가 뭐고 뭘 파는가"를 한 장으로 읽게 한다. mark·cue 는 이미 두고 있다.
# 사람이 읽는 페이지와 달리 **군더더기 없이 사실만** 적는다 — 형용사·홍보 문구는 오히려 방해.
prod_lines = "\n".join(
    f"- [{P[s]['name']}]({P[s].get('url') or f'https://the-moment.us/products/{s}/'}): {P[s].get('tagline','')}"
    for s in SPOKES if s in P
)
tool_lines = "\n".join(
    f"- [{P[t]['name']}](https://the-moment.us/tools/{t}/): {P[t].get('tagline','')}"
    for t in TOOLS if t in P
)
llms = f"""# 모멘터스 (MOMENTUS)

> 강형모 1인 AI 스튜디오. 쓸모 있는 것만 만듭니다.
> 사업자: {BIZ['name']} · 대표 {BIZ['ceo']} · 사업자등록번호 {BIZ['reg']} · 통신판매업신고 {BIZ['mail_order']}
> 문의: {BIZ['email']}

## 유료 제품
{prod_lines}

## 무료 브라우저 도구
{tool_lines}

## 결제
- 결제는 https://pay.the-moment.us 한 곳에서만 이루어집니다. 판매 중인 전 상품을 그곳에서 확인할 수 있습니다.
- 회원가입·로그인이 없습니다. 구매 시 입력한 이메일이 주문의 식별자입니다.
- 구매내역 조회: https://pay.the-moment.us/orders

## 정책
- [이용약관](https://the-moment.us/legal/terms/)
- [개인정보처리방침](https://the-moment.us/legal/privacy/)
- [환불 및 청약철회](https://the-moment.us/legal/refund/)
"""
with open("llms.txt", "w", encoding="utf-8") as f:
    f.write(llms)

# ── OG 이미지 생성 (og/*.png) ──────────────────────────────────────────────
# 매니페스트에서 1200×630 을 굽는다. 실패해도 빌드를 죽이지 않는다(gen_og.py 참조).
import subprocess as _sp, sys as _sys
_sp.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_og.py")],
        check=False)


# ── canonical / og:url / og:image 후처리 ───────────────────────────────────
# page() 호출부가 17곳이라 인자를 하나 더 받게 하면 어딘가는 반드시 빠뜨린다.
# canonical 은 본래 **출력 경로에서 기계적으로 도출되는 값**이므로 마지막에 한 번에 주입한다.
# → 앞으로 페이지를 추가해도 자동으로 붙는다(빠뜨릴 수가 없다).
# 🚫 손으로 canonical 을 박지 마라. 여기서 덮어쓴다.
# ⚠️ 생성기 산출물만 건드린다(`/assets/site.css?v=` 서명으로 판별) — apps/ 아래에는
#    크롬 확장·앱스토어가 실시간 참조하는 손관리 파일이 섞여 있다(apps/README.md).
import glob as _glob, re as _re

# ── 페이지 유형별 JSON-LD ──────────────────────────────────────────────────
# 정본 표: docs/SEO_GEO.md §4.
# 전 페이지에 Organization 하나를 복붙하던 걸 대체한다. 여기도 **경로에서 유형을 판별**하므로
# 새 페이지를 추가해도 자동으로 맞는 스키마가 붙는다(빠뜨릴 수가 없다).
#
# ⚠️ 화면에 없는 걸 스키마에 적지 않는다(구글 스팸 정책 = 리치결과 영구 박탈).
#    그래서 제목·날짜·목록은 **생성된 HTML 에서 뽑고**, 가격은 확실한 것만 쓴다:
#    무료 도구만 price "0", 유료 제품은 가격을 안 적는다(정본이 pay 의 sku 라 여기선 모른다).

_ORG = {"@type": "Organization", "@id": "https://the-moment.us/#org",
        "name": "모멘터스", "alternateName": "MOMENTUS",
        "url": "https://the-moment.us", "email": BIZ["email"]}
_PUB = {"@id": "https://the-moment.us/#org"}


def _txt(h):
    """HTML 조각 → 사람이 보는 텍스트. 스키마에 넣기 전 태그를 턴다."""
    return " ".join(_re.sub(r"<[^>]+>", " ", h).split())


def _h1(html):
    m = _re.search(r"<h1[^>]*>(.*?)</h1>", html, _re.S | _re.I)
    return _txt(m.group(1)) if m else ""


def _desc_of(html):
    m = _re.search(r'<meta name="description" content="([^"]*)"', html)
    return m.group(1) if m else ""


def _date_of(html):
    """이야기 글의 발행일. 화면에 '2026. 07. 05' 로 찍혀 있는 값만 쓴다."""
    m = _re.search(r"(20\d\d)\.\s*(\d\d)\.\s*(\d\d)", html)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def _links(html, prefix):
    """본문에 실제로 있는 링크만 ItemList 로 낸다(없는 항목을 지어내지 않는다)."""
    seen, out = set(), []
    for href, label in _re.findall(r'<a[^>]+href="(' + prefix + r'[^"]*)"[^>]*>(.*?)</a>',
                                   html, _re.S | _re.I):
        t = _txt(label)
        if href in seen or not t or href.rstrip("/") == prefix.rstrip("/"):
            continue
        seen.add(href)
        out.append({"@type": "ListItem", "position": len(out) + 1,
                    "url": "https://the-moment.us" + href, "name": t[:80]})
    return out


def _crumbs(seg, html):
    if not seg:
        return None
    items, acc = [{"@type": "ListItem", "position": 1, "name": "홈",
                   "item": "https://the-moment.us/"}], ""
    for i, s in enumerate(seg):
        acc += s + "/"
        items.append({"@type": "ListItem", "position": i + 2,
                      "name": (_h1(html) if i == len(seg) - 1 else s) or s,
                      "item": "https://the-moment.us/" + acc})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def _faq_schema(html):
    """화면의 FAQ 블록에서 FAQPage 를 만든다. 스키마가 본문에서 파생되므로
       '화면에 없는 걸 스키마에 적지 않는다'가 구조적으로 보장된다."""
    qa = _re.findall(r'<div class="vd-qa-i"><h3>(.*?)</h3><p>(.*?)</p></div>', html, _re.S)
    if not qa:
        return None
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _txt(q),
         "acceptedAnswer": {"@type": "Answer", "text": _txt(a)}} for q, a in qa]}


def _schema_for(rel, url, html, img):
    """그 페이지의 @graph 를 만든다. docs/SEO_GEO.md §4 표와 1:1로 대응한다."""
    seg = [x for x in rel.split("/") if x]
    h1, desc = _h1(html) or "", _desc_of(html)
    node = None

    if not seg:                                                   # 랜딩
        node = {"@type": "WebSite", "name": "MOMENTUS", "alternateName": "모멘터스",
                "url": "https://the-moment.us/", "inLanguage": "ko",
                "publisher": _PUB, "description": desc}
    elif seg[0] == "products" and len(seg) == 2:                  # 유료 제품 상세
        p = P.get(seg[1], {})
        node = {"@type": "SoftwareApplication" if p.get("type") != "product" else "Product",
                "name": h1 or p.get("name", seg[1]), "description": desc,
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Web", "image": img,
                "brand": {"@type": "Brand", "name": "MOMENTUS"}, "publisher": _PUB}
        if p.get("url"):
            # 가격은 안 적는다 — 정본이 pay 의 sku 다. 틀린 가격은 상품 노출이 끊긴다.
            node["offers"] = {"@type": "Offer", "url": p["url"],
                              "availability": "https://schema.org/InStock",
                              "seller": _PUB}
    elif seg[0] == "tools" and len(seg) == 2:                     # 무료 브라우저 도구
        node = {"@type": "SoftwareApplication", "name": h1 or seg[1], "description": desc,
                "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web",
                "image": img, "publisher": _PUB,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW",
                           "availability": "https://schema.org/InStock", "url": url}}
    elif seg == ["tools"]:                                        # 도구 허브
        node = {"@type": "CollectionPage", "name": h1 or "무료 도구", "description": desc,
                "url": url, "publisher": _PUB,
                "mainEntity": {"@type": "ItemList",
                               "itemListElement": _links(html, "/tools/")}}
    elif seg[0] == "apps" and len(seg) == 2 and seg[1] in APPS:   # 네이티브 앱
        # ⚠️ `seg[1] in APPS` 가 필수다. /apps/ 아래엔 앱이 아닌 별칭 페이지가 섞여 있다
        #    (apps/legal.html·apps/privacy-policy.html → 앱스토어가 참조하는 법적 문서 사본).
        a = APPS.get(seg[1], {})
        node = {"@type": "MobileApplication", "name": h1 or a.get("name", seg[1]),
                "description": desc, "applicationCategory": "UtilitiesApplication",
                "operatingSystem": a.get("platform") or "Android",
                "image": img, "publisher": _PUB}
    elif seg[:1] == ["insights"] and len(seg) == 2 and seg[1] != "tag":  # 인사이트 글
        node = {"@type": "BlogPosting", "headline": h1 or desc, "description": desc,
                "image": img, "url": url, "inLanguage": "ko",
                "author": {"@type": "Person", "name": "강형모"}, "publisher": _PUB,
                "mainEntityOfPage": {"@type": "WebPage", "@id": url}}
        d = _date_of(html)
        if d:
            node["datePublished"] = node["dateModified"] = d
    elif seg[0] == "insights":                                    # 인사이트 인덱스·태그
        node = {"@type": "CollectionPage", "name": h1 or "이야기", "description": desc,
                "url": url, "publisher": _PUB,
                "mainEntity": {"@type": "ItemList",
                               "itemListElement": _links(html, "/insights/")}}
    elif seg[0] == "about":
        node = {"@type": "AboutPage", "name": h1 or "소개", "description": desc,
                "url": url, "publisher": _PUB, "mainEntity": _PUB}
    else:                                                          # 법적 문서·앱 하위 등
        node = {"@type": "WebPage", "name": h1 or "", "description": desc,
                "url": url, "inLanguage": "ko", "publisher": _PUB}

    graph = [_ORG, node]
    cr = _crumbs(seg, html)
    if cr:
        graph.append(cr)
    fq = _faq_schema(html)
    if fq:
        graph.append(fq)
    # 빈 값은 스키마에서 뺀다 — 빈 문자열을 넣으면 검증기가 경고한다.
    graph = [{k: v for k, v in n.items() if v not in ("", [], {}, None)} for n in graph]
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False)


_canon_n = 0
_ld_n = 0
for _p in _glob.glob("**/*.html", recursive=True):
    # `_` 로 시작하는 경로는 실험용 로컬 산출물이다(배포 안 됨, 라이브 404 확인 2026-08-07).
    if (_p.startswith(("node_modules/", "design-review/", "_")) or "/404" in _p
            or _p.startswith("naver")):
        continue
    _s = open(_p, encoding="utf-8").read()
    if "/assets/site.css?v=" not in _s:          # 생성기 산출물이 아니면 건너뛴다
        continue
    # ⚠️ canonical 은 **실제로 서빙되는 최종 주소**여야 한다. 리다이렉트되는 주소를 넣으면 신호가 흐려진다.
    #    이 워커는 html_handling="auto-trailing-slash" 라 `/apps/legal.html` 은 `/apps/legal` 로 넘긴다.
    #    (2026-08-04 실측: /apps/legal.html → 200이지만 url_effective 는 /apps/legal)
    if _p == "index.html":
        _rel = ""
    elif _p.endswith("/index.html"):
        _rel = _p[:-len("index.html")]          # foo/index.html → foo/
    else:
        _rel = _p[:-len(".html")]               # foo/bar.html   → foo/bar  (확장자 없이 서빙됨)
    _url = "https://the-moment.us/" + _rel
    # 별칭 페이지는 canonical 을 **원본으로 몰아준다.** 내용이 같은 두 URL 이 각자
    # 자기참조 canonical 을 들면 중복 콘텐츠 신호가 갈린다(2026-08-07 실측).
    # 앱스토어·크롬웹스토어가 이 주소를 참조하므로 URL 자체는 살려 둔다.
    _url = {"apps/legal": "https://the-moment.us/legal/terms/",
            "apps/privacy-policy": "https://the-moment.us/legal/privacy/"}.get(_rel, _url)

    # og:image 도 **경로에서 기계적으로 도출한다** — canonical 과 같은 이유다.
    # `/products/cue/` · `/tools/cue/` → og/cue.png, 없으면 og/default.png.
    # 새 페이지를 추가해도 최소한 기본 이미지는 반드시 붙는다(빠뜨릴 수가 없다).
    # 🚫 손으로 og:image 를 박지 마라. 여기서 덮어쓴다.
    _seg = [x for x in _rel.split("/") if x]
    _cand = next((s for s in reversed(_seg)
                  if os.path.exists(os.path.join("og", f"{s}.png"))), None)
    if _cand is None and _seg:
        _cand = {"insights": "insights", "about": "about", "tools": "tools"}.get(_seg[0])
    _img = f"https://the-moment.us/og/{_cand or 'default'}.png"

    # §7 — RSS 는 **선언까지** 해야 한다. 피드(insights/rss.xml)가 있어도
    # <link rel="alternate"> 가 없으면 리더·수집기가 못 찾는다(2026-08-28 전 페이지 누락).
    _tags = (f'<link rel="canonical" href="{_url}">\n'
             f'<link rel="alternate" type="application/rss+xml" '
             f'title="모멘터스 — 인사이트" href="https://the-moment.us/insights/rss.xml">\n'
             f'<meta property="og:url" content="{_url}">\n'
             f'<meta property="og:image" content="{_img}">\n'
             f'<meta name="twitter:image" content="{_img}">')
    _s2 = _re.sub(r'\n?<link rel="canonical"[^>]*>'
                  r'|\n?<link rel="alternate"[^>]*application/rss\+xml[^>]*>'
                  r'|\n?<meta property="og:url"[^>]*>'
                  r'|\n?<meta property="og:image"[^>]*>'
                  r'|\n?<meta name="twitter:image"[^>]*>', "", _s)
    _s2 = _s2.replace('<meta property="og:title"', _tags + '\n<meta property="og:title"', 1)

    # 페이지 유형별 JSON-LD 로 교체. page() 가 넣은 Organization 단일 블록을 덮어쓴다.
    # 🚫 손으로 ld+json 을 박지 마라. 여기서 통째로 갈아끼운다.
    try:
        _ld = _schema_for(_rel, _url, _s2, _img)
        _s3 = _re.sub(r'\n?<script type="application/ld\+json">.*?</script>', "",
                      _s2, flags=_re.S)
        _s3 = _s3.replace("</head>",
                          f'<script type="application/ld+json">{_ld}</script>\n</head>', 1)
        if _s3 != _s2:
            _ld_n += 1
        _s2 = _s3
    except Exception as _e:   # 스키마 하나 때문에 사이트 생성을 죽이지 않는다
        print(f"  ⚠️ JSON-LD 생성 실패({_p}): {_e}")

    if _s2 != _s:
        open(_p, "w", encoding="utf-8").write(_s2)
        _canon_n += 1

print("SITE GENERATED:")
print(f"  index.html, assets/site.css, shell.js, sitemap.xml, robots.txt, llms.txt, _redirects")
print(f"  canonical/og:url/og:image 주입: {_canon_n}개 · JSON-LD 유형별 주입: {_ld_n}개")
print("  tools/: index + " + ", ".join(TOOLS))
print("  products/: " + ", ".join(SPOKES))
print("  insights/: index + " + ", ".join(PORDER) + " + tag/" + ",".join(k for k,_ in STORY_TAGS))
print("  lab/, about/")
