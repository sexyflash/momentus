# -*- coding: utf-8 -*-
"""MOMENTUS 정적 사이트 생성기 v1 — 루트(the-moment.us) 본 사이트.
   assets/bookmarklets/*.txt(원본 소스)를 드래그 버튼 href에 실제 주입한다.
   실행: python3 scripts/gen_site.py (repo 루트에서)"""
import os
import json
import hashlib

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

CSS = """/* MOMENTUS site.css — v1 */
:root{--ink:#0b0c0e;--ink2:#3a4150;--paper:#fff;--soft:#f4f5f7;--soft2:#e9ebee;--gray:#5b6270;--faint:#9aa0a8;--line:#e6e8ec;
--pt:#ff4b26;--ok:#12b76a;--ig:#e1306c;--yt:#ff0033;--pin:#e60023;--coup:#346aff;
--gut:max(20px,calc((100% - 1200px)/2));
--sans:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Helvetica Neue","Segoe UI",sans-serif;
--mono:"SF Mono",ui-monospace,Menlo,monospace;--ease:cubic-bezier(.16,1,.3,1)}
*{box-sizing:border-box}
body{margin:0;word-break:keep-all;overflow-wrap:break-word;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}h1,h2,h3,h4,p{margin:0;font-weight:400}img{display:block;max-width:100%}
.gnb{position:fixed;inset:0 0 auto;z-index:100;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 var(--gut);background:rgba(255,255,255,.85);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
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
.gnb{gap:14px}.gnb .wm{flex:0 0 auto}
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
.tls{padding:0 var(--gut);max-width:1200px;margin:0 auto}
.tls-head{padding:86px 0 34px;display:flex;flex-direction:column;gap:10px}
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
main{padding-top:56px}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--ink);color:#fff;font-size:14px;font-weight:600;padding:12px 22px;border-radius:99px;border:none;cursor:pointer}
.btn:hover{opacity:.87}.btn.lg{font-size:15px;padding:14px 26px}
.btn.ghost{background:none;color:var(--ink);border:1px solid var(--line)}
.btn.drag{border:2px dashed var(--pt);color:var(--pt);background:#fff5f2;cursor:grab;font-weight:800}
.btn.drag:active{cursor:grabbing}
.free{font-family:var(--mono);font-size:11px;font-weight:700;color:#fff;background:var(--ink);padding:3px 9px;border-radius:6px}
.kick{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--gray)}
.kick.pt{color:var(--pt);font-weight:700}
footer.site{border-top:1px solid var(--line);margin-top:clamp(70px,10vh,120px);padding:44px var(--gut);display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:24px;font-size:13px}
@media(max-width:760px){footer.site{grid-template-columns:1fr 1fr}}
footer.site h4{margin:0 0 12px;font-size:11px;color:var(--faint);font-weight:600;text-transform:uppercase;letter-spacing:.06em}
footer.site a{display:block;padding:4px 0;color:var(--gray)}footer.site a:hover{color:var(--ink)}
footer.site .brand .wm{font-size:18px;font-weight:800}footer.site .brand p{margin-top:10px;color:var(--faint);font-size:12px;line-height:1.6}
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
.vd-pair img{width:100%;aspect-ratio:1;object-fit:cover;display:block}

.vd-cta{max-width:var(--vd-w);margin:0 auto;padding:120px 24px;text-align:center}
.vd-cta .btn-buy{display:inline-flex;align-items:center;justify-content:center;
  min-width:280px;height:64px;padding:0 40px;background:#202020;color:#fff;
  font-size:21px;font-weight:700;letter-spacing:-.02em;border-radius:0;transition:background .2s}
.vd-cta .btn-buy:hover{background:#5A5A5A}
.vd-cta .hint{margin-top:20px;font-size:15px;color:#909090;line-height:1.7}

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
.lg-head h1{font-size:clamp(28px,3.4vw,40px);font-weight:700;letter-spacing:-.03em;color:#202020}
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

"""

# CSS 캐시 버스팅 — Cloudflare가 /assets/site.css를 max-age=14400(4시간) 캐시한다.
# 내용이 바뀌면 URL도 바뀌게 해서 즉시 반영시킨다.
CSS_VER = hashlib.md5(CSS.encode("utf-8")).hexdigest()[:8]

def purl(slug):
    """제품 페이지 주소 — 무료 도구는 /tools/, 유료 스포크는 /products/.
       무료 도구를 본 도메인 경로에 두는 이유는 PLATFORM_TOPOLOGY §5(미끼의 유입 권위)."""
    return f"/tools/{slug}/" if slug in TOOLS else f"/products/{slug}/"


def bar_items(active=""):
    """1단 바 항목 = (라벨, href, 부제, 외부여부, 활성여부, 구분선앞).
       active 는 apex 자기 페이지용(서버 렌더). 스포크는 shell.js 가 도메인으로 판정한다.
       ⚠️ 활성 상태를 라벨로 하드코딩하지 않는다(nav-active-no-hardcode)."""
    active = {"j": "story", "a": "about", "p": "tools"}.get(active, active)   # 레거시 코드 호환
    out = []
    for i, s in enumerate(BAR["spokes"]):
        if s.get("hidden"):
            continue
        out.append(dict(label=s["label"], href=s["href"], sub=s.get("sub", ""),
                        ext=bool(s.get("external")), on=False, sep=False))
    for j, l in enumerate(BAR["links"]):
        out.append(dict(label=l["label"], href=l["href"], sub="",
                        ext=False, on=(active == l["key"]), sep=(j == 0 or l["key"] == "story")))
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
    tel="070-8098-7367",
    email="hello.momentus@gmail.com",
    privacy_officer="강형모",
    updated="2026. 07. 14",
)

# 푸터 제품·도구 목록도 매니페스트 파생 — 하드코딩 목록은 2026-07-27 폐기(새 제품 = 한 줄).
_FT_SPOKES = "".join(f'<a href="{purl(s)}">{P[s]["name"]}</a>' for s in SPOKES)
_FT_TOOLS = "".join(f'<a href="{purl(s)}">{P[s]["short"]}</a>' for s in TOOLS)

