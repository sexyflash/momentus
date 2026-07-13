# -*- coding: utf-8 -*-
"""MOMENTUS 정적 사이트 생성기 v1 — 루트(the-moment.us) 본 사이트.
   assets/bookmarklets/*.txt(원본 소스)를 드래그 버튼 href에 실제 주입한다.
   실행: python3 scripts/gen_site.py (repo 루트에서)"""
import os

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

BM = {}
for k in ["insta-rank", "youtube-rank", "pinterest-grab", "quickpang"]:
    with open(f"assets/bookmarklets/{k}.txt", encoding="utf-8") as f:
        raw = f.read().strip()
    BM[k] = raw.replace("&", "&amp;").replace('"', "&quot;")

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
.cat{padding:clamp(56px,9vh,110px) var(--gut) 0}
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
.rn-hero{padding:calc(56px + clamp(88px,15vh,190px)) var(--gut) clamp(56px,8vh,96px)}
.rn-hero h1{font-size:clamp(34px,5.6vw,74px);font-weight:700;letter-spacing:-.03em;line-height:1.16;max-width:18ch}
.rn-hero .sub{margin-top:30px;font-size:clamp(16px,1.4vw,19px);color:var(--gray);max-width:52ch;line-height:1.75}
.rn-meta{display:flex;justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;
  margin-top:clamp(56px,8vh,100px);padding-top:18px;border-top:1px solid var(--ink);
  font-family:var(--mono);font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);line-height:1.7}
.rn-sell{padding:0 var(--gut);display:flex;flex-direction:column;gap:clamp(84px,13vh,170px)}
.rn-row{display:grid;gap:clamp(28px,3.4vw,56px)}
.rn-row.big{grid-template-columns:1.4fr 1fr;align-items:end}
.rn-row.big.rev{grid-template-columns:1fr 1.4fr}
.rn-row.two{grid-template-columns:1fr 1fr}
.rn-item{display:flex;flex-direction:column;gap:26px}
.rn-item.side{justify-content:flex-end;padding-bottom:6px}
.rn-shot{border-radius:12px;overflow:hidden;border:1px solid var(--line);background:var(--soft);
  transition:transform .4s var(--ease),box-shadow .4s var(--ease)}
.rn-shot img{width:100%;height:100%;object-fit:cover;aspect-ratio:16/10}
.rn-shot.tall img{aspect-ratio:4/3}
.rn-item:hover .rn-shot{transform:translateY(-4px);box-shadow:0 22px 44px -18px rgba(11,12,14,.16)}
.rn-item:hover h3{color:var(--rn-blue)}
.rn-cap .kick{font-family:var(--mono);font-size:13px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--faint);line-height:1.7}
.rn-cap h3{margin-top:18px;font-size:clamp(21px,2.2vw,31px);font-weight:700;letter-spacing:-.03em;
  line-height:1.58;max-width:22ch}
.rn-cap p{margin-top:16px;font-size:15.5px;color:var(--gray);max-width:34ch;line-height:1.78}
.rn-go{display:inline-flex;align-items:center;gap:7px;margin-top:26px;transition:gap .25s var(--ease);
  font-family:var(--mono);font-size:13px;letter-spacing:.06em;color:var(--rn-blue);font-weight:600}
.rn-item:hover .rn-go{gap:12px}
.rn-free{margin-top:clamp(110px,17vh,210px);padding:clamp(60px,9vh,104px) var(--gut) 0;border-top:1px solid var(--line)}
.rn-free .kick{font-family:var(--mono);font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);line-height:1.7}
.rn-free h2{margin-top:18px;font-size:clamp(25px,3vw,40px);font-weight:700;letter-spacing:-.03em;line-height:1.44;max-width:22ch}
.rn-free .lead{margin-top:20px;font-size:16px;color:var(--gray);max-width:50ch;line-height:1.78}
.rn-tools{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:clamp(48px,6vh,72px)}
.rn-tool{border:1px solid var(--line);border-radius:12px;padding:24px 24px 20px;display:flex;flex-direction:column;gap:12px;
  transition:border-color .2s,transform .2s var(--ease)}
.rn-tool:hover{border-color:var(--ink);transform:translateY(-2px)}
.rn-tool .tn{font-size:17px;font-weight:600;letter-spacing:-.02em;line-height:1.5}
.rn-tool .td{font-size:14.5px;color:var(--gray);line-height:1.72}
.rn-bridge{margin-top:auto;padding-top:16px;border-top:1px dashed var(--line);
  font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--rn-blue);line-height:1.6}
.rn-bridge.plain{color:var(--faint)}
.rn-free .cta-dark{margin-top:clamp(72px,10vh,120px)}
@media(max-width:880px){
  .rn-row.big,.rn-row.big.rev,.rn-row.two,.rn-tools{grid-template-columns:1fr}
  .rn-item.side{padding-bottom:0}
}
"""

def gnb(active=""):
    def on(k):
        return " on" if active == k else ""
    return f"""<header class="gnb">
  <a class="wm" href="/">MOMENTUS</a>
  <nav class="lk">
    <div class="hasdrop"><a href="/products/" class="{on('p').strip()}">제품 ▾</a><div class="drop">
      <a href="/products/">전체</a><a href="/products/?f=new">새로 나온</a><a href="/products/?f=fast">일 빨리 끝내기</a><a href="/products/?f=sell">파는 사람 도구</a><a href="/products/?f=research">콘텐츠·리서치</a><a href="/products/?f=study">배우고 정리</a>
    </div></div>
    <a href="/journal/" class="{on('j').strip()}">저널</a>
    <a href="/lab/" class="hidem{on('l')}">만들어드려요</a>
    <a href="/about/" class="hidem{on('a')}">소개</a>
  </nav>
