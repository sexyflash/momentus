// decide-inbox — 결정 페이지 답 받는 자리. 설명은 wrangler.jsonc 머리말.
const MAX = 8 * 1024;
const SLUG = /^[a-z0-9][a-z0-9-]{0,63}$/;
const KEEP = 180 * 24 * 3600;          // 반년 보관 — 결정 기록이라 짧게 두지 않는다

function cors(req) {
  const o = req.headers.get('Origin') || '';
  let ok = false;
  try {
    const h = new URL(o).hostname;
    ok = h.endsWith('.pages.dev') || h === 'localhost' || h === '127.0.0.1';
  } catch (e) { }
  return ok ? { 'Access-Control-Allow-Origin': o, 'Vary': 'Origin',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Read-Key',
                'Access-Control-Max-Age': '86400' } : {};
}
function json(req, code, obj) {
  return new Response(JSON.stringify(obj), { status: code,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...cors(req) } });
}
async function same(a, b) {                 // 길이·내용이 새지 않게 해시끼리 비교
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([a, b].map(v => crypto.subtle.digest('SHA-256', enc.encode(v))));
  return crypto.subtle.timingSafeEqual(x, y);
}

async function answer(req, env) {
  const raw = await req.text();
  if (new TextEncoder().encode(raw).length > MAX) return json(req, 413, { error: '8KB 를 넘었습니다' });
  let d;
  try { d = JSON.parse(raw); } catch (e) { return json(req, 400, { error: 'JSON 이 아닙니다' }); }
  const page = String(d && d.page || '');
  if (!SLUG.test(page)) return json(req, 400, { error: 'page 는 영소문자·숫자·- 만(64자까지)' });
  const a = d.answers;
  if (!a || typeof a !== 'object' || Array.isArray(a) || !Object.keys(a).length)
    return json(req, 400, { error: 'answers 가 비었습니다' });
  for (const [q, v] of Object.entries(a)) {
    if (!/^[\w-]{1,40}$/.test(q) || !v || typeof v !== 'object' || !['rec', 'alt'].includes(v.pick)
        || (v.note != null && typeof v.note !== 'string'))
      return json(req, 400, { error: '항목 ' + q.slice(0, 40) + ' 의 꼴이 틀렸습니다(pick: rec|alt, note: 글)' });
  }
  const got = new Date().toISOString();
  const rec = { page, answers: a, at: d.at || null, received: got,
                ua: (req.headers.get('User-Agent') || '').slice(0, 160) };
  const key = 'ans:' + page + ':' + got + ':' + crypto.randomUUID().slice(0, 8);
  await env.INBOX.put(key, JSON.stringify(rec), { expirationTtl: KEEP });
  return json(req, 200, { ok: true, page, received: got });
}

async function answers(req, env, url) {
  const k = req.headers.get('X-Read-Key') || url.searchParams.get('key') || '';
  if (!env.READ_KEY) return json(req, 500, { error: '읽기 키가 설정되지 않았습니다' });   // 미설정이면 전원 통과가 아니라 막는다
  if (!k || !(await same(k, env.READ_KEY))) return json(req, 401, { error: '읽기 키가 틀렸습니다' });
  const page = url.searchParams.get('page') || '';
  if (!SLUG.test(page)) return json(req, 400, { error: 'page 가 필요합니다' });
  const ls = await env.INBOX.list({ prefix: 'ans:' + page + ':' });
  const out = (await Promise.all(ls.keys.map(x => env.INBOX.get(x.name, 'json')))).filter(Boolean);
  out.sort((x, y) => (x.received < y.received ? 1 : -1));
  return json(req, 200, { page, count: out.length, latest: out[0] || null, submissions: out,
                          truncated: !ls.list_complete });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(req) });
    if (url.pathname === '/answer' && req.method === 'POST') return answer(req, env);
    if (url.pathname === '/answers' && req.method === 'GET') return answers(req, env, url);
    if (url.pathname === '/') return json(req, 200, { ok: true, service: 'decide-inbox' });
    return json(req, 404, { error: '없는 길입니다' });
  },
};
