/**
 * 맥미니 생존 감시견 — 맥이 죽으면 **맥 밖에서** 대표를 부른다.
 *
 * 왜 있나 (2026-08-26 사고):
 *   04:03 securityd 교착 → trustd → tccd → WindowServer 메인 스레드 40초 무응답 →
 *   macOS 워치독이 WindowServer 를 강제종료 → **로그인 세션 통째로 종료.**
 *   그 세션에 있던 전부(슬랙봇 5봇·상주 크롬 6개·나이트워크·챗페이지)가 동시에 죽었다.
 *   자동 로그인은 *부팅 때 1회*만 적용돼서 다시 안 들어갔고, 10:47 에 대표가 손으로
 *   로그인할 때까지 **6시간 44분 침묵**했다. 그 사이 대표가 슬랙으로 사람을 불렀지만
 *   받을 주체가 아예 없었다. 대표: *"내가 불렀는데 어떻게 대답을 안 할 수가 있어."*
 *
 * 핵심 사실: **맥 위에서 도는 감시는 맥이 죽으면 같이 죽는다.**
 *   슬랙봇의 소켓 워치독도, launchd 도, ollama-gateway 의 tunnel_watchdog.sh 도 전부
 *   같은 세션 안에 있었다. 그래서 아무도 못 알렸다 — 감시는 밖에 있어야 한다.
 *   (같은 이유로 supabase-watchdog 를 Vercel 이 아니라 여기 둔 것이다.)
 *
 * 구조 — dead-man switch:
 *   ① 맥이 살아있는 동안 10분마다 이 워커에 `POST /beat` 를 친다.
 *   ② 이 워커는 마지막 신호 시각만 KV 에 적는다.
 *   ③ 크론(15분마다)이 마지막 신호가 STALE_MIN 분보다 오래됐으면 슬랙으로 대표를 부른다.
 *      **맥이 아무것도 안 해도 알림이 나간다** — 그게 dead-man switch 의 요점이다.
 *   ④ 다시 신호가 오면 "돌아왔습니다" 한 번. 그 사이 유실을 대표가 알아야 한다.
 *
 * 발화 규율: 정상일 땐 완전 침묵. 사망 알림은 **1회만**(반복 나그 금지), 복구 때 1회.
 *   사망 알림엔 대표 멘션을 넣는다 — 채널 메시지는 폰 푸시가 안 뜰 수 있는데 멘션은 뜬다.
 *
 * 💰 과금: 크론 96회/일 + 하트비트 144회/일 = 240 요청/일.
 *    Workers 무료 한도 100,000/일 의 0.24%. KV 쓰기 144/일(무료 1,000/일).
 *    🚫 하트비트 주기를 분 단위로 낮추지 마라 — KV 쓰기 한도가 먼저 터진다.
 */

const TIMEOUT_MS = 10_000;
const KEY_LAST = "last_beat";      // { at: epochSec, host, boot, note }
const KEY_STATE = "alert_state";   // { down: bool, since: epochSec, notified_at: epochSec }

export default {
  async scheduled(_event, env, ctx) {
    ctx.waitUntil(check(env));
  },

  async fetch(req, env) {
    const url = new URL(req.url);

    // ① 맥이 살아있다는 신호. 공유 비밀이 맞아야 받는다(아무나 못 찍는다).
    if (req.method === "POST" && url.pathname === "/beat") {
      if (!env.BEAT_SECRET || req.headers.get("x-beat-secret") !== env.BEAT_SECRET) {
        return new Response("nope", { status: 403 });
      }
      let body = {};
      try { body = await req.json(); } catch { /* 본문은 없어도 된다 */ }
      return Response.json(await beat(env, body));
    }

    // ③ 검사 실행(알림 포함). **자기 크론이 없어서** 밖에서 이 주소를 쳐서 돌린다 —
    //    Workers 무료 플랜이 계정당 크론 5개인데 이미 5개가 차 있다(2026-08-26).
    //    지금은 momentus-supabase-watchdog 의 매시 크론이 이 주소를 대신 쳐 준다.
    //    크론 슬롯이 비면 wrangler.jsonc 의 crons 를 되살리고 이 경로는 그대로 둬도 된다.
    if (url.searchParams.get("run") === "1") {
      return Response.json(await check(env), { headers: { "cache-control": "no-store" } });
    }

    // 드릴 — **사망→복구 전 구간을 진짜 코드로** 한 번 돌려본다.
    // 왜 필요한가: 이 감시견은 사고가 나야 처음 말을 하는 물건이라, 안 돌려보면 "있는 줄
    // 알았는데 없는" 상태로 몇 달을 간다. 실제로 첫 배선 때 Cloudflare 엣지가 Python UA 를
    // 막아 신호가 한 번도 안 닿고 있었다(2026-08-26). 문구에 [점검]을 붙여 진짜 장애와 섞이지
    // 않게 한다. 비밀을 알아야 돌릴 수 있고, 원래 상태는 그대로 되돌려 놓는다.
    if (url.searchParams.get("drill") === "1") {
      if (req.headers.get("x-beat-secret") !== env.BEAT_SECRET) {
        return new Response("nope", { status: 403 });
      }
      const savedLast = await env.HEARTBEAT.get(KEY_LAST);
      const savedState = await env.HEARTBEAT.get(KEY_STATE);
      const long_ago = Math.floor(Date.now() / 1000) - 3 * 3600;
      await env.HEARTBEAT.put(KEY_LAST, JSON.stringify({ at: long_ago, host: "drill" }));
      await env.HEARTBEAT.put(KEY_STATE, JSON.stringify({ down: false, since: 0 }));
      const down = await check(env, { drill: true });          // 사망 감지 + 알림
      const again = await check(env, { drill: true });          // 두 번째는 침묵해야 한다
      await env.HEARTBEAT.put(KEY_LAST, JSON.stringify({ at: long_ago, host: "drill" }));
      const back = await beat(env, { host: "drill" }, { drill: true });  // 복구 알림
      if (savedLast) await env.HEARTBEAT.put(KEY_LAST, savedLast);
      if (savedState) await env.HEARTBEAT.put(KEY_STATE, savedState);
      else await env.HEARTBEAT.put(KEY_STATE, JSON.stringify({ down: false, since: 0 }));
      return Response.json({ drill: true, 사망감지: down, 중복억제: again, 복구: back });
    }

    // 배선 점검용 — 슬랙으로 1통.
    if (url.searchParams.get("test") === "1") {
      await slack(env, "🔔 맥미니 감시견 배선 점검입니다. 이 메시지가 보이면 정상입니다.");
      return Response.json({ sent: true });
    }

    // 수동 확인 — 지금 상태.
    return Response.json(await check(env, { silent: true }), {
      headers: { "cache-control": "no-store" },
    });
  },
};