</header>"""

FOOTER = """<footer class="site">
  <div class="brand"><div class="wm">MOMENTUS</div><p>일하는 사람을 위한<br>도구를 만듭니다.</p></div>
  <div><h4>파는 것</h4><a href="https://heyreci.com" target="_blank" rel="noopener">heyreci — 상품 사진 ↗</a><a href="https://mark.the-moment.us" target="_blank" rel="noopener">Mark — 로고 ↗</a><a href="https://planner.the-moment.us" target="_blank" rel="noopener">THE PLAN — 플래너 ↗</a><a href="https://cue.the-moment.us" target="_blank" rel="noopener">Cue — 면접 연습 ↗</a></div>
  <div><h4>주는 것</h4><a href="/products/">브라우저 도구 6종</a><a href="/lab/">만들어드려요</a><a href="/journal/">저널</a><a href="/about/">소개</a></div>
  <div><h4>문의</h4><a href="mailto:hello@the-moment.us">hello@the-moment.us</a><a href="/apps/legal.html">이용약관</a><a href="/apps/privacy-policy.html">개인정보처리방침</a></div>
  <div class="legal"><span>© 2026 모멘터스</span><span>the-moment.us</span></div>
</footer>"""

def page(title, desc, body, active="", extra=""):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
{gnb(active)}
<main>
{body}
</main>
{FOOTER}
{extra}</body>
</html>"""

DRAG_MSG = "클릭이 아니라, 이 버튼을 브라우저 북마크바로 드래그해서 등록하세요. 등록한 뒤 해당 사이트에서 누르면 작동합니다."
DRAG_ATTR = f'onclick="alert(\'{DRAG_MSG}\');return false"'

P = {
 "her": dict(name="her · 음성 입력", short="her", cat="new fast", color="var(--ok)", icon="◉",
   tag="생산성 · 크롬 확장 · NEW", tagline="타이핑 대신, 말로.",
   lead="<b>어디서든 ⌘⇧R 하나면 말이 글이 됩니다.</b> ChatGPT·Claude·Gemini·Notion — 모든 입력창에서. 음성 처리는 전부 당신 기기 안에서만.",
   feats=[("100개 이상 언어","한국어부터 영어·일본어까지, 말하는 대로 즉시 텍스트로."),
          ("모든 입력창에서","따로 앱을 켤 필요 없이, 쓰던 사이트의 입력창 안에서 바로. Perplexity 같은 까다로운 에디터도 대응."),
          ("기기 안에서만 처리","녹음이 서버로 나가지 않습니다. 프라이버시 100%. 끝나면 클립보드 자동 복사.")],
   spec=[("종류","크롬 확장"),("어디서","모든 웹 입력창"),("단축키","⌘⇧R / Ctrl⇧R"),("언어","100+ (한국어)"),("가격","무료"),("버전","v1.0.9")],
   how=[("크롬에 추가","크롬 웹스토어에서 her 설치."),("입력창에서 ⌘⇧R","아무 사이트 입력창에 커서를 두고 단축키."),("말하면 끝","말하는 대로 글이 됩니다. 클립보드에도 자동 복사.")],
   cta="store", store="https://chromewebstore.google.com/"),
 "insta-rank": dict(name="인스타 인기순 정렬", short="인스타 인기순 정렬", cat="research", color="var(--ig)", icon="◲",
   tag="리서치 · 북마크릿", tagline="이 계정, 뭐가 제일 잘 됐나?",
   lead="<b>피드를 좋아요순으로 다시 깝니다.</b> 알고리즘이 섞어놓은 순서 말고, 사람들이 실제로 가장 많이 멈춘 게시물부터. 레퍼런스·벤치마킹의 기준이 달라져요.",
   feats=[("수집 개수 지정","10~2,000개까지 원하는 만큼 수집해서 정렬합니다. 자동 스크롤로 알아서 모아요."),
          ("순위·좋아요·댓글 표시","각 게시물에 #순위와 ❤·💬 수가 뱃지로 붙습니다. 릴스·캐러셀·영상 아이콘 구분."),
          ("원복 버튼","보고 나면 '원복' 한 번으로 원래 피드로. 페이지를 망가뜨리지 않아요.")],
   spec=[("종류","북마크릿 (설치 없음)"),("어디서","instagram.com 계정·해시태그·탐색"),("설치","버튼을 북마크바로 드래그"),("가격","무료")],
   how=[("버튼을 북마크바로 드래그","아래 버튼을 브라우저 북마크바에 끌어놓으면 끝. 설치·로그인 없음."),("인스타그램에서 클릭","보고 싶은 계정/해시태그 페이지에서 북마크 클릭."),("개수 입력 → ❤ 정렬","최대 개수 입력하고 정렬 버튼. 좋아요순으로 다시 깔립니다.")],
   cta="drag", bm="insta-rank"),
 "youtube-rank": dict(name="유튜브 인기순 정렬", short="유튜브 인기순 정렬", cat="research", color="var(--yt)", icon="▶",
   tag="리서치 · 북마크릿", tagline="가장 많이 재생된 순서로.",
   lead="<b>검색 결과·채널·쇼츠를 조회수순으로 다시 정렬합니다.</b> 이 채널의 진짜 대표작이 뭔지, 이 주제에서 뭐가 통했는지 한눈에.",
   feats=[("검색·채널·쇼츠 전부","페이지 유형을 자동 감지해 일반 그리드·검색 리스트·쇼츠까지 정렬합니다."),
          ("조회수·길이·채널 표시","#순위와 정확한 조회수, 영상 길이, 채널명이 함께 표시됩니다."),
          ("오버레이 방식","원본 페이지 위에 겹쳐 보여주고, 닫기 한 번으로 원래대로.")],
   spec=[("종류","북마크릿 (설치 없음)"),("어디서","youtube.com 검색·채널·쇼츠"),("설치","버튼을 북마크바로 드래그"),("가격","무료")],
   how=[("버튼을 북마크바로 드래그","아래 버튼을 북마크바에 끌어놓기."),("유튜브에서 클릭","검색 결과나 채널 페이지에서 북마크 클릭."),("개수 입력 → 정렬","수집 개수 입력 후 '조회수순 정렬'. 대표작부터 봅니다.")],
   cta="drag", bm="youtube-rank"),
 "pinterest-grab": dict(name="핀터레스트 원본 추출", short="핀터레스트 원본 추출", cat="research", color="var(--pin)", icon="⚲",
   tag="리서치 · 북마크릿", tagline="저해상 썸네일 말고, 원본을.",
   lead="<b>핀을 클릭해 고르면, 원본 화질 이미지 URL을 한 번에 복사합니다.</b> 무드보드·레퍼런스 수집이 우클릭 노가다에서 클릭 몇 번으로.",
   feats=[("클릭해서 담기","핀을 클릭하면 선택 표시가 붙고 사이드바에 모입니다. 다시 클릭하면 해제."),
          ("originals 화질","핀터레스트의 축소본이 아니라 /originals/ 원본 URL로 변환해 줍니다."),
          ("일괄 복사","모은 이미지 URL 전체를 클립보드로 한 번에.")],
   spec=[("종류","북마크릿 (설치 없음)"),("어디서","pinterest.com 검색·보드"),("설치","버튼을 북마크바로 드래그"),("가격","무료")],
   how=[("버튼을 북마크바로 드래그","아래 버튼을 북마크바에 끌어놓기."),("핀터레스트에서 클릭","수집기가 켜지면 원하는 핀들을 클릭해 담기."),("복사","'복사' 버튼 한 번 — 원본 URL 목록이 클립보드에.")],
   cta="drag", bm="pinterest-grab"),
 "quickpang": dict(name="퀵팡 · 쿠팡 퀵보기", short="퀵팡", cat="sell", color="var(--coup)", icon="⚡",
   tag="커머스 · 북마크릿 · 1만+ 사용", tagline="클릭 없이 옵션·재고 확인.",
   lead="<b>쿠팡 검색 결과에서 상품을 열지 않고, 옵션과 품절 여부를 그 자리에서 봅니다.</b> 소싱·시장조사할 때 탭 지옥에서 해방. 1만 명이 이 도구로 모멘터스를 알게 됐어요.",
   feats=[("검색 결과에 버튼 장착","목록의 각 상품에 '옵션·재고 보기' 버튼이 생깁니다. 누르면 그 자리에서 펼쳐져요."),
          ("재고 상태 색 구분","구매 가능한 옵션은 초록, 품절은 회색 취소선. n/m 구매가능 카운트까지."),
          ("전체 조회","우하단 '전체 조회' 버튼으로 목록 전체를 순차 조회. 요청 간격은 자동 조절.")],
   spec=[("종류","북마크릿 (설치 없음)"),("어디서","coupang.com 검색 결과"),("설치","버튼을 북마크바로 드래그"),("가격","무료"),("실적","사용자 1만+")],
   how=[("버튼을 북마크바로 드래그","아래 버튼을 북마크바에 끌어놓기."),("쿠팡 검색 결과에서 클릭","상품 목록 페이지에서 북마크 클릭."),("옵션·재고 보기","상품별 버튼 또는 '전체 조회'로 재고를 그 자리에서.")],
   cta="drag", bm="quickpang"),
 "chatpage": dict(name="ChatPage", short="ChatPage", cat="fast study", color="#111", icon="✎",
   tag="생산성 · 크롬 확장 · 별점 5.0", tagline="아무리 긴 유튜브도, 3초 요약.",
   lead="<b>긴 영상을 다 볼 필요 없어요.</b> 버튼 한 번이면 유튜브 영상이 ChatGPT·Claude·Gemini로 넘어가 요약됩니다. 무제한, 무료.",
   feats=[("모든 프리미엄 AI 지원","ChatGPT, Claude, Gemini — 쓰던 AI 그대로. 계정만 있으면 추가 비용 없음."),
          ("길이 무제한","아무리 긴 영상도 자막을 통째로 넘겨 요약합니다."),
          ("스토어 별점 5.0","수천 명이 쓰고 만점을 준 확장. v2.9.7.")],
   spec=[("종류","크롬 확장"),("어디서","youtube.com"),("설치","크롬 웹스토어에서 1클릭"),("가격","무료"),("버전","v2.9.7 · 별점 5.0")],
   how=[("크롬에 추가","크롬 웹스토어에서 ChatPage 설치."),("유튜브에서 버튼 클릭","영상 페이지에 생긴 요약 버튼을 누르기."),("AI가 요약","쓰던 AI가 3초 만에 정리.")],
   cta="store", store="https://chromewebstore.google.com/"),
}
ORDER = ["her", "insta-rank", "youtube-rank", "pinterest-grab", "quickpang", "chatpage"]
CATN = {"fast": "생산성", "sell": "커머스", "research": "리서치", "study": "스터디"}