FOOTER = f"""<footer class="site">
  <div class="brand"><div class="wm">MOMENTUS</div><p>쓸모 있는 것만<br>만듭니다.</p></div>
  <div><h4>제품</h4>{_FT_SPOKES}</div>
  <div><h4>무료 도구</h4>{_FT_TOOLS}</div>
  <div><h4>모멘터스</h4><a href="/log/">로그</a><a href="/about/">소개</a><a href="mailto:{BIZ['email']}">문의하기</a><a href="/legal/terms/">이용약관</a><a href="/legal/privacy/">개인정보처리방침</a><a href="/legal/refund/">환불 규정</a></div>
  <div class="biz">
    <span>{BIZ['name']}</span><span>대표 {BIZ['ceo']}</span><span>사업자등록번호 {BIZ['reg']}</span><span>통신판매업신고 {BIZ['mail_order']}</span>
    <span>{BIZ['addr']}</span><span>{BIZ['tel']}</span><span>{BIZ['email']}</span><span>개인정보보호책임자 {BIZ['privacy_officer']}</span>
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


def page(title, desc, body, active="", extra=""):
    body = _toolfix(body)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="stylesheet" href="/assets/site.css?v={CSS_VER}">
<script type="application/ld+json">{JSONLD}</script>
</head>
<body>
{gnb(active)}
<main>
{body}
</main>
{FOOTER}
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

DRAG_MSG = "클릭이 아니라, 이 버튼을 브라우저 북마크바로 드래그해서 등록하세요. 등록한 뒤 해당 사이트에서 누르면 작동합니다."
DRAG_ATTR = f'onclick="alert(\'{DRAG_MSG}\');return false"'

CATN = {"fast": "생산성", "sell": "커머스", "research": "리서치", "study": "스터디"}

def cta(slug, big=False):
    p = P[slug]
    cls = "btn lg cta-main drag" if (big and p["cta"] == "drag") else ("btn lg cta-main" if big else ("btn drag" if p["cta"] == "drag" else "btn"))
    if p["cta"] == "drag":
        return f'<a class="{cls}" href="{BM[p["bm"]]}" {DRAG_ATTR}>↖ {p["short"]} — 북마크바로 드래그</a>'
    if p["cta"] == "ext":
        return f'<a class="{cls}" href="{p["url"]}" target="_blank" rel="noopener">{p["ctatext"]}</a>'
    return f'<a class="{cls}" href="{p["store"]}" target="_blank" rel="noopener">크롬에 추가 →</a>'

# ---------- assets ----------
os.makedirs("assets", exist_ok=True)
with open("assets/site.css", "w", encoding="utf-8") as f:
    f.write(CSS)

# ---------- shell.js — 스포크(notes·mark·cue…)에 1단 바를 배급 ----------
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
      + "#mmt-bar .in{display:flex;align-items:center;gap:16px;height:100%;"
      +   "padding:0 max(16px,calc((100% - 1200px)/2));overflow-x:auto;scrollbar-width:none}"
      + "#mmt-bar .in::-webkit-scrollbar{display:none}"
      + "#mmt-bar .wm{font-size:13px;font-weight:800;letter-spacing:-.01em;color:#fff;text-decoration:none;flex:0 0 auto}"
      + "#mmt-bar nav{display:flex;align-items:center;gap:4px;flex:0 0 auto}"
      + "#mmt-bar a.it{font-size:13px;font-weight:500;letter-spacing:-.01em;color:var(--mmt-fg);"
      +   "text-decoration:none;padding:5px 9px;border-radius:7px;white-space:nowrap;position:relative}"
      + "#mmt-bar a.it:hover{background:rgba(255,255,255,.1);color:#fff}"
      + "#mmt-bar a.it[aria-current=page]{background:#fff;color:#14161a;font-weight:700}"
      + "#mmt-bar .sep{width:1px;height:13px;background:rgba(255,255,255,.18);flex:0 0 auto;margin:0 5px}"
      + "#mmt-bar i.ext{font-style:normal;font-size:9px;opacity:.55;margin-left:3px;vertical-align:super}"
      + "#mmt-bar a.it[data-sub]::after{content:attr(data-sub);position:absolute;top:calc(100% + 7px);left:50%;"
      +   "transform:translateX(-50%) translateY(-3px);white-space:nowrap;background:#14161a;color:#fff;"
      +   "font-size:12px;font-weight:500;padding:6px 11px;border-radius:8px;opacity:0;visibility:hidden;"
      +   "pointer-events:none;transition:opacity .14s,transform .14s;box-shadow:0 10px 26px -12px rgba(0,0,0,.45)}"
      + "#mmt-bar a.it[data-sub]:hover::after,#mmt-bar a.it[data-sub]:focus-visible::after{"
      +   "opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}"
      + "@media(max-width:820px){#mmt-bar .in{gap:10px}#mmt-bar .sep{display:none}"
      +   "#mmt-bar a.it{padding:5px 7px}#mmt-bar a.it[data-sub]::after{display:none}}"
      + "@media(prefers-reduced-motion:reduce){#mmt-bar a.it[data-sub]::after{transition:none}}";

    var st = document.createElement("style");
    st.setAttribute("data-mmt", "shell");
    st.textContent = css;
    document.head.appendChild(st);

    // 제품이 고정 헤더를 내릴 때 쓸 값 — 제품 CSS 한 줄로 오프셋할 수 있게 노출한다.
    document.documentElement.style.setProperty("--mmt-bar-h", H + "px");

    var host = (location.hostname || "").replace(/^www\\./, "");
    var html = '<div class="in"><a class="wm" href="https://the-moment.us">MOMENTUS</a><nav aria-label="모멘터스">';
    for (var i = 0; i < ITEMS.length; i++) {
      var it = ITEMS[i], a = "";
      if (it.sep) html += '<span class="sep" aria-hidden="true"></span>';
      // ② 활성 표시 = 현재 도메인이 그 항목의 도메인과 같을 때만. 라벨 하드코딩 없음.
      var h = it.href.indexOf("//") > -1 ? it.href.split("//")[1].split("/")[0].replace(/^www\\./, "") : "";
      if (h && h === host) a += ' aria-current="page"';
      if (it.sub) a += ' data-sub="' + it.sub.replace(/"/g, "&quot;") + '"';
      if (it.ext) a += ' target="_blank" rel="noopener"';
      var href = it.href.indexOf("//") > -1 ? it.href : ("https://the-moment.us" + it.href);
      html += '<a class="it" href="' + href + '"' + a + '>' + it.label + (it.ext ? '<i class="ext" aria-hidden="true">↗</i>' : "") + '</a>';
    }
    html += "</nav></div>";

    var bar = document.createElement("div");
    bar.id = "mmt-bar";
    bar.innerHTML = html;
    var put = function () { document.body.insertBefore(bar, document.body.firstChild); };
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

    # feats 3개 → vinylc식 짧은 문단 3덩이
    f = p["feats"]
    note = lambda i: f'<div class="vd-note"><p><b>{f[i][0]}</b></p><p>{f[i][1]}</p></div>'

    # 설치 독 — 항시 노출. 설명서는 접혀 있다가 열림.
    guide = "".join(
        f'<div class="st"><div class="k">STEP {i+1}</div><b>{t}</b><p>{d}</p></div>'
        for i, (t, d) in enumerate(p["how"])
    )
    if p["cta"] == "drag":
        dock_sub = "설치 없음 · 북마크바에 끌어놓기만 하면 끝"
        dock_btn = f'<a class="go" href="{BM[p["bm"]]}" {DRAG_ATTR}>↖ 북마크바로 드래그</a>'
    elif p["cta"] == "ext":
        dock_sub = p["ctasub"]
        dock_btn = f'<a class="go" href="{p["url"]}" target="_blank" rel="noopener">{p["ctatext"]}</a>'
    else:
        dock_sub = "크롬 웹스토어에서 1클릭 · 무료"
        dock_btn = f'<a class="go" href="{p["store"]}" target="_blank" rel="noopener">크롬에 추가 →</a>'

    hint_text = ("클릭 말고, 버튼을 브라우저 북마크바로 드래그해서 등록하세요" if p["cta"] == "drag"
                 else p["ctasub"] if p["cta"] == "ext"
                 else "계정 없음 · 결제 없음 · 1클릭 제거")

    body = f"""<div class="vd">
  <div class="vd-hero">
    <img src="{r(0)}" alt="{p['name']}">
    <div class="cap">
      <div class="kick">{p['tag']}</div>
      <h1>{p['tagline']}</h1>
    </div>
  </div>

  <div class="vd-note"><p>{p['lead']}</p></div>

  <div class="vd-full"><img src="{r(1)}" alt="" loading="lazy"></div>

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

  <div class="vd-full"><img src="{r(11)}" alt="" loading="lazy"></div>

  <div class="vd-cta">
    {cta(slug, big=True)}
    <div class="hint">{hint_text}</div>
  </div>

  <a class="vd-next" href="{purl(nxt)}">
    <img src="{VIMG[(idx * 3 + 5) % len(VIMG)]}" alt="{P[nxt]['name']}" loading="lazy">
    <div class="cap">
      <div class="lbl">Next Product</div>
      <div class="ttl">{P[nxt]['tagline']}</div>
    </div>
  </a>
