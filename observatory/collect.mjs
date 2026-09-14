#!/usr/bin/env node
/**
 * 관측소 수집기 — **사이트 × 6지표** 한 표. 정본: docs/OBSERVATORY.md
 *
 * ── 왜 있나 (2026-09-14 대표)
 * "후행 지표는 필요 없다. 한 번 인용됐다는 것 자체는 의미가 없다. **얼마나 가져가고 얼마나
 *  끌어갈 준비가 된 상태로 발전하고 있느냐** — 그 숫자가 들어왔느냐 변화했느냐의 표가 필요하다."
 * 계기는 이미 다 있었다. 없던 건 ① 한 표로 합치기 ② 전주 대비 변화 ③ 슬랙 ④ 전 사이트 확대다.
 *
 * ── 🚫 계기를 다시 구현하지 마라
 * 이 파일은 **부르기만 한다**. 실제 측정은 전부 기존 자산이 한다:
 *   1 크롤      cue/scripts/botlog.mjs --json       (KV 봇 방문)
 *   2 색인가능성 momentus/scripts/seo_check.py       (sitemap·고아·FAIL)
 *   3 구글노출   cue/scripts/gsc.mjs --json --host   (GSC)
 *   4 빙노출     observatory/bing.mjs                (BWT — 키 발급만 사람 손)
 *   5 유입       cue/scripts/ga.mjs --json           (GA4 전 속성)
 *   6 AI리퍼러   cue/scripts/ga.mjs --json --source  (같은 호출의 유입경로)
 * 계기가 바뀌면 여기가 아니라 그쪽을 고쳐라. 여기서 재구현하면 두 벌이 되어 한쪽만 고쳐진다.
 *
 * ── 모름과 0 을 섞지 마라
 * 값을 못 구했으면 `null` 이다. 0 으로 채우면 표가 거짓말을 하고, 그 거짓말은 에러가 안 난다.
 * 잴 수 없는 칸(웹 호스트 없는 확장앱의 색인 등)은 `sites.json` 의 `note` 가 왜인지 말한다.
 *
 * 쓰는 법
 *   node observatory/collect.mjs                # 수집 → 원장 append → 표
 *   node observatory/collect.mjs --message      # 슬랙에 보낼 본문만 (notify.py 가 쓴다)
 *   node observatory/collect.mjs --json
 *   node observatory/collect.mjs --no-collect   # 측정 안 하고 원장만 읽어 표를 그린다(경보 드릴용)
 *   node observatory/collect.mjs --force        # 같은 주를 다시 재서 **덮어쓰는 행**을 붙인다
 *   node observatory/collect.mjs --site cue     # 한 사이트만
 */
import fs from 'fs';
import path from 'path';
import { execFile } from 'child_process';
import { fileURLToPath } from 'url';
import { siteStats as bingStats, apiKey as bingKey, NO_KEY as BING_NO_KEY } from './bing.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME;
const CUE = path.join(HOME, 'Projects', 'cue');
const MOMENTUS = path.join(HERE, '..');
const NODE = process.execPath;                       // 🔴 크론엔 PATH 가 없다 — 절대경로만 쓴다
const PY = '/usr/bin/python3';
const LEDGER = path.join(HERE, 'data', 'ledger.jsonl');
const SITES = JSON.parse(fs.readFileSync(path.join(HERE, 'sites.json'), 'utf8'));

// AI 답변엔진에서 넘어온 유입으로 세는 호스트. **호스트 문자열 대조**일 뿐 자연어 판단이 아니다.
// 새 엔진이 생기면 여기에 한 줄 더한다(🚫 부분일치로 뭉뚱그리지 마라 — naver 가 gemini 를 삼킨다).
const AI_SOURCES = new Set([
  'chatgpt.com', 'chat.openai.com', 'openai.com',
  'perplexity.ai', 'www.perplexity.ai',
  'claude.ai', 'copilot.microsoft.com', 'gemini.google.com',
]);

const WEEK_TRAFFIC_DAYS = 7;     // 전주 대비를 보려면 **겹치지 않는 7일**이어야 한다
const WIDE_DAYS = 28;            // 드물게 오는 것(첫 AI 리퍼러·첫 노출)은 28일로 봐야 안 놓친다