def cta(slug, big=False):
    p = P[slug]
    cls = "btn lg cta-main drag" if (big and p["cta"] == "drag") else ("btn lg cta-main" if big else ("btn drag" if p["cta"] == "drag" else "btn"))
    if p["cta"] == "drag":
        return f'<a class="{cls}" href="{BM[p["bm"]]}" {DRAG_ATTR}>↖ {p["short"]} — 북마크바로 드래그</a>'
    return f'<a class="{cls}" href="{p["store"]}" target="_blank" rel="noopener">크롬에 추가 →</a>'

# ---------- assets ----------
os.makedirs("assets", exist_ok=True)
with open("assets/site.css", "w", encoding="utf-8") as f:
    f.write(CSS)

# ---------- product detail pages ----------
for slug in ORDER:
    p = P[slug]
    feats = "".join(f'<section class="feature"><div class="fk">기능 0{i+1}</div><h2>{t}</h2><p>{d}</p></section>' for i, (t, d) in enumerate(p["feats"]))
    spec = "".join(f'<div class="r"><span>{k}</span><span>{v}</span></div>' for k, v in p["spec"])
    how = "".join(f'<div class="step"><span class="n">0{i+1}</span><div><b>{t}</b><p>{d}</p></div></div>' for i, (t, d) in enumerate(p["how"]))
    rel = [s for s in ORDER if s != slug][:3]
    relh = "".join(f'<a class="rcard" href="/products/{s}/"><div class="ic" style="background:{P[s]["color"]}">{P[s]["icon"]}</div><h3>{P[s]["name"]}</h3><p>{P[s]["tagline"]}</p></a>' for s in rel)
    hint = '<div class="risk">↖ 클릭 말고, 버튼을 위 북마크바로 <b>드래그</b>해서 등록하세요</div>' if p["cta"] == "drag" else '<div class="risk">계정 없음 · 결제 없음 · 1클릭 제거</div>'
    body = f"""<div class="dwrap">
  <div class="dhead">
    <a class="back" href="/products/">← 전체 제품</a>
    <div><div class="kick">{p['tag']}</div><h1>{p['name']}</h1></div>
    <p class="lead">{p['lead']}</p>
  </div>
  <div class="dbody">
    <div>
      {feats}
      <section class="howto"><h2>쓰는 데 30초</h2><div class="steps">{how}</div></section>
    </div>
    <aside class="buy">
      <span class="free">무료</span>
      <div class="price">₩0 <small>· 평생 무료</small></div>
      {cta(slug, big=True)}
      {hint}
      <div class="spec">{spec}</div>
      <div class="also"><div class="lbl">함께 쓰면 좋은</div>
        <a href="/products/{rel[0]}/"><span class="ic" style="background:{P[rel[0]]['color']}">{P[rel[0]]['icon']}</span>{P[rel[0]]['name']}</a>
        <a href="/products/{rel[1]}/"><span class="ic" style="background:{P[rel[1]]['color']}">{P[rel[1]]['icon']}</span>{P[rel[1]]['name']}</a>
      </div>
    </aside>
  </div>
  <section class="related"><h2>강형모가 만든 다른 무료 제품</h2><div class="rgrid">{relh}</div></section>
</div>"""
    os.makedirs(f"products/{slug}", exist_ok=True)
    with open(f"products/{slug}/index.html", "w", encoding="utf-8") as f:
        f.write(page(f"{p['name']} — MOMENTUS", p["tagline"] + " 무료.", body, active="p"))