</div>

<div class="vd-dock">
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
    with open(f"{_dir}/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"{p['name']} — MOMENTUS", p["tagline"] + " 무료.", body,
                      active=("tools" if slug in TOOLS else ""), extra=DOCK_JS))

# (제품 인덱스 페이지 제거 — 홈이 곧 제품 목록이다. 중복 폐지)

POSTS = {
 "loud-ai-contest": dict(cat="실측 · AI", title="AI로 로고 공모에 524번 나가봤습니다",
   sub="당선율을 가른 건 디자인이 아니라 '언제 냈느냐'였습니다. 마감 임박 56건의 당선은 0건이었습니다.",
   date="2026. 07. 13", mins=7, img="jfeat",
   toc=[("s1","524건의 기록"),("s2","언제 내느냐가 5배를 가른다"),("s3","마감 직전은 왜 0건인가"),("s4","그래서 얼마가 남나")],
   body="""<p>디자인 공모 플랫폼에 <b>AI로 로고를 만들어 524건을 출품</b>했습니다. 사람 디자이너들과 같은 판에서 겨뤘고, 평균 당선율은 <b>5.9%</b>였습니다.</p>

<p>흥미로운 건 결과가 아니라 <b>무엇이 당선을 갈랐는가</b>였습니다. 처음엔 당연히 디자인 퀄리티라고 생각했습니다. 아니었습니다.</p>

<h2 id="s1">524건의 기록</h2>
<p>초기 23일 동안 117건을 냈고 3건이 당선됐습니다. 당선율 2.6%. 워크플로우를 고치며 누적 524건까지 갔고, 평균 당선율은 5.9%로 올라갔습니다.</p>
<p>AI로 만드니 <b>양을 늘리는 건 쉬웠습니다.</b> 하루 5건씩 낼 수 있었죠. 그런데 양을 늘려도 당선율은 잘 안 올랐습니다. 뭔가 다른 변수가 있었습니다.</p>

<h2 id="s2">언제 내느냐가 5배를 가른다</h2>
<p>출품 시점으로 데이터를 갈라봤습니다. 결과가 명확했습니다.</p>
<ul>
<li><b>마감 5일 이상 남기고 출품</b> → 당선율 <b>8.3%</b></li>
<li><b>마감 3일 이내 출품</b> → 당선율 <b>1.6%</b></li>
</ul>
<p><b>5배 차이입니다.</b> 카이제곱 검정 결과 p=0.010 — 우연으로 이런 차이가 날 확률은 1%입니다.</p>
<p>같은 AI가, 같은 방식으로 만든 로고인데 <b>언제 냈느냐만으로 당선율이 5배</b> 갈립니다. 디자인이 아니라 타이밍이었습니다.</p>

<h2 id="s3">마감 직전은 왜 0건인가</h2>
<p>가장 충격적인 숫자는 이겁니다. <b>마감 하루 이내(D-0~1)에 낸 56건 중 당선은 0건이었습니다.</b></p>
<p>왜일까요. 추정은 이렇습니다.</p>
<ul>
<li><b>클라이언트는 일찍 마음을 정합니다.</b> 초반 시안 중에서 후보를 좁히고, 그 뒤에 오는 건 거의 안 봅니다.</li>
<li><b>피드백 사이클이 없습니다.</b> 일찍 내면 클라이언트가 "이 방향으로 조금만 더"라고 말해 줍니다. 마감 직전에 내면 고칠 시간이 없습니다.</li>
<li><b>막판에 몰립니다.</b> 다들 마감에 맞춰 던지니 그 안에서 눈에 띌 확률이 떨어집니다.</li>
</ul>
<p>AI를 쓰면 <b>빨리 만들 수 있다는 게 최대 무기</b>인데, 정작 그 무기를 잘못 쓰고 있었던 겁니다. 빨리 만들 수 있으니 <b>빨리 내야</b> 했는데, 우리는 "더 많이 내자"에만 썼습니다.</p>

<h2 id="s4">그래서 얼마가 남나</h2>
<p>돈 얘기를 하면 이렇습니다.</p>
<ul>
<li>당선 1건당 실비 약 <b>8만 5천 원</b> (낙선분 포함한 전체 원가를 당선 건수로 나눈 값)</li>
<li>주력 공모의 상금이 35~40만 원이니 <b>원가율 21~24%, 마진 76~79%</b></li>
</ul>
<p>초기 23일 기준 순수익은 약 67만 원이었습니다. 대단한 돈은 아닙니다. 다만 <b>사람이 하던 일에 AI를 붙여서 실제로 돈이 나온다는 걸 확인</b>했습니다.</p>

<h2>가져가실 것</h2>
<p>공모전이든 제안서든, AI로 양을 늘릴 수 있는 판이라면 이걸 기억하세요.</p>
<ul>
<li><b>양보다 타이밍입니다.</b> 같은 결과물도 언제 내느냐로 5배가 갈립니다.</li>
<li><b>마감 직전은 버리는 카드입니다.</b> 56건 내고 0건 당선이었습니다.</li>
<li><b>AI의 진짜 무기는 "많이"가 아니라 "빨리"입니다.</b> 일찍 내고, 피드백을 받고, 고치세요.</li>
</ul>"""),

 "ai-agent-lessons": dict(cat="가이드 · AI", title="AI 에이전트를 만들며 세 번 버린 것",
   sub="LLM이 판단해야 할 자리에 규칙을 박으면 반드시 사고가 납니다. 세 번 겪고 나서야 알았습니다.",
   date="2026. 07. 11", mins=6, img="jdesk",
   toc=[("s1","첫 번째: 중단 명령"),("s2","두 번째: 위임 차단"),("s3","세 번째: 자동 분해"),("s4","규칙이 안 되는 이유")],
   body="""<p>제품을 만드는 AI 팀을 슬랙에 두고 있습니다. 이 팀이 코드를 쓰고, 버그를 찾고, 자기 코드를 고쳐서 배포합니다.</p>
<p>만들면서 <b>같은 실수를 세 번</b> 했습니다. 매번 다른 얼굴로 왔지만 병은 하나였습니다. <b>LLM이 판단해야 하는 자리에 규칙(키워드·정규식)을 박은 것</b>입니다.</p>

<h2 id="s1">첫 번째: 중단 명령</h2>
<p>작업을 멈추라는 지시를 감지하려고 "그만 / 멈춰 / 하지마 / stop"을 정규식으로 잡았습니다.</p>
<p>사고가 났습니다. <b>"이거 어때?"</b> 같은 평범한 질문이 오탐에 걸려 <b>진행 중이던 작업을 죽였습니다.</b> 패치를 7번 쌓다가 결국 전부 버리고 LLM 판단으로 넘겼습니다.</p>

<h2 id="s2">두 번째: 위임 차단</h2>
<p>"분석만 하고 실행하지 마"를 구분하려고 동사 목록을 만들었습니다. 분석 동사와 실행 동사를 나눠서 매칭했습니다.</p>
<p>이번엔 <b>"맞아?"</b> 같은 일반 질문이 분석 의도로 잡혔습니다. 그리고 차단 메시지에 내부 용어가 그대로 실려 사용자에게 노출됐습니다. 또 버렸습니다.</p>

<h2 id="s3">세 번째: 자동 분해</h2>
<p>여기서 <b>"이번엔 다르다"고 확신했습니다.</b> 키워드가 아니라 결정론적 신호를 쓰기로 했으니까요 — 글자 수 250자 이상, 번호 목록 3개 이상, 특정 단어 포함. 규칙이 아니라 수치니까 안전하다고 봤습니다.</p>
<p>아니었습니다. 사용자가 <b>채용 공고를 붙여넣자</b> 그 안의 "1. 2. 3." 번호와 "기획"이라는 단어가 조건을 채웠습니다. 단순한 글쓰기 요청이 중장비 분해 작업으로 오발동했고, 결과는 빈손이었습니다.</p>
<p>여기서 진짜 원인을 알았습니다. <b>사용자가 붙여넣는 자료가 신호를 오염시킵니다.</b> 우리는 "사용자의 의도"를 센 게 아니라 "붙여넣은 자료"를 센 거였습니다.</p>

<h2 id="s4">규칙이 안 되는 이유</h2>
<p>세 번 겪고 정리한 결론입니다.</p>
<ul>
<li><b>자연어는 열거할 수 없습니다.</b> "확인할까요?" "되는 거죠?" "맞나요?" — 사람이 어떻게 말할지 미리 다 적을 수 없습니다.</li>
<li><b>부정문이 뒤집습니다.</b> "수정하지 마"라는 문장 안에 "수정"이 들어 있습니다.</li>
<li><b>붙여넣은 자료가 신호를 오염시킵니다.</b> 이게 제일 무섭습니다. 결정론적 수치도 안전하지 않습니다.</li>
</ul>

<h2>그래서 어떻게 하나</h2>
<p>지금은 이 기준으로 나눕니다.</p>
<ul>
<li><b>순수하게 기계적인 판단</b>(경로가 존재하나, 깊이 제한, DB 잠금) → 규칙으로 해도 됩니다.</li>
<li><b>자연어의 의미를 판단</b> → 무조건 LLM에게 맡깁니다. 규칙은 프롬프트에 넣습니다.</li>
<li><b>예외: 걸려도 손해가 0인 자리</b> → 규칙 OK. 예를 들어 "○○씨 있어요?" 같은 순수 호출을 정규식으로 잡아 인사만 하는 건, 틀려도 인사 한 마디라 무해합니다.</li>
</ul>
<p>판별 기준은 하나입니다. <b>오발동했을 때 파괴적인가.</b> 작업을 죽이거나, 차단하거나, 빈손으로 만든다면 — 거기엔 규칙을 넣지 마세요.</p>"""),

 "why-free": dict(cat="관점", title="왜 공짜로 푸는가",
   sub="돈을 받을 이유가 없는 건 그냥 드립니다. 대신 받을 이유가 있는 걸 만듭니다.",
   date="2026. 07. 05", mins=4, img="jfree",
   toc=[("s1","만든 이유"),("s2","공짜로 푸는 기준"),("s3","그럼 뭘로 먹고사나")],
   body="""<p>여기 있는 브라우저 도구 여섯 개는 전부 무료입니다. 로그인도, 결제도, 이메일 수집도 없습니다. 자주 받는 질문이라 이유를 적어둡니다.</p>

<h2 id="s1">만든 이유</h2>
<p>전부 <b>제가 쓰려고 만들었습니다.</b> 쿠팡에서 소싱하다 탭을 열두 개씩 여는 게 지겨워서 퀵팡을 만들었고, 인스타 레퍼런스를 감으로 찾는 게 못미더워서 좋아요순 정렬을 만들었습니다.</p>
<p>내 불편에서 시작한 게 아니면 대체로 실패했습니다. "남들이 필요할 것 같아서" 만든 건 결국 저부터 안 쓰게 됩니다.</p>

<h2 id="s2">공짜로 푸는 기준</h2>
<p>기준은 단순합니다. <b>돈을 받을 이유가 있느냐.</b></p>
<ul>
<li><b>브라우저 도구</b> — 만드는 데 며칠, 유지비 0원. 서버도 안 씁니다. 여기서 돈을 받을 이유가 없습니다.</li>
<li><b>상품 사진·로고·플래너</b> — 만들 때마다 원가가 듭니다. GPU를 돌리고, 시안을 그리고, 사람이 다듬습니다. 여기선 받습니다.</li>
</ul>
<p>무료 도구를 유료로 바꿀 계획은 없습니다. 원가가 0인 건 계속 0원입니다.</p>

<h2 id="s3">그럼 뭘로 먹고사나</h2>
<p>솔직히 아직 대단한 답을 못 찾았습니다. 어떤 달은 만 원, 어떤 달은 이만 원입니다.</p>
<p>다만 확실한 건, <b>무료 도구가 우리 실력의 증명</b>이라는 것입니다. 쿠팡 재고를 그 자리에서 보여주는 도구를 만 명이 쓴다면, 그 사람들이 상품 사진이 필요할 때 우리를 떠올릴 겁니다.</p>
<p>파는 걸 먼저 들이밀지 않습니다. 쓸모 있는 걸 먼저 드리고, 필요할 때 찾아오시면 됩니다.</p>"""),
}