// ── 주차 키: KST 기준 ISO 주(월요일 시작). 크론이 월 08:00 이라 주 경계와 맞물린다.
export function weekKey(d = new Date()) {
  const kst = new Date(d.getTime() + 9 * 3600000);
  const t = new Date(Date.UTC(kst.getUTCFullYear(), kst.getUTCMonth(), kst.getUTCDate()));
  const dow = (t.getUTCDay() + 6) % 7;               // 월=0
  t.setUTCDate(t.getUTCDate() - dow + 3);            // 그 주의 목요일
  const y = t.getUTCFullYear();
  const jan4 = new Date(Date.UTC(y, 0, 4));
  const wk = 1 + Math.round(((t - jan4) / 86400000 - 3 + ((jan4.getUTCDay() + 6) % 7)) / 7);
  return `${y}-W${String(wk).padStart(2, '0')}`;
}

const run = (cmd, args, opts = {}) => new Promise((res) => {
  execFile(cmd, args, { maxBuffer: 64 * 1024 * 1024, timeout: opts.timeout || 600000, cwd: opts.cwd, env: { ...process.env, ...(opts.env || {}) } },
    (err, stdout, stderr) => res({ err, out: String(stdout || ''), errOut: String(stderr || '') }));
});

async function pool(items, n, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(Array.from({ length: Math.min(n, items.length) }, async () => {
    while (i < items.length) { const k = i++; out[k] = await fn(items[k], k); }
  }));
  return out;
}

// ───────────────────────────── 계기 호출 ─────────────────────────────

/** 5·6번 — GA4 전 속성 한 번에. 속성 id → {users,sessions,views,sources[]} */
async function gaAll(days) {
  const r = await run(NODE, ['scripts/ga.mjs', '--json', '--source', '--days', String(days)], { cwd: CUE });
  try {
    const j = JSON.parse(r.out);
    const m = {};
    for (const p of j.properties || []) m[p.property] = p;
    return { byProperty: m, period: j.period };
  } catch {
    return { byProperty: {}, error: (r.errOut || r.out || String(r.err)).slice(0, 200) };
  }
}

/** 2번 — sitemap 장수·내부링크 도달·고아·FAIL. seo_check 는 사람용 출력뿐이라 여기서 읽는다. */
async function seoCheck(domain) {
  const r = await run(PY, [path.join(MOMENTUS, 'scripts', 'seo_check.py'), '--live', '--domain', domain, '--pages', '1', '--orphans'],
    { cwd: MOMENTUS, timeout: 900000 });
  const out = r.out;
  const res = { sitemap: null, reached: null, orphans: null, orphanPct: null, fail: null, warn: null, raw: null };
  const o = /sitemap (\d+)장 · 내부 링크 도달 (\d+)장 · 고아 (\d+)장/.exec(out);
  if (o) {
    res.sitemap = +o[1]; res.reached = +o[2]; res.orphans = +o[3];
    res.orphanPct = res.sitemap ? +(res.orphans / res.sitemap * 100).toFixed(1) : 0;
  }
  const f = /FAIL (\d+)건 · warn (\d+)건/.exec(out);
  if (f) { res.fail = +f[1]; res.warn = +f[2]; }
  // 한 줄도 못 읽었으면 **모른다** — 0 으로 채우지 말고 왜 못 읽었는지를 남긴다.
  if (res.fail === null) res.raw = (r.errOut || out || String(r.err)).slice(-300);
  return res;
}

/** 3번 — GSC. sc-domain 속성은 서브도메인을 전부 덮으므로 --host 로 갈라 본다. */
async function gsc(site, days) {
  if (!site.gsc) return { unavailable: 'GSC 속성 없음' };
  const r = await run(NODE, ['scripts/gsc.mjs', '--json', '--days', String(days), '--host', site.domain],
    { cwd: CUE, env: { GSC_SITE: site.gsc } });
  try {
    const j = JSON.parse(r.out);
    const p = j.performance || {};
    const sm = (j.sitemaps || [])[0] || null;
    return {
      property: site.gsc, impressions: p.impressions ?? null, clicks: p.clicks ?? null,
      position: p.position ?? null,
      sitemapLastRead: sm ? sm.lastDownloaded : null, sitemapErrors: sm ? sm.errors : null,
    };
  } catch {
    return { unavailable: (r.errOut || r.out || String(r.err)).slice(0, 200) };
  }
}