# ---------- products listing ----------
cards = []
for slug in ORDER:
    p = P[slug]
    newb = '<span class="newb">NEW</span>' if "new" in p["cat"] else ""
    med = "크롬 확장" if p["cta"] == "store" else "북마크릿 · 끌어놓기"
    tags = "".join(f'<span class="tagx">{CATN[c]}</span>' for c in p["cat"].split() if c in CATN)
    tstyle = ' style="background:linear-gradient(135deg,#151619,#0b0c0e)"' if slug == "her" else ""
    timg = "" if slug == "her" else f'<img src="https://picsum.photos/seed/{slug}/640/400" alt="">'
    cards.append(f"""<a class="pcard" href="/products/{slug}/" data-cat="{p['cat']}">
  <div class="thumb"{tstyle}>{timg}<span class="ic" style="background:{p['color']}">{p['icon']}</span><span class="badge">{p['tag'].split(' ·')[0]}</span>{newb}</div>
  <div class="bd"><div class="top"><span class="free">무료</span><span class="med">{med}</span></div><h3>{p['name']}</h3><p class="d">{p['tagline']}</p>
  <div class="foot"><div class="tags">{tags}</div><span class="go">자세히 →</span></div></div>
</a>""")
FILTER_JS = """<script>
var cards=[].slice.call(document.querySelectorAll('.pcard')),chips=[].slice.call(document.querySelectorAll('.chip'));
function apply(f){chips.forEach(function(c){c.classList.toggle('on',c.dataset.f===f);});
cards.forEach(function(c){var ok=(f==='all')||(c.dataset.cat||'').split(' ').indexOf(f)>=0;c.style.display=ok?'':'none';});
history.replaceState(null,'',f==='all'?location.pathname:('?f='+f));}
document.getElementById('filterRow').addEventListener('click',function(e){var c=e.target.closest('.chip');if(c)apply(c.dataset.f);});
var m=(location.search.match(/f=(\\w+)/)||[])[1];apply(m&&chips.some(function(c){return c.dataset.f===m;})?m:'all');
</script>"""
plist = f"""<div class="phead"><div class="kick">Products · 전부 무료</div><h1>필요한 걸로 골라 쓰세요.</h1>
<p>강형모가 만든 무료 브라우저 제품들. 지금 6개 — 계속 늘어납니다. <b style="color:var(--ink)">하려는 일</b>로 걸러 보세요.</p></div>
<div class="filters"><div class="row" id="filterRow">
  <button class="chip on" data-f="all">전체 <span class="n">6</span></button>
  <button class="chip" data-f="new">🆕 새로 나온 <span class="n">1</span></button>
  <button class="chip" data-f="fast">⚡ 일 빨리 끝내기 <span class="n">2</span></button>
  <button class="chip" data-f="sell">🛒 파는 사람 도구 <span class="n">1</span></button>
  <button class="chip" data-f="research">🔎 콘텐츠·리서치 <span class="n">3</span></button>
  <button class="chip" data-f="study">📚 배우고 정리 <span class="n">1</span></button>
</div></div>
<div class="pgrid" id="grid">{''.join(cards)}</div>"""
os.makedirs("products", exist_ok=True)
with open("products/index.html", "w", encoding="utf-8") as f:
    f.write(page("제품 — MOMENTUS", "무료 브라우저 제품 전체. 북마크릿·크롬 확장.", plist, active="p", extra=FILTER_JS))