PORDER = ["loud-ai-contest", "ai-agent-lessons", "why-free"]

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

for i, slug in enumerate(PORDER):
    ps = POSTS[slug]
    rel = [x for x in PORDER if x != slug][:3]
    relh = "".join(
        f'<a href="/log/{x}/"><b>{POSTS[x]["title"]}</b><p>{POSTS[x]["sub"]}</p>'
        f'<div class="more">더 읽기 →</div></a>' for x in rel)
    body = f"""<article class="an-post">
  <div class="top">
    <div class="cat">{ps['cat']}</div>
    <h1>{ps['title']}</h1>
    <div class="date">{ps['date']} · {ps['mins']}분 읽기</div>
  </div>
  <div class="cover th g{(i % 3) + 1}"></div>
</article>

<div class="an-body">
{ps['body']}
</div>

<div class="an-share">
  <a href="https://twitter.com/intent/tweet?url=https://the-moment.us/log/{slug}/" target="_blank" rel="noopener">X에 공유</a>
  <a href="/log/">← 블로그 전체</a>
</div>

<section class="an-rel">
  <h2>이어서 읽기</h2>
  <div class="g">{relh}</div>
</section>"""
    os.makedirs(f"log/{slug}", exist_ok=True)
    with open(f"log/{slug}/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"{ps['title']} — MOMENTUS 로그", ps["sub"], body, active="j"))

# 로그 = 영상(유튜브) + 글. 같은 시간축, 같은 카드.
entries = []
for i, x in enumerate(PORDER):
    p0 = POSTS[x]
    entries.append(dict(kind="post", slug=x, title=p0["title"], date=p0["date"],
                        cat=p0["cat"], desc=p0["sub"], grad=f"g{(i % 3) + 1}"))
for v in VIDEOS:
    entries.append(dict(kind="video", url=v["url"], title=v["title"], date=v["date"],
                        cat="영상", desc=v["desc"], thumb=v["thumb"]))
entries.sort(key=lambda e: e["date"], reverse=True)

cats = []
for e in entries:
    c0 = e["cat"].split("·")[0].strip()
    if c0 not in cats:
        cats.append(c0)
tabs = '<button type="button" data-f="all" aria-pressed="true">전체</button>' + "".join(
    f'<button type="button" data-f="{c0}" aria-pressed="false">{c0}</button>' for c0 in cats)

def card(e):
    c0 = e["cat"].split("·")[0].strip()
    if e["kind"] == "video":
        th = f'<div class="th vid"><img src="{e["thumb"]}" alt="" loading="lazy"><span class="play"></span></div>'
        href, ext = e["url"], ' target="_blank" rel="noopener"'
    else:
        th = f'<div class="th {e["grad"]}"></div>'
        href, ext = f'/log/{e["slug"]}/', ''
    return (f'<div class="an-card" data-cat="{c0}"><a href="{href}"{ext}>{th}'
            f'<h3>{e["title"]}</h3>'
            f'<div class="m"><span class="cat">{e["cat"]}</span><span>{e["date"]}</span></div>'
            f'<p>{e["desc"]}</p></a></div>')

cards = "".join(card(e) for e in entries)
jbody = f"""<div class="an">
  <div class="an-lhead">
    <h1>로그</h1>
    <p class="an-lsub">만든 것, 안 된 것, 배운 것. 전부 남깁니다.<br>
      얘기는 <a href="{YT_URL}" target="_blank" rel="noopener">유튜브 댓글</a>에서 합니다 — 거기서 다음에 뭘 만들지 정합니다.</p>
    <div class="an-tabs" id="bltabs">{tabs}</div>
  </div>
  <div class="an-grid" id="blgrid">{cards}</div>
  <p class="an-empty" id="blempty" hidden>해당하는 글이 없어요.</p>
</div>"""

BLOG_JS = """<script>
(function(){
  var tabs=document.getElementById('bltabs'), grid=document.getElementById('blgrid'),
      empty=document.getElementById('blempty');
  if(!tabs||!grid) return;
  var items=[].slice.call(grid.querySelectorAll('.an-card'));
  tabs.addEventListener('click', function(e){
    var btn=e.target.closest('button[data-f]'); if(!btn) return;
    var f=btn.dataset.f, shown=0;
    [].slice.call(tabs.querySelectorAll('button')).forEach(function(b){
      b.setAttribute('aria-pressed', String(b===btn));
    });
    items.forEach(function(it){
      var ok=(f==='all')||it.dataset.cat===f;
      it.hidden=!ok; if(ok) shown++;
    });
    empty.hidden = shown>0;
  });
})();
</script>"""
with open("log/index.html", "w", encoding="utf-8") as f:
    f.write(page("로그 — MOMENTUS", "AI로 제품을 만들며 알게 된 것들. 실측 데이터와 실패 기록.", jbody, active="j", extra=BLOG_JS))

# (만들어드려요 폐기 — 요청은 유튜브 댓글에서 받는다)

# ---------- about ----------
about_body = """<div class="an-ahero">
  <h1>AI가 사람을 이기는 지점을 찾습니다.</h1>
  <p>모멘터스는 AI로 제품을 만드는 방법을 실험하는 스튜디오입니다. 매일 만들고, 직접 쓰고, 알게 된 걸 공개합니다.</p>
  <a class="btn" href="/">만든 것들 보기 →</a>
</div>

<section class="an-sec">
  <div class="an-row">
    <div class="an-lbl">
      <h2>하려는 일</h2>
      <p>AI가 사람보다 잘하는 일과 여전히 못하는 일이 매달 바뀝니다. 그 경계를 직접 만들어 보며 확인합니다.</p>
    </div>
    <div class="an-two">
      <div>
        <h3>경계를 실측합니다</h3>
        <p>AI가 어디까지 하는지는 써봐야 압니다. 로고 공모에 AI로 참여해 사람 디자이너들과 같은 판에서 겨루고, 결과를 기록합니다. 이기기도 하고 집니다.</p>
      </div>
      <div>
        <h3>스스로 고치는 팀을 만듭니다</h3>
        <p>슬랙에 사는 AI 팀이 제품을 만들고, 버그를 찾고, 자기 코드를 고쳐서 배포합니다. 사람이 하던 일을 어디까지 넘길 수 있는지 실험합니다.</p>
      </div>
      <div>
        <h3>먼저 씁니다</h3>
        <p>여기 있는 제품은 전부 우리가 먼저 쓰려고 만든 것입니다. 매일 안 쓰게 되면 버립니다. 살아남은 것만 남아 있습니다.</p>
      </div>
      <div>
        <h3>배운 걸 공개합니다</h3>
        <p>뭐가 됐고 뭐가 안 됐는지 블로그에 씁니다. 같은 시도를 하는 사람이 같은 벽에 부딪히지 않게.</p>
      </div>
    </div>
  </div>
</section>

<section class="an-sec">
  <div class="an-row">
    <div class="an-lbl">
      <h2>만들 때 지키는 것</h2>
      <p>제품을 만들지 말지, 남길지 버릴지를 정하는 기준입니다.</p>
    </div>
    <div class="an-num">
      <div>
        <div class="n">01</div>
        <h3>내가 안 쓰면 만들지 않는다.</h3>
        <p>남이 필요할 것 같아서 만든 건 전부 실패했습니다. 내 불편에서 시작한 것만 살아남았습니다.</p>
      </div>
      <div>
        <div class="n">02</div>
        <h3>설명서가 필요하면 진 것이다.</h3>
        <p>쓰는 법을 설명해야 하는 도구는 안 씁니다. 눌러보면 알아야 합니다.</p>
      </div>
      <div>
        <div class="n">03</div>
        <h3>공짜로 풀 수 있으면 푼다.</h3>
        <p>돈을 받을 이유가 없는 건 그냥 드립니다. 브라우저 도구가 그렇습니다.</p>
      </div>
      <div>
        <div class="n">04</div>
        <h3>안 쓰이면 버린다.</h3>
        <p>애착으로 남긴 제품이 사이트를 무겁게 만듭니다. 안 쓰면 지웁니다.</p>
      </div>
      <div>
        <div class="n">05</div>
        <h3>실패도 기록한다.</h3>
        <p>안 된 이유가 다음 제품의 재료입니다. 지우지 않습니다.</p>
      </div>
      <div>
        <div class="n">06</div>
        <h3>멈추지 않는다.</h3>
        <p>어떤 달은 만 원, 어떤 달은 이만 원. 대단하지 않지만 한 번도 쉬지 않았습니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="an-sec">
  <div class="an-row">
    <div class="an-lbl">
      <h2>만드는 사람</h2>
      <p>디지털 제품을 오래 만들어 온 사람들입니다.</p>
    </div>
    <div class="an-two">
      <div>
        <h3>남의 제품을 20년 만들었습니다</h3>
        <p>이모션글로벌, NC소프트 재팬, 아이플래테아, 네오랩컨버전스, 엔카닷컴. 이름을 다 아실 필요는 없습니다. 그 시간에 배운 걸로 이제 우리 걸 만듭니다.</p>
      </div>
      <div>
        <h3>둘이서 합니다</h3>
        <p>제품을 만드는 사람과, 그게 굴러가게 하는 사람. 둘 다 있어야 회사가 됩니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="an-cta">
  <h2>대단한 걸 만들고 있진 않습니다.<br>다만 매일 만듭니다.</h2>
  <p class="sub">만드는 과정을 전부 공개합니다. 뭐가 됐고 뭐가 안 됐는지, 숫자까지.<br>지켜봐 주시겠어요?</p>
  <div class="an-cta-btns">
    <a class="btn" href="{YT_URL}" target="_blank" rel="noopener">유튜브에서 지켜보기 →</a>
    <a class="btn ghost" href="/log/">지금까지 한 것 보기</a>
  </div>
  <p class="note">뭘 만들면 좋을지도 거기서 말해 주세요. 댓글이 다음 제품이 됩니다.</p>
</section>"""
os.makedirs("about", exist_ok=True)
with open("about/index.html", "w", encoding="utf-8") as f:
    f.write(page("소개 — MOMENTUS", "AI로 제품을 만드는 방법을 실험하는 스튜디오. 매일 만들고, 직접 쓰고, 알게 된 걸 공개합니다.", about_body, active="a"))

# ---------- landing (root index.html) ----------
land_body = """<div class="vc">
  <div class="vc-head">
    <h1>쓸모 있는 것만 만듭니다.</h1>
    <p>필요해서 만들었고, 매일 씁니다. 필요한 것만 골라 쓰세요.</p>
  </div>

  <div class="vc-sort" id="vcsort">
    <button type="button" data-f="all" aria-pressed="true">전체</button>
    <button type="button" data-f="sell" aria-pressed="false">파는 사람</button>
    <button type="button" data-f="brand" aria-pressed="false">브랜드</button>
    <button type="button" data-f="me" aria-pressed="false">나를 위해</button>
  </div>

  <div class="vc-grid" id="vcgrid">
    <article class="vc-item" data-cat="sell">
      <a href="/products/quickpang/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000060/vinylc_tumbler.jpg" alt="들어가 보지 않아도 옵션과 재고가 보입니다"></div>
        <h3>들어가 보지 않아도 옵션과 재고가 보입니다</h3>
        <div class="cat">Coupang</div>
      </a>
    </article>
    <article class="vc-item" data-cat="sell">
      <a href="/products/insta-rank/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000072/VinylC_life.jpg" alt="이 계정, 대체 뭐가 제일 잘 됐나"></div>
        <h3>이 계정, 대체 뭐가 제일 잘 됐나</h3>
        <div class="cat">Instagram</div>
      </a>
    </article>
    <article class="vc-item" data-cat="sell">
      <a href="/products/youtube-rank/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000069/VinylC_010.jpg" alt="이 채널의 대표작이 뭔지, 5초 만에"></div>
        <h3>이 채널의 대표작이 뭔지, 5초 만에</h3>
        <div class="cat">YouTube</div>
      </a>
    </article>
    <article class="vc-item big" data-cat="sell">
      <a href="/products/heyreci/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000007/01_thumb.jpg" alt="폰으로 찍은 사진이 30초 만에 판매용 컷이 됩니다" loading="lazy"></div>
        <h3>폰으로 찍은 사진이 30초 만에 판매용 컷이 됩니다</h3>
        <div class="cat">Product Photo</div>
      </a>
    </article>
    <article class="vc-item" data-cat="brand">
      <a href="/products/pinterest-grab/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000063/vinylc_ecobag_01.jpg" alt="저해상 썸네일 말고, 원본을 가져옵니다" loading="lazy"></div>
        <h3>저해상 썸네일 말고, 원본을 가져옵니다</h3>
        <div class="cat">Pinterest</div>
      </a>
    </article>
    <article class="vc-item" data-cat="me">
      <a href="/products/chatpage/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000030/07_thumb.jpg" alt="1시간 42분짜리를 끝까지 볼 필요는 없습니다" loading="lazy"></div>
        <h3>1시간 42분짜리를 끝까지 볼 필요는 없습니다</h3>
        <div class="cat">AI Summary</div>
      </a>
    </article>
    <article class="vc-item" data-cat="me">
      <a href="/products/her/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000033/02_thumb_pc.jpg" alt="손이 못 따라갈 만큼 생각이 빠를 때, 그냥 말하면 됩니다" loading="lazy"></div>
        <h3>손이 못 따라갈 만큼 생각이 빠를 때, 그냥 말하면 됩니다</h3>
        <div class="cat">Voice</div>
      </a>
    </article>
    <article class="vc-item big" data-cat="brand">
      <a href="/products/mark/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000009/03_thumb.jpg" alt="내 업종 로고를 먼저 보고 고릅니다" loading="lazy"></div>
        <h3>내 업종 로고를 먼저 보고 고릅니다</h3>
        <div class="cat">Logo</div>
      </a>
    </article>
    <article class="vc-item" data-cat="me">
      <a href="/products/theplan/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000036/03_thumb.jpg" alt="내 손에 맞는 플래너를 골라서 씁니다" loading="lazy"></div>
        <h3>내 손에 맞는 플래너를 골라서 씁니다</h3>
        <div class="cat">Planner</div>
      </a>
    </article>
    <article class="vc-item" data-cat="me">
      <a href="/products/cue/">
        <div class="vc-thumb"><img src="https://www.vinylc.com/upload/goods/GD00000039/vinylc_bag_00.jpg" alt="면접장에서 얼어붙지 않으려면 소리 내어 연습해야 합니다" loading="lazy"></div>
        <h3>면접장에서 얼어붙지 않으려면 소리 내어 연습해야 합니다</h3>
        <div class="cat">Interview</div>
      </a>
    </article>
  </div>
  <p class="vc-empty" id="vcempty" hidden>해당하는 제품이 없어요.</p>
</div>"""

LAND_JS = """<script>
(function(){
  var sort=document.getElementById('vcsort'), grid=document.getElementById('vcgrid'),
      empty=document.getElementById('vcempty');
  if(!sort||!grid) return;
  var items=[].slice.call(grid.querySelectorAll('.vc-item'));
  sort.addEventListener('click', function(e){
    var btn=e.target.closest('button[data-f]'); if(!btn) return;
    var f=btn.dataset.f, shown=0;
    [].slice.call(sort.querySelectorAll('button')).forEach(function(b){
      b.setAttribute('aria-pressed', String(b===btn));
    });
    items.forEach(function(it){
      var ok = (f==='all') || it.dataset.cat===f;
      it.hidden = !ok;
      if(ok) shown++;
    });
    empty.hidden = shown>0;
  });
})();
</script>"""


with open("index.html", "w", encoding="utf-8") as f:
    f.write(page("MOMENTUS — 일하는 사람을 위한 도구를 만듭니다", "상품 사진, 로고, 플래너, 면접 연습. 매일 쓰는 브라우저 도구까지.", land_body, active="", extra=LAND_JS))

# ---------- 법적 페이지 (약관·개인정보·환불) ----------
LEGAL_CSS_WRAP = '<div class="lg">'

BIZ_TABLE = f"""<table class="lg-biz">
<tr><th>상호</th><td>{BIZ['name']}</td></tr>
<tr><th>대표자</th><td>{BIZ['ceo']}</td></tr>
<tr><th>사업자등록번호</th><td>{BIZ['reg']}</td></tr>
<tr><th>통신판매업신고</th><td>{BIZ['mail_order']}</td></tr>
<tr><th>사업장 주소</th><td>{BIZ['addr']}</td></tr>
<tr><th>전화</th><td>{BIZ['tel']}</td></tr>
<tr><th>이메일</th><td><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></td></tr>
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
    <p><a href="mailto:{BIZ['email']}">{BIZ['email']}</a> · {BIZ['tel']}</p>

    <h2>5. 사업자 정보</h2>
    {BIZ_TABLE}
  </div>
</div>"""

for slug, title, body, desc in [
    ("privacy", "개인정보처리방침", PRIVACY, "모멘터스는 개인정보를 수집하지 않습니다. 브라우저 도구는 모든 처리를 기기 안에서 수행합니다."),
    ("terms", "이용약관", TERMS, "모멘터스 무료 브라우저 도구 및 유료 제품 이용약관."),
    ("refund", "환불 규정", REFUND, "모멘터스 유료 제품의 환불 규정 및 청약철회 안내."),
]:
    os.makedirs(f"legal/{slug}", exist_ok=True)
    with open(f"legal/{slug}/index.html", "w", encoding="utf-8") as fh:
        fh.write(page(f"{title} — MOMENTUS", desc, body, active=""))

# 크롬 웹스토어가 참조하는 기존 URL 유지 (내용만 교체)
os.makedirs("apps", exist_ok=True)
with open("apps/privacy-policy.html", "w", encoding="utf-8") as fh:
    fh.write(page("개인정보처리방침 — MOMENTUS", "모멘터스는 개인정보를 수집하지 않습니다.", PRIVACY, active=""))
with open("apps/legal.html", "w", encoding="utf-8") as fh:
    fh.write(page("이용약관 — MOMENTUS", "모멘터스 이용약관.", TERMS, active=""))

# ---------- /tools/ 허브 (1단 바의 '무료 도구' 착지점) ----------
_TYPEN = {"bookmarklet": "북마크릿", "extension": "크롬 확장"}
_tls_rows = "".join(
    f'''<a class="tls-row" href="{purl(s)}">
    <div class="ic" aria-hidden="true">{P[s]["icon"]}</div>
    <div class="bd"><div class="nm">{P[s]["short"]}</div><div class="ds">{P[s]["tagline"]}</div></div>
    <div class="mt">{_TYPEN.get(P[s]["type"], P[s]["type"])} · 무료</div>
  </a>''' for s in TOOLS)
tools_body = f"""<div class="tls">
  <div class="tls-head">
    <div class="k">TOOLS</div>
    <h1>설치 없이, 지금 되는 도구</h1>
    <p>전부 무료입니다. 북마크바에 끌어놓거나 크롬에 추가하면 끝. 회원가입도, 결제도 없습니다.</p>
  </div>
  <div class="tls-list">{_tls_rows}</div>
</div>"""
os.makedirs("tools", exist_ok=True)
with open("tools/index.html", "w", encoding="utf-8") as f:
    f.write(page("무료 도구 — MOMENTUS", "설치 없이 바로 쓰는 무료 브라우저 도구. 쿠팡 옵션·재고, 인스타·유튜브 인기순 정렬, 핀터레스트 원본 추출, 유튜브 AI 요약, 음성 입력.", tools_body, active="tools"))

# ---------- 리다이렉트 — 옮긴 무료 도구 주소 회수 ----------
#   무료 도구가 /products/<slug>/ → /tools/<slug>/ 로 이동(2026-07-27). 기존 링크·검색 결과 보존.
with open("_redirects", "w", encoding="utf-8") as f:
    f.write("# 생성물(scripts/gen_site.py). 손으로 고치지 말 것.\n")
    for s in TOOLS:
        f.write(f"/products/{s}/* /tools/{s}/ 301\n")
        f.write(f"/products/{s} /tools/{s}/ 301\n")

# ---------- sitemap ----------
urls = ["", "log/", "about/", "tools/", "legal/privacy/", "legal/terms/", "legal/refund/"] \
    + [purl(s).lstrip("/") for s in ORDER] + [f"log/{s}/" for s in PORDER]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f"  <url><loc>https://the-moment.us/{u}</loc></url>\n"
sm += "</urlset>\n"
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sm)

print("SITE GENERATED:")
print("  index.html, assets/site.css, shell.js, sitemap.xml, _redirects")
print("  tools/: index + " + ", ".join(TOOLS))
print("  products/: " + ", ".join(SPOKES))
print("  log/: index + " + ", ".join(PORDER))
print("  lab/, about/")