/** 1번 — 크롤러 실방문. KV 로그를 가진 사이트에만 있다(지금은 cue 워커 하나). */
async function crawl(site, days) {
  if (!site.crawl) return { unavailable: '워커 봇로그 없음' };
  const repo = site.crawl.repo.replace(/^~/, HOME);
  const r = await run(NODE, ['scripts/botlog.mjs', '--json', '--days', '60', '--ns', site.crawl.ns], { cwd: repo, timeout: 600000 });
  let j;
  try { j = JSON.parse(r.out); } catch { return { unavailable: (r.errOut || r.out || String(r.err)).slice(0, 200) }; }
  if (j.error) return { unavailable: String(j.error).slice(0, 200) };
  const cutoff = new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);
  const bots = {};
  let total = 0;
  for (const [day, m] of Object.entries(j.byDay || {})) {
    if (day < cutoff) continue;
    for (const [b, n] of Object.entries(m)) { bots[b] = (bots[b] || 0) + n; total += n; }
  }
  return { total, bots, days };
}

// ───────────────────────────── 원장 ─────────────────────────────

export function readLedger() {
  try {
    return fs.readFileSync(LEDGER, 'utf8').trim().split('\n').filter(Boolean).map((l) => {
      try { return JSON.parse(l); } catch { return null; }
    }).filter(Boolean);
  } catch { return []; }
}

/** (주차, 사이트) 하나에 행 하나. 같은 짝이 여러 번이면 **나중 것이 이긴다**(--force 재측정). */
export function collapse(rows) {
  const m = new Map();
  for (const r of rows) m.set(`${r.week}|${r.site}`, r);
  return m;
}

export function prevWeekKey(wk) {
  const [y, w] = wk.split('-W').map(Number);
  const jan4 = new Date(Date.UTC(y, 0, 4));
  const mon = new Date(jan4.getTime() - ((jan4.getUTCDay() + 6) % 7) * 86400000 + (w - 1) * 7 * 86400000);
  return weekKey(new Date(mon.getTime() - 7 * 86400000 - 9 * 3600000));
}

// ───────────────────────────── 판정 ─────────────────────────────

const aiSessions = (sources) => (sources || []).filter((s) => AI_SOURCES.has(s.src)).reduce((a, s) => a + s.sessions, 0);
const aiList = (sources) => (sources || []).filter((s) => AI_SOURCES.has(s.src));

/**
 * 경보. **행동을 바꾸는 것만 운다.** 임계는 감이 아니라 실측으로 잡았다:
 *   크롤 −50% — cue 실측 주간 합계 3,230 → 3,459 (+7%). 정상 변동과 7배 떨어져 있다.
 *   최소 200건 가드 — 정상 주가 3,000+ 이라 배포 직후·첫 주의 작은 수에 오발동하지 않게.
 */
