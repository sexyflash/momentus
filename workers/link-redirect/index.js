/**
 * /l/<키> — 앱 바이너리에 박히는 영구 링크 층.
 *
 * 왜 _redirects 가 아니라 워커인가 (2026-08-01 실측):
 *   _redirects 에 개별 규칙(/l/flipper …)을 catch-all(/l/*) 보다 먼저 뒀는데도
 *   catch-all 이 전부 삼켰다. 선매치 승리가 보장되지 않는다.
 *   이 층은 "앱은 URL을 못 고친다"는 전제 전체가 얹혀 있는 자리라
 *   문서에 없는 우선순위 동작에 걸 수 없어 코드로 확정한다.
 *
 * 왜 apex 워커에 안 합쳤나:
 *   apex 는 정적자산 + _redirects 로 돈다(퀵팡 외부유입 1만+가 그 경로에 걸려 있다).
 *   라우트 the-moment.us/l/* 가 the-moment.us/* 보다 구체적이라 이것만 가로챈다.
 *
 * ⚠️ 302(임시)를 쓴다. 301은 브라우저·스토어 크롤러가 목적지를 영구 캐시해서
 *    나중에 target 을 바꿔도 기존 설치본이 옛 주소로 계속 간다 = 이 층의 존재 이유가 사라진다.
 * ⚠️ map.json 은 scripts/gen_site.py 가 data/products.json 에서 생성한다. 손으로 고치지 마라.
 */
import MAP from "./map.json";

export default {
  fetch(request) {
    const url = new URL(request.url);
    // /l/flipper/setup/ → "flipper/setup"
    const key = url.pathname.replace(/^\/l\/?/, "").replace(/\/+$/, "");
    const target = MAP.map[key] ?? MAP.catchall;

    const dest = new URL(target, "https://the-moment.us");
    // 유입 추적 파라미터(utm 등)를 목적지까지 넘긴다. 목적지가 이미 쿼리를 가지면 건드리지 않는다.
    if (url.search && !dest.search) dest.search = url.search;

    return new Response(null, {
      status: 302,
      headers: {
        Location: dest.toString(),
        // 이 층은 언제든 갈아탈 수 있어야 한다 — 중간 캐시가 붙들지 못하게 못박는다.
        "Cache-Control": "no-store",
      },
    });
  },
};
