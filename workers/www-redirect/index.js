/**
 * www.the-moment.us → the-moment.us (301)
 *
 * 왜 별도 워커인가 (2026-08-01):
 *   apex 는 momentus 워커가 정적자산으로 서빙하고, 그 경로에 _redirects 가 걸려 있다
 *   (특히 /apps/quickpang/* → /tools/quickpang/ — 외부 유입 1만+). apex 워커에
 *   스크립트를 끼우면 자산 우선순위와 _redirects 처리 순서가 바뀔 수 있는데
 *   공식 문서가 그 동작을 명시하지 않는다. 그래서 apex 는 건드리지 않고
 *   www 에만 이 워커를 붙인다. 실패해도 www 만 영향받는다.
 *
 * 이건 임시 해법이다. 정본은 zone 의 Single Redirect 규칙 —
 *   그건 dns_records/ruleset 쓰기 권한이 있어야 만들 수 있다.
 */
export default {
  fetch(request) {
    const url = new URL(request.url);
    url.hostname = "the-moment.us";
    url.protocol = "https:";
    return Response.redirect(url.toString(), 301);
  },
};
