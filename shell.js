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

    var host = (location.hostname || "").replace(/^www\./, "");
    var html = '<div class="in"><a class="wm" href="https://the-moment.us">MOMENTUS</a><nav aria-label="모멘터스">';
    for (var i = 0; i < ITEMS.length; i++) {
      var it = ITEMS[i], a = "";
      if (it.sep) html += '<span class="sep" aria-hidden="true"></span>';
      // ② 활성 표시 = 현재 도메인이 그 항목의 도메인과 같을 때만. 라벨 하드코딩 없음.
      var h = it.href.indexOf("//") > -1 ? it.href.split("//")[1].split("/")[0].replace(/^www\./, "") : "";
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