export function judge(cur, prev, history) {
  const A = [];
  const tag = cur.label;
  const everBefore = (pick) => history.some((h) => h.site === cur.site && h.week < cur.week && pick(h));

  // 🟢 우리가 기다리는 신호 — 처음 들어왔을 때 한 번만 운다
  const ai = aiSessions(cur.ga?.wide?.sources);
  if (ai > 0 && !everBefore((h) => aiSessions(h.ga?.wide?.sources) > 0)) {
    A.push({ lv: 'good', t: `🟢 ${tag} — **첫 AI 리퍼러** ${ai}세션 (${aiList(cur.ga.wide.sources).map((s) => `${s.src} ${s.sessions}`).join(' · ')})` });
  }
  if ((cur.gsc?.wide?.impressions || 0) > 0 && !everBefore((h) => (h.gsc?.wide?.impressions || 0) > 0)) {
    A.push({ lv: 'good', t: `🟢 ${tag} — **구글 첫 노출** ${cur.gsc.wide.impressions}회` });
  }
  if ((cur.bing?.impressions || 0) > 0 && !everBefore((h) => (h.bing?.impressions || 0) > 0)) {
    A.push({ lv: 'good', t: `🟢 ${tag} — **빙 첫 노출** ${cur.bing.impressions}회` });
  }

  // 🔴 사슬이 끊긴 자리 — 앞이 막히면 뒤를 볼 필요가 없다
  const pc = prev?.crawl?.total, cc = cur.crawl?.total;
  if (typeof pc === 'number' && typeof cc === 'number' && pc >= 200 && cc < pc * 0.5) {
    A.push({ lv: 'bad', t: `🔴 ${tag} — 크롤 급감 ${pc.toLocaleString()} → ${cc.toLocaleString()} (${Math.round((cc / pc - 1) * 100)}%)` });
  }
  const po = prev?.index?.orphanPct, co = cur.index?.orphanPct;
  if (typeof co === 'number') {
    if (typeof po === 'number' && co - po >= 15) A.push({ lv: 'bad', t: `🔴 ${tag} — 고아율 급증 ${po}% → ${co}%` });
    else if (co >= 20 && !(typeof po === 'number' && po >= 20)) A.push({ lv: 'bad', t: `🔴 ${tag} — 고아율 ${co}% (sitemap ${cur.index.sitemap}장 중 ${cur.index.orphans}장)${typeof po === 'number' ? '' : ' [첫 회 기준선]'} — 2번에서 막혔다. 3~6 은 볼 필요 없다` });
  }
  const pf = prev?.index?.fail, cf = cur.index?.fail;
  if (typeof cf === 'number' && cf > 0 && (typeof pf !== 'number' || cf > pf)) {
    // ⚠️ 전주 기록이 없으면 '신규'가 아니라 **기준선**이다. 없는 비교를 있는 척 쓰지 마라.
    A.push({ lv: 'bad', t: typeof pf === 'number' ? `🔴 ${tag} — FAIL ${pf} → ${cf} 신규` : `🔴 ${tag} — FAIL ${cf}건 (첫 회 기준선)` });
  }
  const ps = prev?.ga?.week?.sessions, cs = cur.ga?.week?.sessions;
  if (typeof cs === 'number' && cs === 0 && typeof ps === 'number' && ps > 0) {
    A.push({ lv: 'bad', t: `🔴 ${tag} — GA 세션 0 (전주 ${ps}) — 측정이 끊겼거나 유입이 멎었다` });
  }
  return A;
}

// ───────────────────────────── 수집 ─────────────────────────────

export async function collect({ only = null, week = weekKey() } = {}) {
  const sites = SITES.sites.filter((s) => !only || s.id === only);
  const [ga7, ga28] = await Promise.all([gaAll(WEEK_TRAFFIC_DAYS), gaAll(WIDE_DAYS)]);
  const bingReady = !!bingKey();

  const rows = await pool(sites, 4, async (s) => {
    const row = {
      at: new Date().toISOString(), week, site: s.id, label: s.label, domain: s.domain,
      crawl: null, index: null, gsc: null, bing: null, ga: null, note: s.note || null,
    };
    const jobs = [];
    if (s.domain) {
      jobs.push(crawl(s, WEEK_TRAFFIC_DAYS).then((v) => { row.crawl = v; }));
      if (s.seo) jobs.push(seoCheck(s.domain).then((v) => { row.index = v; }));
      jobs.push(Promise.all([gsc(s, WEEK_TRAFFIC_DAYS), gsc(s, WIDE_DAYS)]).then(([w, d]) => { row.gsc = { week: w, wide: d }; }));
      jobs.push((bingReady ? bingStats(s.domain, WEEK_TRAFFIC_DAYS) : Promise.resolve({ domain: s.domain, unavailable: BING_NO_KEY }))
        .then((v) => { row.bing = v; }));
    } else {
      row.crawl = { unavailable: s.note || '웹 호스트 없음' };
      row.index = { unavailable: s.note || '웹 호스트 없음' };
      row.gsc = { unavailable: s.note || '웹 호스트 없음' };
      row.bing = { unavailable: s.note || '웹 호스트 없음' };
    }
    await Promise.all(jobs);
    const g7 = ga7.byProperty[s.ga], g28 = ga28.byProperty[s.ga];
    row.ga = {
      week: g7 ? { users: g7.users, sessions: g7.sessions, views: g7.views, sources: g7.sources || [] } : { unavailable: ga7.error || 'GA4 속성 응답 없음' },
      wide: g28 ? { users: g28.users, sessions: g28.sessions, views: g28.views, sources: g28.sources || [] } : { unavailable: ga28.error || 'GA4 속성 응답 없음' },
      period: ga7.period || null,
    };
    return row;
  });
  return rows;
}

