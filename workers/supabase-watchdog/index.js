/**
 * Supabase 감시견 — 잠들면 자동으로 깨우고, 못 깨우면 사람을 부른다.
 *
 * 왜 있나 (2026-08-03 사고):
 *   무료 Supabase 프로젝트는 일정 기간 비활성이면 pause 된다 = 로그인 사망.
 *   kontext 는 Vercel 크론이 매일 Supabase 를 칠 예정이었는데, 그 라우트가 POST 만
 *   export 해서 크론(GET)이 매일 405 를 맞고 끝났다 → 트래픽 0 → pause.
 *   대표가 대시보드에서 손으로 깨워야 했고, 깨워도 또 잠들었다.
 *
 * 핵심 사실: **잠든 프로젝트는 요청으로 안 깨어난다.** 복구는 Management API(또는 사람)만 할 수 있다.
 *   → 그래서 "핑만 계속 보내기"는 해결이 아니다. 감시 + 복구 + 알림이 한 벌이어야 한다.
 *
 * 층 구조 (이 워커는 ②③④):
 *   ① 예방  각 서비스의 Vercel 크론이 매일 Supabase 를 친다        ← 본체. 이게 돌면 여긴 놀고 있다
 *   ② 감시  이 워커가 1시간마다 상태 확인                          ← Vercel 과 독립
 *   ③ 복구  잠들었으면 Management API 로 restore 시도
 *   ④ 알림  복구 성공/실패 모두 슬랙. 정상일 땐 침묵.
 *
 * 정본 문서: ~/Projects/momentus/docs/PLAN_PAY_LAYER.md
 */

const TIMEOUT_MS = 10_000;

export default {
  async scheduled(_event, env, ctx) {
    ctx.waitUntil(runCheck(env));
    // 곁다리 태우기 — 맥미니 생존 감시견(mac-heartbeat)에는 **자기 크론이 없다.**
    // Workers 무료 플랜이 계정당 크론 5개인데 이미 5개가 차 있어서(2026-08-26),
    // 이미 도는 이 크론이 그 워커의 검사를 대신 눌러 준다. 요청 1회/시간뿐이다.
    // 🔒 반드시 격리한다 — 저쪽이 어떻게 실패하든 Supabase 감시는 그대로 돌아야 한다.
    if (env.HEARTBEAT_TICK_URL) {
      ctx.waitUntil(
        fetch(env.HEARTBEAT_TICK_URL, { signal: AbortSignal.timeout(TIMEOUT_MS) })
          .catch(() => {}),
      );
    }
  },

  // 수동 확인용. GET /  → 지금 상태를 JSON 으로.  GET /?test=1 → 슬랙 배선 점검 1통.
  async fetch(req, env) {
    if (new URL(req.url).searchParams.get("test") === "1") {
      await sendTestAlert(env);
      return Response.json({ sent: "슬랙 테스트 알림 발송함 — #운영실 확인" });
    }
    const report = await runCheck(env, { silent: true });
    return Response.json(report, {
      headers: { "cache-control": "no-store" },
    });
  },
};

async function runCheck(env, { silent = false } = {}) {
  const targets = env.WATCH || [];
  // ANON_KEYS = {"kontext":"sb_publishable_...","heyreci":"..."} 형태의 시크릿(JSON 문자열).
  // 없으면 감지 전용으로 떨어진다 — 죽지 않는다.
  let anon = {};
  try { anon = env.ANON_KEYS ? JSON.parse(env.ANON_KEYS) : {}; } catch { anon = {}; }

  const report = { checked: targets.length, results: [] };

  for (const t of targets) {
    const health = await probe(t.ref, anon[t.name], t.table);
    const row = { name: t.name, ref: t.ref, ...health };

    if (!health.alive) {
      // ③ 복구 시도
      const restore = await tryRestore(env, t.ref);
      row.restore = restore;

      // ④ 알림 — 이상일 때만. 정상 회차는 조용하다(룰: 정기 루틴은 긴급 없으면 침묵).
      if (!silent) await alert(env, t, health, restore);
    }

    report.results.push(row);
  }

  return report;
}

/**
 * 살아있나 판정 — 그리고 **동시에 예방까지 한다.**
 *
 * anon 키가 있으면 PostgREST 루트(`/rest/v1/`)를 친다. 이건 스키마를 조회하므로
 * **Postgres 에 실제 활동이 찍힌다** → 비활성 카운터가 리셋된다 = pause 예방.
 * 즉 ①(각 서비스의 Vercel 크론)이 또 고장 나도 이 워커가 매시간 깨워 둔다. 이중화.
 *
 * anon 키가 없으면 GoTrue health 로 떨어진다(감지만 되고 예방은 안 됨).
 * anon 키는 클라이언트 번들에 들어가는 **공개키**라 워커에 두는 것이 위험하지 않다.
 * 🚫 service_role 키를 여기 쓰지 마라 — 전권 키를 살아있나 확인에 쓸 이유가 없다.
 */
