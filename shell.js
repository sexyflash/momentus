/* MOMENTUS shell.js — 1단 브랜드 바. 생성물(scripts/gen_site.py). 손으로 고치지 말 것. */
(function () {
  "use strict";
  try {
    if (document.getElementById("mmt-bar")) return;
    var H = 40, ITEMS = [{"label":"플래너","href":"https://notes.the-moment.us","sub":"notes — 내 손에 맞게 조립하는 디지털 플래너","ext":false,"sep":false},{"label":"로고","href":"https://mark.the-moment.us","sub":"mark — 내 업종 로고를 먼저 보고 고릅니다","ext":false,"sep":false},{"label":"모의면접","href":"https://cue.the-moment.us","sub":"cue — 입으로 답하고 AI가 짚어줍니다","ext":false,"sep":false},{"label":"상품사진","href":"https://heyreci.com","sub":"heyreci.com으로 이동","ext":true,"sep":false},{"label":"무료 도구","href":"/tools/","sub":"","ext":false,"sep":true},{"label":"이야기","href":"/log/","sub":"","ext":false,"sep":true},{"label":"소개","href":"/about/","sub":"","ext":false,"sep":false}];
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
      + "#mmt-bar .mmt-wm{font-size:13px;font-weight:800;letter-spacing:-.01em;color:#fff;text-decoration:none;flex:0 0 auto}"
      + "#mmt-bar .mmt-nav{display:flex;align-items:center;gap:4px;flex:0 0 auto}"
      + "#mmt-bar a.mmt-it{font-size:13px;font-weight:500;letter-spacing:-.01em;color:var(--mmt-fg);"
      +   "text-decoration:none;padding:5px 9px;border-radius:7px;white-space:nowrap;position:relative}"
      + "#mmt-bar a.mmt-it:hover{background:rgba(255,255,255,.1);color:#fff}"
      + "#mmt-bar a.mmt-it[aria-current=page]{background:#fff;color:#14161a;font-weight:700}"
      + "#mmt-bar .mmt-sep{width:1px;height:13px;background:rgba(255,255,255,.18);flex:0 0 auto;margin:0 5px}"
      + "#mmt-bar i.mmt-ext{font-style:normal;font-size:9px;opacity:.55;margin-left:3px;vertical-align:super}"
      + "#mmt-bar a.mmt-it[data-sub]::after{content:attr(data-sub);position:absolute;top:calc(100% + 7px);left:50%;"
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

    var host = (location.hostname || "").replace(/^www\./, "");
    var html = '<div class="mmt-in"><a class="mmt-wm" href="https://the-moment.us">MOMENTUS</a><nav class="mmt-nav" aria-label="모멘터스">';
    for (var i = 0; i < ITEMS.length; i++) {
      var it = ITEMS[i], a = "";
      if (it.sep) html += '<span class="mmt-sep" aria-hidden="true"></span>';
      // ② 활성 표시 = 현재 도메인이 그 항목의 도메인과 같을 때만. 라벨 하드코딩 없음.
      var h = it.href.indexOf("//") > -1 ? it.href.split("//")[1].split("/")[0].replace(/^www\./, "") : "";
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
      "--mmt-maxw": "1320px",                  // 2단 바 컨테이너 최대폭
      "--mmt-bar2-h": "64px",                  // 2단 제품 바 높이
      "--mmt-fs-logo": "22px",
      "--mmt-fs-nav": "14px",
      "--mmt-fw-nav": "600",
      "--mmt-nav-gap": "26px",
      "--mmt-fs-cta": "14px",
      "--mmt-cta-pad": "9px 18px",
      "--mmt-cta-r": "999px"
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