# ---------- journal posts ----------
POSTS = {
 "insta-reference": dict(cat="가이드 · AX", title="인스타 레퍼런스, '감'으로 찾지 말고 세어서 찾기",
   sub="잘 나가는 콘텐츠엔 이유가 있습니다. 좋아요순 정렬 하나로 벤치마킹의 기준을 바꾸는 법.",
   date="2026. 07. 08", mins=6, img="jfeat",
   toc=[("s1","왜 '감'이 틀리나"),("s2","세어서 보면 달라진다"),("s3","이렇게 쓰세요")],
   body="""<p>레퍼런스를 찾을 때 우리는 보통 '감'에 의존합니다. 피드를 스크롤하다 눈에 띄는 걸 저장하죠. 그런데 <b>눈에 띈다는 것과 실제로 잘 됐다는 건 다릅니다.</b></p>
<h2 id="s1">왜 '감'이 틀리나</h2>
<p>알고리즘은 최신순·관계순으로 피드를 섞습니다. 그래서 우리가 보는 순서는 '인기'가 아니라 '타이밍'이에요. 진짜 잘 된 게시물은 스크롤 저 아래 묻혀 있거나, 반대로 그저 최근이라 위에 떠 있을 뿐입니다.</p>
<p>벤치마킹의 목적은 "이 계정에서 뭐가 통했나"를 아는 거예요. 그런데 통했는지를 판단할 근거 없이 스크롤 순서대로 보면, 사실상 알고리즘이 추천하는 걸 베끼게 됩니다.</p>
<h2 id="s2">세어서 보면 달라진다</h2>
<p>기준을 하나만 바꾸면 됩니다 — <b>좋아요순</b>. 이 계정에서 사람들이 실제로 가장 많이 멈춘 게 뭔지, 숫자로 줄을 세우는 거죠. 그러면 '감으로 좋아 보이는 것'이 아니라 '검증된 것'이 위로 올라옵니다.</p>
<blockquote>레퍼런스는 훔치는 게 아니라, 세는 것이다.</blockquote>
<p>이걸 매번 손으로 할 순 없으니, 버튼 하나로 피드를 좋아요순으로 다시 까는 도구를 만들었습니다.</p>
<div class="inline-cta"><div class="ic" style="background:var(--ig)">◲</div><div class="t"><b>인스타 인기순 정렬</b><span>무료 · 버튼 하나 드래그로 지금 써보기</span></div><a class="btn" href="/products/insta-rank/">써보기 →</a></div>
<h2 id="s3">이렇게 쓰세요</h2>
<ul><li>도구를 북마크바에 끌어놓습니다 (설치 없음).</li><li>보고 싶은 계정·해시태그 페이지에서 버튼 클릭.</li><li>좋아요순으로 다시 깔린 대표 게시물만 확인.</li></ul>
<p>레퍼런스의 질이 달라지면, 만드는 것의 질도 달라집니다. 다음 글에선 유튜브 리서치를 같은 방식으로 뒤집는 법을 다룹니다.</p>"""),
 "quickpang-10k": dict(cat="메이킹 로그", title="퀵팡으로 1만 명이 온 뒤 배운 것",
   sub="트래픽은 폭발했는데, 왜 아무것도 남지 않았나. 무료 도구 하나가 가르쳐준 것들.",
   date="2026. 07. 05", mins=5, img="j4",
   toc=[("s1","하루아침의 1만 명"),("s2","남은 것과 새어나간 것"),("s3","그래서 이 사이트를 만들었다")],
   body="""<p>작년 2월, 쿠팡 검색 결과에서 클릭 없이 옵션·재고를 보여주는 북마크릿 하나를 인스타그램에 올렸습니다. 이름은 퀵팡. 셀러들 사이에 퍼지는 데 오래 걸리지 않았어요.</p>
<h2 id="s1">하루아침의 1만 명</h2>
<p>팔로워가 1만 명이 됐습니다. 소싱하는 사람들에게 '탭 수십 개 열고 비교하는 노가다'는 매일의 고통이었고, 그걸 버튼 하나로 줄여주니 반응은 당연했는지도 모릅니다.</p>
<p>배운 것 하나. <b>사람들은 도구 설명에 안 움직입니다. 자기 고통이 사라지는 장면에 움직입니다.</b> 퀵팡을 소개한 게시물은 기능 나열이 아니라 "이 화면이 이렇게 된다"는 전후 비교였어요.</p>
<h2 id="s2">남은 것과 새어나간 것</h2>
<p>그런데 문제가 있었습니다. 1만 명이 도구를 받아갔는데, <b>그 다음이 없었어요.</b> 도구엔 제가 누군지, 다른 무엇을 만드는지로 이어지는 연결고리가 하나도 없었습니다. 트래픽은 폭발했지만 어디에도 고이지 않고 그대로 흘러나갔죠.</p>
<blockquote>도구는 미끼가 아니라 배달부다. 배달부가 돌아올 주소를 모르면, 배달은 한 번으로 끝난다.</blockquote>
<h2 id="s3">그래서 이 사이트를 만들었다</h2>
<p>이 사이트(the-moment.us)는 그 교훈의 결과물입니다. 도구마다 돌아올 주소를 달고, 쓰다 마음에 들면 옆의 다른 도구로 이어지게. 퀵팡도 다시 정비해서 올려뒀습니다.</p>
<div class="inline-cta"><div class="ic" style="background:var(--coup)">⚡</div><div class="t"><b>퀵팡 · 쿠팡 퀵보기</b><span>무료 · 1만 명이 쓴 그 도구</span></div><a class="btn" href="/products/quickpang/">써보기 →</a></div>"""),
 "why-free": dict(cat="칼럼", title="왜 전부 무료로 푸는가",
   sub="공짜인데도 대충 만들지 않는 이유. 그리고 무료가 되려 남기는 것들.",
   date="2026. 07. 01", mins=4, img="j6",
   toc=[("s1","값을 안 매기는 이유"),("s2","무료가 남기는 것")],
   body="""<p>여기 있는 제품은 전부 무료입니다. 로그인도, 결제도, 이메일 수집도 없어요. 이 얘길 하면 꼭 돌아오는 질문이 있습니다. "그럼 뭐가 남아요?"</p>
<h2 id="s1">값을 안 매기는 이유</h2>
<p>비싸고 어려워서 미뤄두던 일들이 있잖아요. 인스타 벤치마킹, 소싱 시장조사, 긴 영상 소화 — 도구가 있으면 되는데, 그 도구가 월 구독이거나 배우기 어렵거나. 그래서 시작조차 안 하게 되는 일들.</p>
<p>그걸 <b>그냥 한 번 눌러보게</b> 만들고 싶었습니다. 결제 창이 뜨는 순간 사람들은 "다음에"를 누르니까요. 무료여야 눌러보고, 눌러봐야 됩니다 — 이 도구들의 가치는 써본 다음에야 생기거든요.</p>
<h2 id="s2">무료가 남기는 것</h2>
<p>대신 남는 게 있습니다. 도구가 실제로 당신 일을 되게 하면, 당신은 언젠가 돌아옵니다. 다른 불편이 생겼을 때 "그 사람이 뭐 만들었더라" 하고요. 그게 이 <a href="/lab/">만들어드려요</a> 게시판이 있는 이유이기도 합니다.</p>
<blockquote>도구는 공짜지만, 신뢰는 공짜로 안 생긴다. 도구는 신뢰를 버는 가장 정직한 방법이다.</blockquote>
<p>혼자 만들어서 유지비가 거의 들지 않는다는 것도 솔직한 이유 중 하나입니다. AI와 함께 일하면 한 사람의 생산량이 예전과 다르거든요. 그 얘기는 <a href="/about/">소개</a>에서 이어집니다.</p>"""),
}
PORDER = ["insta-reference", "quickpang-10k", "why-free"]

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