/** 원장에 붙인다. 같은 주 같은 사이트가 이미 있으면 **행을 늘리지 않는다**(--force 면 덮어쓰는 행). */
export function append(rows, { force = false } = {}) {
  const have = collapse(readLedger());
  const added = [];
  const skipped = [];
  for (const r of rows) {
    if (have.has(`${r.week}|${r.site}`) && !force) { skipped.push(r.site); continue; }
    added.push(r);
  }
  if (added.length) {
    fs.mkdirSync(path.dirname(LEDGER), { recursive: true });
    fs.appendFileSync(LEDGER, added.map((r) => JSON.stringify(r)).join('\n') + '\n');
  }
  return { added: added.length, skipped };
}

// ───────────────────────────── 표 ─────────────────────────────

/** 화면 폭. 한글·CJK 는 두 칸을 먹는다 — 이걸 안 세면 표가 사이트마다 어긋난다. */
const W = (s) => [...String(s)].reduce((a, c) => a + (/[ᄀ-ᅟ⺀-꓏가-힣豈-﫿︰-﹏＀-｠￠-￦]/.test(c) ? 2 : 1), 0);
const pad = (s, n) => String(s) + ' '.repeat(Math.max(1, n - W(s)));

/** 전주 대비. 전주 기록이 없으면 **빈칸** — '0' 도 '±0' 도 거짓이다. */
const D = (cur, prev) => {
  if (typeof cur !== 'number' || typeof prev !== 'number') return '';
  const d = cur - prev;
  return d === 0 ? ' =' : ` ${d > 0 ? '+' : ''}${d}`;
};
const N = (v, unavail) => (typeof v === 'number' ? String(v) : (unavail ? '—' : '?'));

/** 못 잰 칸을 **사유별로** 묶는다. 사이트마다 같은 문장을 10번 쓰면 아무도 안 읽는다. */
function whyGroups(rows) {
  const g = new Map();
  const add = (col, why, label) => {
    if (!why) return;
    const k = `${col}|${String(why).split(/ — |\(/)[0].slice(0, 60)}`;
    (g.get(k) || g.set(k, { col, why: String(why).slice(0, 110), sites: [] }).get(k)).sites.push(label);
  };
  for (const r of rows) {
    // 웹 호스트가 없는 제품(확장앱·북마크릿)은 1~4번이 **구조적으로** 빈다.
    // 칸마다 같은 문장을 네 번 쓰면 진짜 고칠 거리가 그 밑에 묻힌다.
    if (!r.domain) { add('1~4번', '웹 호스트 없음 — 원천적으로 잴 수 없다', r.label); continue; }
    add('1 크롤', r.crawl?.unavailable, r.label);
    add('2 색인', r.index?.unavailable, r.label);
    add('3 구글', r.gsc?.unavailable || r.gsc?.week?.unavailable, r.label);
    add('4 빙', r.bing?.unavailable, r.label);
    add('5 유입', r.ga?.week?.unavailable, r.label);
  }
  return [...g.values()].map((v) => `  ${v.col} — ${v.why} (${v.sites.join('·')})`);
}

