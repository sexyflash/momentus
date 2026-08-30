// apex(the-moment.us) 워커 — 두 가지만 한다: 네이버 소유확인, 북마크릿 픽셀 수집.
//
// ⚠️ 이 워커는 wrangler.jsonc 의 `assets.run_worker_first` 에 적힌 경로에서만 실행된다.
//    나머지 요청은 예전처럼 자산이 직접 처리한다
//    (html_handling·not_found_handling·_redirects 동작을 건드리지 않기 위해서다).

// ── 1x1 투명 GIF (43바이트) ──────────────────────────────────────────────
const PIXEL = Uint8Array.from(atob(
  'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
), (c) => c.charCodeAt(0));

const NO_STORE = {
  'content-type': 'image/gif',
  'cache-control': 'no-store, no-cache, must-revalidate',
  'access-control-allow-origin': '*',
};

/**
 * 북마크릿이 "지금 실행됐다"고 알리는 픽셀.
 *
 * ★ 왜 픽셀인가 — 북마크릿은 **남의 페이지 안**에서 돈다. 그 사이트 CSP 를 그대로 받는다.
 *   2026-08-30 실측:
 *     인스타     script-src ❌ · connect-src ❌ · img-src ❌  → 어떤 방법으로도 불가
 *     핀터레스트  script ❌ · connect ❌ · img ✅ (img-src *)
 *     유튜브·쿠팡 CSP 헤더 없음 → 전부 가능
 *   세 곳의 **공통분모가 이미지**뿐이라 픽셀로 간다. gtag.js·fetch 는 못 쓴다.
 *
 * ★ 왜 GA 로 바로 안 쏘고 여기를 거치나 — **비밀키를 숨기려고.**
 *   측정 프로토콜은 api_secret 이 필요한데, 북마크릿 소스는 랜딩 페이지에 그대로 노출된다.
 *   거기 키를 박으면 누구나 우리 속성에 가짜 이벤트를 넣을 수 있다.
 *   그래서 키는 워커 시크릿(GA_MP_SECRET)에만 두고, 픽셀은 도구 이름만 들고 온다.
 *
 * ★ 무엇을 보내지 않는가 (중요)
 *   보는 페이지 주소·제목·내용은 **일절 받지 않는다.** 남의 사이트에서 도는 코드라
 *   그걸 실어 보내면 우리가 사용자의 열람 기록을 수집하는 게 된다. 도구 이름과
 *   익명 식별자뿐이다. Referer 도 안 쓴다.
 */
async function pixel(url, env, ctx) {
  const q = url.searchParams;
  const tool = (q.get('t') || '').slice(0, 24);
  // 우리가 아는 도구만 받는다 — 아무 문자열이나 통과시키면 이벤트 이름이 오염된다.
  const KNOWN = ['quickpang', 'youtube-rank', 'pinterest-grab', 'insta-rank'];
  const secret = env.GA_MP_SECRET;

  if (KNOWN.includes(tool) && secret) {
    // cid 는 도구가 만든 익명 난수다. 없거나 이상하면 우리가 하나 만든다(집계용).
    const raw = q.get('cid') || '';
    const cid = /^\d{6,12}\.\d{9,12}$/.test(raw) ? raw : `${Date.now() % 1e9}.${Date.now()}`;
    const body = JSON.stringify({
      client_id: cid,
      events: [{
        name: 'tool_run',
        params: {
          tool,
          // 이게 없으면 GA4 가 세션을 못 묶어 표준 보고서에서 빠진다.
          session_id: q.get('sid') || String(Math.floor(Date.now() / 1000)),
          engagement_time_msec: 1,
        },
      }],
    });
    const mp = 'https://www.google-analytics.com/mp/collect'
      + '?measurement_id=G-1T66ZV28MB&api_secret=' + encodeURIComponent(secret);
    // 픽셀 응답을 붙잡아 두지 않는다 — 도구가 기다릴 이유가 없다.
    ctx.waitUntil(
      fetch(mp, { method: 'POST', body }).catch(() => {})
    );
  }
  // 무엇이 오든 픽셀은 항상 정상으로 돌려준다. 계측이 도구를 망가뜨리면 안 된다.
  return new Response(PIXEL, { headers: NO_STORE });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === '/px.gif') return pixel(url, env, ctx);

    // 네이버 소유확인 — 확인 파일은 이름을 미리 알 수 없다(사이트별 난수).
    // 그런데 **내용이 이름에서 그대로 파생**된다: `naver<hex>.html` → `naver-site-verification: naver<hex>.html`.
    // 그래서 코드를 받기 전에 미리 응답해 둘 수 있다. 콘솔에서 "확인" 한 번이면 통과, 재배포가 필요 없다.
    // (정적 파일로 두면 html_handling:auto-trailing-slash 가 .html 을 308 로 보내는데,
    //  네이버 검증 로봇은 308 을 안 따라가서 깨진다. mark 에 그 함정이 기록돼 있다.)
    const nv = /^\/(naver[0-9a-f]{8,64}\.html)$/.exec(url.pathname);
    if (nv) {
      return new Response('naver-site-verification: ' + nv[1], {
        headers: { 'content-type': 'text/html; charset=utf-8' },
      });
    }

    // 형식이 안 맞으면 원래대로 자산에 넘긴다.
    return env.ASSETS.fetch(request);
  },
};