for slug in PORDER:
    ps = POSTS[slug]
    others = [s for s in PORDER if s != slug]
    toch = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in ps["toc"])
    railh = "".join(f'<li><a href="/journal/{s}/"><span class="th"><img src="https://picsum.photos/seed/{POSTS[s]["img"]}/128/88" alt=""></span><span class="t">{POSTS[s]["title"]}</span></a></li>' for s in others)
    body = f"""<div class="post-top">
  <div class="kick pt">{ps['cat']}</div>
  <h1>{ps['title']}</h1>
  <p class="sub">{ps['sub']}</p>
</div>
<div class="post-grid">
  <aside class="post-toc"><nav aria-label="목차"><p class="rail-title">목차</p><ul>{toch}</ul></nav></aside>
  <div class="post-main">
    <div class="post-meta">
      <div class="byline"><span class="av">모</span><span><b>모멘터스</b><time>{ps['date']} · {ps['mins']}분 읽기</time></span></div>
      <div class="share"><a id="shX" href="#" target="_blank" rel="noopener" aria-label="X 공유">X</a><a id="shF" href="#" target="_blank" rel="noopener" aria-label="페이스북 공유">f</a><a id="shL" href="#" target="_blank" rel="noopener" aria-label="링크드인 공유">in</a><button id="shC" aria-label="링크 복사">↗</button></div>
    </div>
    <figure class="post-cover"><img src="https://picsum.photos/seed/{ps['img']}/1200/675" alt=""></figure>
    <article class="prose">{ps['body']}</article>
    {COMMENT_HTML}
  </div>
  <aside class="post-aside"><div class="rail"><p class="rail-title">연관해서 읽기</p><ul class="rail-posts">{railh}</ul></div></aside>
</div>"""
    os.makedirs(f"journal/{slug}", exist_ok=True)
    with open(f"journal/{slug}/index.html", "w", encoding="utf-8") as f:
        f.write(page(f"{ps['title']} — MOMENTUS 저널", ps["sub"], body, active="j", extra=post_js(slug)))

# ---------- journal listing ----------
feat = POSTS["insta-reference"]
rest = ["quickpang-10k", "why-free"]
jcards = "".join(f"""<a class="jpost" href="/journal/{s}/"><div class="im"><span class="catb">{POSTS[s]['cat'].split(' ·')[0]}</span><img src="https://picsum.photos/seed/{POSTS[s]['img']}/600/420" alt=""></div><h3>{POSTS[s]['title']}</h3><p class="ex">{POSTS[s]['sub']}</p><div class="meta">{POSTS[s]['date']} · {POSTS[s]['mins']}분</div></a>""" for s in rest)
jbody = f"""<div class="jhead"><div class="kick pt">Journal</div><h1>만드는 이야기,<br>쓰는 법.</h1>
<p>브라우저를 더 잘 쓰는 법(가이드·칼럼)과, 이 제품들이 어떻게 만들어지는지(메이킹 로그). 연재합니다.</p></div>
<section class="jfeat"><a href="/journal/insta-reference/">
  <div class="im"><img src="https://picsum.photos/seed/{feat['img']}/900/620" alt=""></div>
  <div><div class="kick pt">{feat['cat']}</div><h2>{feat['title']}</h2><p class="ex">{feat['sub']}</p><div class="meta">{feat['date']} · 모멘터스 · {feat['mins']}분</div></div>
</a></section>
<section class="jlist">{jcards}</section>"""
os.makedirs("journal", exist_ok=True)
with open("journal/index.html", "w", encoding="utf-8") as f:
    f.write(page("저널 — MOMENTUS", "만드는 이야기와 쓰는 법. 가이드·칼럼·메이킹 로그.", jbody, active="j"))

