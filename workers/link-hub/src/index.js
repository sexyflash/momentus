/**
 * link-hub — 알림톡 버튼이 가리키는 단 하나의 도메인.
 *
 * 왜 만들었나: 카카오 알림톡은 **버튼 링크의 도메인을 템플릿에 고정**시킨다.
 * 제품마다 도메인이 다르면(bb/dl/cue…) 도메인 수만큼 템플릿이 갈라져
 * "사건 5종 공용 템플릿"이 무너진다. 그래서 버튼은 전부 여기만 보고,
 * 실제 목적지는 이 워커가 결정한다. 새 서비스가 늘어도 **템플릿은 그대로**다.
 *
 *   r.the-moment.us/BB03990C  → bb.the-moment.us/s/BB03990C   (빈방 현황)
 *   r.the-moment.us/DLxxxxxx  → dl.the-moment.us/d/xxxxxx     (플래너 다운로드)
 *   r.the-moment.us/CUxxxxxx  → cue.the-moment.us/spike?...   (큐 이용권)
 *
 * 규칙은 접두 2글자. 예외가 필요하면 D1 link_routes 가 먼저 이긴다.
 * 클릭은 D1 link_hits 에 남긴다 — 어느 알림이 실제로 열렸는지 아는 유일한 근거.
 */

const PREFIX = {
  BB: (code) => `https://bb.the-moment.us/s/${code}`,
  DL: (code) => `https://dl.the-moment.us/d/${code.slice(2)}`,
  CU: (code) => `https://cue.the-moment.us/spike?view=pass&code=${encodeURIComponent(code.slice(2))}`,
  MK: (code) => `https://mark.the-moment.us/?ref=${encodeURIComponent(code)}`,
  OR: () => `https://pay.the-moment.us/orders`,
};

const FALLBACK = "https://the-moment.us/";

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    const code = decodeURIComponent(u.pathname.replace(/^\/+/, "").split("/")[0] || "").trim();

    if (!code) return Response.redirect(FALLBACK, 302);
    if (code === "health") return new Response("ok", { headers: { "content-type": "text/plain" } });

    let target = null;

    // ① D1 예외 규칙이 접두 규칙보다 우선한다(특수 캠페인·임시 링크)
    if (env.DB) {
      try {
        const row = await env.DB.prepare(
          "SELECT target FROM link_routes WHERE code=? AND (expires_at IS NULL OR expires_at > datetime('now'))"
        ).bind(code).first();
        if (row && row.target) target = row.target;
      } catch { /* 테이블이 없어도 접두 규칙으로 계속 간다 */ }
    }

    // ② 접두 2글자 규칙
    if (!target) {
      const fn = PREFIX[code.slice(0, 2).toUpperCase()];
      if (fn) target = fn(code);
    }

    if (!target) return Response.redirect(FALLBACK, 302);

    // ③ 클릭 기록 — 응답을 막지 않는다
    if (env.DB) {
      ctx.waitUntil(
        env.DB.prepare(
          "INSERT INTO link_hits (code, target, ua, ip, ref) VALUES (?,?,?,?,?)"
        ).bind(code, target,
               (req.headers.get("user-agent") || "").slice(0, 200),
               req.headers.get("cf-connecting-ip") || "",
               (req.headers.get("referer") || "").slice(0, 200)).run().catch(() => {})
      );
    }
    return Response.redirect(target, 302);
  },
};
