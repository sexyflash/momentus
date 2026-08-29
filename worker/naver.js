// apex(the-moment.us) 워커 — **네이버 소유확인 한 가지만** 한다.
//
// 왜 워커가 필요한가:
//   서치어드바이저가 발급하는 확인 파일은 이름을 미리 알 수 없다(사이트별 난수).
//   그런데 **내용이 이름에서 그대로 파생**된다 — `naver<hex>.html` → `naver-site-verification: naver<hex>.html`.
//   그래서 코드를 받기 전에 미리 응답해 둘 수 있다. 콘솔에서 "확인" 한 번이면 통과, 재배포가 필요 없다.
//   (정적 파일로 두면 html_handling:auto-trailing-slash 가 .html 을 308 로 보내는데,
//    네이버 검증 로봇은 308 을 안 따라가서 깨진다. mark 에 그 함정이 기록돼 있다.)
//
// ⚠️ 이 워커는 wrangler.jsonc 의 `assets.run_worker_first: ["/naver*"]` 로
//    **그 경로에서만** 실행된다. 나머지 요청은 예전처럼 자산이 직접 처리한다
//    (html_handling·not_found_handling·_redirects 동작을 건드리지 않기 위해서다).
export default {
  async fetch(request, env) {
    const nv = /^\/(naver[0-9a-f]{8,64}\.html)$/.exec(new URL(request.url).pathname);
    if (nv) {
      return new Response('naver-site-verification: ' + nv[1], {
        headers: { 'content-type': 'text/html; charset=utf-8' },
      });
    }
    // /naver* 인데 형식이 안 맞으면 원래대로 자산에 넘긴다.
    return env.ASSETS.fetch(request);
  },
};