# ---------- lab ----------
lab_body = """<div class="lab-hero"><div class="kick pt">Lab · 만들어드려요</div>
<h1>불편한 거 있으면,<br>말해주세요.</h1>
<p class="lead">"이런 게 불편해요"를 남겨주세요. 다른 분들이 공감(▲)하고, 공감 많은 것부터 제가 만들어 드려요. <b style="color:var(--ink)">돈 받고 만드는 게 아니에요</b> — 많이 불편하다는 걸 제가 대신 풀어드리는 거예요.</p></div>
<div class="lab-wrap">
  <div class="submitb" id="submitb"><textarea id="ptext" placeholder="예: 네이버 블로그 이미지들 한 번에 다운로드하고 싶어요…"></textarea>
  <div class="row"><span class="hint">기한 약속은 안 해요. 공감 많으면 만들 확률이 확 올라가요.</span><button class="btn" id="psend" style="padding:10px 22px;font-size:14px">제보하기</button></div></div>
  <div class="ldone" id="ldone"><span>✓</span><div><b>접수됐어요, 고마워요.</b> 비슷한 불편을 겪는 분이 많으면 우선 만들게요. 만들면 여기서 알려드릴게요.</div></div>
  <section class="board"><div class="board-head"><h2>지금 사람들이 원하는 것</h2><span>공감순</span></div><div id="list"></div></section>
  <div class="hsteps">
    <div class="hstep"><div class="n">01</div><b>제보</b><p>불편한 걸 한 줄 남겨요.</p></div>
    <div class="hstep"><div class="n">02</div><b>공감(▲)</b><p>같은 불편이면 눌러요. 수요가 쌓여요.</p></div>
    <div class="hstep"><div class="n">03</div><b>내가 픽</b><p>공감 많은 것부터 만듭니다.</p></div>
    <div class="hstep"><div class="n">04</div><b>알림</b><p>완성되면 제품으로 등록 + 알림.</p></div>
  </div>
  <p class="note-c">이미 만들어진 건 <a href="/products/" style="color:var(--ink);text-decoration:underline">제품</a>에서, 만드는 과정은 <a href="/journal/" style="color:var(--ink);text-decoration:underline">저널</a>에서 볼 수 있어요.</p>
</div>"""
LAB_JS = """<script>
document.getElementById('psend').addEventListener('click',function(){var t=document.getElementById('ptext').value.trim();if(!t)return;
try{var k='momentus_lab_requests';var a=JSON.parse(localStorage.getItem(k)||'[]');a.push({text:t,ts:Date.now()});localStorage.setItem(k,JSON.stringify(a));}catch(e){}
document.getElementById('submitb').style.display='none';document.getElementById('ldone').classList.add('show');});
var items=[
 {id:'r1',t:'네이버 블로그 본문 이미지 한 번에 저장',d:'상세페이지 만들 때 이미지 긁는 게 너무 번거로워요.',v:128,tag:'리서치'},
 {id:'r2',t:'쿠팡 여러 상품 가격/재고 한눈에 비교',d:'소싱할 때 탭 여러 개 열어 비교하는 게 지쳐요.',v:94,tag:'커머스',state:'building'},
 {id:'r3',t:'유튜브 자막 통째로 복사',d:'요약 말고 원문 자막 자체가 필요할 때가 있어요.',v:61,tag:'생산성'},
 {id:'r4',t:'인스타 저장한 게시물 정리·내보내기',d:'저장만 하고 다시 못 찾아요.',v:47,tag:'리서치'},
 {id:'r5',t:'스레드/X 글타래 이미지로 저장',d:'캡처 여러 장 이어붙이기 귀찮아요.',v:33,tag:'콘텐츠'}];
var voted={};try{voted=JSON.parse(localStorage.getItem('momentus_lab_votes')||'{}');}catch(e){}
function render(){items.sort(function(a,b){return b.v-a.v;});
document.getElementById('list').innerHTML=items.map(function(it){
var on=voted[it.id]?' on':'';var st=it.state==='building'?'<span class="tagx building">만드는 중</span>':'';
return '<div class="litem"><button class="vote'+on+'" data-id="'+it.id+'"><span class="ar">▲</span><span class="n">'+it.v+'</span></button><div><h3></h3><p></p><div class="tags"><span class="tagx">'+it.tag+'</span>'+st+'</div></div></div>';}).join('');
var rows=document.querySelectorAll('#list .litem');
items.forEach(function(it,i){if(rows[i]){rows[i].querySelector('h3').textContent=it.t;rows[i].querySelector('p').textContent=it.d;}});
[].slice.call(document.querySelectorAll('.vote')).forEach(function(v){v.addEventListener('click',function(){
var id=v.dataset.id,it=items.filter(function(x){return x.id===id;})[0];
if(voted[id]){voted[id]=false;it.v--;}else{voted[id]=true;it.v++;}
try{localStorage.setItem('momentus_lab_votes',JSON.stringify(voted));}catch(e){}render();});});}
render();
</script>"""
os.makedirs("lab", exist_ok=True)
with open("lab/index.html", "w", encoding="utf-8") as f:
    f.write(page("만들어드려요 — MOMENTUS", "불편한 걸 말해주세요. 공감 많은 것부터 무료로 만들어 드려요.", lab_body, active="l", extra=LAB_JS))

# ---------- about ----------
about_body = """<div class="awrap">
  <section class="ahero"><div class="kick pt">About</div>
    <h1>혼자, 매일 만듭니다.</h1>
    <p class="lead">MOMENTUS는 강형모의 1인 AI 스튜디오예요. AI 슈트를 입은 한 사람이, 혼자선 불가능한 생산량으로 브라우저에서 쓰는 작은 제품들을 계속 만듭니다.</p>
    <div class="avat"><div class="a">강</div><div><b>강형모</b><span>Founder · MOMENTUS</span></div></div>
  </section>
  <div class="split3">✳ ✳ ✳</div>
  <p class="say">비싸고 어려워서 미뤄두던 일들을, 그냥 한 번 눌러보게 만들고 싶었어요. 그래서 여기 있는 건 <b>전부 무료</b>로 풉니다. 로그인도, 결제도, 이메일 수집도 없이 — 도구가 실제로 당신 일을 되게 하면, 그거면 충분해요.</p>
  <div class="stats3">
    <div class="stat3"><b>6+</b><span>무료 제품 (계속 증가)</span></div>
    <div class="stat3"><b>1만+</b><span>퀵팡으로 모인 사용자</span></div>
    <div class="stat3"><b>5.0</b><span>ChatPage 스토어 별점</span></div>
  </div>
  <section class="tl"><h2>만든 것들</h2>
    <div class="trow"><span class="yr">2026</span><div><b>her · ChatPage</b><p>말로 조작하는 확장 · 유튜브 3초 요약</p></div></div>
    <div class="trow"><span class="yr">2025</span><div><b>Mark</b><p>AI 로고 자동 생성 — 작품 1,193건</p></div></div>
    <div class="trow"><span class="yr">2024</span><div><b>퀵팡</b><p>쿠팡 퀵보기 — 1만 사용자의 시작</p></div></div>
  </section>
  <section class="cta-dark"><h2>필요한 게 있으면,<br>말해주세요.</h2><p>불편한 걸 알려주면, 그중에서 골라 만들어 드려요.</p>
  <div class="btns"><a href="/lab/">만들어드려요 →</a><a class="ghost" href="mailto:hello@the-moment.us">hello@the-moment.us</a></div></section>
</div>"""
os.makedirs("about", exist_ok=True)
with open("about/index.html", "w", encoding="utf-8") as f:
    f.write(page("소개 — MOMENTUS", "강형모의 1인 AI 스튜디오. 무료 브라우저 제품을 매일 만듭니다.", about_body, active="a"))