export function table(rows, ledger) {
  const byWeek = collapse(ledger);
  const wk = rows[0]?.week;
  const pw = wk ? prevWeekKey(wk) : null;
  const hasPrev = rows.some((r) => byWeek.has(`${pw}|${r.site}`));
  // 🔴 회차가 통째로 빠진 걸 **조용히 '첫 회'로 넘기지 마라.** 크론이 죽으면 아무 에러도 안 나고,
  //    표는 계속 예쁘게 나오면서 ± 만 사라진다 — 그게 제일 못 잡는 고장이다(룰 #9).
  const everOlder = ledger.some((h) => h.week < pw);
  const L = [];
  L.push(`관측소 ${wk}   ${hasPrev ? `전주(${pw}) 대비 ±`
    : everOlder ? `🔴 지난주(${pw}) 회차가 통째로 없다 — 크론이 안 돌았는지 봐라`
    : '첫 회 — 전주 기록이 없어 ± 는 다음 주부터'}`);
  L.push('유입·노출 = 최근 7일 · AI 리퍼러 = 최근 28일(드물어서 넓게 본다)');
  L.push('');
  L.push(pad('사이트', 16) + pad('1크롤', 12) + pad('2고아/전체', 15) + pad('3구글', 9) + pad('4빙', 8) + pad('5세션', 9) + '6AI');
  L.push('─'.repeat(72));
  const alerts = [];
  for (const r of rows) {
    const p = byWeek.get(`${pw}|${r.site}`) || null;
    const crawlV = r.crawl?.total, orph = r.index?.orphans;
    const gi = r.gsc?.week?.impressions, bi = r.bing?.impressions, ses = r.ga?.week?.sessions;
    const ai = r.ga?.wide && !r.ga.wide.unavailable ? aiSessions(r.ga.wide.sources) : null;
    L.push(
      pad(r.label, 16)
      + pad(N(crawlV, r.crawl?.unavailable) + D(crawlV, p?.crawl?.total), 12)
      + pad(typeof orph === 'number' ? `${orph}/${r.index.sitemap}${D(orph, p?.index?.orphans)}` : N(null, r.index?.unavailable), 15)
      + pad(N(gi, r.gsc?.unavailable || r.gsc?.week?.unavailable) + D(gi, p?.gsc?.week?.impressions), 9)
      + pad(N(bi, r.bing?.unavailable) + D(bi, p?.bing?.impressions), 8)
      + pad(N(ses, r.ga?.week?.unavailable) + D(ses, p?.ga?.week?.sessions), 9)
      + (typeof ai === 'number' ? String(ai) + D(ai, p?.ga?.wide && !p.ga.wide.unavailable ? aiSessions(p.ga.wide.sources) : undefined) : '—')
    );
    alerts.push(...judge(r, p, ledger));
  }
  L.push('─'.repeat(72));
  L.push('— 잴 수 없는 칸(사유 아래) · ? 이번 회차에 못 쟀다 · = 전주와 같음');
  return { lines: L, alerts, whys: whyGroups(rows) };
}

/** 슬랙 본문. 🚫 변화 없는 주에 장문을 쏘지 마라 — 조용하면 짧게. */
export function message(rows, ledger) {
  const { lines, alerts, whys } = table(rows, ledger);
  const good = alerts.filter((a) => a.lv === 'good');
  const bad = alerts.filter((a) => a.lv === 'bad');
  const head = good.length || bad.length
    ? [...good.map((a) => a.t), ...bad.map((a) => a.t)].join('\n') + '\n'
    : '조용한 주 — 새 신호도, 끊긴 자리도 없습니다.\n';
  // 슬랙은 마크다운 표를 안 그린다(메모리 slack-mrkdwn-not-markdown).
  // 코드블록만 자릿수를 지켜준다.
  return `*관측소 주간 표*\n${head}\`\`\`\n${lines.join('\n')}\n\`\`\``
    + (whys.length ? `\n_못 잰 칸_\n${whys.join('\n')}` : '');
}

// ───────────────────────────── 진입점 ─────────────────────────────

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const arg = (k) => (args.includes(k) ? args[args.indexOf(k) + 1] : null);
  const wk = arg('--week') || weekKey();
  const only = arg('--site');

  let rows;
  let appended = null;
  if (args.includes('--no-collect')) {
    const m = collapse(readLedger());
    rows = SITES.sites.filter((s) => !only || s.id === only)
      .map((s) => m.get(`${wk}|${s.id}`)).filter(Boolean);
    if (!rows.length) { console.error(`🔴 원장에 ${wk} 행이 없다 — 먼저 한 번 수집해라`); process.exit(1); }
  } else {
    rows = await collect({ only, week: wk });
    appended = append(rows, { force: args.includes('--force') });
  }
  const ledger = readLedger();

  if (args.includes('--json')) {
    const { alerts } = table(rows, ledger);
    console.log(JSON.stringify({ week: wk, appended, alerts, rows }, null, 2));
  } else if (args.includes('--message')) {
    console.log(message(rows, ledger));
  } else {
    const { lines, alerts, whys } = table(rows, ledger);
    console.log('\n' + lines.join('\n'));
    if (whys.length) { console.log('\n못 잰 칸:'); for (const w of [...new Set(whys)]) console.log(w); }
    if (alerts.length) { console.log('\n경보:'); for (const a of alerts) console.log('  ' + a.t.replace(/\*\*/g, '')); }
    else console.log('\n경보: 없음');
    if (appended) console.log(`\n원장: ${appended.added}행 추가` + (appended.skipped.length ? ` · ${appended.skipped.length}행 skip(이미 ${wk} 기록 있음, 덮어쓰려면 --force)` : ''));
    console.log();
  }
}