/** 신호 1회 접수 — 시각을 적고, 죽었다고 알린 뒤였으면 돌아온 사실을 알린다(룰 #9). */
async function beat(env, body, { drill = false } = {}) {
  const now = Math.floor(Date.now() / 1000);
  await env.HEARTBEAT.put(KEY_LAST, JSON.stringify({
    at: now, host: body.host || "", boot: body.boot || 0, note: body.note || "",
  }));
  const st = await readState(env);
  if (st.down) {
    const downMin = Math.round((now - (st.since || now)) / 60);
    await slack(env,
      `${drill ? "[점검] " : ""}✅ 맥미니가 돌아왔습니다 — ${fmtDur(downMin)} 만에 응답이 다시 옵니다.\n` +
      `· 그 사이 슬랙으로 부르신 게 있으면 봇이 못 받았습니다. 다시 한 번 보내주세요.\n` +
      `· 그동안 예정돼 있던 자동 작업들도 건너뛰었을 수 있습니다.`);
    await env.HEARTBEAT.put(KEY_STATE, JSON.stringify({ down: false, since: 0, notified_at: 0 }));
    return { ok: true, at: now, 복구알림: "발송" };
  }
  return { ok: true, at: now };
}

async function readState(env) {
  try { return JSON.parse(await env.HEARTBEAT.get(KEY_STATE)) || {}; } catch { return {}; }
}

async function check(env, { silent = false, drill = false } = {}) {
  const now = Math.floor(Date.now() / 1000);
  const staleMin = Number(env.STALE_MIN || 25);

  let last = null;
  try { last = JSON.parse(await env.HEARTBEAT.get(KEY_LAST)); } catch { /* 없음 */ }

  // 신호를 한 번도 받은 적이 없으면 = 아직 배선 전이다. 알리지 않는다(오탐 방지).
  if (!last || !last.at) {
    return { state: "대기", detail: "아직 신호를 한 번도 못 받았습니다", stale_min: staleMin };
  }

  const ageMin = Math.round((now - last.at) / 60);
  const report = { state: ageMin > staleMin ? "끊김" : "정상", age_min: ageMin,
                   stale_min: staleMin, last_beat_at: last.at, host: last.host };
  if (silent || ageMin <= staleMin) return report;

  // ③ 끊겼다 — 처음 감지했을 때만 부른다. 반복 알림은 나그다.
  const st = await readState(env);
  if (st.down) { report.notified = "이미 알림"; return report; }

  await env.HEARTBEAT.put(KEY_STATE, JSON.stringify({
    down: true, since: last.at, notified_at: now,
  }));
  const mention = (!drill && env.OWNER_USER_ID) ? `<@${env.OWNER_USER_ID}> ` : "";
  await slack(env,
    `${mention}${drill ? "[점검] " : ""}🚨 맥미니가 ${fmtDur(ageMin)} 째 응답이 없습니다.\n` +
    `· 마지막 신호: ${fmtKst(last.at)}\n` +
    `· 지금 슬랙으로 사람을 불러도 아무도 못 받습니다. 자동 작업도 전부 멈춰 있습니다.\n` +
    `· 화면이 로그인 화면에 멈춰 있을 가능성이 큽니다 — 맥미니에 로그인해 주세요.\n` +
    `· 살아나면 이 채널로 돌아왔다고 알려드립니다.`);
  report.notified = "발송";
  return report;
}

function fmtDur(min) {
  if (min < 60) return `${min}분`;
  const h = Math.floor(min / 60), m = min % 60;
  return m ? `${h}시간 ${m}분` : `${h}시간`;
}

function fmtKst(sec) {
  const d = new Date((sec + 9 * 3600) * 1000);
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())} ` +
         `${p(d.getUTCHours())}:${p(d.getUTCMinutes())} (한국시간)`;
}

/**
 * 슬랙 발송 — ops(조은정 CD) 봇 토큰으로 보낸다. 표시명·아바타가 그 페르소나 그대로다.
 * (slack-bot CLAUDE.md 룰 #3 과 같은 취지 — 정체성이 섞이면 대표가 누가 말하는지 모른다.)
 * 알림 실패로 감시 자체를 죽이지 않는다.
 */
async function slack(env, text) {
  if (!env.SLACK_BOT_TOKEN || !env.SLACK_CHANNEL) return;
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
  } catch { /* 무시 */ }
}