# ---------- landing (root index.html) ----------
land_body = """<section class="rn-hero">
  <h1>일하는 사람을 위한<br>도구를 만듭니다.</h1>
  <p class="sub">상품 사진, 로고, 플래너, 면접 연습. 그리고 매일 쓰는 브라우저 도구는 무료로 드립니다.</p>
  <div class="rn-meta">
    <span>Momentus</span>
    <span>파는 것 04 · 주는 것 06</span>
  </div>
</section>

<section class="rn-sell">
  <div class="rn-row big">
    <a class="rn-item" href="https://heyreci.com" target="_blank" rel="noopener">
      <div class="rn-shot tall">
        <img src="https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=1400&q=75&auto=format&fit=crop" alt="스튜디오 조명 아래 놓인 화장품 상품 사진">
      </div>
    </a>
    <div class="rn-item side">
      <div class="rn-cap">
        <span class="kick">heyreci · 쇼핑몰 셀러</span>
        <h3>모델 촬영비 0원으로 카탈로그를 만듭니다</h3>
        <p>폰으로 찍은 상품 사진이 30초 만에 판매용 컷이 됩니다. 배경·모델·상세페이지까지, 이미지 도구 40종.</p>
        <span class="rn-go">heyreci.com에서 써보기 ↗</span>
      </div>
    </div>
  </div>

  <div class="rn-row two">
    <a class="rn-item" href="https://mark.the-moment.us" target="_blank" rel="noopener">
      <div class="rn-shot">
        <img src="https://images.unsplash.com/photo-1713616147761-c126f8009c6f?w=1000&q=75&auto=format&fit=crop" alt="종이에 로고를 스케치하는 모습" loading="lazy">
      </div>
      <div class="rn-cap">
        <span class="kick">Mark · 자영업 사장님</span>
        <h3>내 업종 로고를 먼저 보고 고릅니다</h3>
        <p>같은 업종만 깊이 판 시안 600여 개. 간판과 명함에 얹은 모습까지 보고, 마음에 들면 그때 맡기세요.</p>
        <span class="rn-go">업종별 시안 보기 ↗</span>
      </div>
    </a>
    <a class="rn-item" href="https://planner.the-moment.us" target="_blank" rel="noopener">
      <div class="rn-shot">
        <img src="https://images.unsplash.com/photo-1673597487243-8e84ae538b8d?w=1000&q=75&auto=format&fit=crop" alt="태블릿에 띄운 달력 플래너" loading="lazy">
      </div>
      <div class="rn-cap">
        <span class="kick">THE PLAN · 굿노트 · 아이패드</span>
        <h3>내 손에 맞는 플래너를 골라서 씁니다</h3>
        <p>스타일과 구성, 시작 요일까지 고른 대로 조립해 PDF로 드립니다. 남의 플래너에 나를 맞추지 마세요.</p>
        <span class="rn-go">플래너 고르러 가기 ↗</span>
      </div>
    </a>
  </div>

  <div class="rn-row big rev">
    <div class="rn-item side">
      <div class="rn-cap">
        <span class="kick">Cue · 경력직 이직</span>
        <h3>면접장에서 얼어붙지 않으려면, 소리 내어 연습해야 합니다</h3>
        <p>눈으로 읽으면 다 아는 것 같습니다. 입으로 뱉어봐야 압니다. 동문서답하면 AI가 짚어 줍니다.</p>
        <span class="rn-go">한 판 해보기 ↗</span>
      </div>
    </div>
    <a class="rn-item" href="https://cue.the-moment.us" target="_blank" rel="noopener">
      <div class="rn-shot">
        <img src="https://images.unsplash.com/photo-1698047681452-08eba22d0c64?w=1400&q=75&auto=format&fit=crop" alt="면접에서 답변하는 지원자" loading="lazy">
      </div>
    </a>
  </div>
</section>

<section class="rn-free">
  <span class="kick">그리고 — 공짜</span>
  <h2>매일 쓰는 도구는 그냥 드립니다.</h2>
  <p class="lead">설치도 로그인도 결제도 없습니다. 쓰다 보면 위의 제품이 왜 필요한지 알게 되실 겁니다.</p>

  <div class="rn-tools">
    <a class="rn-tool" href="/products/quickpang/">
      <span class="tn">퀵팡</span>
      <span class="td">쿠팡 검색 결과에서, 들어가 보지 않고 옵션과 재고를 확인</span>
      <span class="rn-bridge">셀러시라면 → heyreci 상품 사진 ↗</span>
    </a>
    <a class="rn-tool" href="/products/insta-rank/">
      <span class="tn">인스타 인기순 정렬</span>
      <span class="td">이 계정, 대체 뭐가 제일 잘 됐나 — 피드를 좋아요순으로</span>
      <span class="rn-bridge">잘 되는 컷을 만들려면 → heyreci ↗</span>
    </a>
    <a class="rn-tool" href="/products/pinterest-grab/">
      <span class="tn">핀터레스트 원본 추출</span>
      <span class="td">저해상 썸네일 말고, 무드보드에 쓸 원본 화질 그대로</span>
      <span class="rn-bridge">무드보드를 로고로 → Mark ↗</span>
    </a>
    <a class="rn-tool" href="/products/chatpage/">
      <span class="tn">ChatPage</span>
      <span class="td">1시간짜리 영상도 쓰던 AI로 넘겨 3초 만에 요약</span>
      <span class="rn-bridge">면접 준비 중이라면 → Cue ↗</span>
    </a>
    <a class="rn-tool" href="/products/her/">
      <span class="tn">her · 음성 입력</span>
      <span class="td">타이핑이 생각을 못 따라갈 때. 모든 입력창에서, 말로</span>
      <span class="rn-bridge">말하기 연습이 필요하면 → Cue ↗</span>
    </a>
    <a class="rn-tool" href="/products/youtube-rank/">
      <span class="tn">유튜브 인기순 정렬</span>
      <span class="td">이 채널의 대표작이 뭔지, 조회수순으로 5초 만에</span>
      <span class="rn-bridge plain">제품 전체 보기 →</span>
    </a>
  </div>

  <div class="cta-dark">
    <h2>불편한 게 있으면 말해 주세요.</h2>
    <p>공감이 많이 쌓인 것부터 만들어 드립니다. 돈 받고 만드는 게 아닙니다.</p>
    <div class="btns">
      <a href="/lab/">불편한 거 알려주기</a>
      <a class="ghost" href="/products/">제품 전체 보기</a>
    </div>
  </div>
</section>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page("MOMENTUS — 일하는 사람을 위한 도구를 만듭니다", "상품 사진, 로고, 플래너, 면접 연습. 매일 쓰는 브라우저 도구 6종은 무료로 드립니다.", land_body, active=""))

# ---------- sitemap ----------
urls = ["", "products/", "journal/", "lab/", "about/"] + [f"products/{s}/" for s in ORDER] + [f"journal/{s}/" for s in PORDER]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f"  <url><loc>https://the-moment.us/{u}</loc></url>\n"
sm += "</urlset>\n"
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sm)

print("SITE GENERATED:")
print("  index.html, assets/site.css, sitemap.xml")
print("  products/: index + " + ", ".join(ORDER))
print("  journal/: index + " + ", ".join(PORDER))
print("  lab/, about/")