async function probe(ref, anonKey, table) {
  // ── 생사 판정: GoTrue health. 키 없이도 401 + JSON 을 주며, 그 응답 자체가 "구동 중"의 증거다.
  //    2026-08-03 실측으로 검증된 유일한 경로다.
  //    🚫 `/rest/v1/` 루트로 바꾸지 마라 — anon 키를 거부한다("Only secret API keys can be used").
  //       한 번 그렇게 짰다가 살아있는 프로젝트를 죽었다고 오판했다.
  let alive = false, status = 0, body;
  try {
    const res = await fetch(`https://${ref}.supabase.co/auth/v1/health`, {
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: { accept: "application/json" },
    });
    status = res.status;
    body = (await res.text()).slice(0, 300);
    alive = (status === 200 || status === 401) && body.trim().startsWith("{");
    if (alive) body = undefined;
  } catch (e) {
    return { alive: false, status: 0, body: `fetch failed: ${e.message}`, kept_awake: false };
  }

  // ── 예방(best-effort): 살아있을 때만, 실제 테이블을 1행 조회해 **Postgres 에 활동을 남긴다.**
  //    이게 성공하면 각 서비스의 Vercel 크론이 또 고장 나도 이 워커가 매시간 깨워 둔다(이중화).
  //    실패해도 생사 판정에는 영향 없다 — 예방이 약해질 뿐 오탐을 만들지 않는다.
  let kept_awake = false;
  if (alive && anonKey && table) {
    try {
      const r = await fetch(`https://${ref}.supabase.co/rest/v1/${table}?select=*&limit=1`, {
        signal: AbortSignal.timeout(TIMEOUT_MS),
        headers: { apikey: anonKey, authorization: `Bearer ${anonKey}`, accept: "application/json" },
      });
      kept_awake = r.ok; // RLS 로 0행이 와도 200 이면 DB 를 친 것 = 활동 기록됨
    } catch { /* 예방 실패는 조용히 넘어간다 */ }
  }

  return { alive, status, body, kept_awake };
}

/**
 * ③ Management API 로 restore.
 * ⚠️ 이 엔드포인트 동작은 실제로 한 번 성공시켜 검증하기 전까지 확정이 아니다.
 *    실패해도 ④ 알림은 그대로 나가므로 "조용히 죽는" 경우는 없다.
 */
async function tryRestore(env, ref) {
  if (!env.SUPABASE_MGMT_TOKEN) return { attempted: false, reason: "no SUPABASE_MGMT_TOKEN" };
  try {
    const res = await fetch(`https://api.supabase.com/v1/projects/${ref}/restore`, {
      method: "POST",
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: {
        authorization: `Bearer ${env.SUPABASE_MGMT_TOKEN}`,
        "content-type": "application/json",
      },
      body: "{}",
    });
    return { attempted: true, ok: res.ok, status: res.status, body: (await res.text()).slice(0, 300) };
  } catch (e) {
    return { attempted: true, ok: false, status: 0, body: `restore failed: ${e.message}` };
  }
}

/**
 * ④ 알림 — **조은정 CD(ops 페르소나)가 #운영실로 말한다.**
 *
 * 🚫 Incoming Webhook 을 쓰지 마라. 대표는 페르소나에게 보고받는다 —
 *    웹훅으로 보내면 낯선 앱 이름·아바타로 떨어져 "이건 누가 보낸 거냐"가 된다.
 *    ops 봇 토큰으로 chat.postMessage 하면 표시명·아바타가 조은정 CD 그대로다(2026-08-03 실측).
 * 🚫 username/icon_emoji 를 넣지 마라. 봇 자기 정체성을 덮어쓰는 순간 정체성이 꼬인다
 *    (slack-bot CLAUDE.md 룰 #3 과 같은 취지).
 *
 * 문구 규칙: jargon 0. 지금 뭘 하면 되는지만. 정상 회차엔 아예 말하지 않는다.
 */
async function alert(env, t, health, restore) {
  if (!env.SLACK_BOT_TOKEN || !env.SLACK_CHANNEL) return;

  const dash = `https://supabase.com/dashboard/project/${t.ref}`;
  const recovered = restore?.ok;

  const text = recovered
    ? `✅ ${t.name} 데이터베이스가 멈춰 있어서 자동으로 다시 켰습니다.\n` +
      `· 사이트: ${t.site}\n` +
      `· 잠시 뒤 로그인이 정상으로 돌아옵니다. 따로 하실 일은 없습니다.\n` +
      `· 원인 점검이 필요하면: ${dash}`
    : `🚨 ${t.name} 데이터베이스가 멈췄습니다. 자동 복구에 실패했습니다.\n` +
      `· 사이트: ${t.site} — 지금 로그인이 안 됩니다.\n` +
      `· 지금 여기 들어가서 켜 주세요 → ${dash}\n` +
      `· 확인된 상태: ${health.status || "응답 없음"} ${health.body ? `(${health.body.slice(0, 120)})` : ""}`;

  try {
    await fetch("https://slack.com/api/chat.postMessage", {
      method: "POST",
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: {
        authorization: `Bearer ${env.SLACK_BOT_TOKEN}`,
        "content-type": "application/json; charset=utf-8",
      },
      body: JSON.stringify({ channel: env.SLACK_CHANNEL, text }),
    });
  } catch {
    // 알림 실패로 감시 자체를 죽이지 않는다.
  }
}

/** 배선 점검용 — GET /?test=1 이면 실제로 슬랙에 한 통 쏴 본다(감시 결과와 무관). */
export async function sendTestAlert(env) {
  const t = { name: "감시견 배선 점검", ref: "test", site: "the-moment.us" };
  await alert(env, t, { status: 0, body: "테스트 발송입니다 — 실제 장애가 아닙니다" }, { ok: false });
}
